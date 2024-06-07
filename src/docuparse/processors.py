import io
import pathlib
import re
from typing import Any, Dict, Protocol

import pymupdf
import pytesseract
from PIL import Image

from docuparse import logger
from docuparse.error_handlers import handle_file_exceptions, handle_pdf_exceptions


class FileProcessor(Protocol):  # pylint: disable=too-few-public-methods
    """
    Protocol for file processors.
    There will be one of these for each of the potential file types.
    """

    def process(self, file_path: pathlib.Path | str) -> Dict[str, Any]:
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
    """

    def process(self, file_path: pathlib.Path | str) -> Dict[str, Any]:
        """
        Process the PDF file and return the extracted text and images.
        Get text and images from the pdf.
        add the texts to the dictionary
        ocr the images and add the returned text to the dictionary
        return the dictionary
        """
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)

        try:
            doc = pymupdf.open(file_path)
        except OSError as e:
            handle_file_exceptions(e, str(file_path))

        text_dat = []
        try:
            for page in doc:
                text_dat.append(page.get_text())
                for image in page.get_images():
                    pix = pymupdf.Pixmap(doc, image[0])
                    pil_image: Image.Image = Image.open(io.BytesIO(pix.tobytes()))
                    if pil_image.mode != "RGB":
                        pil_image = pil_image.convert("RGB")
                    text_dat.append(self.ocr_image(pil_image))
        except (OSError, RuntimeError, ValueError) as e:
            handle_pdf_exceptions(e)

        logger.debug(f"{file_path} has {len(text_dat)} instances of extracted text.")

        return {"text_data": text_dat}

    def ocr_image(self, image_dat: pathlib.Path | str | Image.Image) -> str:
        """
        run ocr on the image

        Set the cmd line.
        Detect the type passed in and process.

        If angle does not appear to be 0, rotate the image.
        """
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if isinstance(image_dat, (str, pathlib.Path)):
            image_dat = Image.open(image_dat)
        osd = pytesseract.image_to_osd(image_dat, config="--psm 0 -c min_characters_to_try=5")
        rotation_match = re.search(r"(?<=Rotate: )\d+", osd)
        if rotation_match:
            angle = int(rotation_match.group(0))
            if angle != 0:
                logger.warning(f"Image detecting a rotation of {angle}")
                image_dat = image_dat.rotate(angle, expand=True)

        text = pytesseract.image_to_string(image_dat).strip()
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

    def process(self, file_path: pathlib.Path | str) -> Dict[str, Any]:
        """
        process the image
        """
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)
        text = self.ocr_image(file_path)
        return {"text": text}
