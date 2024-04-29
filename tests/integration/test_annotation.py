import pytest

from app.models.annotation import Annotation
from app.models.user import User
from app.repos.annotation import AnnotationRepo
from app.repos.user import UserRepo
from app.utils.auth import AuthUtils


class TestAnnotationEndpoints:
    @pytest.fixture(scope="class")
    def authenticated_client(self, app) -> tuple:
        with app.test_client() as client:
            token = AuthUtils.authenticate(username="admin", password="password")
            yield client, token

    @pytest.fixture(scope="class")
    def test_annotation(self) -> Annotation:
        annotation: Annotation = AnnotationRepo.create(name="Test Annotation Endpoint")
        yield annotation
        AnnotationRepo.delete(annotation.id)

    def test_get_annotation(
        self, authenticated_client: tuple, test_annotation: Annotation
    ) -> None:
        client, token = authenticated_client
        response = client.get(
            f"/annotation/{test_annotation.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json["id"] == str(test_annotation.id)

    def test_create_annotation(
        self,
        authenticated_client: tuple,
    ) -> None:
        client, token = authenticated_client
        response = client.post(
            "/annotation",
            json={"name": "Test Annotation Endpoint 2"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        assert response.json["name"] == "Test Annotation Endpoint 2"

    def test_delete_annotation(
        self, authenticated_client: tuple, test_annotation: Annotation
    ) -> None:
        client, token = authenticated_client
        response = client.delete(
            f"/annotation/{test_annotation.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 204
