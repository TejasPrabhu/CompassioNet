import os
import sys
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


def create_app(config):
    # Get the path to the root directory of the project
    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
    PARENT_PATH = os.path.dirname(ROOT_PATH)

    # print(os.environ.get("DB_HOST"))

    # Add the root directory to the Python path
    sys.path.append(PARENT_PATH)

    app = Flask(__name__)
    # TODO: retrive a list of allowed hosts from config file
    CORS(app)
    app.config.from_object(config)
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/api/"
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/api/refresh"
    app.config["JWT_COOKIE_SECURE"] = (
        True if os.environ.get("FLASK_ENV") == "production" else False
    )
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    jwt = JWTManager(app)

    # then, you import and register your Blueprints from each module
    from backend.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from backend.user import user as user_blueprint

    app.register_blueprint(user_blueprint)

    # print(app.blueprints.keys)

    # from .products import products as products_blueprint

    # app.register_blueprint(products_blueprint)

    # from .donations import donations as donations_blueprint

    # app.register_blueprint(donations_blueprint)

    return app
