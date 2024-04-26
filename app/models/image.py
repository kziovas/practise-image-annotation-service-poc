import os

from sqlalchemy import UUID, Column, Enum, ForeignKey, Integer, String, UniqueConstraint

from app.core_services import db
from app.enums import AnnotationStatus
from app.models.common import TimestampMixin

image_annotation_association = db.Table(
    "image_annotation_association",
    Column("image_id", Integer, ForeignKey("image.id"), primary_key=True),
    Column("annotation_id", Integer, ForeignKey("annotation.id"), primary_key=True),
)


class Image(TimestampMixin, db.Model):
    id = Column(UUID, primary_key=True)
    _filename = Column("filename", String(128), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    _annotation_status = Column(Enum(AnnotationStatus), default=AnnotationStatus.Queued)
    comments = db.relationship("Comment", backref="image", lazy="dynamic")
    summary = db.relationship("ImageSummary", backref="image", lazy="dynamic")
    annotations = db.relationship(
        "Annotation", secondary=image_annotation_association, back_populates="images"
    )

    __table_args__ = (
        UniqueConstraint("user_id", "filename", name="unique_user_filename"),
    )

    def __repr__(self):
        return f"<Image {self._filename}>"

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        existing_filenames = [
            image._filename
            for image in Image.query.filter_by(user_id=self.user_id).all()
        ]
        if value not in existing_filenames:
            self._filename = value
        else:
            # Extract file name and extension
            filename, extension = os.path.splitext(value)
            counter = 1
            new_filename = f"{filename}_{counter}{extension}"
            while new_filename in existing_filenames:
                counter += 1
                new_filename = f"{filename}_{counter}{extension}"
            self._filename = new_filename

    @property
    def annotation_status(self):
        return self._annotation_status.value

    @annotation_status.setter
    def annotation_status(self, status):
        if status not in AnnotationStatus:
            raise ValueError("Invalid annotation status")
        self._annotation_status = status

    @property
    def image_path(self):
        return f"uploads/{self.user_id}/{self._filename}"
