from typing import List
from uuid import UUID

from app.services.annotation_service import AnnotationService


def trigger_simulate_image_annotation(image_ids: List[UUID]):
    for image_id in image_ids:
        AnnotationService.simulate_annotation(image_id)
