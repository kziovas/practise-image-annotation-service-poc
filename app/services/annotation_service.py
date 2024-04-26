import random
from uuid import UUID

from app.enums import AnnotationStatus
from app.errors import ImageNotFound
from app.repos.annotation import AnnotationRepo
from app.repos.image import ImageRepo


class AnnotationService:
    MIN_MOCK_ANNOTATION_NUMBER: int = 2

    @classmethod
    def _create_random_annotation(cls) -> None:
        name = "Annotation" + str(random.randint(1, 100))
        AnnotationRepo.create(name)
        return None

    @classmethod
    def initialize(cls) -> None:
        try:
            all_annotations = AnnotationRepo.get_all()
            if len(all_annotations) < cls.MIN_MOCK_ANNOTATION_NUMBER:
                num_annotations_to_create = cls.MIN_MOCK_ANNOTATION_NUMBER - len(
                    all_annotations
                )
                for _ in range(num_annotations_to_create):
                    cls._create_random_annotation()

        except Exception as e:
            raise e

    @classmethod
    def simulate_annotation(cls, image_id: UUID) -> None:
        try:
            image = ImageRepo.get_by_id(image_id)
            if not image:
                raise ImageNotFound("Image not found")

            if image.annotation_status == AnnotationStatus.Queued:
                ImageRepo.update(
                    image_id, annotation_status=AnnotationStatus.Processing
                )
            elif image.annotation_status == AnnotationStatus.Processing:
                ImageRepo.update(image_id, annotation_status=AnnotationStatus.Success)
                all_annotations = AnnotationRepo.get_all()
                if (
                    all_annotations
                    and len(all_annotations) >= cls.MIN_MOCK_ANNOTATION_NUMBER
                ):
                    random_annotations = random.sample(
                        all_annotations, cls.MIN_MOCK_ANNOTATION_NUMBER
                    )
                    ImageRepo.update(image_id, annotations=random_annotations)

        except Exception as e:
            raise e
