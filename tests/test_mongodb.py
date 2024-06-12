# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=unused-argument
from typing import Any

import mongomock
import pytest
from pymongo import MongoClient

from docuparse import get_logger
from docuparse.store import MongoDBConnection, MongoDBDataReader, MongoDBDataWriter

logger = get_logger()


@pytest.fixture
def mock_mongo_client(monkeypatch):
    def mock_client(*args, **kwargs):
        return mongomock.MongoClient()

    monkeypatch.setattr(MongoClient, "__new__", mock_client)


@pytest.fixture
def mongodb_connection(mock_mongo_client):
    connection = MongoDBConnection("mongodb://localhost:27017/", "test_db")
    return connection


def test_connect(mongodb_connection):
    mongodb_connection.connect()
    assert mongodb_connection.client is not None
    assert mongodb_connection.db is not None
    assert mongodb_connection.db.name == "test_db"


def test_close(mongodb_connection):
    mongodb_connection.connect()
    mongodb_connection.close()
    assert mongodb_connection.client is None
    assert mongodb_connection.db is None


def test_reconnect(mongodb_connection):
    mongodb_connection.connect()
    assert mongodb_connection.client is not None
    assert mongodb_connection.db is not None
    mongodb_connection.close()
    assert mongodb_connection.client is None
    assert mongodb_connection.db is None
    mongodb_connection.connect()
    assert mongodb_connection.client is not None
    assert mongodb_connection.db is not None


def test_lookup_real():
    query = {"merged_text": {"$regex": "Dummy PDF file", "$options": "i"}}
    reader = MongoDBDataReader()
    result: list[dict[str, Any]] = reader.read_data(query)
    assert result
    assert reader.length() > 0


def test_write_force_real():
    w = MongoDBDataWriter().write_data({"test": {"v": "true"}}, force=True)
    assert w


def test_write_exists():
    w = MongoDBDataWriter().exists("test")
    assert w


def test_write_not_exists():
    w = MongoDBDataWriter().exists("test009009903")
    assert not w


def run_test():
    logger.info("begin pymongo testing")
    logger.info("end pymongo testing")


if __name__ == "__main__":
    pytest.main()
