from flask import Blueprint, jsonify, request

from app.api.serializers.user import UserSchema
from app.repos.user import UserRepo

user_blueprint = Blueprint("user", __name__)
user_schema = UserSchema()


@user_blueprint.route("/user/users", methods=["GET"])
def get_users():
    users = UserRepo.get_all()
    return jsonify(user_schema.dump(users, many=True)), 200


@user_blueprint.route("/user/<uuid:user_id>", methods=["GET"])
def get_user(user_id):
    user = UserRepo.get_by_id(user_id)
    if user:
        return jsonify(user_schema.dump(user)), 200
    else:
        return jsonify({"message": "User not found"}), 404


@user_blueprint.route("/user/email/<string:email>", methods=["GET"])
def get_user_by_email(email):
    user = UserRepo.get_by_email(email)
    if user:
        return jsonify(user_schema.dump(user)), 200
    else:
        return jsonify({"message": "User not found"}), 404


@user_blueprint.route("/user/username/<string:username>", methods=["GET"])
def get_user_by_username(username):
    user = UserRepo.get_by_username(username)
    if user:
        return jsonify(user_schema.dump(user)), 200
    else:
        return jsonify({"message": "User not found"}), 404


@user_blueprint.route("/user", methods=["POST"])
def create_user():
    data = request.json
    if not data:
        return jsonify({"message": "No user data provided"}), 400
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    new_user = UserRepo.create(
        username=data.get("username"),
        email=data.get("email"),
        password_hash=data.get("password_hash"),
    )

    return jsonify(user_schema.dump(new_user)), 201


@user_blueprint.route("/user/<uuid:user_id>", methods=["PUT"])
def update_user(user_id):
    user = UserRepo.get_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    data = request.json
    if not data:
        return jsonify({"message": "No user data provided"}), 400
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    updated_user = UserRepo.update(
        user_id=user_id,
        username=data.get("username", user.username),
        email=data.get("email", user.email),
        password_hash=data.get("password_hash", user.password_hash),
    )

    return jsonify(user_schema.dump(updated_user)), 200


@user_blueprint.route("/user/<uuid:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = UserRepo.get_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    if UserRepo.delete(user_id=user_id):
        return "", 204
    else:
        return jsonify({"message": "User deletion failed"}), 404
