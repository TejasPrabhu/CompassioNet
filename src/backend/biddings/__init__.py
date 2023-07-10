from flask import Blueprint

biddings = Blueprint("biddings", __name__, url_prefix="/biddings")

# these imports are placed here to avoid circular dependencies
from . import routes
