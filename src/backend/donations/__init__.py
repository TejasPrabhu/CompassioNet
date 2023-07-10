from flask import Blueprint

donations = Blueprint("donations", __name__, url_prefix="/donations")

# these imports are placed here to avoid circular dependencies
from . import routes
