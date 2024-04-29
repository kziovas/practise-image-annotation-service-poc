import pytest
from flask import json
from werkzeug.test import Client as FlaskClient

from app.models.image_summary import ImageSummary
from app.models.user import User
from app.repos.image import ImageRepo
from app.repos.image_summary import ImageSummaryRepo
from app.repos.user import UserRepo
from app.utils.auth import AuthUtils


class TestImageEndpoints:
    @pytest.fixture(scope="class")
    def test_user(self) -> User:
        user: User = UserRepo.create(
            username="test_user_image",
            email="test_user_image@example.com",
            password="password",
        )
        yield user
        UserRepo.delete(user.id)

    @pytest.fixture(scope="class")
    def authenticated_client(self, app, test_user: User):
        with app.test_client() as client:
            token = AuthUtils.authenticate(
                username=test_user.username, password="password"
            )
            yield client, token
            # Teardown
            UserRepo.delete(test_user.id)

    @pytest.fixture(scope="class")
    def image_summary(self, test_user: User) -> ImageSummary:
        image = ImageRepo.create(user_id=test_user.id, filename="test_image.jpg")
        summary = ImageSummaryRepo.create(
            image_id=image.id,
            comment_count=5,
            comment_summary="Great image!",
            average_comment_length=15,
            users_commented_count=3,
            sentiment_score=80,
        )
        yield summary
        ImageSummaryRepo.delete(summary.id)
        ImageRepo.delete(image.id)

    @pytest.mark.usefixtures("authenticated_client")
    def test_get_image(self, authenticated_client, test_user: User) -> None:
        client, token = authenticated_client
        image = ImageRepo.create(user_id=test_user.id, filename="test_image.jpg")

        response = client.get(
            f"/image/{image.id}", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert "filename" in json.loads(response.data)
        assert json.loads(response.data)["filename"] == "test_image.jpg"

        ImageRepo.delete(image.id)

    @pytest.mark.usefixtures("authenticated_client")
    def test_get_image_summary(
        self, authenticated_client, test_user: User, image_summary: ImageSummary
    ) -> None:
        client, token = authenticated_client
        image_id = image_summary.image_id

        response = client.get(
            f"/image/{image_id}/summary", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert json.loads(response.data)["comment_count"] == 5
        assert json.loads(response.data)["sentiment_score"] == 80

    @pytest.mark.usefixtures("authenticated_client")
    def test_create_image(self, authenticated_client, test_user: User) -> None:
        client, token = authenticated_client

        response = client.post(
            "/image",
            json={
                "filename": "test_image.jpg",
                "user_id": str(test_user.id),
                "annotation_ids": [],
                "is_public": True,
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        assert "filename" in json.loads(response.data)
        assert json.loads(response.data)["filename"] is not None

        ImageRepo.delete(json.loads(response.data)["id"])

    @pytest.mark.usefixtures("authenticated_client")
    def test_delete_image(self, authenticated_client, test_user: User) -> None:
        client, token = authenticated_client

        image = ImageRepo.create(user_id=test_user.id, filename="test_image.jpg")

        response = client.delete(
            f"/image/{image.id}", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 204

        ImageRepo.delete(image.id)
