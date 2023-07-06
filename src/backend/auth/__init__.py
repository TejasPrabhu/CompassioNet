from flask import Blueprint

auth = Blueprint("auth", __name__)

# these imports are placed here to avoid circular dependencies
from . import routes

# from .routes import *
