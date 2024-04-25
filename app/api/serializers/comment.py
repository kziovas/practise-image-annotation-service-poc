from marshmallow import Schema, fields

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    body = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
    image_id = fields.Int(dump_only=True)
