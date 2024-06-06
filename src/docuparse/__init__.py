"""
Contains default stuff
"""

import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv

logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S")

# Create a logger object
logger = logging.getLogger(__name__)


# Load environment variables from .env file
load_dotenv(dotenv_path="./conf/dev.env")


@dataclass()
class Config:
    """
    Config management for project
    """

    PROJECT_NAME: str | None = os.getenv("PROJECT_NAME")
    ENVIRONMENT: str | None = os.getenv("ENVIRONMENT")


# Create an instance of the Config class
config = Config()
HOA_PROP_NAME = "Crystal Falls"
