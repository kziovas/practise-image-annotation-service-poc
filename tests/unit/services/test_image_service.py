import os

from werkzeug.datastructures import FileStorage

from app.models.user import User
from app.services.image_service import ImageService


class TestImageService:
    def test_save_image(self, app, new_user):
        uploaded_file = FileStorage(
            stream=open("tests/data/mini_car.jpg", "rb"),
            filename="test_image.jpg",
            content_type="image/jpeg",
        )

        file_path = ImageService.save_image(uploaded_file, new_user, "test_image.jpg")
        assert os.path.exists(file_path)

        os.remove(file_path)
        current_dir = os.path.dirname(file_path)
        while True:
            os.rmdir(current_dir)
            current_dir = os.path.dirname(current_dir)
            if os.path.split(current_dir)[-1] == "uploads":
                break
