import hashlib
from unittest.mock import patch

import pytest

from app.errors import SecretKeyNotFoundError
from app.utils.password import PasswordUtils


class TestPasswordUtils:

    @patch("app.utils.password.PasswordUtils._get_secret_key", return_value="test_key")
    def test_hash_password(self, mock_get_secret_key, app):
        """Test the hash_password method."""
        PasswordUtils.initialize(app)
        hashed_password = PasswordUtils.hash_password("password")
        assert (
            hashed_password
            == hashlib.sha256("passwordtest_key".encode("utf-8")).hexdigest()
        )

    @patch("app.utils.password.PasswordUtils._get_secret_key", return_value=None)
    def test_hash_password_secret_key_not_found(self, mock_get_secret_key, app):
        """Test hash_password when the secret key is not found."""
        PasswordUtils.initialize(app)
        with pytest.raises(SecretKeyNotFoundError):
            PasswordUtils.hash_password("password")

    @patch("app.utils.password.PasswordUtils._get_secret_key", return_value="test_key")
    def test_verify_password(self, mock_get_secret_key, app):
        """Test the verify_password method."""
        PasswordUtils.initialize(app)
        hashed_password = hashlib.sha256("passwordtest_key".encode("utf-8")).hexdigest()
        assert PasswordUtils.verify_password("password", hashed_password)

    @patch("app.utils.password.PasswordUtils._get_secret_key", return_value="test_key")
    def test_verify_password_invalid_password(self, mock_get_secret_key, app):
        """Test verify_password with an invalid password."""
        PasswordUtils.initialize(app)
        hashed_password = hashlib.sha256("passwordtest_key".encode("utf-8")).hexdigest()
        assert not PasswordUtils.verify_password("invalid_password", hashed_password)
