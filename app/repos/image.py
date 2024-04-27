from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_, or_
from werkzeug.utils import secure_filename

from app.models.image import Image
from app.models.image_summary import ImageSummary
from app.services.core_services import db


class ImageRepo:
    model = Image

    @classmethod
    def get_all(cls) -> List[Image]:
        return cls.model.query.all()

    @classmethod
    def get_all_allowed(cls, requesting_user_id: UUID) -> List[Image]:
        return cls.model.query.filter(
            or_(cls.model._is_public.is_(True), cls.model.user_id == requesting_user_id)
        ).all()

    @classmethod
    def get_by_id(cls, image_id: UUID, requesting_user_id: UUID) -> Optional[Image]:
        return cls.model.query.filter(
            and_(
                or_(
                    cls.model._is_public.is_(True),
                    cls.model.user_id == requesting_user_id,
                ),
                cls.model.id == image_id,
            )
        ).first()

    @classmethod
    def get_by_user_id(cls, owner_id: UUID, requesting_user_id: UUID) -> List[Image]:
        if owner_id == requesting_user_id:
            return cls.model.query.filter(cls.model.user_id == owner_id).all()
        else:
            return cls.model.query.filter(
                cls.model.is_public, cls.model.user_id == owner_id
            ).all()

    @classmethod
    def create(cls, user_id: UUID, filename: str, **kwargs) -> Image:
        filename = secure_filename(filename)
        new_image = Image(user_id=user_id, filename=filename, **kwargs)
        db.session.add(new_image)
        db.session.commit()
        return new_image

    @classmethod
    def update(cls, image_id: UUID, **kwargs) -> Optional[Image]:
        image = cls.model.query.get(image_id)
        if image:
            for key, value in kwargs.items():
                if key == "filename":
                    value = secure_filename(value)
                setattr(image, key, value)
            db.session.commit()

        return image

    @classmethod
    def delete(cls, image_id: UUID) -> bool:
        image = cls.model.query.get(image_id)
        if image:
            db.session.delete(image)
            db.session.commit()
            return True
        return False

    @classmethod
    def get_by_username(
        cls, username: str, requesting_user_id: UUID
    ) -> Optional[List[Image]]:
        from app.repos.user import UserRepo  # Importing here to avoid circular imports

        user = UserRepo.get_by_username(username)
        if user:
            if user.id == requesting_user_id:
                return cls.model.query.filter_by(user_id=user.id).all()
            else:
                return cls.model.query.filter(
                    cls.model.is_public, cls.model.user_id == user.id
                ).all()
        return None

    @classmethod
    def get_image_summary(cls, image_id: UUID) -> Optional[ImageSummary]:
        image = cls.get_by_id(image_id)
        if image:
            return image.summary.first()
        return None
