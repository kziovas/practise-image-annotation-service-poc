from flask import Blueprint, jsonify, request

from app.api.serializers.comment import CommentSchema
from app.api.serializers.image import UpdateImageSchema, ViewImageSchema
from app.api.serializers.image_summary import ImageSummarySchema
from app.repos.comment import CommentRepo
from app.repos.image import ImageRepo
from app.repos.user import UserRepo
from app.services.image_summary_service import ImageSummaryService

image_blueprint = Blueprint("image", __name__)
view_image_schema = ViewImageSchema()
modify_image_schema = UpdateImageSchema()
comment_schema = CommentSchema()
image_summary_schema = ImageSummarySchema()


@image_blueprint.route("/image", methods=["GET"])
def get_images():
    images = ImageRepo.get_all()
    return jsonify(view_image_schema.dump(images, many=True)), 200


@image_blueprint.route("/image/<uuid:image_id>", methods=["GET"])
def get_image(image_id):
    image = ImageRepo.get_by_id(image_id)
    if image:
        return jsonify(view_image_schema.dump(image)), 200
    else:
        return jsonify({"message": "Image not found"}), 404


@image_blueprint.route("/image/user/<uuid:user_id>", methods=["GET"])
def get_images_by_user_id(user_id):
    user_images = ImageRepo.get_by_user_id(user_id)
    if user_images:
        return jsonify(view_image_schema.dump(user_images, many=True)), 200
    else:
        return jsonify({"message": "No images found for the user"}), 404


@image_blueprint.route("/image/user/<string:username>", methods=["GET"])
def get_images_by_username(username):
    user = UserRepo.get_by_username(username)
    if not user:
        return jsonify({"message": "User not found"}), 404

    images = ImageRepo.get_by_user_id(user.id)
    return jsonify(view_image_schema.dump(images, many=True)), 200


@image_blueprint.route("/image/<uuid:image_id>/comments", methods=["GET"])
def get_image_comments(image_id):
    comments = CommentRepo.get_by_image_id(image_id)
    return jsonify(comment_schema.dump(comments, many=True)), 200


@image_blueprint.route("/image/<uuid:image_id>/summary", methods=["GET"])
def get_image_summary(image_id):
    image_summary = ImageRepo.get_image_summary(image_id)
    if image_summary:
        return jsonify(image_summary_schema.dump(image_summary)), 200
    else:
        return jsonify({"message": "Image summary not found"}), 404


@image_blueprint.route("/image", methods=["POST"])
def create_image():
    data = request.json
    if not data:
        return jsonify({"message": "No image data provided"}), 400

    user_id = data.get("user_id")
    user = UserRepo.get_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    new_image = ImageRepo.create(user_id=user_id, filename=data.get("filename"))
    ImageSummaryService.update_image_summary(new_image.id)
    return jsonify(modify_image_schema.dump(new_image)), 201


@image_blueprint.route("/image/<uuid:image_id>", methods=["PUT"])
def update_image(image_id):
    data = request.json
    if not data:
        return jsonify({"message": "No image data provided"}), 400

    image = ImageRepo.get_by_id(image_id)
    if not image:
        return jsonify({"message": "Image not found"}), 404

    updated_image = ImageRepo.update(image_id, **data)
    ImageSummaryService.update_image_summary(image_id)
    return jsonify(modify_image_schema.dump(updated_image)), 200


@image_blueprint.route("/image/<uuid:image_id>", methods=["DELETE"])
def delete_image(image_id):
    success = ImageRepo.delete(image_id)
    if success:
        return "", 204
    else:
        return jsonify({"message": "Image not found"}), 404
