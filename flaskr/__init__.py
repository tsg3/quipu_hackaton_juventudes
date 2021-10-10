import os
from flask import Flask, request, session, redirect, url_for
import flaskr.app.persistence.users as users

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    path = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(path, "../config/data"))
    file = open(path, "r")
    app.config.from_mapping(
        SECRET_KEY=file.read()
    )
    file.close()

    @app.route('/')
    def index():
        roles = users.get_roles()
        # roles = "roles"
        if 'username' in session:
            return f'Logged in as {session["username"]} -> roles={roles}'
        return f'You are not logged in -> roles={roles}'

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return '''
            <form method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Login>
            </form>
        '''

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect(url_for('index'))

    return app