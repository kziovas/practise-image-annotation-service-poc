from flask import Blueprint, jsonify, request

from app.api.serializers.comment import CommentSchema
from app.repos.comment import CommentRepo
from app.repos.image import ImageRepo
from app.repos.user import UserRepo

comment_blueprint = Blueprint("comment", __name__)
comment_schema = CommentSchema()


@comment_blueprint.route("/comment", methods=["GET"])
def get_comments():
    comments = CommentRepo.get_all()
    return jsonify(comment_schema.dump(comments, many=True)), 200


@comment_blueprint.route("/comment/<uuid:comment_id>", methods=["GET"])
def get_comment(comment_id):
    comment = CommentRepo.get_by_id(comment_id)
    if comment:
        return jsonify(comment_schema.dump(comment)), 200
    else:
        return jsonify({"message": "Comment not found"}), 404


@comment_blueprint.route("/comment", methods=["POST"])
def create_comment():
    data = request.json
    if not data:
        return jsonify({"message": "No comment data provided"}), 400

    user_id = data.get("user_id")
    user = UserRepo.get_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    image_id = data.get("image_id")
    image = ImageRepo.get_by_id(image_id)
    if not image:
        return jsonify({"message": "Image not found"}), 404

    body = data.get("body")
    new_comment = CommentRepo.create(body=body, user_id=user_id, image_id=image_id)
    return jsonify(comment_schema.dump(new_comment)), 201


@comment_blueprint.route("/comment/user/<uuid:user_id>", methods=["GET"])
def get_comments_by_user_id(user_id):
    user_comments = CommentRepo.get_by_user_id(user_id)
    if user_comments:
        return jsonify(comment_schema.dump(user_comments, many=True)), 200
    else:
        return jsonify({"message": "No comments found for the user"}), 404


@comment_blueprint.route("/comment/image/<uuid:image_id>", methods=["GET"])
def get_comments_by_image_id(image_id):
    image_comments = CommentRepo.get_by_image_id(image_id)
    if image_comments:
        return jsonify(comment_schema.dump(image_comments, many=True)), 200
    else:
        return jsonify({"message": "No comments found for the image"}), 404


@comment_blueprint.route("/comment/<uuid:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    data = request.json
    if not data:
        return jsonify({"message": "No comment data provided"}), 400

    body = data.get("body")
    if not body:
        return jsonify({"message": "No comment body provided"}), 400

    comment = CommentRepo.get_by_id(comment_id)
    if not comment:
        return jsonify({"message": "Comment not found"}), 404

    updated_comment = CommentRepo.update(comment_id, body)
    return jsonify(comment_schema.dump(updated_comment)), 200


@comment_blueprint.route("/comment/<uuid:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    success = CommentRepo.delete(comment_id)
    if success:
        return "", 204
    else:
        return jsonify({"message": "Comment not found"}), 404
