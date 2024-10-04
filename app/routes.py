from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import RegistrationForm, LoginForm, SearchForm
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from . import db, bcrypt

main = Blueprint("main", __name__)


@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in.", "success")
        return redirect(url_for("main.login"))
    return render_template("auth/register.html", title="Register", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("main.dashboard"))
        else:
            flash("Login unsuccessful. Check email and password.", "danger")
    return render_template("auth/login.html", title="Login", form=form)


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


@main.route("/music")
@login_required
def music():
    search = request.args.get("search")
    search_form = SearchForm()
    search_form.search.data = search
    return render_template("music.html", title="Music", search_form=search_form)
