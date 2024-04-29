from uuid import UUID

import pytest

from app.models.user import User



class TestUserModel:
    def test_user_creation(self, new_user):
        assert new_user.username == "test_user"
        assert new_user.email == "test@example.com"
        assert new_user.password_hash == "hashed_password"

    def test_user_representation(self, new_user):
        assert repr(new_user) == "<User test_user>"

    def test_user_id_generation(self, new_user):
        assert isinstance(new_user.id, UUID)
