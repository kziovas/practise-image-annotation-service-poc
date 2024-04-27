from functools import wraps

from flask import Flask, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity

from app.config import Config
from app.repos.user import UserRepo
from app.utils.password import PasswordUtils


class AuthUtils:
    @classmethod
    def initialize(cls, app: Flask) -> None:
        """Initialize the AuthUtils class with the Flask app instance."""
        with app.app_context():
            admin_username = app.config.get("ADMIN_USERNAME", Config.ADMIN_USERNAME)
            admin_password = app.config.get("ADMIN_PASSWORD", Config.ADMIN_PASSWORD)
            admin_user = UserRepo.get_by_username(admin_username)
            if not admin_user:
                UserRepo.create(
                    username=admin_username,
                    email="admin@example.com",
                    password=admin_password,
                )

    @classmethod
    def authenticate(cls, username: str, password: str):
        """Authenticate the user based on username and password.

        Args:
            username (str): The username of the user.
            password (str): The password provided by the user.

        Returns:
            str: JWT token if authentication succeeds, None otherwise.
        """
        user = UserRepo.get_by_username(username)
        if user:
            hashed_password = user.password_hash
            if PasswordUtils.verify_password(password, hashed_password):
                # Authentication successful, return JWT token
                return create_access_token(identity=username)
        return None

    @classmethod
    def is_bearer_or_admin(cls, fn):
        """Decorator to check if the token bearer is the user or admin."""

        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user_id = kwargs.get("user_id")
            user = UserRepo.get_by_username(current_user)
            if user:
                if (str(user.id) == str(user_id)) or (
                    current_user == Config.ADMIN_USERNAME
                ):
                    return fn(*args, **kwargs)
            return jsonify({"error": "Unauthorized"}), 401

        return wrapper

    @classmethod
    def inject_requesting_user(cls, fn):
        """Decorator to inject the requesting user into the method if it exists."""

        @wraps(fn)
        def wrapper(*args, **kwargs):
            requesting_username = get_jwt_identity()
            requesting_user = UserRepo.get_by_username(requesting_username)
            if requesting_user:
                kwargs["requesting_user"] = requesting_user
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "User not found"}), 404

        return wrapper

    @classmethod
    def admin_required(cls, fn):
        """Decorator to require admin privileges for a route."""

        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user == "admin":
                return fn(*args, **kwargs)
            else:
                return jsonify({"error": "Admin privileges required"}), 403

        return wrapper
