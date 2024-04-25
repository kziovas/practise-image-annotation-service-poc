from flask import Flask
from app.config import Config
from app.core_services import init_app

def create_app()->Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
