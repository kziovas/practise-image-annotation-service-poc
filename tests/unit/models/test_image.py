from uuid import uuid4

import pytest

from app.enums import AnnotationStatus
from app.models.image import Image


class TestImageModel:
    def test_image_model_creation(self, new_image):
        assert new_image.user_id is not None
        assert new_image.filename == "test_image.jpg"
        assert new_image.annotation_status == AnnotationStatus.Queued.value

    def test_image_model_filename_update(self, new_image):
        new_filename = "updated_image.jpg"
        new_image.filename = new_filename
        assert new_image.filename == new_filename

    def test_image_model_annotation_status_update(self, new_image):
        new_status = AnnotationStatus.Processing
        new_image.annotation_status = new_status
        assert new_image.annotation_status == new_status.value
