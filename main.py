#!./venv/bin/python

"""
Module Docstring
"""
import sys

import click

from docuparse import get_logger
from docuparse.containers import FileDataDirectory


def _execute(directory: str, force: bool):
    FileDataDirectory(directory).process_files(force=bool(force))


@click.group()
def docuparse():
    """A simple command-line interface using click."""


@click.command()
@click.option("--force", is_flag=True, help="Force data overwrite.")
@click.option("--verbose", is_flag=True, help="Enable verbose mode.")
@click.argument("directory", default="data/test/pdf/")
def test(directory: str, force: bool, verbose: bool):
    """
    Runs collection against a small test dataset.
    """
    logger = get_logger(verbose)
    logger.info("beginning test run.")
    click.echo("begging collection of test")
    _execute(directory=directory, force=force)


@click.command()
@click.option("--force", is_flag=True, help="Force data overwrite.")
@click.option("--verbose", is_flag=True, help="Enable verbose mode.")
@click.option("--dry-run", is_flag=True, help="Enable verbose mode.")
@click.argument("directory", default="data/test/pdf/")
def run(directory: str, force: bool, verbose: bool, dry_run):
    """
    Runs collection against a small test dataset.
    """
    logger = get_logger(verbose)
    click.echo("begging collection of test")
    logger.info("beginning run.")
    FileDataDirectory(directory).process_files(force=bool(force), dry_run=dry_run)


docuparse.add_command(test)
docuparse.add_command(run)


def main() -> int:
    """
    main thread

    Returns:
        0 int if good.  int > 0 if some error.
    """

    # logger.debug("begin run")
    # m = OCREngine()
    # m.perform_ocr("data/test/screenshots/47d68d48a450545f76f85cc34aee9da8c7f93798.jpeg")
    # n = FileDataDirectory("data/plats/CAP ROCK ESTATES")

    # n = FileDataDirectory("data/plats/GRAND MESA")
    # n = FileDataDirectory("data/plats/BLUFFS")
    # # n = FileDataDirectory("data/test/plats")
    # n = FileDataDirectory("data/plats/TOWNHOMES")

    # n.process_files()

    # l = OCREngine().perform_ocr("data/test/screenshots/47d68d48a450545f76f85cc34aee9da8c7f93798.jpeg")
    # n = FileDataDirectory("data/test/pdf/")
    # n = n.process_files()
    # m = OCREngine("data/test/screenshots/47d68d48a450545f76f85cc34aee9da8c7f93798.jpeg")

    # for dir in Path("data/plats").iterdir():
    #     n = FileDataDirectory(dir)
    #     n.process_files()
    return 0


if __name__ == "__main__":
    sys.exit(docuparse())
