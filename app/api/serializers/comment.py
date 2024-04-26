from marshmallow import Schema, fields

class CommentSchema(Schema):
    id = fields.UUID(dump_only=True)
    body = fields.Str(required=True)
    user_id = fields.UUID(required=True, allow_none=False)
    image_id = fields.UUID(required=True, allow_none=False)

