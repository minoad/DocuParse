import pathlib
from typing import Any, Dict, Protocol

import pymupdf
import pytesseract
from PIL import Image


class FileProcessor(Protocol):  # pylint: disable=too-few-public-methods
    """
    Protocol for file processors.
    """

    def process(self, file_path: pathlib.Path) -> Dict[str, Any]:
        """Process the file and return the extracted data."""
        raise NotImplementedError


class OCRProcessor(Protocol):  # pylint: disable=too-few-public-methods
    """
    Protocol for OCR processors.
    """

    def ocr_image(self, image_path: pathlib.Path) -> str:
        """Perform OCR on the given image and return the extracted text."""
        raise NotImplementedError


class PDFProcessor:  # pylint: disable=too-few-public-methods
    """
    pdf processor
    """

    def process(self, file_path: pathlib.Path) -> Dict[str, Any]:
        """
        Process the PDF file and return the extracted text and images.
        """
        doc = pymupdf.open(file_path)
        text = ""
        return {str(doc): text}
        # for page in doc:
        #     text += page.get_text()
        # images = [img for img in doc.get_images(full=True)]
        # return {"text": text, "images": images}


class ImageProcessor:  # pylint: disable=too-few-public-methods
    """
    pdf processor
    """

    def ocr_image(self, image_path: pathlib.Path) -> str:
        """
        run ocr on the image
        """
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text

    def process(self, file_path: pathlib.Path) -> Dict[str, Any]:
        """
        process the image
        """
        text = self.ocr_image(file_path)
        return {"text": text}
