""" helpers for JSOn web token"""
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies
from flask import url_for, redirect, make_response

secret_key = "kasia"  # TODO fix this
jwt = JWTManager()


def create_token(email, url):
    """Create jwt token for email

    :param email: user's email
    :param url: url where endpoint should redirect to
    :return: token
    """
    access_token = create_access_token(identity=email, fresh=True)
    resp = make_response(redirect(url_for(url), 302))
    set_access_cookies(resp, access_token)

    return resp
