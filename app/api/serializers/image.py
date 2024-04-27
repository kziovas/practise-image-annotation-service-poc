from marshmallow import Schema, fields

from app.api.serializers.comment import CommentSchema
from app.repos.annotation import AnnotationRepo


class ImageSchema(Schema):
    id = fields.UUID(dump_only=True)
    filename = fields.Str(required=True)
    user_id = fields.UUID(required=True, allow_none=False)
    comments = fields.Nested(CommentSchema, many=True, dump_only=True)
    annotation_ids = fields.List(fields.UUID, required=False)


class ViewImageSchema(ImageSchema):
    annotation_status = fields.Str(required=True, dump_only=True)

    def dump(self, obj, *, many=None, **kwargs):
        if many:
            for item in obj:
                if hasattr(item, "annotations") and not hasattr(item, "annotation_ids"):
                    item.annotation_ids = [
                        annotation.id for annotation in item.annotations
                    ]
                    delattr(item, "annotations")
        else:
            if hasattr(obj, "annotations") and not hasattr(obj, "annotation_ids"):
                obj.annotation_ids = [annotation.id for annotation in obj.annotations]
                delattr(obj, "annotations")
        return super().dump(obj, many=many, **kwargs)

    def load(self, data, *, many=None, **kwargs):
        if many:
            for item in data:
                if "annotation_ids" in item:
                    annotation_ids = item.pop("annotation_ids")
                    item["annotations"] = [
                        AnnotationRepo.get_by_id(annotation_id)
                        for annotation_id in annotation_ids
                    ]
        else:
            if "annotation_ids" in data:
                annotation_ids = data.pop("annotation_ids")
                data["annotations"] = [
                    AnnotationRepo.get_by_id(annotation_id)
                    for annotation_id in annotation_ids
                ]
        return super().load(data, many=many, **kwargs)
