from flask import Blueprint, jsonify, request

from app.api.serializers.comment import CommentSchema
from app.api.serializers.image import UpdateImageSchema, ViewImageSchema
from app.core_services import db
from app.models import Annotation, Comment, Image, User

image_blueprint = Blueprint("image", __name__)
view_image_schema = ViewImageSchema()
modify_image_schema = UpdateImageSchema()


@image_blueprint.route("/image", methods=["GET"])
def get_images():
    images = Image.query.all()
    return jsonify(view_image_schema.dump(images, many=True)), 200


@image_blueprint.route("/image/<int:image_id>", methods=["GET"])
def get_image(image_id):
    image = Image.query.get(image_id)
    if image:
        return jsonify(view_image_schema.dump(image)), 200
    else:
        return jsonify({"message": "Image not found"}), 404


@image_blueprint.route("/image/user/<int:user_id>", methods=["GET"])
def get_images_by_user_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    images = Image.query.filter_by(user_id=user_id).all()
    return jsonify(view_image_schema.dump(images, many=True)), 200


@image_blueprint.route("/image/user/<string:username>", methods=["GET"])
def get_images_by_username(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    images = Image.query.filter_by(user_id=user.id).all()
    return jsonify(view_image_schema.dump(images, many=True)), 200


@image_blueprint.route("/image/<int:image_id>/comments", methods=["GET"])
def get_image_comments(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"message": "Image not found"}), 404

    comments = Comment.query.filter_by(image_id=image_id).all()

    return jsonify(CommentSchema().dump(comments, many=True)), 200


@image_blueprint.route("/image", methods=["POST"])
def create_image():
    data = request.json
    if not data:
        return jsonify({"message": "No image data provided"}), 400

    user_id = data.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Extract annotation IDs from the request data
    annotation_ids = data.get("annotation_ids", [])

    new_image = Image(user_id=user_id)
    new_image.filename = data.get("filename")

    # Associate annotations with the image
    if annotation_ids:
        annotations = Annotation.query.filter(Annotation.id.in_(annotation_ids)).all()
        new_image.annotations.extend(annotations)

    db.session.add(new_image)
    db.session.commit()
    return jsonify(modify_image_schema.dump(new_image)), 201


@image_blueprint.route("/image/<int:image_id>", methods=["PUT"])
def update_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"message": "Image not found"}), 404

    data = request.json
    if not data:
        return jsonify({"message": "No image data provided"}), 400

    # Update image attributes
    image.filename = data.get("filename", image.filename)
    image.user_id = data.get("user_id", image.user_id)

    # Update annotations associated with the image
    annotation_ids = data.get("annotation_ids", [])
    if annotation_ids:
        new_annotations = Annotation.query.filter(
            Annotation.id.in_(annotation_ids)
        ).all()
        for annotation in new_annotations:
            if annotation not in image.annotations:
                image.annotations.append(annotation)

    db.session.commit()
    return jsonify(modify_image_schema.dump(image)), 200


@image_blueprint.route("/image/<int:image_id>", methods=["DELETE"])
def delete_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"message": "Image not found"}), 404
    db.session.delete(image)
    db.session.commit()
    return "", 204
