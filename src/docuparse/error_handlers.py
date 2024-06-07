from typing import NoReturn

import pymupdf

from docuparse import logger


def handle_file_exceptions(e: Exception, path: str = "") -> NoReturn:
    """
    Handle exceptions for file operations.

    Args:
        e (Exception): The exception to handle.
    """
    if isinstance(e, FileNotFoundError):
        logger.error("FileNotFoundError: The file %s does not exist. %s", path, e)
    elif isinstance(e, PermissionError):
        logger.error("PermissionError: Permission denied to access the file %s: %s", path, e)
    elif isinstance(e, IsADirectoryError):
        logger.error("IsADirectoryError: %s is a directory, not a file. %s", path, e)
    elif isinstance(e, IOError):
        logger.error("IOError: An I/O error occurred while accessing the file %s: %s", path, e)
    else:
        logger.error("An unexpected error occurred: %s", e)
    raise e


def handle_pdf_exceptions(e: Exception, path: str = "") -> NoReturn:
    """
    Handle exceptions for pymupdf-specific exceptions.

    Args:
        e (Exception): The exception to handle.
        path (str): The path of the file being processed.
    """
    if isinstance(e, pymupdf.FileDataError):
        logger.error("FileDataError: The file %s is corrupted or not a valid PDF. %s", path, e)
    elif isinstance(e, RuntimeError):
        logger.error("RuntimeError: A runtime error occurred while processing the file %s: %s", path, e)
    elif isinstance(e, ValueError):
        logger.error("ValueError: A value error occurred while processing the file %s: %s", path, e)
    else:
        logger.error("An unexpected error occurred: %s", e)
    raise e
