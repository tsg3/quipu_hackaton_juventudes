from flask import Blueprint, request, session, redirect, url_for
import flask_login

forum_pages = Blueprint('forum', __name__, url_prefix="/forum")
@forum_pages.route('/')
def index():
    if flask_login.current_user.get_id() != None:
        return "Forum: Logged"
    return redirect(url_for('index.index'))