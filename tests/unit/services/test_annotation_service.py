from unittest.mock import MagicMock, patch
from uuid import uuid4

from app.enums import AnnotationStatus
from app.errors import ImageNotFound
from app.services.annotation_service import AnnotationService


class TestAnnotationService:
    @patch("app.repos.image.ImageRepo.get_by_id")
    @patch("app.repos.annotation.AnnotationRepo.get_all")
    @patch("app.repos.image.ImageRepo.update")
    def test_simulate_annotation_queued(
        self,
        mock_update,
        mock_get_all_annotations,
        mock_get_by_id,
        new_user,
        new_annotation,
        new_image,
    ):
        mock_user_id = new_user.id

        mock_image = MagicMock()
        mock_image.annotation_status = AnnotationStatus.Queued.value
        mock_get_by_id.return_value = mock_image

        mock_get_all_annotations.return_value = [new_annotation]

        AnnotationService.simulate_annotation(new_image.id, mock_user_id)

        mock_update.assert_called_once_with(
            image_id=new_image.id, annotation_status=AnnotationStatus.Processing
        )
