from flask import Blueprint, url_for, redirect, render_template, flash, request, session
from flask_login import current_user, login_user, logout_user
from app.users.forms import LoginForm
from app.models import User
from app import bcrypt

users = Blueprint('users', __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            session['logged_in'] = True
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login unsuccessful! Please check username and password!", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect(url_for("home"))
