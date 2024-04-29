from uuid import UUID

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError

from app.api.serializers.comment import CommentSchema
from app.api.serializers.image import ImageSchema, ViewImageSchema
from app.api.serializers.image_summary import ImageSummarySchema
from app.config import Config
from app.handlers.image import trigger_simulate_image_annotation
from app.models.user import User
from app.repos.annotation import AnnotationRepo
from app.repos.image import ImageRepo
from app.repos.user import UserRepo
from app.services.image_service import ImageService
from app.utils.auth import AuthUtils

image_blueprint = Blueprint("image", __name__)
image_schema = ImageSchema()
view_image_schema = ViewImageSchema()
comment_schema = CommentSchema()
image_summary_schema = ImageSummarySchema()


@image_blueprint.route("/image/upload", methods=["POST"])
@jwt_required()
@AuthUtils.inject_requesting_user
def upload_image(requesting_user: User):
    """
    Upload a new image.

    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The image file to upload
      - name: user_id
        in: formData
        type: string
        required: true
        description: ID of the user uploading the image
    responses:
      201:
        description: Image uploaded successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ViewImageSchema'
      400:
        description: Bad request - No image file provided or validation error
      401:
        description: Unauthorized - Only the owner of the image can upload it
      500:
        description: Internal Server Error - Failed to save the image
    """
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return jsonify({"message": "No image file provided"}), 400

    data = request.form.to_dict(flat=True)
    try:
        image_data: dict = image_schema.load(data)
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

    if not requesting_user.id == image_data["user_id"]:
        return jsonify({"error": "Unauthorized"}), 401

    new_image = ImageRepo.create(**image_data)

    try:
        ImageService.save_image(uploaded_file, requesting_user, new_image.filename)
    except Exception as e:
        return jsonify({"message": f"Failed to save image: {str(e)}"}), 500

    return jsonify(view_image_schema.dump(new_image)), 201


@image_blueprint.route("/image/images/all", methods=["GET"])
@jwt_required()
@AuthUtils.admin_required
def get_all_images():
    """
    Get all images.

    ---
    responses:
      200:
        description: List of all images
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/ViewImageSchema'
    """
    images = ImageRepo.get_all()
    return jsonify(view_image_schema.dump(images, many=True)), 200


@image_blueprint.route("/image/images", methods=["GET"])
@jwt_required()
@AuthUtils.inject_requesting_user
def get_all_allowed_images(requesting_user: User):
    """
    Get all images allowed for the requesting user.

    ---
    responses:
      200:
        description: List of all images allowed for the requesting user
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/ViewImageSchema'
    """
    images = ImageRepo.get_all_allowed(requesting_user_id=requesting_user.id)
    return jsonify(view_image_schema.dump(images, many=True)), 200


@image_blueprint.route("/image/<uuid:image_id>", methods=["GET"])
@jwt_required()
@AuthUtils.inject_requesting_user
def get_image(image_id, requesting_user: User):
    """
    Get a specific image by ID.

    ---
    parameters:
      - name: image_id
        in: path
        description: ID of the image to retrieve
        required: true
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: Image details
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ViewImageSchema'
      404:
        description: Image not found
    """
    image = ImageRepo.get_by_id(
        image_id=image_id, requesting_user_id=UUID(str(requesting_user.id))
    )
    if image:
        trigger_simulate_image_annotation(
            [UUID(str(image.id))], UUID(str(requesting_user.id))
        )
        return jsonify(view_image_schema.dump(image)), 200
    else:
        return jsonify({"message": "Image not found"}), 404


@image_blueprint.route("/image/user/<uuid:user_id>", methods=["GET"])
@jwt_required()
@AuthUtils.inject_requesting_user
def get_images_by_user_id(user_id, requesting_user: User):
    """
    Get all images belonging to a specific user by ID.

    ---
    parameters:
      - name: user_id
        in: path
        description: ID of the user to retrieve images for
        required: true
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: List of images belonging to the user
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/ViewImageSchema'
      404:
        description: No images found for the user
    """

    user_images = ImageRepo.get_by_user_id(
        owner_id=user_id, requesting_user_id=UUID(str(requesting_user.id))
    )

    if user_images:
        return jsonify(view_image_schema.dump(user_images, many=True)), 200
    else:
        return jsonify({"message": "No images found for the user"}), 404


@image_blueprint.route("/image/user/<string:username>", methods=["GET"])
@jwt_required()
@AuthUtils.inject_requesting_user
def get_images_by_username(username: str, requesting_user: User):
    """
    Get all images belonging to a specific user by username.

    ---
    parameters:
      - name: username
        in: path
        description: Username of the user to retrieve images for
        required: true
        schema:
          type: string
    responses:
      200:
        description: List of images belonging to the user
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/ViewImageSchema'
      404:
        description: User not found or no images found for the user
    """
    owner_user = UserRepo.get_by_username(username)
    if not owner_user:
        return jsonify({"message": "User not found"}), 404

    images = ImageRepo.get_by_user_id(
        owner_id=UUID(str(owner_user.id)),
        requesting_user_id=UUID(str(requesting_user.id)),
    )
    return jsonify(view_image_schema.dump(images, many=True)), 200


