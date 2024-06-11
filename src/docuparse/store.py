"""
Storage protocols and concretes
"""

# from io import TextIOWrapper
from pathlib import Path
from typing import Any, Protocol

from pymongo import MongoClient

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

    def __init__(self, file_path):
        path = file_path
        if isinstance(path, str):
            path: Path = Path(file_path)

        self.file_path: Path = path
        self.file = path

    def write_data(self, data: dict[str, Any] | list[Any]) -> None:
        """
        Write file data
        """
        with open(self.file_path, "w", encoding="utf8") as f:
            f.write(str(data) + "\n")

    def close(self):
        """
        File closer
        """
        raise NotImplementedError

    def exists(self, uri: str) -> bool:
        """
        Check if a file exists
        """
        raise NotImplementedError

    # def close(self) -> None:
    #     self.file.close()


# class DatabaseDataWriter:
#     def __init__(self, connection_string: str):
#         self.connection_string = connection_string
#         self.connection = self._connect_to_database(connection_string)

#     def _connect_to_database(self, connection_string: str):
#         # Mock database connection
#         print(f"Connecting to database with {connection_string}")
#         return None

#     def write_data(self, data: Any) -> None:
#         # Mock writing data to the database
#         print(f"Writing data to database: {data}")

#     def close(self) -> None:
#         # Mock closing the database connection
#         print("Closing database connection")


class MongoDBDataWriter:
    """
    A class for writing data to a MongoDB collection.

    Args:
        connection_string (str): MongoDB connection string.
        database_name (str): The name of the database.
        collection_name (str): The name of the collection.
    """

    def __init__(
        self,
        connection_string: str = config.mongo_connection_string,
        database_name: str = config.mongo_database,
        collection_name: str = config.mongo_collection,
    ):
        """
        Initialize the MongoDBDataWriter.

        :param connection_string: MongoDB connection string.
        :param database_name: The name of the database.
        :param collection_name: The name of the collection.

        TODO:
            - Add a context manager.
        """
        self.connection_string = connection_string
        self.client: MongoClient = MongoClient(connection_string)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    def write_data(self, data: dict[str, Any], force: bool = False) -> bool:
        """
        Write data to the MongoDB collection.

        :param data: The data to write. Must be a dictionary where keys are IDs.
        """
        # im expecting a dict with a single key
        if len(list(data.keys())) != 1:
            logger.error(f"detected multiple keys in dict expecting one at {data.keys()}")
            raise ValueError

        key = list(data.keys())[0]
        value = data[key]
        value["_id"] = key

        if self.exists(key):  # if it exists
            if force:  # and we are forcing, replace
                logger.info(f"replacing {key} with force.")
                return self.collection.replace_one({"_id": key}, value).acknowledged

            logger.info(f"not writing {key}. Index exists.  Use force=True to replace.")
            return False

        # Base case, not forcing and index does not exist
        logger.info(f"writing {key} to mongo while not forcing.")
        return self.collection.insert_one(value).acknowledged

    def exists(self, uri: str) -> bool:
        """
        Check if a document with the given URI exists in the collection.

        Args:
            uri (str): The URI of the document to check.

        Returns:
            bool: True if a document with the given URI exists, False otherwise.
        """
        return bool(self.collection.find_one(str(uri)))

    def close(self) -> None:
        """
        Close the connection to MongoDB.
        """
        self.client.close()
