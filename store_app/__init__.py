from flask import Flask

from Instance.config import configuration

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configuration[config_name])

    from store_app.api.version1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")

    return app