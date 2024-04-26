from sqlalchemy import UUID, Column, String

from app.core_services import db
from app.models.common import TimestampMixin


class User(TimestampMixin, db.Model):
    id = Column(UUID, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(db.String(128))
    comments = db.relationship("Comment", backref="user", lazy="dynamic")
    images = db.relationship("Image", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"
