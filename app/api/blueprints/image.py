from uuid import UUID

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError
from werkzeug.utils import secure_filename

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
    images = ImageRepo.get_all()
    return jsonify(view_image_schema.dump(images, many=True)), 200


@image_blueprint.route("/image/images", methods=["GET"])
@jwt_required()
@AuthUtils.inject_requesting_user
def get_all_allowed_images(requesting_user: User):
    images = ImageRepo.get_all_allowed(requesting_user_id=requesting_user.id)
    return jsonify(view_image_schema.dump(images, many=True)), 200


@image_blueprint.route("/image/<uuid:image_id>", methods=["GET"])
@jwt_required()
@AuthUtils.inject_requesting_user
def get_image(image_id, requesting_user: User):
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
    image = ImageRepo.get_by_id(
        image_id=image_id, requesting_user_id=UUID(str(requesting_user.id))
    )
    if not image:
        return jsonify({"message": "Image not found"}), 404

    image_summary = ImageRepo.get_image_summary(image_id)
    if image_summary and (UUID(str(image.user_id)) == UUID(str(requesting_user.id))):
        return jsonify(image_summary_schema.dump(image_summary)), 200
    else:
        return jsonify({"message": "Image summary not found"}), 404


@image_blueprint.route("/image", methods=["POST"])
@jwt_required()
@AuthUtils.inject_requesting_user
def create_image(requesting_user: User):
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
