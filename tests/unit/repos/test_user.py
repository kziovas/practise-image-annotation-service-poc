from uuid import UUID

import pytest

from app.models.user import User
from app.repos.user import UserRepo


class TestUserRepo:

    def test_get_user_by_id(self, new_user):
        retrieved_user = UserRepo.get_by_id(new_user.id)
        assert retrieved_user == new_user

    def test_get_user_by_username(self, new_user):
        retrieved_user = UserRepo.get_by_username("test_user")
        assert retrieved_user == new_user

    def test_update_user(self, new_user):
        updated_user = UserRepo.update(new_user.id, username="updated_username")
        assert updated_user.username == "updated_username"

    def test_delete_user(self, new_user):
        assert UserRepo.delete(new_user.id) == True
