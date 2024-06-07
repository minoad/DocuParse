#!./venv/bin/python

"""
Module Docstring
"""
import sys

from docuparse import logger
from docuparse.processors import FileDataDirectory


def main() -> int:
    """
    main thread

    Returns:
        0 int if good.  int > 0 if some error.
    """
    logger.debug("begin run")
    # n = FileDataDirectory("data/plats/CAP ROCK ESTATES")
    n = FileDataDirectory("data/plats/BLUFFS")
    n.process_files()
    return 0


if __name__ == "__main__":
    sys.exit(main())
