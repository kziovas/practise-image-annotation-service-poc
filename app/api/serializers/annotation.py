from marshmallow import Schema, fields

from app.repos.image import ImageRepo


class AnnotationSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    image_ids = fields.List(fields.UUID, dump_only=True)

    def dump(self, obj, *, many=None, **kwargs):
        if many:
            for item in obj:
                if hasattr(item, "images") and not hasattr(item, "image_ids"):
                    item.image_ids = [image.id for image in item.images]
                    delattr(item, "images")
        else:
            if hasattr(obj, "images") and not hasattr(obj, "image_ids"):
                obj.image_ids = [image.id for image in obj.images]
                delattr(obj, "images")
        return super().dump(obj, many=many, **kwargs)
