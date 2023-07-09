from flask import Blueprint

user = Blueprint("user", __name__, url_prefix="/user")

# these imports are placed here to avoid circular dependencies
from . import routes
