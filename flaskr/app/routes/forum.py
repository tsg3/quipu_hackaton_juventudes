from flask import Blueprint, request, redirect, url_for, render_template
import flask_login
from uuid import uuid4
import base64

import flaskr.app.persistence.forum as forum_db 

forum_pages = Blueprint('forum', __name__, url_prefix="/forum")
@forum_pages.route('/', methods=['GET'])
def index():
    if flask_login.current_user.get_id() == None:
        return redirect(url_for('index.index'))

    forums = forum_db.get_forums()
    if forums != -1:
        forums_list = [list(forum) for forum in forums]
        for i in range(len(forums_list)):
            forums_list[i][0] = base64.urlsafe_b64encode(forums_list[i][0]).rstrip(b"=").decode()
        return render_template("forums.html", forums=forums_list)

    return redirect(url_for('index.index'))

@forum_pages.route('/post', methods=['GET', 'POST'])
def post():
    if flask_login.current_user.get_id() == None:
        return redirect(url_for('index.index'))
    elif request.method == "POST":
        key = uuid4().hex
        res = forum_db.post_forum(flask_login.current_user.get_id(), key, request.form)
        if res == 0:
            return redirect(url_for('.index'))
        return redirect(url_for('.post'))
    return """
    <form method="post">
        <p>titulo<input type=text name=titulo>
        <p>datos<input type=text name=datos>
        <p><input type=submit value=Post>
    </form>"""

@forum_pages.route('/read/<uuid>', methods=['GET', 'POST']) # Only GET for the moment
def read(uuid):
    if flask_login.current_user.get_id() == None:
        return redirect(url_for('index.index'))

    key = uuid.encode()
    padding = 4 - (len(key) % 4)
    key = base64.urlsafe_b64decode(key + (b"=" * padding))
    match = forum_db.get_forum(key)

    if match != -1 and match != -2:
        state = "Abierto" if match[3] == 0 else "Cerrado"
        return f"""<h1>[{state}] Título: {match[0]}</h1>
            ~ Publicado por {match[4]} {match[5]} {match[6]} el: {match[2]}
            <p>{match[1]}"""

    return redirect(url_for('index.index'))