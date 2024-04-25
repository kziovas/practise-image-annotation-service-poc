from marshmallow import Schema, fields

from app.api.serializers.annotation import AnnotationSchema
from app.api.serializers.comment import CommentSchema


class ImageSchema(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.Str(required=True)
    user_id = fields.Int(required=True, allow_none=False)
    comments = fields.Nested(CommentSchema, many=True, dump_only=True)


class ModifyImageSchema(ImageSchema):
    annotation_ids = fields.List(fields.Int, load_only=True)


class ViewImageSchema(ImageSchema):
    annotations = fields.Nested(AnnotationSchema, many=True, dump_only=True)
