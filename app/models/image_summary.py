from app.core_services import db
from app.models.common import TimestampMixin
from sqlalchemy import Column, UUID, Integer, ForeignKey,Text

class ImageSummary(TimestampMixin,db.Model):
    id = Column(UUID, primary_key=True)
    image_id = Column(Integer, ForeignKey("image.id"), nullable=False)
    comment_summary = Column(Text)
    comment_sentiments_score = Column(Integer)
    def __repr__(self) -> str:
        return f"<Image Summary {}>"