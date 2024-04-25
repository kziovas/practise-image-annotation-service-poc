from marshmallow import Schema, fields

class ImageSchema(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.Str(required=True)
    user_id = fields.Int(dump_only=True)
