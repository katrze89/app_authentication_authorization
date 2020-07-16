"""User class and user's functionality

"""
from flask_login import UserMixin   # pylint: disable=import-error


class User(UserMixin):  # pylint: disable=too-few-public-methods
    """User Model

    """
    def __init__(self, idx, name, email):
        self.id = idx  # pylint: disable=invalid-name
        self.name = name
        self.email = email


class Users:
    """Model for all Users

    """
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        """Add object User to self.users

        :param user: object User
        :return: True or False
        """
        try:
            self.users[str(user.id)] = user
            return True
        except AttributeError:
            return False

    def get_user(self, idx):
        """Obtain object User by id

        :param idx: id of the User
        :return: User object or None
        """
        try:
            return self.users[str(idx)]
        except KeyError:
            return None

    def remove_user(self, idx):
        """Remove object User frm self.users

        :param idx: id of the user
        :return:
        """
        try:
            self.users.pop(str(idx))
        except KeyError:
            pass


users = Users()  # pylint: disable=invalid-name