@image_blueprint.route("/image/<uuid:image_id>/summary", methods=["GET"])
@jwt_required()
@AuthUtils.inject_requesting_user
def get_image_summary(image_id, requesting_user: User):
    """
    Get summary information for a specific image by ID.

    ---
    parameters:
      - name: image_id
        in: path
        description: ID of the image to retrieve summary for
        required: true
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: Image summary information
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ImageSummarySchema'
      404:
        description: Image summary not found
    """
    image = ImageRepo.get_by_id(
        image_id=image_id, requesting_user_id=UUID(str(requesting_user.id))
    )
    if not image:
        return jsonify({"message": "Image not found"}), 404

    image_summary = ImageRepo.get_image_summary(
        image_id, requesting_user_id=UUID(str(requesting_user.id))
    )
    if image_summary and (UUID(str(image.user_id)) == UUID(str(requesting_user.id))):
        return jsonify(image_summary_schema.dump(image_summary)), 200
    else:
        return jsonify({"message": "Image summary not found"}), 404


@image_blueprint.route("/image", methods=["POST"])
@jwt_required()
@AuthUtils.inject_requesting_user
def create_image(requesting_user: User):
    """
    Create a new image.

    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/components/schemas/ImageSchema'
    responses:
      201:
        description: Image created successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ViewImageSchema'
      400:
        description: Bad request - No image data provided or validation error
      401:
        description: Unauthorized - Only the owner of the image can create it
    """
    data = request.json
    if not data:
        return jsonify({"message": "No image data provided"}), 400

    try:
        image_data: dict = image_schema.load(data)
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

    if not str(image_data.get("user_id")) == str(requesting_user.id):
        return jsonify({"error": "Unauthorized"}), 401

    annotation_ids = image_data.pop("annotation_ids", [])
    annotations = [
        AnnotationRepo.get_by_id(annotation_id) for annotation_id in annotation_ids
    ]
    image_data["annotations"] = annotations

    new_image = ImageRepo.create(**image_data)

    return jsonify(view_image_schema.dump(new_image)), 201


@image_blueprint.route("/image/<uuid:image_id>", methods=["PUT"])
@jwt_required()
@AuthUtils.inject_requesting_user
def update_image(image_id, requesting_user: User):
    """
    Update an existing image.

    ---
    parameters:
      - name: image_id
        in: path
        description: ID of the image to update
        required: true
        schema:
          type: string
          format: uuid
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/components/schemas/ImageSchema'
    responses:
      200:
        description: Image updated successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ViewImageSchema'
      400:
        description: Bad request - No image data provided or validation error
      401:
        description: Unauthorized - Only the owner of the image or admin can update it
      404:
        description: Image not found
    """
    data = request.json
    if not data:
        return jsonify({"message": "No image data provided"}), 400

    try:
        image_data: dict = image_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

    image = ImageRepo.get_by_id(
        image_id=image_id, requesting_user_id=UUID(str(requesting_user.id))
    )

    image_user_id = str(image.user_id) if image else None
    image_data_user_id = (
        str(image_data.get("user_id")) if image_data.get("user_id") else None
    )
    requesting_username = (
        str(requesting_user.username) if requesting_user.username else None
    )

    if not (
        image_data_user_id == str(requesting_user.id) == image_user_id
        or requesting_username == Config.ADMIN_USERNAME
    ):
        return jsonify({"error": "Unauthorized"}), 401

    annotation_ids = image_data.pop("annotation_ids", [])
    annotations = [
        AnnotationRepo.get_by_id(annotation_id) for annotation_id in annotation_ids
    ]
    image_data["annotations"] = annotations

    updated_image = ImageRepo.update(image_id, **image_data)

    if updated_image:
        # Trigger image annotation
        trigger_simulate_image_annotation(
            [UUID(str(updated_image.id))], UUID(str(requesting_user.id))
        )

        return jsonify(view_image_schema.dump(updated_image)), 200
    else:
        return jsonify({"message": "Image not found"}), 404


@image_blueprint.route("/image/<uuid:image_id>", methods=["DELETE"])
@jwt_required()
@AuthUtils.inject_requesting_user
def delete_image(image_id, requesting_user: User):
    """
    Delete an existing image.

    ---
    parameters:
      - name: image_id
        in: path
        description: ID of the image to delete
        required: true
        schema:
          type: string
          format: uuid
    responses:
      204:
        description: Image deleted successfully
      401:
        description: Unauthorized - Only the owner of the image or admin can delete it
      404:
        description: Image not found
    """
    image = ImageRepo.get_by_id(
        image_id=image_id, requesting_user_id=requesting_user.id
    )
    image_user_id = str(image.user_id) if image else None
    requesting_username = (
        str(requesting_user.username) if requesting_user.username else None
    )

    if not (
        str(requesting_user.id) == image_user_id
        or requesting_username == Config.ADMIN_USERNAME
    ):
        return jsonify({"error": "Unauthorized"}), 401

    success = ImageRepo.delete(image_id)
    if success:
        return "", 204
    else:
        return jsonify({"message": "Image not found"}), 404
