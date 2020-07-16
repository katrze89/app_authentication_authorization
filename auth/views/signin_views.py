""" views responsible for login and logout"""
from flask import Blueprint, flash, url_for, render_template, make_response  # pylint: disable=import-error
from flask_jwt_extended import jwt_required, unset_jwt_cookies  # pylint: disable=import-error
from werkzeug.security import check_password_hash  # pylint: disable=import-error
from werkzeug.utils import redirect  # pylint: disable=import-error

from auth.forms.singin_form import SigninForm
from auth.helpers import find_user_active
from auth.helpers.jwt_helpers import create_token


signin_bp = Blueprint("signin", __name__, url_prefix="/signin")  # pylint: disable=invalid-name


@signin_bp.route("/", methods=["GET", "POST"])
def login():
    """sign in user

    :return: go to signin form, home or Bad request
    """
    form = SigninForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = find_user_active(email, True)

        if user is None:
            flash("Email or/and password is invalid", "danger")
            return render_template("signin.html", form=form)

        if not check_password_hash(user["password"], password):
            flash("Email or/and password is invalid", "danger")
            return render_template("signin.html", form=form)

        return create_token(user["email"], "main.home")

    return render_template("signin.html", form=form)


@signin_bp.route("/logout")
@jwt_required
def logout():
    """Logout user

    :return: redirect to root endpoint
    """

    resp = make_response(redirect(url_for("main.home")))
    unset_jwt_cookies(resp)
    return resp
