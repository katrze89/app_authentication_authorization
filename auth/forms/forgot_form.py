""" Forms to forgot password and reset password"""
import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class ForgotForm(FlaskForm):
    """ Form when user forget password"""
    email = StringField("Enter your email to reset a password", validators=[DataRequired()])
    submit = SubmitField("Reset password")


class ResetForm(FlaskForm):
    """ Form to add new password"""
    new_password = PasswordField("Enter new password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm new password", validators=[DataRequired()])
    submit = SubmitField("Set password")

    @staticmethod
    def validate_new_password(form, field):  # pylint: disable=unused-argument
        """Validate passwort to have at least one number, one small letter and one big letter

        :param form:
        :param field:
        :return: ValidationError
        """
        pattern = re.compile("^.*(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$")  # pylint: disable=anomalous-backslash-in-string
        if not pattern.match(field.data):
            raise ValidationError("Password must contain at least one digit, small and big letter")
