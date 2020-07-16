from unittest import TestCase
from unittest.mock import patch

from pymongo import errors

from auth.db.db_conf import create_db_instance


class TestCreateDbInstance(TestCase):
    def setUp(self) -> None:
        self.correct_connection = 'mongodb://memo:memo@localhost:27017/?authSource=memo'

    @patch("auth.db.db_conf.MongoClient")
    def test_correct_connection(self, mock_MongoClient):
        db = create_db_instance("localhost", 27017, "memo", "memo", "memo")
        db["memo"].list_collection_names()
        mock_MongoClient.assert_called_with(self.correct_connection)

    @patch("auth.db.db_conf.MongoClient")
    def test_incorrect_password(self, mock_MongoClient):
        db = create_db_instance("localhost", 27017, "memo", "memo2", "memo")
        db["memo"].list_collection_names()
        with self.assertRaises(AssertionError):
            mock_MongoClient.assert_called_with(self.correct_connection)

    @patch("auth.db.db_conf.MongoClient")
    def test_incorrect_db(self, mock_MongoClient):
        db = create_db_instance("localhost", 27017, "memo", "memo", "memo2")
        db["memo"].list_collection_names()
        with self.assertRaises(AssertionError):
            mock_MongoClient.assert_called_with(self.correct_connection)

    @patch("auth.db.db_conf.MongoClient")
    def test_incorrect_port(self, mock_MongoClient):
        db = create_db_instance("localhost", 27018, "memo", "memo", "memo")
        db["memo"].list_collection_names()
        with self.assertRaises(AssertionError):
            mock_MongoClient.assert_called_with(self.correct_connection)

    @patch("auth.db.db_conf.MongoClient")
    def test_incorrect_host(self, mock_MongoClient):
        db = create_db_instance("localhost2", 27017, "memo", "memo", "memo")
        db["memo"].list_collection_names()
        with self.assertRaises(AssertionError):
            mock_MongoClient.assert_called_with(self.correct_connection)

    @patch("auth.db.db_conf.MongoClient")
    def test_insert_with_ConnectionFailure(self, mock_MongoClient):
        mock_MongoClient.site_effect = errors.ConnectionFailure
        create_db_instance("localhost2", 27017, "memo", "memo", "memo")
        self.assertEqual(mock_MongoClient.assert_called_once(), None)

    @patch("auth.db.db_conf.MongoClient")
    def test_insert_with_ServerSelectionTimeoutError(self, mock_MongoClient):
        mock_MongoClient.site_effect = errors.ServerSelectionTimeoutError
        create_db_instance("localhost2", 27017, "memo", "memo", "memo")
        self.assertEqual(mock_MongoClient.assert_called_once(), None)

    @patch("auth.db.db_conf.MongoClient")
    def test_insert_with_OperationFailure(self, mock_MongoClient):
        mock_MongoClient.site_effect = errors.OperationFailure
        create_db_instance("localhost2", 27017, "memo", "memo", "memo")
        self.assertEqual(mock_MongoClient.assert_called_once(), None)
