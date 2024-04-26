from typing import List, Optional
from uuid import UUID

from app.services.core_services import db
from app.models.comment import Comment


class CommentRepo:
    model = Comment

    @classmethod
    def get_all(cls) -> List[Comment]:
        return cls.model.query.all()

    @classmethod
    def get_by_id(cls, comment_id: UUID) -> Optional[Comment]:
        return cls.model.query.get(comment_id)

    @classmethod
    def get_by_user_id(cls, user_id: UUID) -> List[Comment]:
        return cls.model.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_by_image_id(cls, image_id: UUID) -> List[Comment]:
        return cls.model.query.filter_by(image_id=image_id).all()

    @classmethod
    def create(cls, body: str, user_id: UUID, image_id: UUID) -> Optional[Comment]:
        new_comment = cls.model(body=body, user_id=user_id, image_id=image_id)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment

    @classmethod
    def update(cls, comment_id: UUID, body: str) -> Optional[Comment]:
        comment = cls.get_by_id(comment_id)
        if comment:
            comment.body = body
            db.session.commit()
        return comment

    @classmethod
    def delete(cls, comment_id: UUID) -> bool:
        comment = cls.get_by_id(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return True
        return False
