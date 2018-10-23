from flask import Flask
from Instance.config import TestingConfig

def create_app(config_class=TestingConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    return app
