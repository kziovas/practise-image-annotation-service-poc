import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://admin:password@localhost:5432/image_annotation_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
