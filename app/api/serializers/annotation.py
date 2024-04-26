from marshmallow import Schema, fields


class AnnotationSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    images = fields.List(fields.Int, dump_only=True)
