from flask import Flask

from app.api.blueprints.annotation import annotation_blueprint
from app.api.blueprints.comment import comment_blueprint
from app.api.blueprints.image import image_blueprint
from app.api.blueprints.user import user_blueprint
from app.config import Config
from app.core_services import init_core_services


def init_app(app: Flask) -> Flask:
    app.config.from_object(Config)
    init_core_services(app)
    return app


def register_blueprints(app: Flask) -> Flask:
    blueprints = [
        user_blueprint,
        annotation_blueprint,
        comment_blueprint,
        image_blueprint,
    ]
    for bp in blueprints:
        app.register_blueprint(bp)

    return app


def create_app() -> Flask:
    app = Flask(__name__)

    init_app(app)
    register_blueprints(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
