from flask import Blueprint, jsonify, request

from app.api.entities.annotation import AnnotationResponse
from app.api.serializers.annotation import AnnotationSchema
from app.core_services import db
from app.models import Annotation

annotation_blueprint = Blueprint("annotation", __name__)
annotation_schema = AnnotationSchema()


@annotation_blueprint.route("/annotation", methods=["GET"])
def get_annotations():
    annotations_db = Annotation.query.all()
    annotations_response = []

    for annotation in annotations_db:
        image_ids = [image.id for image in annotation.images]
        annotation_data = AnnotationResponse(
            id=annotation.id, name=annotation.name, images=image_ids
        )
        annotations_response.append(annotation_data)

    # Dump the constructed data structure using the schema
    return jsonify(annotation_schema.dump(annotations_response, many=True)), 200


@annotation_blueprint.route("/annotation/<int:annotation_id>", methods=["GET"])
def get_annotation(annotation_id):
    annotation = Annotation.query.get(annotation_id)
    if annotation:
        image_ids = [image.id for image in annotation.images]
        annotation_response = AnnotationResponse(
            id=annotation.id, name=annotation.name, images=image_ids
        )
        return jsonify(annotation_schema.dump(annotation_response)), 200
    else:
        return jsonify({"message": "Annotation not found"}), 404


@annotation_blueprint.route("/annotation", methods=["POST"])
def create_annotation():
    data = request.json
    if not data:
        return jsonify({"message": "No annotation data provided"}), 400
    errors = annotation_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_annotation = Annotation(name=data.get("name"))
    db.session.add(new_annotation)
    db.session.commit()
    return jsonify(annotation_schema.dump(new_annotation)), 201


@annotation_blueprint.route("/annotation/<int:annotation_id>", methods=["PUT"])
def update_annotation(annotation_id):
    annotation = Annotation.query.get(annotation_id)
    if not annotation:
        return jsonify({"message": "Annotation not found"}), 404
    data = request.json
    if not data:
        return jsonify({"message": "No annotation data provided"}), 400
    errors = annotation_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    annotation.name = data.get("name", annotation.name)
    db.session.commit()
    return jsonify(annotation_schema.dump(annotation)), 200


@annotation_blueprint.route("/annotation/<int:annotation_id>", methods=["DELETE"])
def delete_annotation(annotation_id):
    annotation = Annotation.query.get(annotation_id)
    if not annotation:
        return jsonify({"message": "Annotation not found"}), 404
    db.session.delete(annotation)
    db.session.commit()
    return "", 204
