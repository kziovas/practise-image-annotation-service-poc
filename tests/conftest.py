# tests/conftest.py

import pytest

from app.models.user import User
from app.services.core_services import db


@pytest.fixture(scope="module")
def new_user():
    user = User(
        username="test_user", email="test@example.com", password_hash="password"
    )
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()


@pytest.fixture(scope="module")
def new_user_data():
    return {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password",
    }
