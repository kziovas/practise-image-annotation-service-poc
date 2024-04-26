from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin(object):
    __tablename__ = "timestamp_mixin"
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime)
