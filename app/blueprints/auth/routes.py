from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user

from . import bp
from .forms import LoginForm
from ...extensions import db
from ...models.user import User


@bp.route("/login/", methods=["GET", "POST"], endpoint="client_login")
def client_login():
    if current_user.is_authenticated:
        # Send admins to the admin dashboard by default
        if getattr(current_user, "is_admin", False):
            return redirect(url_for("admin.index"))
        return redirect(url_for("dashboard.files"))
    form = LoginForm()
    if form.validate_on_submit():
        username = (form.email.data or "").strip().lower()
        user = User.query.filter_by(email=username).first()
        if user and user.check_password(form.password.data) and user.active:
            login_user(user, remember=form.remember.data)
            # Prefer admin dashboard after login if user is admin
            if user.is_admin:
                return redirect(url_for("admin.index"))
            next_url = request.args.get("next")
            return redirect(next_url or url_for("dashboard.files"))
        flash("Invalid credentials", "error")
    return render_template("auth/login.html", form=form)


@bp.route("/logout/", methods=["POST", "GET"])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("main.index"))
