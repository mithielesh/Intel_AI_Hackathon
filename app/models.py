from . import db, login_manager
from flask_login import UserMixin
from flask import redirect, url_for


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


# Required by flask-login
@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))


# Customized to disable flash message.
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("main.login"))
