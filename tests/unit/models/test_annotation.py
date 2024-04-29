from app.models.annotation import Annotation


class TestAnnotationModel:
    def test_annotation_model_creation(self, new_annotation):
        assert new_annotation.id is not None
        assert new_annotation.name == "Test Annotation"

    def test_annotation_model_update_name(self, new_annotation):
        new_name = "Updated Annotation"
        new_annotation.name = new_name
        assert new_annotation.name == new_name
