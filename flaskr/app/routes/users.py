import base64

from flask import Blueprint, request, redirect, url_for, render_template, session
import flask_login

import flaskr.app.persistence.users as user_db
import flaskr.app.persistence.forum as forum_db
from flaskr.app.models.users import User

users_pages = Blueprint('index', __name__)
@users_pages.route('/')
def index():
    return render_template("index.html")

@users_pages.route('/profile', methods=['GET'])
@flask_login.fresh_login_required
def profile():
    key = flask_login.current_user.get_id()
    res = user_db.get_user_data(key)

    if res == -1: # Error
        return redirect(url_for('.index'))

    elif res[8] == 1:
        return render_template("profile.html", user=res)

    return redirect(url_for('.index')) # Deleted user

@users_pages.route('/profile/saved/forums', methods=['GET'])
@flask_login.fresh_login_required
def read_saved_forums():
    key = flask_login.current_user.get_id()
    if key != None:
        
        res = forum_db.get_saved_forums(key)
        if res == -1: # Error
            return redirect(url_for('.index'))

        forums_list = [list(forum) for forum in res]
        for i in range(len(forums_list)):
            forums_list[i][0] = base64.urlsafe_b64encode(forums_list[i][0]).rstrip(b"=").decode()

        return render_template("saved_forums.html", forums=forums_list)

    return redirect(url_for('.index')) # Not logged

@users_pages.route('/register', methods=['GET', 'POST'])
def register():
    if flask_login.current_user.get_id() != None:
        return redirect(url_for('.index')) # Logged

    elif request.method == 'POST': # POST
        form = {}

        try:
            apellidos = request.form["apellidos"].split()
            form["apellido1"] = apellidos[0]
            form["apellido2"] = apellidos[1]
        except Exception as e:
            print(e)
            return redirect(url_for('.register')) # No apellidos

        if request.form["contrasena"] != request.form["contrasena_v"]:
            return redirect(url_for('.register')) # Diferentes contraseñas
        
        form["idRol"] = 1 if request.form["rol"] == "Jóven" else 4
        form["correo"] = request.form["correo"]
        form["nombre"] = request.form["nombre"]
        form["fecha"] = request.form["fecha"]
        form["genero"] = request.form["genero"]
        form["nacionalidad"] = request.form["nacionalidad"]
        form["residencia"] = request.form["residencia"]
        form["contrasena"] = request.form["contrasena"]

        res = user_db.create_user(form)
        if res == 0:
            return redirect(url_for('.index')) # Worked

        return redirect(url_for('.register')) # Error DB
    return render_template("registrarme.html") # GET

def redirect_dest():
    return redirect(request.args.get("next"))

@users_pages.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = user_db.login_user(request.form)
        if res != -1 and res != -2:
            user = User()
            match = user_db.get_user_for_session(res[0])
            user.id = res[0]
            user.correo = match[1]
            user.contrasena = match[2]
            user.estado = match[3]
            flask_login.login_user(user)
            
    if flask_login.current_user.is_authenticated:
        return redirect_dest()
    return render_template("login.html", next=request.args.get("next"))

@users_pages.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('.index'))