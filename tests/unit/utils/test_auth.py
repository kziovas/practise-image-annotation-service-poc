from unittest.mock import patch

from flask import Flask

from app.models.user import User
from app.repos.user import UserRepo
from app.utils.auth import AuthUtils


class TestAuthUtils:
    def test_initialize(self, app: Flask) -> None:
        """Test the initialize method."""
        with app.app_context():
            admin_username = app.config.get("ADMIN_USERNAME")
            admin_user = UserRepo.get_by_username(admin_username)
            assert admin_user is not None

    def test_authenticate_valid_credentials(self, app: Flask, new_user: User) -> None:
        """Test the authenticate method with valid credentials."""
        with app.app_context():
            test_username = new_user.username
            test_password = "password"
            with patch(
                "app.utils.auth.UserRepo.get_by_username", return_value=new_user
            ), patch("app.utils.auth.PasswordUtils.verify_password", return_value=True):
                token = AuthUtils.authenticate(test_username, test_password)
                assert token is not None

    def test_authenticate_invalid_credentials(self, app: Flask) -> None:
        """Test the authenticate method with invalid credentials."""
        with app.app_context():
            with patch("app.utils.auth.UserRepo.get_by_username", return_value=None):
                token = AuthUtils.authenticate("invalid_username", "invalid_password")
                assert token is None

    @patch("app.utils.auth.get_jwt_identity", return_value="test_user")
    def test_is_bearer_or_admin_user(
        self, mock_jwt_identity, app: Flask, new_user: User
    ) -> None:
        """Test the is_bearer_or_admin decorator."""
        with app.app_context():
            test_username = new_user.username
            test_password = new_user.password_hash
            token = AuthUtils.authenticate(test_username, test_password)
            with patch(
                "app.utils.auth.UserRepo.get_by_username", return_value=new_user
            ):
                with app.test_request_context(
                    headers={"Authorization": f"Bearer {token}"}
                ):

                    @AuthUtils.is_bearer_or_admin
                    def test_fn(requesting_user=None) -> None:
                        return requesting_user

                    result = test_fn()
                    assert result is not None

    @patch("app.utils.auth.get_jwt_identity", return_value="test_user")
    def test_inject_requesting_user(self, app: Flask, new_user: User) -> None:
        """Test the inject_requesting_user decorator."""
        with app.app_context():
            test_username = new_user.username
            test_password = new_user.password_hash
            token = AuthUtils.authenticate(test_username, test_password)
            with patch(
                "app.utils.auth.UserRepo.get_by_username", return_value=new_user
            ):
                with app.test_request_context(
                    headers={"Authorization": f"Bearer {token}"}
                ):

                    @AuthUtils.inject_requesting_user
                    def test_fn(requesting_user=None) -> None:
                        return requesting_user

                    result = test_fn()
                    assert result.username == new_user.username

    @patch("app.utils.auth.get_jwt_identity", return_value="admin")
    @patch("flask_jwt_extended.verify_jwt_in_request")
    def test_admin_required(
        self, mock_verify_jwt, mock_get_jwt_identity, app: Flask
    ) -> None:
        """Test the admin_required decorator."""

        @AuthUtils.admin_required
        def test_fn() -> str:
            return "Admin route"

        with app.app_context():
            result = test_fn()

            mock_get_jwt_identity.assert_called_once()
            assert result == "Admin route"
