from unittest import TestCase

from auth import app
from auth.views import initiate


class TestInitiate(TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def test_incorrect_service(self):
        self.app.get()
        response = self.app.get('/login/google2', follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_request_uri(self):
        self.app.get()
        response = initiate("google")
        uri = str(response.get_data()).split('href="')[1]
        uri = uri.split('">')[0]
        uri = uri.replace("amp;", "")
        request_uri = "https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=73265906969-q8n866doeclji8sjaesu8umjp2ml1094.apps.googleusercontent.com&redirect_uri=https%3A%2F%2F127.0.0.1%3A3010%2Flogin%2Fcallback&scope=openid+email+profile"
        self.assertEqual(uri, request_uri)
