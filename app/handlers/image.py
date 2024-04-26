from sqlalchemy import event
from sqlalchemy.orm import Session

from app.models.image import Image
from app.services.annotation_service import AnnotationService


@event.listens_for(Image, "load")
@event.listens_for(Image, "refresh")
@event.listens_for(Image, "persistent_to_detached")
def trigger_simulate_annotation(target: Image, context: Session):
    breakpoint()
    AnnotationService.simulate_annotation(target.id)
