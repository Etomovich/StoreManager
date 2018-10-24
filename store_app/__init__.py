from flask import Flask
from Instance.config import Config
##from store_app.api.version1 import the_api


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #the_api.init_app(app)

    from store_app.api.version1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")


    return app