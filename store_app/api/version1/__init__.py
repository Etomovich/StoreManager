from flask import Blueprint

bp = Blueprint("api_version1", __name__)

from store_app.api.version1.api_routes import the_api