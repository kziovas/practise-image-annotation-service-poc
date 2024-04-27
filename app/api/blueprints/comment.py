from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.api.serializers.comment import CommentSchema
from app.config import Config
from app.models.user import User
from app.repos.comment import CommentRepo
from app.repos.image import ImageRepo
from app.repos.user import UserRepo
from app.services.image_summary_service import ImageSummaryService
from app.utils.auth import AuthUtils

comment_blueprint = Blueprint("comment", __name__)
comment_schema = CommentSchema()


@comment_blueprint.route("/comment", methods=["GET"])
@jwt_required()
@AuthUtils.admin_required
def get_comments():
    """
    Get all comments.

    ---
    responses:
      200:
        description: List of comments
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/CommentSchema'
    """
    comments = CommentRepo.get_all()
    return jsonify(comment_schema.dump(comments, many=True)), 200


@comment_blueprint.route("/comment/<uuid:comment_id>", methods=["GET"])
@jwt_required()
@AuthUtils.inject_requesting_user
def get_comment(comment_id, requesting_user: User):
    """
    Get a specific comment by ID.

    ---
    parameters:
      - name: comment_id
        in: path
        description: ID of the comment to retrieve
        required: true
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: Comment details
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommentSchema'
      404:
        description: Comment not found
    """
    comment = CommentRepo.get_by_id(comment_id)
    if comment:
        return jsonify(comment_schema.dump(comment)), 200
    else:
        return jsonify({"message": "Comment not found"}), 404


@comment_blueprint.route("/comment", methods=["POST"])
@jwt_required()
@AuthUtils.inject_requesting_user
def create_comment(requesting_user: User):
    """
    Create a new comment.

    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CommentSchema'
    responses:
      201:
        description: Created comment
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommentSchema'
      400:
        description: Invalid request data
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    data = request.json
    if not data:
        return jsonify({"message": "No comment data provided"}), 400

    user_id = data.get("user_id")
    user = UserRepo.get_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    image_id = data.get("image_id")
    image = ImageRepo.get_by_id(image_id, requesting_user_id=requesting_user.id)
    if not image:
        return jsonify({"message": "Image not found"}), 404
    if not (
        (str(requesting_user.id) == user_id)
        or str(requesting_user.username) == Config.ADMIN_USERNAME
    ):
        return jsonify({"error": "Unauthorized"}), 401

    body = data.get("body")
    new_comment = CommentRepo.create(body=body, user_id=user_id, image_id=image_id)
    ImageSummaryService.update_image_summary(image_id)

    return jsonify(comment_schema.dump(new_comment)), 201


@comment_blueprint.route("/comment/user/<uuid:user_id>", methods=["GET"])
@jwt_required()
@AuthUtils.is_bearer_or_admin
def get_comments_by_user_id(user_id):
    """
    Get all comments by user ID.

    ---
    parameters:
      - name: user_id
        in: path
        description: ID of the user whose comments to retrieve
        required: true
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: List of comments by user
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/CommentSchema'
      404:
        description: No comments found for the user
    """
    user_comments = CommentRepo.get_by_user_id(user_id)
    if user_comments:
        return jsonify(comment_schema.dump(user_comments, many=True)), 200
    else:
        return jsonify({"message": "No comments found for the user"}), 404


@comment_blueprint.route("/comment/image/<uuid:image_id>", methods=["GET"])
@jwt_required()
@AuthUtils.inject_requesting_user
def get_comments_by_image_id(image_id, requesting_user: User):
    """
    Get all comments for an image by image ID.

    ---
    parameters:
      - name: image_id
        in: path
        description: ID of the image whose comments to retrieve
        required: true
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: List of comments for the image
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/CommentSchema'
      404:
        description: No comments found for the image
    """
    image_comments = CommentRepo.get_by_image_id(image_id)
    if image_comments:
        return jsonify(comment_schema.dump(image_comments, many=True)), 200
    else:
        return jsonify({"message": "No comments found for the image"}), 404


@comment_blueprint.route("/comment/<uuid:comment_id>", methods=["PUT"])
@jwt_required()
@AuthUtils.inject_requesting_user
def update_comment(comment_id, requesting_user: User):
    """
    Update an existing comment.

    ---
    parameters:
      - name: comment_id
        in: path
        description: ID of the comment to update
        required: true
        schema:
          type: string
          format: uuid
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CommentSchema'
    responses:
      200:
        description: Updated comment
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommentSchema'
      400:
        description: Invalid request data
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Comment not found
    """
    data = request.json
    if not data:
        return jsonify({"message": "No comment data provided"}), 400

    body = data.get("body")
    if not body:
        return jsonify({"message": "No comment body provided"}), 400

    comment = CommentRepo.get_by_id(comment_id)
    if not comment:
        return jsonify({"message": "Comment not found"}), 404
    if not (
        str(comment.user_id) == str(requesting_user.id)
        or str(requesting_user.username) == Config.ADMIN_USERNAME
    ):
        return jsonify({"error": "Unauthorized"}), 401

    updated_comment = CommentRepo.update(comment_id, body)
    ImageSummaryService.update_image_summary(comment.image_id)
    return jsonify(comment_schema.dump(updated_comment)), 200


@comment_blueprint.route("/comment/<uuid:comment_id>", methods=["DELETE"])
@jwt_required()
@AuthUtils.inject_requesting_user
def delete_comment(comment_id, requesting_user: User):
    """
    Delete an existing comment.

    ---
    parameters:
      - name: comment_id
        in: path
        description: ID of the comment to delete
        required: true
        schema:
          type: string
          format: uuid
    responses:
      204:
        description: Comment deleted successfully
      404:
        description: Comment not found
      401:
        description: Unauthorized - Only the owner of the comment or admin can delete it
    """
    comment = CommentRepo.get_by_id(comment_id)
    if not comment:
        return jsonify({"message": "Comment not found"}), 404

    if not (
        str(comment.user_id) == str(requesting_user.id)
        or str(requesting_user.username) == Config.ADMIN_USERNAME
    ):
        return jsonify({"error": "Unauthorized"}), 401

    image_id = comment.image_id
    success = CommentRepo.delete(comment_id)
    if success:
        ImageSummaryService.update_image_summary(image_id)
        return "", 204
    else:
        return jsonify({"message": "Comment not found"}), 404
