import os

from flask import Flask, request, url_for, redirect, session
from flask_login import LoginManager

from flaskr.app.routes.users import users_pages
from flaskr.app.routes.forum import forum_pages
from flaskr.app.persistence.users import get_user_for_session, login_user
from flaskr.app.models.users import User

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
    app.register_blueprint(forum_pages)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        match = get_user_for_session(user_id)
        if match == -1 or match == -2:
            return None

        user = User()
        user.id = user_id
        user.correo = match[1]
        user.contrasena = match[2]
        user.estado = match[3]
        return user

    @login_manager.request_loader
    def load_user(request):
        res = login_user(request.form)
        if res == -1 or res == -2:
            return None

        match = get_user_for_session(res[0])
        if match == -1 or match == -2:
            return None
        
        user = User()
        user.id = res[0]
        user.correo = match[1]
        user.contrasena = match[2]
        user.estado = match[3]
        return user

    @login_manager.unauthorized_handler
    def login_needed():
        return redirect(url_for('index.login', next=request.full_path))

    @login_manager.needs_refresh_handler
    def refresh():
        return redirect(url_for('index.login', next=request.full_path))

    @app.before_request
    def make_session_not_permanent():
        session.permanent = False

    return app