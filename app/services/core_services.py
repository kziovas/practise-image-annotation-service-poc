from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Create core services as singletons
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
swagger = Swagger()


def init_core_services(app: Flask):
    # Initialize database with the app
    db.init_app(app)

    # Initialize Flask-Migrate with the app and db
    migrate.init_app(app, db)

    # Initialize Flask-JWT-Extended with the app
    jwt.init_app(app)

    # Initialize Swagger
    init_swagger(swagger, app)

    # Create the database tables if they dont exist
    with app.app_context():
        db.create_all()


def init_swagger(swagger: Swagger, app: Flask) -> Swagger:
    from app.api.serializers.annotation import AnnotationSchema
    from app.api.serializers.comment import CommentSchema
    from app.api.serializers.image import ImageSchema, ViewImageSchema
    from app.api.serializers.image_summary import ImageSummarySchema
    from app.api.serializers.user import UserLoginSchema, UserSchema

    spec = APISpec(
        title="Image Annotation",
        version="1.0.0",
        openapi_version="3.0",
        plugins=[
            FlaskPlugin(),
            MarshmallowPlugin(),
        ],
    )
    spec.components.schema("AnnotationSchema", schema=AnnotationSchema)
    spec.components.schema("CommentSchema", schema=CommentSchema)
    spec.components.schema("ImageSchema", schema=ImageSchema)
    spec.components.schema("ViewImageSchema", schema=ViewImageSchema)
    spec.components.schema("UserSchema", schema=UserSchema)
    spec.components.schema("UserLoginSchema", schema=UserLoginSchema)
    spec.components.schema("ImageSummarySchema", schema=ImageSummarySchema)
    template = spec.to_flasgger(
        app,
    )
    swagger.init_app(app)
    swagger.template = template
    return swagger
