"""API initiation

"""
from datetime import timedelta

from flask import Flask, flash, redirect, url_for, make_response  # pylint: disable=import-error
from flask_jwt_extended import unset_jwt_cookies, unset_access_cookies

from auth.views import auth_bp, main_bp, signin_bp, forgot_bp
from auth.helpers.jwt_helpers import jwt
from auth.helpers import mail


app = Flask(__name__)  # pylint: disable=invalid-name
app.config['SECRET_KEY'] = 'Es\xdb\xc7\x1cfvL\x15B\xe7\x90z\xef\xab\xb0'

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(signin_bp)
app.register_blueprint(forgot_bp)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "apkamemo@gmail.com"
app.config['MAIL_PASSWORD'] = "12memo34"
mail.init_app(app)

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_SECRET_KEY"] = "super-secret"  # TODO change this
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=30)

# app.config["JWT_ACCESS_COOKIE_PATH"] = "/api"
# TODO  list of the urls you want the access tokens to be accessible from

jwt.init_app(app)


@app.errorhandler(404)
def page_not_found(exception):  # pylint: disable=unused-argument
    """Error when page is not found

    :return: "Page not found"
    """
    return "Page not found"


@app.errorhandler(500)
def server_error(exception):  # pylint: disable=unused-argument
    """Internal Server Error

    :return: "Server error"
    """
    return "Server error"


@jwt.unauthorized_loader
def unauthorized_loader(callback):  # pylint: disable=unused-argument
    """When user want to enter the endpoint without authorization

    :param callback:
    :return: Redirect to login page
    """
    flash("You must be logged in.", "danger")
    return redirect(url_for("signin.login"))


@jwt.invalid_token_loader
def invalid_token_callback(callback):  # pylint: disable=unused-argument
    """When the user have invalid token

    :param callback:
    :return: redirect to login and remove both tokens
    """
    flash("Invalid access token.", "danger")
    resp = make_response(redirect(url_for("signin.login")))
    unset_jwt_cookies(resp)
    return resp


@jwt.expired_token_loader
def expired_token_callback(callback):  # pylint: disable=unused-argument
    """When user's access token expires

    :param callback:
    :return: redirect to refresh token
    """
    resp = make_response(redirect(url_for("signin.login")))
    unset_access_cookies(resp)
    return resp


if __name__ == "__main__":
    app.run(ssl_context="adhoc", port=3010)
