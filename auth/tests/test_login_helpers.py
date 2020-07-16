import os
from unittest import TestCase
from oauthlib.oauth2 import WebApplicationClient

from auth.helpers import create_client, find_user


class TestCreateClient(TestCase):

    def setUp(self) -> None:
        service = "google"
        self.result = create_client(service)

    def test_correct_service(self):
        self.assertNotEqual(self.result, ("Bad request", 400))

    def test_incorrect_service(self):
        service = "google2"
        result = create_client(service)
        self.assertEqual(result, ("Bad request", 400))

    def test_client_is_webapplicationclient_instance(self):
        client, _ = self.result
        self.assertIsInstance(client, WebApplicationClient)

    def test_client_is_init_with_correct_client(self):
        client, _ = self.result
        client_id = client.client_id
        corr_client_id = os.environ["GOOGLE_CLIENT_ID"]
        self.assertEqual(client_id, corr_client_id)

    def test_conf_is_dict_instance(self):
        _, conf = self.result
        self.assertIsInstance(conf, dict)

    def test_conf_keys(self):
        _, conf = self.result
        keys = ["client_id", "client_secret", "auth_endpoint", "scope", "token_endpoint", "user_endpoint"]
        dict_keys = list(conf.keys())
        self.assertEqual(keys, dict_keys)

    def test_conf_values(self):
        correct_conf = {"client_id": os.environ["GOOGLE_CLIENT_ID"],
                "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
                "auth_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
                "scope": '["openid", "email", "profile"]',
                "token_endpoint": "https://www.googleapis.com/oauth2/v4/token",
                "user_endpoint": "https://www.googleapis.com/oauth2/v1/userinfo"}
        _, conf = self.result
        self.assertEqual(correct_conf, conf)
