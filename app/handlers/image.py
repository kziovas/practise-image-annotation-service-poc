from sqlalchemy import event

from app.models.image import Image
from app.services.annotation_service import AnnotationService


@event.listens_for(Image, "load")
def trigger_simulate_annotation(target, context):
    AnnotationService.simulate_annotation(target.id)
