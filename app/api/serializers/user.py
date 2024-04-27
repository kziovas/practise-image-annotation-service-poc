from marshmallow import Schema, ValidationError, fields, validates

from app.repos.user import UserRepo
from app.utils.password import PasswordUtils


class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=False, load_only=True)


class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates("username")
    def validate_username(self, value):
        user = UserRepo.get_by_username(value)
        if not user:
            raise ValidationError("Invalid username")

    @validates("password")
    def validate_password(self, value):
        username = self.context.get("username")
        if username:
            user = UserRepo.get_by_username(username)
            if not user:
                raise ValidationError("Invalid username")

            hashed_password = user.password_hash
            password_matched = PasswordUtils.verify_password(value, hashed_password)
            if not password_matched:
                raise ValidationError("Incorrect password")
        else:
            raise ValidationError("Invalid username")
