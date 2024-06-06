#!./venv/bin/python

"""
Module Docstring
"""
import sys

from docuparse import config, logger


def main() -> int:
    """
    main thread

    Returns:
        0 int if good.  int > 0 if some error.
    """
    logger.debug("begin run")
    logger.debug(config)
    print("testing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
