from flask import Blueprint, jsonify, request
from app.api.serializers.annotation import AnnotationSchema
from app.repos.annotation import AnnotationRepo

annotation_blueprint = Blueprint("annotation", __name__)
annotation_schema = AnnotationSchema()

@annotation_blueprint.route("/annotation", methods=["GET"])
def get_annotations():
    annotations = AnnotationRepo.get_all()
    return jsonify(annotation_schema.dump(annotations, many=True)), 200

@annotation_blueprint.route("/annotation/<int:annotation_id>", methods=["GET"])
def get_annotation(annotation_id):
    annotation = AnnotationRepo.get_by_id(annotation_id)
    if annotation:
        return jsonify(annotation_schema.dump(annotation)), 200
    else:
        return jsonify({"message": "Annotation not found"}), 404

@annotation_blueprint.route("/annotation", methods=["POST"])
def create_annotation():
    data = request.json
    if not data:
        return jsonify({"message": "No annotation data provided"}), 400
    name = data.get("name")
    if not name:
        return jsonify({"message": "Name is required"}), 400

    new_annotation = AnnotationRepo.create(name=name)
    return jsonify(annotation_schema.dump(new_annotation)), 201

@annotation_blueprint.route("/annotation/<int:annotation_id>", methods=["PUT"])
def update_annotation(annotation_id):
    data = request.json
    if not data:
        return jsonify({"message": "No annotation data provided"}), 400
    name = data.get("name")
    if not name:
        return jsonify({"message": "Name is required"}), 400

    annotation = AnnotationRepo.get_by_id(annotation_id)
    if not annotation:
        return jsonify({"message": "Annotation not found"}), 404

    updated_annotation = AnnotationRepo.update(annotation_id, name)
    return jsonify(annotation_schema.dump(updated_annotation)), 200

@annotation_blueprint.route("/annotation/<int:annotation_id>", methods=["DELETE"])
def delete_annotation(annotation_id):
    success = AnnotationRepo.delete(annotation_id)
    if success:
        return "", 204
    else:
        return jsonify({"message": "Annotation not found"}), 404
