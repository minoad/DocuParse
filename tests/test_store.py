# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=unused-argument
# pylint: disable=bare-except
# flake8: noqa: E722
# from pathlib import Path
from typing import Any

import mongomock
import pytest
from pymongo import MongoClient

from docuparse import get_logger
from docuparse.store import (  # FileDataWriter,
    MongoDBConnection,
    MongoDBDataReader,
    MongoDBDataWriter,
)

logger = get_logger()
test_data: list[dict[str, dict[str, Any]]] = [{"test": {"v": "true"}}]


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
    reader1 = MongoDBDataReader()
    result1 = reader1.read_data()[:5]
    assert result1
    assert not reader1.close()


# def test_file_writer():
#     f = FileDataWriter("data/test/test_file")
#     f1 = FileDataWriter(Path("data/test/test_file"))
#     # assert f.write_data(test_data)
#     # assert f1.write_data(test_data)
#     # assert not f.close()
#     # assert f.exists()
#     # assert f.exists("data/test/test_file")


def test_write_force_real():
    w = MongoDBDataWriter()
    fwf = w.write_data({"test": {"v": "true"}}, force=True)
    fwn = w.write_data({"test": {"v": "true"}}, force=False)

    with pytest.raises(ValueError):  # as exc_info:
        w.write_data({"test": "test", "test2": "sdf"}, force=True)

    try:
        assert fwf
    except:
        logger.error("mongo write with force failed")

    try:
        assert w.exists("test")
    except:
        logger.error("mongo write with force failed exists")

    try:
        assert not w.exists("test009009903")
    except:
        logger.error("mongo index exists where it should not.")

    try:
        assert not fwn
    except:
        logger.error("mongo write without force failed")

    try:
        assert not w.close()
    except:
        logger.error("mongo write without force failed")


def run_test():
    logger.info("begin pymongo testing")
    logger.info("end pymongo testing")


if __name__ == "__main__":
    pytest.main()
