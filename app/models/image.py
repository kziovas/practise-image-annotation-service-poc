from app.core_services import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('images', lazy='dynamic'))
    comments = db.relationship('Comment', backref='image', lazy='dynamic')
    annotations = db.relationship('Annotation', secondary='image_annotation_association', backref=db.backref('images', lazy='dynamic'))

    def __repr__(self):
        return f'<Image {self.filename}>'


