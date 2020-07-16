"""Module responsible for main view

"""
from flask import Blueprint, render_template, url_for, flash  # pylint: disable=import-error
from flask_jwt_extended import get_jwt_identity, jwt_optional, jwt_required
from werkzeug.utils import redirect

from auth.forms import RegisterForm
from auth.helpers import send_confirmation_email, add_user

main_bp = Blueprint("main", __name__, url_prefix="/")  # pylint: disable=invalid-name


@main_bp.route("/", methods=["GET", "POST"])
@jwt_optional
def home():
    """root endpoint in application

    :return: redirect to index html or say that user is logged
    """
    current_user = get_jwt_identity()
    if current_user is not None:
        return render_template("login.html", name=current_user)

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data

        if send_confirmation_email(email, name):
            flash("Email send", "success")
            resp_id = add_user(email, name, "", password, False)
            if resp_id is not None:
                return redirect(url_for("main.home"))

        return "Bad request", 400

    return render_template("index.html", form=form)
