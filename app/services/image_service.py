import os

from flask import Flask, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.models.user import User


class ImageService:
    @classmethod
    def initialize(cls, app: Flask):
        """Initialize the ImageService class with the Flask app instance."""
        pass

    @classmethod
    def save_image(
        cls, uploaded_file: FileStorage, requesting_user: User, filename: str
    ) -> str:
        """Save the uploaded image file.

        Args:
            uploaded_file (FileStorage): The file object to be saved.
            requesting_user (User): The user who is requesting to upload the image.

        Returns:
            str: The file path where the image is saved.
        """
        # Save the uploaded file
        filename = secure_filename(filename)
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], str(requesting_user.id), filename
        )
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        uploaded_file.save(file_path)

        return file_path
