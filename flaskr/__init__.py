import os
from flask import Flask
from flaskr.app.routes.routes import users_pages

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    path = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(path, "../config/data"))
    file = open(path, "r")
    app.config.from_mapping(
        SECRET_KEY=file.read()
    )
    file.close()

    app.register_blueprint(users_pages)

    return app