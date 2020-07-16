"""Form to register user

"""
import re

from flask_wtf import FlaskForm  # pylint: disable=import-error
from wtforms import StringField, PasswordField, SubmitField  # pylint: disable=import-error
from wtforms.validators import DataRequired, Email, Length, ValidationError  # pylint: disable=import-error

from auth.helpers import find_user


class RegisterForm(FlaskForm):  # pylint: disable=too-few-public-methods
    """Form to register user"""
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Sign up for Memo")

    @staticmethod
    def validate_email(form, field):  # pylint: disable=unused-argument
        """Validate email -> cannot be in the database

        :param form:
        :param field:
        :return: ValidationError
        """
        if find_user(field.data, ""):
            raise ValidationError("Email is already registered")

    @staticmethod
    def validate_password(form, field):  # pylint: disable=unused-argument
        """Validate password to have at least one number, one small letter and one big letter

        :param form:
        :param field:
        :return: ValidationError
        """
        pattern = re.compile("^.*(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$")  # pylint: disable=anomalous-backslash-in-string
        if not pattern.match(field.data):
            raise ValidationError("Password must contain at least one digit, small and big letter")
