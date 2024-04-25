from flask import Flask
from app.config import Config
from app.core_services import init_core_services
from app.api.user import user_blueprint

def init_app(app: Flask)->Flask:
    init_core_services(app)
    return app



def create_app()->Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    init_app(app)
    app.register_blueprint(user_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
