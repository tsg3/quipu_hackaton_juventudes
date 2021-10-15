import base64

from flask import Blueprint, request, redirect, url_for, render_template
import flask_login

import flaskr.app.persistence.users as user_db
import flaskr.app.persistence.forum as forum_db
from flaskr.app.models.users import User

users_pages = Blueprint('index', __name__)
@users_pages.route('/')
def index():
    if flask_login.current_user.get_id() != None:
        return "Main page: Logged"
    return "Main page: Not logged"

@users_pages.route('/profile', methods=['GET'])
def profile():
    key = flask_login.current_user.get_id()
    if key != None:
        
        res = user_db.get_user_data(key)

        if res == -1: # Error
            return redirect(url_for('.index'))

        elif res[8] == 1:
            return render_template("profile.html", user=res)

        return redirect(url_for('.index')) # Deleted user

    return redirect(url_for('.index')) # Not logged

@users_pages.route('/profile/saved/forums', methods=['GET'])
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
    if request.method == 'POST':
        res = user_db.create_user(request.form)
        if res == 0:
            return redirect(url_for('.index'))
        return redirect(url_for('.register'))
    return '''
        <form method="post">
            <p>idRol<input type=text name=idRol>
            <p>correo<input type=text name=correo>
            <p>nombre<input type=text name=nombre>
            <p>apellido1<input type=text name=apellido1>
            <p>apellido2<input type=text name=apellido2>
            <p>ano<input type=text name=ano>
            <p>mes<input type=text name=mes>
            <p>dia<input type=text name=dia>
            <p>genero<input type=text name=genero>
            <p>nacionalidad<input type=text name=nacionalidad>
            <p>residencia<input type=text name=residencia>
            <p>contrasena<input type=text name=contrasena>
            <p><input type=submit value=Register>
        </form>
    '''

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
            
            return redirect(url_for('.index'))
        return redirect(url_for('.login'))
    if request.method == 'GET' and flask_login.current_user.is_authenticated:
        return redirect(url_for('.index'))
    return '''
        <form method="post">
            <p>correo<input type=text name=correo>
            <p>contrasena<input type=text name=contrasena>
            <p><input type=submit value=Login>
        </form>
    '''

@users_pages.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('.index'))