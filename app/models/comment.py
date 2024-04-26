import uuid

from sqlalchemy import UUID, Column, ForeignKey, Text

from app.models.common import TimestampMixin
from app.services.core_services import db


class Comment(TimestampMixin, db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    body = Column(Text)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    image_id = Column(UUID(as_uuid=True), ForeignKey("image.id"), nullable=False)

    def __repr__(self):
        return f"<Comment {self.id}>"
