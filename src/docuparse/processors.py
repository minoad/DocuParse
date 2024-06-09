"""
This module contains classes and protocols for file processing and OCR (Optical Character Recognition).

Classes:
- OCREngine: Provides functionality for performing OCR on images.
- FileProcessor: Protocol for file processors.
- OCRProcessor: Protocol for OCR processors.
- PDFProcessor: File processor for PDF files.
- ImageProcessor: File processor for images.
- FileDataDirectory: Represents a directory containing files to be processed.

Protocols:
- FileProcessor: Protocol for file processors.
- OCRProcessor: Protocol for OCR processors.

"""

# Rest of the code...
import io
import pathlib
import re
from typing import Any, Dict, Protocol

import pymupdf
import pytesseract
from PIL import Image

from docuparse import logger
from docuparse.error_handlers import handle_file_exceptions
from docuparse.ocr import OCREngine

# TODO: Move this to its own file.


class FileProcessor(Protocol):  # pylint: disable=too-few-public-methods
    """
    Protocol for file processors.
    There will be one of these for each of the potential file types.
    """

    def process_file(self, file_path: pathlib.Path | str) -> Dict[str, Any]:
        """Process the file and return the extracted data."""
        raise NotImplementedError


class OCRProcessor(Protocol):  # pylint: disable=too-few-public-methods
    """
    Protocol for OCR processors.
    OCR Process.  Extracts text from images.
    We can accept a string, a path, or a file-like object.
    """

    def ocr_image(self, image: pathlib.Path | str | Image.Image) -> str:
        """Perform OCR on the given image and return the extracted text."""
        raise NotImplementedError


class PDFProcessor:  # pylint: disable=too-few-public-methods
    """
    File processor for pdf's.
    process_file for pages -> process_page for text | images -> process_images for text
    """

    def __init__(self, ocr_engine: OCREngine):
        self.text: dict[str, list[str]] = {}
        self.ocr_engine = ocr_engine

    def _process_image(self, image: pymupdf.Pixmap, file_name: str = "") -> str:
        try:
            with Image.open(io.BytesIO(image.tobytes())) as pil_image:
                if pil_image.mode != "RGB":
                    pil_image = pil_image.convert("RGB")
                # ocr_image = self.ocr_image(pil_image)
                ocr_image = self.ocr_engine.perform_ocr(pil_image, file_name)
                image_text = re.sub(r"[^A-Za-z0-9]+", " ", ocr_image)
        except (OSError, RuntimeError, ValueError) as e:
            if "unsupported colorspace for" in str(e):
                logger.error(f"{e}")
                return ""
            logger.error(e)
            raise e

        return image_text

    def _process_page(self, page: pymupdf.Page, doc: pymupdf.Document, file_name: str = "") -> list[str]:
        """
        Given a page:
            text = []
            construct a list of page.get_text()
            for each image in page, ocr and append to text
        """
        text = []
        text.append(page.get_text())  # type: ignore
        for image in page.get_images():
            try:
                image_text = self._process_image(pymupdf.Pixmap(doc, image[0]), file_name)
                text.append(image_text)
            except (OSError, RuntimeError, ValueError) as e:
                logger.error(e)
                raise e
        return text

    def process_file(self, file_path: pathlib.Path | str) -> dict[str, list[str]]:
        """
        Process the PDF file and return the extracted text and images.
        Get text and images from the pdf.
        add the texts to the dictionary
        ocr the images and add the returned text to the dictionary
        return the dictionary
        """
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)

        text_dat = []
        try:
            with pymupdf.open(file_path) as doc:
                for page in doc:
                    page_text = self._process_page(page, doc, str(file_path))  # type: ignore
                    text_dat.extend(page_text)
        except (OSError, RuntimeError, ValueError) as e:
            handle_file_exceptions(e, str(file_path.resolve()))

        logger.info(f"{file_path} has {len(text_dat)} instances of extracted text.")
        text = {str(file_path.resolve()): text_dat}
        self.text = text
        return text


class ImageProcessor:  # pylint: disable=too-few-public-methods
    """
    file processor for images.
    Includes the ocr processor.
    """

    def ocr_image(self, image: pathlib.Path | str | Image.Image) -> str:
        """
        run ocr on the image
        """
        img = Image.open(image)
        text = pytesseract.image_to_string(img)
        return text

    def process_file(self, file_path: pathlib.Path | str) -> Dict[str, Any]:
        """
        process the image
        """
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)
        text = self.ocr_image(file_path)
        return {"text": text}
