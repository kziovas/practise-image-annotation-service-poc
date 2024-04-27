from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from app.api.serializers.user import UserLoginSchema, UserSchema
from app.config import Config
from app.repos.user import UserRepo
from app.utils.auth import AuthUtils

user_blueprint = Blueprint("user", __name__)
user_schema = UserSchema()
user_login_schema = UserLoginSchema()


@user_blueprint.route("/user/login", methods=["POST"])
def login():
    """
    Authenticate a user and generate an access token.

    ---
    parameters:
      - name: Content-Type
        in: header
        required: true
        description: Content type header
        schema:
        type: string
        default: application/json
      - name: body
        in: body
        required: true
        description: JSON object containing username and password
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Authentication successful, returns access token
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
      400:
        description: Bad request - Request body must be JSON or validation error
      401:
        description: Unauthorized - Invalid username or password
    """
    if not request.json:
        return jsonify({"error": "Request body must be JSON"}), 400

    login_data = request.json
    try:
        user_login_schema.context = {"username": login_data.get("username")}
        validated_login_data = user_login_schema.load(login_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if not isinstance(validated_login_data, dict):
        return jsonify({"error": "Invalid login data"}), 400
    username = validated_login_data.get("username", "")
    password = validated_login_data.get("password", "")
    token = AuthUtils.authenticate(username, password)
    if token:
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@user_blueprint.route("/user/users", methods=["GET"])
@jwt_required()
@AuthUtils.admin_required
def get_users():
    """
    Get all users.

    ---
    responses:
      200:
        description: List of users
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/UserSchema'
    """
    users = UserRepo.get_all()
    return jsonify(user_schema.dump(users, many=True)), 200


@user_blueprint.route("/user/<uuid:user_id>", methods=["GET"])
@jwt_required()
@AuthUtils.admin_required
def get_user_by_id(user_id):
    """
    Get a user by ID.

    ---
    parameters:
      - name: user_id
        in: path
        description: ID of the user to retrieve
        required: true
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: User details
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserSchema'
      404:
        description: User not found
    """
    user = UserRepo.get_by_id(user_id=user_id)
    if user:
        return jsonify(user_schema.dump(user)), 200
    else:
        return jsonify({"message": "User not found"}), 404


@user_blueprint.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    """
    Get current user details.

    ---
    responses:
      200:
        description: Current user details
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserSchema'
      404:
        description: User not found
    """
    username = get_jwt_identity()
    user = UserRepo.get_by_username(username)
    if user:
        return jsonify(user_schema.dump(user)), 200
    else:
        return jsonify({"message": "User not found"}), 404


@user_blueprint.route("/user/email/<string:email>", methods=["GET"])
@jwt_required()
def get_user_by_email(email):
    """
    Get a user by email.

    ---
    parameters:
      - name: email
        in: path
        description: Email of the user to retrieve
        required: true
        schema:
          type: string
    responses:
      200:
        description: User details
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserSchema'
      404:
        description: User not found or unauthorized
    """
    requesting_username = get_jwt_identity()
    user = UserRepo.get_by_email(email)
    if user and (
        user.username == requesting_username
        or str(requesting_username) == Config.ADMIN_USERNAME
    ):
        return jsonify(user_schema.dump(user)), 200
    else:
        return jsonify({"message": "User not found or unauthorized"}), 404


@user_blueprint.route("/user", methods=["POST"])
def create_user():
    """
    Create a new user.

    ---
    parameters:
      - name: body
        in: body
        required: true
        description: JSON object containing user details
        schema:
          $ref: '#/components/schemas/UserSchema'
    responses:
      201:
        description: User created successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserSchema'
      400:
        description: Bad request - No user data provided or validation error
    """
    data = request.json
    if not data:
        return jsonify({"message": "No user data provided"}), 400
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    new_user = UserRepo.create(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password"),
    )

    return jsonify(user_schema.dump(new_user)), 201


@user_blueprint.route("/user/<uuid:user_id>", methods=["PUT"])
@jwt_required()
@AuthUtils.is_bearer_or_admin
def update_user(user_id):
    """
    Update an existing user.

    ---
    parameters:
      - name: user_id
        in: path
        description: ID of the user to update
        required: true
        schema:
          type: string
          format: uuid
      - name: body
        in: body
        required: true
        description: JSON object containing user details
        schema:
          $ref: '#/components/schemas/UserSchema'
    responses:
      200:
        description: User updated successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserSchema'
      400:
        description: Bad request - No user data provided or validation error
      404:
        description: User not found
    """
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
        password=data.get("password"),
    )

    return jsonify(user_schema.dump(updated_user)), 200


@user_blueprint.route("/user/<uuid:user_id>", methods=["DELETE"])
@jwt_required()
@AuthUtils.is_bearer_or_admin
def delete_user(user_id):
    """
    Delete a user.

    ---
    parameters:
      - name: user_id
        in: path
        description: ID of the user to delete
        required: true
        schema:
          type: string
          format: uuid
    responses:
      204:
        description: User deleted successfully
      404:
        description: User not found
    """
    user = UserRepo.get_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    if UserRepo.delete(user_id=user_id):
        return "", 204
    else:
        return jsonify({"message": "User deletion failed"}), 404
