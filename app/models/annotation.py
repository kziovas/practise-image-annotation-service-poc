import uuid

from sqlalchemy import UUID, Column, String

from app.models.common import TimestampMixin
from app.models.image import image_annotation_association
from app.services.core_services import db


class Annotation(TimestampMixin, db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True)
    images = db.relationship(
        "Image", secondary=image_annotation_association, back_populates="annotations"
    )

    def __repr__(self):
        return f"<Annotation {self.name}>"
