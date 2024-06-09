"""
Contains default stuff
"""

import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv

logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")

# Create a logger object
logger = logging.getLogger(__name__)


# Load environment variables from .env file
load_dotenv(dotenv_path="./conf/dev.env")


@dataclass()
class Config:
    """
    Config management for project
    """

    project_name: str | None = os.getenv("PROJECT_NAME")
    environment: str | None = os.getenv("ENVIRONMENT")
    pytesseract_executable: str | None = os.getenv("pytesseract_exe", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    mongo_db_config: str | None = os.getenv("mongo_db_config", '{"server": "server_name.db"}')


# Create an instance of the Config class
config = Config()
HOA_PROP_NAME = "Crystal Falls"
