import pytest

from app.models.comment import Comment
from app.models.user import User
from app.repos.comment import CommentRepo
from app.repos.image import ImageRepo
from app.repos.user import UserRepo
from app.utils.auth import AuthUtils


class TestCommentEndpoints:
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
    def test_comment(self, test_user: User) -> Comment:
        comment_body = "This is a test comment."
        image = ImageRepo.create(user_id=test_user.id, filename="test_image.jpg")
        comment = CommentRepo.create(
            body=comment_body, user_id=test_user.id, image_id=image.id
        )
        yield comment
        CommentRepo.delete(comment.id)
        ImageRepo.delete(image.id)

    def test_get_comment(self, authenticated_client, test_comment) -> None:
        client, token = authenticated_client
        response = client.get(
            f"/comment/{test_comment.id}", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json["id"] == str(test_comment.id)

    def test_create_comment(
        self, authenticated_client, test_user, test_comment
    ) -> None:
        client, token = authenticated_client
        response = client.post(
            "/comment",
            json={
                "user_id": str(test_user.id),
                "body": "Test comment",
                "image_id": str(test_comment.image_id),
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        assert response.json["body"] == "Test comment"

    def test_delete_comment(self, authenticated_client, test_comment) -> None:
        client, token = authenticated_client
        response = client.delete(
            f"/comment/{test_comment.id}", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 204
