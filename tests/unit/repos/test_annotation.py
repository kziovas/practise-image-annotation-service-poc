import uuid

from app.repos.annotation import AnnotationRepo


class TestAnnotationRepo:
    def test_get_all_annotations(self, new_annotation):
        annotations = AnnotationRepo.get_all()
        assert new_annotation in annotations

    def test_get_annotation_by_id(self, new_annotation):
        retrieved_annotation = AnnotationRepo.get_by_id(new_annotation.id)
        assert retrieved_annotation.id == new_annotation.id

    def test_create_annotation(self):
        annotation_name = f"New Annotation {uuid.uuid4().hex[:6]}"  # Randomized name
        new_annotation = AnnotationRepo.create(name=annotation_name)
        assert new_annotation is not None
        assert new_annotation.name == annotation_name

        # Clean up after the test
        AnnotationRepo.delete(new_annotation.id)

    def test_update_annotation(self, new_annotation):
        new_name = f"Updated Annotation {uuid.uuid4().hex[:6]}"  # Randomized name
        updated_annotation = AnnotationRepo.update(new_annotation.id, name=new_name)
        assert updated_annotation is not None
        assert updated_annotation.name == new_name

    def test_delete_annotation(self, new_annotation):
        annotation_id = new_annotation.id
        assert AnnotationRepo.delete(annotation_id) is True
        assert AnnotationRepo.get_by_id(annotation_id) is None
