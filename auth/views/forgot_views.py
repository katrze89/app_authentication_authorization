""" Module related to forgot password"""
from flask import Blueprint, flash, url_for, render_template
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from auth.forms import ForgotForm, ResetForm
from auth.helpers import find_user_active, send_forgot_email, find_user, update_user

forgot_bp = Blueprint("forgot", __name__, url_prefix="/forgot")  # pylint: disable=invalid-name

secret_key = "kasia"  # TODO fix this


@forgot_bp.route("/", methods=["GET", "POST"])
def forgot():
    """Send email to reset password

    :return: redirect to home or reset_password
    """
    form = ForgotForm()

    if form.validate_on_submit():
        email = form.email.data

        user = find_user_active(email, True)

        if user is None:
            flash("No such user in the database", "danger")
            return redirect(url_for("main.home"))

        send_forgot_email(email, user["name"])

        flash(f"Email to {email}send", "success")
        return redirect(url_for("main.home"))

    return render_template("reset_password.html", form=form)


@forgot_bp.route("/reset/<token>")
def reset_password(token):
    """Reset password

    :param token: token to reset password
    :return: redirect to index or Bad request
    """
    try:
        forgot_serializer = URLSafeTimedSerializer(secret_key)
        email = forgot_serializer.loads(token, salt='email-reset-salt', max_age=5400)
    except:  # pylint: disable=bare-except
        return "The reset link is invalid or has expired."

    if find_user(email, ""):
        user = find_user_active(email, False)
        if not user:
            return redirect(url_for("forgot.reset_password_form", email=email))

        flash(f"Email {email} is not registered", "danger")
        return redirect(url_for("main.home"))

    flash(f"Email {email} not in the database", "danger")
    return redirect(url_for("main.home"))


@forgot_bp.route("/reset/form/<email>", methods=["GET", "POST"])
def reset_password_form(email):
    """Set new password

    :param email: user's email
    :return: redirect to index or Bad request
    """
    form = ResetForm()

    if form.validate_on_submit():
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        user = find_user_active(email, True)

        if user is None:
            flash("No such user in the database", "danger")
            return redirect(url_for("main.home"))

        if new_password != confirm_password:
            flash("Passwords do not match", "danger")
            return render_template("new_password.html", form=form, email=email)

        update_user(user, {"$set": {"password": generate_password_hash(new_password)}})

        flash(f"Password has been changed", "success")
        return redirect(url_for("main.home"))

    return render_template("new_password.html", form=form, email=email)
