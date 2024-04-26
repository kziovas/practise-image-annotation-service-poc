import uuid

from sqlalchemy import UUID, Column, ForeignKey, Integer, Text

from app.models.common import TimestampMixin
from app.services.core_services import db


class ImageSummary(TimestampMixin, db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id = Column(UUID(as_uuid=True), ForeignKey("image.id"), nullable=False)
    comment_count = Column(Integer, default=0)
    comment_summary = Column(Text, default="")
    sentiment_score = Column(Integer, default=50)

    def __repr__(self) -> str:
        return f"<Image Summary {self.id}>"
