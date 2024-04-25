from app.core_services import db

image_annotation_association = db.Table(
    'image_annotation_association',
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'), primary_key=True),
    db.Column('annotation_id', db.Integer, db.ForeignKey('annotation.id'), primary_key=True)
)
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='image', lazy='dynamic')
    annotations = db.relationship('Annotation', secondary=image_annotation_association, back_populates='images')

    def __repr__(self):
        return f'<Image {self.filename}>'


