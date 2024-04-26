import uuid

from sqlalchemy import UUID, Column, String

from app.models.common import TimestampMixin
from app.services.core_services import db


class User(TimestampMixin, db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(db.String(128))
    comments = db.relationship(
        "Comment", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    images = db.relationship(
        "Image", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"
