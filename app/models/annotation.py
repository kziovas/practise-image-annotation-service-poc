from sqlalchemy import UUID, Column, String

from app.core_services import db
from app.models.common import TimestampMixin
from app.models.image import image_annotation_association


class Annotation(TimestampMixin, db.Model):
    id = Column(UUID, primary_key=True)
    name = Column(String(50), unique=True)
    images = db.relationship(
        "Image", secondary=image_annotation_association, back_populates="annotations"
    )

    def __repr__(self):
        return f"<Annotation {self.name}>"
