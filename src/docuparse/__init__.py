"""
Contains default stuff
"""

import logging
import os
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv


def get_logger(verbose: bool = False) -> logging.Logger:
    if verbose:
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s", level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S"
        )
    else:
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S"
        )
    # Create a logger object
    return logging.getLogger(__name__)


# Load environment variables from .env file
load_dotenv(dotenv_path="./conf/dev.env")


@dataclass
class Config:  # pylint: disable=too-many-instance-attributes
    """
    Config management for project
    Ignoring too-many-instance-attributes as this is a config object.
    """

    project_name: str = field(default_factory=lambda: os.getenv("PROJECT_NAME", ""))
    environment: str = field(default_factory=lambda: os.getenv("ENVIRONMENT", ""))
    pytesseract_executable: str = field(
        default_factory=lambda: os.getenv("PYTESSERACT_EXE", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    )

    mongo_server: str = field(default_factory=lambda: os.getenv("MONGO_SERVER", ""))
    mongo_database: str = field(default_factory=lambda: os.getenv("MONGO_DATABASE", ""))
    mongo_port: str = field(default_factory=lambda: os.getenv("MONGO_PORT", ""))
    mongo_user: str = field(default_factory=lambda: os.getenv("MONGO_USER", ""))
    mongo_password: str = field(default_factory=lambda: os.getenv("MONGO_PASSWORD", ""))
    mongo_collection: str = field(default_factory=lambda: os.getenv("MONGO_COLLECTION", ""))

    mongo_connection_string: str = field(init=False)

    def __post_init__(self):
        if self.mongo_user and self.mongo_password and self.mongo_server and self.mongo_port:
            self.mongo_connection_string = (
                f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_server}:{self.mongo_port}/"
            )
        else:
            self.mongo_uri = None


# Create an instance of the Config class
config = Config()
HOA_PROP_NAME = "Crystal Falls"
