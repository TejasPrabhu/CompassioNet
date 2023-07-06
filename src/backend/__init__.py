import os
from flask import Flask
from flask_cors import CORS


def create_app(config):
    app = Flask(__name__)
    # TODO: retrive a list of allowed hosts from config file
    CORS(app)
    app.config.from_object(config)

    # then, you import and register your Blueprints from each module
    from backend.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # print(app.blueprints.keys)

    # from .products import products as products_blueprint

    # app.register_blueprint(products_blueprint)

    # from .donations import donations as donations_blueprint

    # app.register_blueprint(donations_blueprint)

    return app
