from app.core_services import db

class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    images = db.relationship('Image', secondary='image_annotation_association', backref='annotations')

    def __repr__(self):
        return f'<Annotation {self.name}>'
