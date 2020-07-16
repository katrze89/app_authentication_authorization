"""Module responsible for user authentication and account creation

"""
import json
import requests
from flask import Blueprint, redirect, request, url_for, render_template, flash, session  # pylint: disable=import-error
from itsdangerous import URLSafeTimedSerializer

from auth.helpers import create_client, find_user, add_user, find_user_active, update_user
from auth.forms import RegisterForm
from auth.helpers.jwt_helpers import create_token

auth_bp = Blueprint("auth", __name__, url_prefix="/login")  # pylint: disable=invalid-name

SERVICE = ""

secret_key = "kasia"  # TODO fix this


@auth_bp.route("/<service>")
def initiate(service):
    """ initiate the OAuth 2 flow

    :param service: name of the external service
    :return: redirect to service authorization endpoint or Bed request
    """
    client, conf = create_client(service)
    global SERVICE  # pylint: disable=global-statement
    SERVICE = service
    if client == "Bad request":
        return "Bad request", 400

    request_uri = client.prepare_request_uri(
        conf["auth_endpoint"],
        redirect_uri="https://127.0.0.1:3010/login/callback",
        scope=json.loads(conf["scope"])
    )
    return redirect(request_uri)


@auth_bp.route("callback")
def callback():
    """1. the service sends a unique authorization code
       2. the client sends the authorization code to the token URL
       3. the service sends the client token to use

    :return: "User not verified." or  redirect to root endpoint
    """
    code = request.args.get("code")
    client, conf = create_client(SERVICE)
    if client == "Bad request":
        return "Bad request", 400
    token_url, headers, body = client.prepare_token_request(
        conf["token_endpoint"],
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(conf["client_id"], conf["client_secret"]),
    )
    if SERVICE == "github":
        token_response = token_response.text.split("=")

        token_response = {"access_token": token_response[1].split("&")[0],
                          "scope": token_response[2].split("&")[0],
                          "token_type": token_response[3]}
    else:
        token_response = token_response.json()

    client.parse_request_body_response(json.dumps(token_response))

    uri, headers, body = client.add_token(conf["user_endpoint"])
    user_info_response = requests.get(uri, headers=headers, data=body)

    if user_info_response.status_code == 200:
        unique_id = user_info_response.json()["id"]  # pylint: disable=unused-variable
        users_email = user_info_response.json()["email"]  # pylint: disable=unused-variable
        users_name = user_info_response.json()["name"]  # pylint: disable=unused-variable

        users_email = users_email if users_email is not None else "Empty"
        users_login = user_info_response.json()["login"] if users_email == "Empty" else "Empty"
    else:
        return "User not verified.", 400

    if not find_user(users_email, users_login):
        session["name"] = users_name
        session["email"] = users_email
        session["login"] = users_login

        return redirect(url_for("auth.register_user"))

    return create_token(users_email, "main.home")


@auth_bp.route("/register", methods=["GET", "POST"])
def register_user():  # pylint: disable=unused-argument
    """Register user via external services in the database

    :return: redirect to index or Bad request
    """
    name = session["name"]
    email = session["email"]
    login = session["login"]

    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data

        resp_id = add_user(email, name, login, password, True)
        if resp_id is not None:
            return create_token(email, "main.home")

        return "Bad request", 400

    form.name.data = name
    form.email.data = "" if email == "Empty" else email

    return render_template("register.html", form=form)


@auth_bp.route("/create_account/<token>")
def confirm_account(token):
    """Confirm email to create account

    :param token: token to verify account
    :return: redirect to index or Bad request
    """
    try:
        confirm_serializer = URLSafeTimedSerializer(secret_key)
        email = confirm_serializer.loads(token, salt='email-confirm-salt', max_age=5400)
    except:  # pylint: disable=bare-except
        return "The reset link is invalid or has expired."

    if find_user(email, ""):
        user = find_user_active(email, False)
        if user:
            if update_user(user, {"$set": {"is_authorized": True}}):
                flash(f"Email {email} activated", "success")
                return redirect(url_for("main.home"))

            return "Bad request", 400

        flash(f"Email {email} is already registered", "danger")
        return redirect(url_for("main.home"))

    flash(f"Email {email} not in the database", "danger")
    return redirect(url_for("main.home"))
