from marshmallow import Schema, fields

from app.api.serializers.annotation import AnnotationSchema
from app.api.serializers.comment import CommentSchema


class ImageSchema(Schema):
    id = fields.UUID(dump_only=True)
    filename = fields.Str(required=True)
    user_id = fields.UUID(required=True, allow_none=False)
    comments = fields.Nested(CommentSchema, many=True, dump_only=True)


class UpdateImageSchema(ImageSchema):
    annotation_ids = fields.List(fields.UUID, required=False, load_only=True)


class ViewImageSchema(ImageSchema):
    annotations = fields.Nested(AnnotationSchema, many=True, dump_only=True)
    annotation_status = fields.Str(required=True, dump_only=True)
