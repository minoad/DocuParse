#!./venv/bin/python

"""
Module Docstring
"""
import sys

from docuparse import logger
from docuparse.containers import FileDataDirectory
from docuparse.ocr import OCREngine


def main() -> int:
    """
    main thread

    Returns:
        0 int if good.  int > 0 if some error.
    """
    logger.debug("begin run")
    m = OCREngine()
    m.perform_ocr("data/test/screenshots/47d68d48a450545f76f85cc34aee9da8c7f93798.jpeg")
    # n = FileDataDirectory("data/plats/CAP ROCK ESTATES")
    n = FileDataDirectory("data/plats/GRAND MESA")
    n.process_files()
    # n = FileDataDirectory("data/plats/BLUFFS")
    # n.process_files()

    # l = OCREngine().perform_ocr("data/test/screenshots/47d68d48a450545f76f85cc34aee9da8c7f93798.jpeg")
    # n = FileDataDirectory("data/test/pdf/")
    # n = n.process_files()
    # m = OCREngine("data/test/screenshots/47d68d48a450545f76f85cc34aee9da8c7f93798.jpeg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
