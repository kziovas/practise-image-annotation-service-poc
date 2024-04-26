from typing import List, Optional
from uuid import UUID

from app.models.image_summary import ImageSummary
from app.services.core_services import db


class ImageSummaryRepo:
    model = ImageSummary

    @classmethod
    def get_all(cls) -> List[ImageSummary]:
        return cls.model.query.all()

    @classmethod
    def get_by_image_id(cls, image_id: UUID) -> Optional[ImageSummary]:
        return cls.model.query.filter_by(image_id=image_id).first()

    @classmethod
    def get_by_id(cls, summary_id: UUID) -> Optional[ImageSummary]:
        return cls.model.query.get(summary_id)

    @classmethod
    def create(
        cls,
        image_id: UUID,
        comment_summary: str,
        comment_count: int,
        sentiment_score: int,
    ) -> ImageSummary:
        new_summary = ImageSummary(
            image_id=image_id,
            comment_count=comment_count,
            comment_summary=comment_summary,
            sentiment_score=sentiment_score,
        )
        db.session.add(new_summary)
        db.session.commit()
        return new_summary

    @classmethod
    def update(
        cls,
        summary_id: UUID,
        comment_summary: str,
        comment_count: int,
        sentiment_score: int,
    ) -> Optional[ImageSummary]:
        summary = cls.model.query.get(summary_id)
        if summary:
            summary.comment_summary = comment_summary
            summary.sentiment_score = sentiment_score
            summary.comment_count = comment_count
            db.session.commit()
        return summary

    @classmethod
    def delete(cls, summary_id: UUID) -> bool:
        summary = cls.model.query.get(summary_id)
        if summary:
            db.session.delete(summary)
            db.session.commit()
            return True
        return False
