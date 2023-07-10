from flask import Blueprint

products = Blueprint("products", __name__, url_prefix="/products")

# these imports are placed here to avoid circular dependencies
from . import routes
