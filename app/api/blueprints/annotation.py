from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.api.serializers.annotation import AnnotationSchema
from app.repos.annotation import AnnotationRepo
from app.utils.auth import AuthUtils

annotation_blueprint = Blueprint("annotation", __name__)
annotation_schema = AnnotationSchema()


@annotation_blueprint.route("/annotation/annotations", methods=["GET"])
@jwt_required()
def get_annotations():
    """
    Get all annotations.

    ---
    responses:
      200:
        description: List of annotations
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/AnnotationSchema'
    """
    annotations = AnnotationRepo.get_all()
    return jsonify(annotation_schema.dump(annotations, many=True)), 200


@annotation_blueprint.route("/annotation/<uuid:annotation_id>", methods=["GET"])
@jwt_required()
def get_annotation(annotation_id: str):
    """
    Get a specific annotation by ID.

    ---
    parameters:
      - name: annotation_id
        in: path
        description: ID of the annotation to retrieve
        required: true
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: Annotation details
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AnnotationSchema'
      404:
        description: Annotation not found
    """
    annotation = AnnotationRepo.get_by_id(annotation_id)
    if annotation:
        return jsonify(annotation_schema.dump(annotation)), 200
    else:
        return jsonify({"message": "Annotation not found"}), 404


@annotation_blueprint.route("/annotation", methods=["POST"])
@jwt_required()
@AuthUtils.admin_required
def create_annotation():
    """
    Create a new annotation.

    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/AnnotationSchema'
    responses:
      201:
        description: Created annotation
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AnnotationSchema'
      400:
        description: Validation error
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                errors:
                  type: object
    """
    try:
        annotation_data = annotation_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

    new_annotation = AnnotationRepo.create(name=annotation_data.get("name"))
    return jsonify(annotation_schema.dump(new_annotation)), 201


@annotation_blueprint.route("/annotation/<uuid:annotation_id>", methods=["PUT"])
@jwt_required()
@AuthUtils.admin_required
def update_annotation(annotation_id: str):
    """
    Update an existing annotation.

    ---
    parameters:
      - name: annotation_id
        in: path
        description: ID of the annotation to update
        required: true
        schema:
          type: string
          format: uuid
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/AnnotationSchema'
    responses:
      200:
        description: Updated annotation
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AnnotationSchema'
      400:
        description: Validation error
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                errors:
                  type: object
      404:
        description: Annotation not found
    """
    try:
        annotation_data = annotation_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

    annotation = AnnotationRepo.get_by_id(annotation_id)
    if not annotation:
        return jsonify({"message": "Annotation not found"}), 404

    updated_annotation = AnnotationRepo.update(
        annotation_id, name=annotation_data.get("name")
    )
    return jsonify(annotation_schema.dump(updated_annotation)), 200


@annotation_blueprint.route("/annotation/<uuid:annotation_id>", methods=["DELETE"])
@jwt_required()
@AuthUtils.admin_required
def delete_annotation(annotation_id: str):
    """
    Delete an existing annotation.

    ---
    parameters:
      - name: annotation_id
        in: path
        description: ID of the annotation to delete
        required: true
        schema:
          type: string
          format: uuid
    responses:
      204:
        description: Annotation deleted successfully
      404:
        description: Annotation not found
    """
    success = AnnotationRepo.delete(annotation_id)
    if success:
        return "", 204
    else:
        return jsonify({"message": "Annotation not found"}), 404
