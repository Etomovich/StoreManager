from flask import Flask
from Instance.config import Config
from store_app.api.version1 import user_api,products_api


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    user_api.init_app(app)

    products_api.init_app(app)

    from store_app.api.version1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")


    return app