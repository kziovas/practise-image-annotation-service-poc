import pytest

from app.repos.image import ImageRepo
from app.services.core_services import db


class TestImageRepo:
    def test_create_image(self, new_image):
        assert new_image.id is not None
        assert new_image.user_id is not None
        assert new_image.filename == "test_image.jpg"

    def test_get_image_by_id(self, new_image):
        retrieved_image = ImageRepo.get_by_id(new_image.id, new_image.user_id)
        assert retrieved_image.id == new_image.id
        assert retrieved_image.user_id == new_image.user_id
        assert retrieved_image.filename == new_image.filename

    def test_update_image(self, new_image):
        updated_filename = "updated_image.jpg"
        ImageRepo.update(new_image.id, filename=updated_filename)
        updated_image = ImageRepo.get_by_id(new_image.id, new_image.user_id)
        assert updated_image.filename == updated_filename

    def test_delete_image(self, new_image):
        ImageRepo.delete(new_image.id)
        deleted_image = ImageRepo.get_by_id(new_image.id, new_image.user_id)
        assert deleted_image is None
