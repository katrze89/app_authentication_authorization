"""Form to sign in user

"""
from flask_wtf import FlaskForm  # pylint: disable=import-error
from wtforms import StringField, PasswordField, SubmitField  # pylint: disable=import-error
from wtforms.validators import DataRequired, Email  # pylint: disable=import-error


class SigninForm(FlaskForm):  # pylint: disable=too-few-public-methods
    """Form to sign in user"""
    email = StringField("Email address", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")
