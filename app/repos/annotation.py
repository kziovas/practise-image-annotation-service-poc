from typing import List, Optional

from app.core_services import db
from app.models import Annotation


class AnnotationRepo:
    model = Annotation

    @classmethod
    def get_all(cls) -> List[Annotation]:
        return cls.model.query.all()

    @classmethod
    def get_by_id(cls, annotation_id: int) -> Optional[Annotation]:
        return cls.model.query.get(annotation_id)

    @classmethod
    def create(cls, name: str) -> Annotation:
        new_annotation = Annotation(name=name)
        db.session.add(new_annotation)
        db.session.commit()
        return new_annotation

    @classmethod
    def update(cls, annotation_id: int, name: str) -> Optional[Annotation]:
        annotation = cls.model.query.get(annotation_id)
        if annotation:
            annotation.name = name
            db.session.commit()
        return annotation

    @classmethod
    def delete(cls, annotation_id: int) -> bool:
        annotation = cls.model.query.get(annotation_id)
        if annotation:
            db.session.delete(annotation)
            db.session.commit()
            return True
        return False
