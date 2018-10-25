from flask import Blueprint

bp = Blueprint("api_version1", __name__)

from store_app.api.version1 import errors
from store_app.api.version1.models import user_model
from store_app.api.version1.views.user_view import user_api
from store_app.api.version1.views.product_views import products_api