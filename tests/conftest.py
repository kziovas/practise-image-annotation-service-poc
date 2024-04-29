# tests/conftest.py

import pytest

from annotations_app import create_app
from app.models.user import User
from app.services.core_services import db


@pytest.fixture(scope="module")
def app():
    """Create and configure a new Flask application for testing."""
    app = create_app()
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture(scope="module")
def new_user(app):
    """Create a new user and add it to the test database."""
    with app.app_context():
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
    """Provide data for creating a new user."""
    return {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password",
    }
