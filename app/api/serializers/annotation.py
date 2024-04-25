from marshmallow import Schema, fields

class AnnotationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
