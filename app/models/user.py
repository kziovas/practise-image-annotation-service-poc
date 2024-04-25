from app.core_services import db 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    images = db.relationship('Image', backref='user', lazy='dynamic')  
    def __repr__(self):
        return f'<User {self.username}>'
