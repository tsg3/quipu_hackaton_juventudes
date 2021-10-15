from flask import Blueprint, request, redirect, url_for, render_template
import flask_login
from uuid import uuid4
import base64
from datetime import datetime

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

@forum_pages.route('/read/<uuid>', methods=['GET'])
def read(uuid):
    if flask_login.current_user.get_id() == None:
        return redirect(url_for('index.index'))

    key = uuid.encode()
    padding = 4 - (len(key) % 4)
    key = base64.urlsafe_b64decode(key + (b"=" * padding))
    match = forum_db.get_forum(key)

    if match != -1 and match != -2:
        comments = forum_db.get_comments(key)
        state = "Abierto" if match[3] == 0 else "Cerrado"
        saved = forum_db.check_saved(flask_login.current_user.get_id(), key)

        return render_template("forum.html", 
            forum=match, state=state, uuid=uuid, comments=comments, saved=saved)

    return redirect(url_for('index.index'))

@forum_pages.route('/read/<uuid>/comment', methods=['POST'])
def comment(uuid):
    if flask_login.current_user.get_id() == None:
        return redirect(url_for('index.index'))

    if request.form["texto"] != "":
        key = uuid.encode()
        padding = 4 - (len(key) % 4)
        key = base64.urlsafe_b64decode(key + (b"=" * padding))

        res = forum_db.post_comment(
            request.form["texto"], flask_login.current_user.get_id(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), idForum=key
        )
        
        if res > -1:
            return redirect(url_for('.read', uuid=uuid))

        return redirect(url_for('index.index'))

    return redirect(url_for('index.index'))

@forum_pages.route('/read/<uuid>/reply', methods=['POST'])
def reply(uuid):
    if flask_login.current_user.get_id() == None:
        return redirect(url_for('index.index'))

    if request.form["texto"] != "" or request.form["comment_key"] != "":
        
        key = None
        try:
            key = int(request.form["comment_key"])
        except:
            return redirect(url_for('index.index'))

        res = forum_db.post_comment(
            request.form["texto"], flask_login.current_user.get_id(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), idComment=key
        )
        
        if res > -1:
            return redirect(url_for('.read', uuid=uuid))

        return redirect(url_for('index.index'))

    return redirect(url_for('index.index'))

@forum_pages.route('/read/<uuid>/save', methods=['POST'])
def save(uuid):
    if flask_login.current_user.get_id() == None:
        return redirect(url_for('index.index')) # Not logged
        
    key = uuid.encode()
    padding = 4 - (len(key) % 4)
    key = base64.urlsafe_b64decode(key + (b"=" * padding))

    res = forum_db.save_forum(flask_login.current_user.get_id(), key)
    
    if res == 0:
        return redirect(url_for('.read', uuid=uuid)) # Worked

    return redirect(url_for('index.index')) # Error