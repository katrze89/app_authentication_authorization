"""Configuration for database"""
import logging
from pymongo import MongoClient, errors  # pylint: disable=import-error


def create_db_instance(host, port, user, password, db_name):
    """Connect database

    :param host: host
    :param port: port
    :param user: user name
    :param password: user password
    :param db_name: name od the database
    :return: database
    """
    try:
        client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/?authSource={db_name}")
        db_memo = client[db_name]
        db_memo.list_collection_names()
        return db_memo
    except errors.ConnectionFailure:
        logging.error("Could not connect to MongoDB")
        return None
    except errors.ServerSelectionTimeoutError:
        logging.error("Could not connect to MongoDB")
        return None
    except errors.OperationFailure as exc:
        logging.error(exc)
        return None


memo_db = create_db_instance("localhost", 27017, "memo", "memo", "memo")  # pylint: disable=invalid-name

memo_users = memo_db["users"] if memo_db is not None else None # pylint: disable=invalid-name
