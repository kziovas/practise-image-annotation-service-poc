import hashlib
from typing import Optional

from flask import Flask

from app.errors import SecretKeyNotFoundError


class PasswordUtils:
    _app_config = None

    @classmethod
    def initialize(cls, app: Flask) -> None:
        """Initialize the PasswordUtils class with the Flask app instance."""
        cls._app_config = app.config

    @staticmethod
    def _get_secret_key() -> Optional[str]:
       """Retrieve the secret key from the Flask app config.

        Returns:
            Optional[str]: The secret key if found, or None if not found.
        """
        return PasswordUtils._app_config.get("SECRET_KEY")

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes the given password using the secret key.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.

        Raises:
            SecretKeyNotFoundError: If the secret key is not found in the Flask app config.
        """
        secret_key = PasswordUtils._get_secret_key()

        if secret_key is None:
            raise SecretKeyNotFoundError("SECRET_KEY not found in Flask app config")
        hashed_password = hashlib.sha256(
            (password + secret_key).encode("utf-8")
        ).hexdigest()
        return hashed_password

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        """Verifies if the given password matches the hashed password.

        Args:
            password (str): The password to be verified.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return (
            hashlib.sha256(
                (password + cls._get_secret_key()).encode("utf-8")
            ).hexdigest()
            == hashed_password
        )
