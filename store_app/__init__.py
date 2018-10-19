from flask import Flask

from Instance.config import configuration

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configuration[config_name])
    configuration[config_name].init_app(app)

    return app