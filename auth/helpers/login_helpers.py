"""helpers for login

"""
import configparser
from datetime import datetime
import os

from pymongo import errors  # pylint: disable=import-error
from werkzeug.security import generate_password_hash  # pylint: disable=import-error

from oauthlib.oauth2 import WebApplicationClient  # pylint: disable=import-error

from auth.db import memo_users


def create_client(service):
    """Create client for web application and obtain endpoints

    :param service: name of the external service
    :return: tuple of client and config or Bad Request
    """
    config = configparser.ConfigParser()
    base_dir = os.path.abspath(os.path.dirname(os.getcwd()))

    path = os.path.join(base_dir, "auth", "configuration.ini")
    config.read(path)
    if service in config.sections():
        conf = {"client_id": config[service]["CLIENT_ID"],
                "client_secret": config[service]["CLIENT_SECRET"],
                "auth_endpoint": config[service]["AUTH_ENDPOINT"],
                "scope": config[service]["SCOPE"],
                "token_endpoint": config[service]["TOKEN_ENDPOINT"],
                "user_endpoint": config[service]["USER_ENDPOINT"]}

        client = WebApplicationClient(conf["client_id"])
        return client, conf
    return "Bad request", 400


def find_user(email, login):
    """Check if user is in database

    :param email: email of the user
    :param login: github login of the user
    :return: True or False
    """
    if email == "Empty":
        return memo_users.find_one({"login": login}) is not None
    return memo_users.find_one({"email": email}) is not None


def find_user_active(email, authorised):
    """Find user with authorization status

    :param email: user's email
    :param authorised: user's authorization status
    :return: document or None
    """
    return memo_users.find_one({"email": email, "is_authorized": authorised})


def update_user(document, new_values):
    """Update document in users

    :param document: document
    :param new_values: dict with new values
    :return: True or False
    """
    try:
        memo_users.update_one(document, new_values)
        return True
    except:  # pylint: disable=bare-except
        return False


def add_user(email, name, login, password, is_authorized):
    """Add user to database

    :param email: user email
    :param name: user name
    :param login: github user's login
    :param password: user password
    :param is_authorized: True/False is user account is authorized
    :return: True or False
    """
    user = {"email": email,
            "name": name,
            "login": login,
            "password": generate_password_hash(password),
            "is_authorized": is_authorized,
            "data_auth": datetime.now()}
    try:
        resp_id = memo_users.insert_one(user)
        return resp_id.inserted_id
    except errors.WriteError:
        return None
