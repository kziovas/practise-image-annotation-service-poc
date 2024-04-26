from typing import List, Optional
from uuid import UUID

from app.core_services import db
from app.models.user import User


class UserRepo:
    model = User

    @classmethod
    def get_all(cls) -> List[User]:
        return cls.model.query.all()

    @classmethod
    def get_by_id(cls, user_id: UUID) -> Optional[User]:
        return cls.model.query.get(user_id)

    @classmethod
    def get_by_email(cls, email: str) -> Optional[User]:
        return cls.model.query.filter_by(email=email).first()

    @classmethod
    def get_by_username(cls, username: str) -> Optional[User]:
        return cls.model.query.filter_by(username=username).first()

    @classmethod
    def create(cls, username: str, email: str, password_hash: str) -> Optional[User]:
        new_user = cls.model(
            username=username, email=email, password_hash=password_hash
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def update(cls, user_id: UUID, **kwargs) -> Optional[User]:
        user = cls.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.session.commit()
        return user

    @classmethod
    def delete(cls, user_id: UUID) -> bool:
        user = cls.get_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
