import io
import pathlib
import re
from dataclasses import dataclass, field
from typing import Any, Dict, Protocol

import pymupdf
import pytesseract
from PIL import Image

from docuparse import logger
from docuparse.error_handlers import handle_file_exceptions


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

    def __init__(self):
        self.text: dict[str, list[str]] = {}

    def _process_image(self, image: pymupdf.Pixmap) -> str:
        text = []

        try:
            with Image.open(io.BytesIO(image.tobytes())) as pil_image:
                if pil_image.mode != "RGB":
                    pil_image = pil_image.convert("RGB")
                ocr_image = self.ocr_image(pil_image)
                image_text = re.sub(r"[^A-Za-z0-9]+", " ", ocr_image)
                text.append(image_text)
        except (OSError, RuntimeError, ValueError) as e:
            logger.error(e)
            raise e
        return " ".join(text)

    def _process_page(self, page: pymupdf.Page, doc: pymupdf.Document) -> list[str]:
        """
        Given a page:
            text = []
            construct a list of page.get_text()
            for each image in page, ocr and append to text
        """
        text = []
        text.append(page.get_text())
        for image in page.get_images():
            try:
                image_text = self._process_image(pymupdf.Pixmap(doc, image[0]))
                text.append(image_text)
            except (OSError, RuntimeError, ValueError) as e:
                logger.error(e)
                raise e
        return text

    def process_file(self, file_path: pathlib.Path | str) -> Dict[str, Any]:
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
            with pymupdf.open(file_path) as doc:  # opened file
                for page in doc:
                    page_text = self._process_page(page, doc)
                    text_dat.extend(page_text)
        except (OSError, RuntimeError, ValueError) as e:
            handle_file_exceptions(e, str(file_path.resolve()))

        logger.info(f"{file_path} has {len(text_dat)} instances of extracted text.")
        self.text = {str(file_path.resolve()): text_dat}
        return self.text

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

        try:
            osd = pytesseract.image_to_osd(image_dat)
        except pytesseract.TesseractError as e:
            if "Too few characters" in str(e):
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

    def process_file(self, file_path: pathlib.Path | str) -> Dict[str, Any]:
        """
        process the image
        """
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)
        text = self.ocr_image(file_path)
        return {"text": text}


DEFAULT_PROCESSORS: Dict[str, FileProcessor] = {
    ".pdf": PDFProcessor(),  # Instantiate PDFProcessor
    ".png": ImageProcessor(),  # Instantiate ImageProcessor
    ".jpeg": ImageProcessor(),  # Instantiate ImageProcessor
    ".jpg": ImageProcessor(),  # Instantiate ImageProcessor
    # Add other file processors here
}


@dataclass()
class FileDataDirectory:  # pylint: disable=too-few-public-methods
    """
    Represents a directory containing files to be processed.

    Args:
        directory (str): The path to the directory.
        db_uri (str): The URI of the database.

    Attributes:
        directory (Path): The path to the directory.
        processors (dict): A dictionary mapping file extensions to processor objects.

    """

    directory: str | pathlib.Path
    processors: Dict[str, FileProcessor | ImageProcessor] = field(default_factory=dict)
    data: list[str] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.directory, str):
            self.directory = pathlib.Path(self.directory)

        for k, v in DEFAULT_PROCESSORS.items():
            self.register_processor(extension=k, processor=v)

    def register_processor(self, extension: str, processor: FileProcessor | ImageProcessor):
        """
        Register a processor for a specific file extension.

        Args:
            extension (str): The file extension (e.g., '.pdf').
            processor (FileProcessor or ImageProcessor): The processor object.
        """
        self.processors[extension.lower()] = processor

    def process_files(self):
        """
        Process all files in the specified directory using the registered processors.

        Raises:
            ValueError: If the specified directory is not a valid directory.
        """
        if not self.directory.is_dir():
            raise ValueError(f"The path {self.directory} is not a valid directory.")

        for file_path in self.directory.iterdir():
            if file_path.suffix.lower() in self.processors:
                processor = self.processors[file_path.suffix.lower()]
                data = processor.process_file(file_path=file_path)
                logger.info(data)
                self.data.append(data)
