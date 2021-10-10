from flask import Blueprint, request, redirect, url_for, session
from flaskr.app.persistence.users import *

users_pages = Blueprint('index', __name__)
@users_pages.route('/')
def index():
    if 'username' in session:
        return "Main page: Logged"
    return "Main page: Not logged"

@users_pages.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        res = create_user(request.form)
        if res == 0:
            return redirect(url_for('.index'))
        return redirect(url_for('.register'))
    return '''
        <form method="post">
            <p>idRol<input type=text name=idRol>
            <p>username<input type=text name=username>
            <p>nombre<input type=text name=nombre>
            <p>apellido1<input type=text name=apellido1>
            <p>apellido2<input type=text name=apellido2>
            <p>ano<input type=text name=ano>
            <p>mes<input type=text name=mes>
            <p>dia<input type=text name=dia>
            <p>genero<input type=text name=genero>
            <p>nacionalidad<input type=text name=nacionalidad>
            <p>residencia<input type=text name=residencia>
            <p>actividad<input type=text name=actividad>
            <p>contrasena<input type=text name=contrasena>
            <p><input type=submit value=Register>
        </form>
    '''

@users_pages.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = login_user(request.form)
        if res == 0:
            session['username'] = request.form['username']
            return redirect(url_for('.index'))
        return redirect(url_for('.login'))
    if request.method == 'GET' and 'username' in session:
        return redirect(url_for('.index'))
    return '''
        <form method="post">
            <p>username<input type=text name=username>
            <p>contrasena<input type=text name=contrasena>
            <p><input type=submit value=Login>
        </form>
    '''

@users_pages.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('.index'))