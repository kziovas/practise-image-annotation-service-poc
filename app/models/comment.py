from sqlalchemy import UUID, Column, ForeignKey, Integer, Text

from app.services.core_services import db
from app.models.common import TimestampMixin


class Comment(TimestampMixin, db.Model):
    id = Column(UUID, primary_key=True)
    body = Column(Text)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    image_id = Column(UUID, ForeignKey("image.id"), nullable=False)

    def __repr__(self):
        return f"<Comment {self.id}>"
