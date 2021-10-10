from flask import Blueprint, request, redirect, url_for, render_template
import flask_login

import flaskr.app.persistence.forum as forum_db 

forum_pages = Blueprint('forum', __name__, url_prefix="/forum")
@forum_pages.route('/', methods=['GET'])
def index():
    if flask_login.current_user.get_id() == None:
        return redirect(url_for('index.index'))

    forums = forum_db.get_forums()
    if forums != -1:
        return render_template("forums.html", forums=forums)

    return redirect(url_for('index.index'))

@forum_pages.route('/post', methods=['GET', 'POST'])
def post():
    if flask_login.current_user.get_id() == None:
        return redirect(url_for('index.index'))
    elif request.method == "POST":
        res = forum_db.post_forum(flask_login.current_user.get_id(), request.form)
        if res == 0:
            return redirect(url_for('.index'))
        return redirect(url_for('.post'))
    return """
    <form method="post">
        <p>titulo<input type=text name=titulo>
        <p>datos<input type=text name=datos>
        <p><input type=submit value=Post>
    </form>"""

@forum_pages.route('/read', methods=['POST'])
def read():
    if flask_login.current_user.get_id() == None or request.form.get("read") == None:
        return redirect(url_for('index.index'))

    match = forum_db.get_forum(request.form.get("read"))
    if match != -1 and match != -2:
        return f"""<h1>Título: {match[0]}</h1>
            <p>{match[1]}"""

    return redirect(url_for('index.index'))