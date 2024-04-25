from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Create core services as singletons
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def init_app(app: Flask):
    # Initialize database with the app
    db.init_app(app)

    # Initialize Flask-Migrate with the app and db
    migrate.init_app(app, db)

    # Initialize Flask-JWT-Extended with the app
    jwt.init_app(app)

    # Create the database tables if they dont exist
    with app.app_context():
        db.create_all()