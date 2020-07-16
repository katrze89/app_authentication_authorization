from unittest import TestCase
from unittest.mock import patch

from auth import app
from auth.helpers.send_emails import send_email, send_confirmation_email, send_forgot_email


class TestSendEmail(TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_correct_data(self):
        with app.test_request_context():
            response = send_email("topic", ["katarzyna.rzesikowska@gmail.com"], "Kasia")
            self.assertTrue(response)

    def test_incorrect_email(self):
        with app.test_request_context():
            response = send_email("topic", ["katarzyna.rzesikowska"], "Kasia")
            self.assertFalse(response)

    def test_incorrect_email_format(self):
        with app.test_request_context():
            response = send_email("topic", "katarzyna.rzesikowska@gmail.com", "Kasia")
            self.assertFalse(response)

    @patch("auth.helpers.send_emails.Message")
    def test_Message_called(self, mock_Message):
        send_email("subject", ["recipients"], "html_body")
        mock_Message.assert_called()

    @patch("auth.helpers.send_emails.Message")
    def test_Message_called_once(self, mock_Message):
        send_email("subject", ["recipients"], "html_body")
        mock_Message.assert_called_once()

    @patch("auth.helpers.send_emails.Message")
    def test_Message_called_with(self, mock_Message):
        send_email("subject", ["recipients"], "html_body")
        mock_Message.assert_called_with("subject", recipients=["recipients"])

    @patch("auth.helpers.send_emails.Message")
    @patch("auth.helpers.send_emails.mail")
    def test_mail_called(self, mock_mail, mock_Message):
        send_email("subject", ["recipients"], "html_body")
        mock_mail.send.assert_called()

    @patch("auth.helpers.send_emails.Message")
    def test_Message_throws_exception(self, mock_Message):
        mock_Message.side_effect = Exception
        response = send_email("subject", ["recipients"], "html_body")
        self.assertFalse(response)

    @patch("auth.helpers.send_emails.Message")
    @patch("auth.helpers.send_emails.mail")
    def test_mail_called_once(self, mock_mail, mock_Message):
        send_email("subject", ["recipients"], "html_body")
        mock_mail.send.assert_called_once()

    @patch("auth.helpers.send_emails.Message")
    @patch("auth.helpers.send_emails.mail")
    def test_mail_called_with_object_Message(self, mock_mail, mock_Message):
        send_email("subject", ["recipients"], "html_body")
        msg = mock_Message("subject", recipients=["recipients"])
        mock_mail.send.assert_called_with(msg)

    @patch("auth.helpers.send_emails.Message")
    @patch("auth.helpers.send_emails.mail")
    def test_mail_throws_exception(self, mock_mail, mock_Message):
        mock_mail.send.side_effect = Exception
        response = send_email("subject", ["recipients"], "html_body")
        self.assertFalse(response)

    @patch("auth.helpers.send_emails.Message")
    @patch("auth.helpers.send_emails.mail")
    def test_function_return_true(self, mock_mail, mock_Message):
        response = send_email("subject", ["recipients"], "html_body")
        self.assertTrue(response)


class TestSendConfirmationEmail(TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_correct_data(self):
        with app.test_request_context():
            res = send_confirmation_email("katarzyna.rzesikowska@gmail.com", "Kasia")
            self.assertTrue(res)

    def test_incorrect_email(self):
        with app.test_request_context():
            res = send_confirmation_email("katarzyna.rzesikowska", "Kasia")
            self.assertFalse(res)


class TestSendForgotEmail(TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_correct_data(self):
        with app.test_request_context():
            res = send_forgot_email("katarzyna.rzesikowska@gmail.com", "Kasia")
            self.assertTrue(res)

    def test_incorrect_email(self):
        with app.test_request_context():
            res = send_forgot_email("katarzyna.rzesikowska", "Kasia")
            self.assertFalse(res)
