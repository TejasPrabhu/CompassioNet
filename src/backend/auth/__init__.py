from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/auth")

# these imports are placed here to avoid circular dependencies
from . import routes
