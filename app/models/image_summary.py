from sqlalchemy import UUID, Column, ForeignKey, Integer, Text

from app.core_services import db
from app.models.common import TimestampMixin


class ImageSummary(TimestampMixin, db.Model):
    id = Column(UUID, primary_key=True)
    image_id = Column(Integer, ForeignKey("image.id"), nullable=False)
    comment_summary = Column(Text)
    sentiments_score = Column(Integer)

    def __repr__(self) -> str:
        return f"<Image Summary {self.id}>"
