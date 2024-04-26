from sqlalchemy import UUID, Column, ForeignKey, Integer, Text

from app.core_services import db
from app.models.common import TimestampMixin


class Comment(TimestampMixin, db.Model):
    id = Column(UUID, primary_key=True)
    body = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    image_id = Column(Integer, ForeignKey("image.id"), nullable=False)

    def __repr__(self):
        return f"<Comment {self.id}>"
