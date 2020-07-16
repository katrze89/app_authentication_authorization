from unittest import TestCase
from unittest.mock import patch

from pymongo import errors

from auth.helpers.login_helpers import (
    add_user,
    update_user,
    find_user_active,
    find_user
)


class TestFindUser(TestCase):
    @patch("auth.helpers.login_helpers.memo_users")
    def test_find_user_email_empty_called(self, mock_memo_users):
        find_user("Empty", "katrze89")
        mock_memo_users.find_one.assert_called()

    @patch("auth.helpers.login_helpers.memo_users")
    def test_find_user_email_empty_called_once(self, mock_memo_users):
        find_user("Empty", "katrze89")
        mock_memo_users.find_one.assert_called_once()

    @patch("auth.helpers.login_helpers.memo_users")
    def test_find_user_email_empty_called_with(self, mock_memo_users):
        find_user("Empty", "katrze89")
        mock_memo_users.find_one.assert_called_with({
            "login": "katrze89"})

    @patch("auth.helpers.login_helpers.memo_users")
    def test_find_user_email_empty_return_true(self, mock_memo_users):
        result = find_user("Empty", "katrze89")
        self.assertTrue(result)

    @patch("auth.helpers.login_helpers.memo_users", return_value=None)
    def test_find_user_email_empty_return_false(self, mock_memo_users):
        mock_memo_users.find_one.return_value = None
        result = find_user("Empty", "katrze89")
        self.assertFalse(result)

    @patch("auth.helpers.login_helpers.memo_users")
    def test_find_user_email_not_empty_called(self, mock_memo_users):
        find_user("katarzyna.rzesikowska@gmail.com", "katrze89")
        mock_memo_users.find_one.assert_called()

    @patch("auth.helpers.login_helpers.memo_users")
    def test_find_user_email_not_empty_called_once(self, mock_memo_users):
        find_user("katarzyna.rzesikowska@gmail.com", "katrze89")
        mock_memo_users.find_one.assert_called_once()

    @patch("auth.helpers.login_helpers.memo_users")
    def test_find_user_email_not_empty_called_with(self, mock_memo_users):
        find_user("katarzyna.rzesikowska@gmail.com", "katrze89")
        mock_memo_users.find_one.assert_called_with({
            "email": "katarzyna.rzesikowska@gmail.com"})

    @patch("auth.helpers.login_helpers.memo_users")
    def test_find_user_email_not_empty_return_true(self, mock_memo_users):
        result = find_user("katarzyna.rzesikowska@gmail.com", "katrze89")
        self.assertTrue(result)

    @patch("auth.helpers.login_helpers.memo_users", return_value=None)
    def test_find_user_email_not_empty_return_false(self, mock_memo_users):
        mock_memo_users.find_one.return_value = None
        result = find_user("katarzyna.rzesikowska@gmail.com", "katrze89")
        self.assertFalse(result)


class TestFindUserActive(TestCase):
    @patch("auth.helpers.login_helpers.memo_users")
    def test_find_user_active_called(self, mock_memo_users):
        find_user_active("katarzyna.rzesikowska@gmail.com", True)
        mock_memo_users.find_one.assert_called()

    @patch("auth.helpers.login_helpers.memo_users")
    def test_find_user_active_called_once(self, mock_memo_users):
        find_user_active("katarzyna.rzesikowska@gmail.com", True)
        mock_memo_users.find_one.assert_called_once()

    @patch("auth.helpers.login_helpers.memo_users")
    def test_find_user_active_called_with(self, mock_memo_users):
        find_user_active("katarzyna.rzesikowska@gmail.com", True)
        mock_memo_users.find_one.assert_called_with({
            "email": "katarzyna.rzesikowska@gmail.com",
            "is_authorized": True})


class TestUpdateUser(TestCase):

    @patch("auth.helpers.login_helpers.memo_users")
    def test_update_called(self, mock_memo_users):
        update_user("document", "new")
        mock_memo_users.update_one.assert_called()

    @patch("auth.helpers.login_helpers.memo_users")
    def test_update_called_once(self, mock_memo_users):
        update_user("document", "new")
        mock_memo_users.update_one.assert_called_once()

    @patch("auth.helpers.login_helpers.memo_users")
    def test_update_called_with(self, mock_memo_users):
        update_user("document", "new")
        mock_memo_users.update_one.assert_called_with("document", "new")

    @patch("auth.helpers.login_helpers.memo_users")
    def test_update_return_true(self, mock_memo_users):
        self.assertTrue(update_user("document", "new"))

    @patch("auth.helpers.login_helpers.memo_users", )
    def test_insert_with_exception(self, mock_memo_users):
        mock_memo_users.update_one.site_effect = Exception
        update_user("document", "new")
        self.assertFalse(mock_memo_users.update_one.assert_called_once())


class TestAddUser(TestCase):

    @patch("auth.helpers.login_helpers.memo_users")
    def test_insert_called(self, mock_memo_users):
        add_user("email2", "name", "login", "password", True)
        mock_memo_users.insert_one.assert_called()

    @patch("auth.helpers.login_helpers.memo_users")
    def test_insert_called_once(self, mock_memo_users):
        add_user("email2", "name", "login", "password", True)
        mock_memo_users.insert_one.assert_called_once()

    @patch("auth.helpers.login_helpers.datetime")
    @patch("auth.helpers.login_helpers.generate_password_hash")
    @patch("auth.helpers.login_helpers.memo_users")
    def test_insert_called_with(self, mock_memo_users, mock_generate_password_hash, mock_datetime):
        add_user("email2", "name", "login", "password", True)

        mock_memo_users.insert_one.assert_called_with({
            'email': 'email2',
            'name': 'name',
            'login': 'login',
            'password': mock_generate_password_hash("password"),
            'is_authorized': True,
            'data_auth': mock_datetime.now()})

    @patch("auth.helpers.login_helpers.memo_users")
    def test_insert_return_id(self, mock_memo_users):
        add_user("email2", "name", "login", "password", True)
        self.assertNotEqual(mock_memo_users.insert_one().inserted_id, None)

    @patch("auth.helpers.login_helpers.memo_users", )
    def test_insert_with_exception(self, mock_memo_users):
        mock_memo_users.insert_one.site_effect = errors.WriteError
        add_user("email2", "name", "login", "password", True)
        self.assertEqual(mock_memo_users.insert_one.assert_called_once(), None)
