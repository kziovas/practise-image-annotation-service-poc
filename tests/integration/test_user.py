import json
import uuid
from typing import Any

import pytest
from flask.testing import FlaskClient

from app.models.user import User
from app.repos.user import UserRepo


class TestUserEndpoints:

    def test_login(self, client: FlaskClient) -> None:
        user = UserRepo.create(
            username="test_user_login",
            email="test_user_login@example.com",
            password="password",
        )

        response = client.post(
            "/user/login",
            json={"username": "test_user_login", "password": "password"},
            content_type="application/json",
        )
        assert response.status_code == 200
        assert "access_token" in json.loads(response.data)

        response = client.post(
            "/user/login",
            json={"username": "invalid_user", "password": "invalid_password"},
            content_type="application/json",
        )
        assert response.status_code == 400

        UserRepo.delete(user.id)

    def test_get_users(self, client: FlaskClient) -> None:
        response = client.get("/user/users")
        assert response.status_code == 401

    def test_get_user_by_id(self, client: FlaskClient) -> None:
        user = UserRepo.create(
            username="test_user_by_id",
            email="_user_by_id@example.com",
            password="password",
        )
        user_id = user.id

        response = client.get(f"/user/{user_id}")
        assert response.status_code == 401
        UserRepo.delete(user.id)

    def test_get_user(self, client: FlaskClient) -> None:
        response = client.get("/user")
        assert response.status_code == 401

    def test_get_user_by_email(self, client: FlaskClient) -> None:
        response = client.get("/user/email/test@example.com")
        assert response.status_code == 401

    def test_create_user(self, client: FlaskClient) -> None:
        response = client.post(
            "/user",
            json={
                "username": "new_user",
                "email": "new@example.com",
                "password": "password",
            },
            content_type="application/json",
        )
        assert response.status_code == 201

    def test_update_user(self, client: FlaskClient) -> None:
        response = client.put(
            "/user/123e4567-e89b-12d3-a456-426614174000",
            json={"username": "updated_user"},
            content_type="application/json",
        )
        assert response.status_code == 401

    def test_delete_user(self, client: FlaskClient) -> None:
        response = client.delete("/user/123e4567-e89b-12d3-a456-426614174000")
        assert response.status_code == 401
