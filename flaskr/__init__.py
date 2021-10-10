import os

from flask import Flask
from flask_login import LoginManager

from flaskr.app.routes.routes import users_pages
from flaskr.app.persistence.users import get_user_for_session
from flaskr.app.models.user_model import User

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

    login_manager = LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        user = User()
        match = get_user_for_session(user_id)
        user.id = user_id
        user.username = match[1]
        user.contrasena = match[2]
        user.estado = match[3]
        return user

    return app