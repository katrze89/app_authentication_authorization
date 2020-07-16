"""Module responsible for generating tokens and sending to user"""
from itsdangerous import URLSafeTimedSerializer
from flask import url_for, render_template
from flask_mail import Message, Mail  # pylint: disable=import-error


mail = Mail()  # pylint: disable=invalid-name

secret_key = "kasia"  # TODO fix this


def send_email(subject: str, recipients: list, html_body: str):
    """ send email

    :param subject: Title of the email
    :param recipients: list of recipients
    :param html_body: email body
    :return: True/False
    """
    try:
        msg = Message(subject, recipients=recipients)
    except:  # pylint: disable=broad-except
        return False

    msg.html = html_body
    msg.sender = "apkamemo@gmail.com"
    try:
        mail.send(msg)
        return True
    except:  # pylint: disable=broad-except
        return False


def send_confirmation_email(email, name):
    """Send email to confirm the account

    :param email: user's email
    :param name: user's name
    :return:
    """
    confirm_serializer = URLSafeTimedSerializer(secret_key)

    confirm_url = url_for(
        'auth.confirm_account',
        token=confirm_serializer.dumps(email, salt='email-confirm-salt'),
        _external=True)

    html = render_template(
        'email_create.html',
        confirm_url=confirm_url,
        name=name
    )

    return send_email("Confirm your account", [email], html)


def send_forgot_email(email, name):
    """Send email to reset password

    :param email: user's email
    :param name: user's name
    :return:
    """
    reset_serializer = URLSafeTimedSerializer(secret_key)

    reset_url = url_for(
        'forgot.reset_password',
        token=reset_serializer.dumps(email, salt='email-reset-salt'),
        _external=True)

    html = render_template(
        'email_reset.html',
        reset_url=reset_url,
        name=name
    )

    return send_email("Reset the password", [email], html)
