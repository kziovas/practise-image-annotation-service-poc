from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password_hash = fields.Str(required=True, load_only=True)
