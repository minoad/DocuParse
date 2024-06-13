"""
Storage protocols and concretes
"""

# from io import TextIOWrapper
from pathlib import Path
from typing import Any, Protocol

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database as mongoDB
from pymongo.errors import (
    ConfigurationError,
    ConnectionFailure,
    InvalidURI,
    OperationFailure,
    ServerSelectionTimeoutError,
)

from docuparse import config, get_logger

logger = get_logger()


class DataWriter(Protocol):
    """
    Data writer. A protocol for anything that writes data.
    """

    def write_data(self, data: dict[str, Any] | list[Any], force: bool = False) -> None:
        """
        Write the provided data.

        :param data: The data to write.
        """

    def close(self) -> None:
        """
        Close the data writer, performing any necessary cleanup.
        """

    def exists(self, uri: str) -> bool:
        """
        Check if a uri exists
        """


class FileDataWriter:
    """
    Write out a file.
    """

    def __init__(self, file_path: str | Path):
        self.file_path: Path = Path(file_path) if isinstance(file_path, str) else file_path

    def write_data(self, data: dict[str, Any] | list[Any]) -> bool:
        """
        Write file data
        """
        try:
            with open(self.file_path, "w", encoding="utf8") as f:
                f.write(str(data) + "\n")
        except FileNotFoundError as e:
            logger.error(f"unable to write to {str(self.file_path)} with error {e}")
            raise e
        return True

    def close(self):
        """
        File closer
        """

    def exists(self, uri: str | None | Path = "") -> bool:
        """
        Check if a file exists.
        """
        p: Path = self.file_path if not uri else Path(uri)
        return p.exists()


class DataConnector(Protocol):
    """
    Connection interface for readers and writers that require connection first.
    """

    def connect(self) -> None:
        """
        Establish the connection
        """

    def close(self) -> None:
        """
        Close the connection
        """


class DataReader(Protocol):
    """
    Data reader
    """

    def __init__(self, connection: DataConnector):
        """Data reader protocol"""

    def read_data(self, query: dict[str, Any] | None = None) -> list[dict[str, Any]] | None:
        """Read data from the data source."""

    def length(self) -> int:
        """Returns the length of the read data"""


# Concretes


class MongoDBConnection:
    """
    Creates the mongo connection.
    connect to the db and collection.
        operate on db:                      self.connection.db
        operate on collection in the db:    self.connection.collection
    """

    def __init__(
        self,
        connection_string: str = config.mongo_connection_string,
        database_name: str = config.mongo_database,
        collection_name: str = config.mongo_collection,
    ):
        self.connection_string: str = connection_string
        self.collection_name: str = collection_name
        self.database_name: str = database_name
        self.client: MongoClient
        self.db: mongoDB[Any]
        self.connect()

    def connect(self) -> None:
        """Connect to the MongoDB server."""
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.database_name]
            self.collection: Collection[Any] = self.db[self.collection_name]
        except (ConfigurationError, ConnectionFailure, InvalidURI, ServerSelectionTimeoutError) as e:
            logger.error(f"failed to connect to {self.connection_string}")
            raise e

    def close(self) -> None:
        """Close the connection to the MongoDB server."""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None


class MongoDBDataReader:
    """
    A class for reading data from MongoDB collections.
    """

    def __init__(self, connection: MongoDBConnection = MongoDBConnection()):
        self.connection: MongoDBConnection = connection
        self.count: int

    def read_data(self, query: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """
        Read data from a specific collection.

        Args:
            query (dict[str, Any] | None): The query to filter the data. Defaults to None.

        Returns:
            list[dict[str, Any]]: The list of documents matching the query.
        """
        if not query:
            query = {}
        if self.connection.db is None:
            raise ConnectionFailure("Not connected to any database. Call connect() first.")

        try:
            results = list(self.connection.collection.find(query))
            self.count = len(results)
            return results
        except OperationFailure as e:
            logger.error(f"failed read operation on mongo {self.connection} with {e}")
            raise e

    def length(self) -> int:
        """
        Returns the length of the latest read operation.
        """
        return self.count if self.count else 0

    def close(self) -> None:
        """
        Close the connection to the MongoDB server.
        """
        if self.connection:
            self.connection.close()


class MongoDBDataWriter:
    """
    A class for writing data to a MongoDB collection.
    """

    def __init__(self, connection: MongoDBConnection = MongoDBConnection()):
        self.connection = connection

    def write_data(self, data: dict[str, dict[str, Any]], force: bool = False) -> bool:
        """
        Write data to the MongoDB collection.
            data: value must be a dict of dict[str, dict[str, Any]]
            ex: {"test": {"v": "true"}}
                "test" is the index, test.value is what is getting written to the db.
        """
        # TODO: If we get more than 1 key, do the write multiple.
        if len(list(data.keys())) != 1:
            logger.error(f"detected multiple keys in dict expecting one at {data.keys()}")
            raise ValueError

        key = list(data.keys())[0]
        value: dict = data[key]
        value["_id"] = key

        try:
            # collection = self.connection.collection
            if self.exists(key):
                if force:
                    logger.info(f"Replacing {key} with force.")
                    result = self.connection.collection.replace_one({"_id": key}, value)
                    return result.acknowledged
                logger.info(f"Not writing {key}. Index exists. Use force=True to replace.")
                return False
            logger.info(f"Writing {key} to MongoDB while not forcing.")
            result = self.connection.collection.insert_one(value)
            return result.acknowledged
        except OperationFailure as e:
            logger.error(f"Failed write operation on MongoDB: {e}")
            raise e

    def exists(self, uri: str) -> bool:
        """
        Check if a document with the given URI exists in the collection.

        Args:
            uri (str): The URI of the document to check.

        Returns:
            bool: True if a document with the given URI exists, False otherwise.
        """
        return bool(self.connection.collection.find_one(str(uri)))

    def close(self) -> None:
        """
        Close the connection to MongoDB.
        """
        self.connection.close()
