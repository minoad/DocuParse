"""
Contains all of the ocr logic
"""

import pathlib
from typing import Any

import nltk
import pytesseract
from nltk.corpus import words
from PIL import Image, ImageOps
from textstat import flesch_reading_ease  # pylint: disable=no-name-in-module

from docuparse import config, get_logger

logger = get_logger()

nltk.download("words")


class OCREngine:
    """
    A class that represents an OCR (Optical Character Recognition) engine.

    The OCREngine class provides methods for performing OCR on images, calculating word confidence,
    calculating readability score, and evaluating the quality of OCR text based on English language assumptions.
    """

    def __init__(
        self,
        file_ref: str | pathlib.Path | Image.Image | None = None,
    ):
        """
        accept a file_ref that may or may not exist.
        If it exists, it can be a string, path, or Image data.
        If not None and string or pathlib.Path or Image.Image, load the image into the class.
        """
        self.image: Image.Image
        self.image_data: dict[str, Any]
        self.image_data = {"file_path": str(file_ref)}
        if config.pytesseract_executable:
            logger.info("Using pytesseract executable defined in config at %s", config.pytesseract_executable)
            pytesseract.pytesseract.tesseract_cmd = config.pytesseract_executable
        self._load_file(file_ref)
        # if self.image:
        #     self.perform_ocr()

    def _load_file(self, file_ref):
        if isinstance(file_ref, str):
            self.image = Image.open(pathlib.Path(file_ref))
        if isinstance(file_ref, pathlib.Path):
            self.image = Image.open(file_ref)
        if isinstance(file_ref, Image.Image):
            self.image = file_ref

    def get_image_filename(self):
        """
        Collect the image filename.
        """
        return getattr(self.image, "filename", "")

    def is_english_word(self, word):
        """Check if a word is an English word."""
        # TODO: Spacy can do this much faster
        # nlp = spacy.load("en_core_web_sm")
        # doc = nlp("I love coffee")
        # print(doc.vocab.strings["coffee"])  # 3197928453018144401
        # print(doc.vocab.strings[3197928453018144401])  # 'coffee'
        return word.lower() in words.words()

    def calculate_word_confidence(self, text, max_count: int = 0):
        """Calculate the percentage of valid English words in the text."""
        ocr_words: list[str] = [i for i in text.split() if i.isalnum()]

        if max_count:
            ocr_words = ocr_words[0 : min(max_count, len(ocr_words))]

        valid_words = [word for word in ocr_words if self.is_english_word(word)]
        # logger.info(valid_words)
        return len(valid_words) / len(ocr_words) if ocr_words else 0

    def readability_score(self, text):
        """Calculate the readability score of the text using Flesch reading ease."""
        reading_score = flesch_reading_ease(text)
        return reading_score

    def ocr_quality(self, text, max_count: int = 0):
        """
        Evaluate the quality of OCR text based on English language assumptions.

        Returns a dictionary with word confidence, character confidence, and readability score.
        """
        word_conf = self.calculate_word_confidence(text, max_count)
        # char_conf = calculate_character_confidence(text)
        readability = self.readability_score(text)

        quality = {
            "word_confidence": word_conf,
            #    'character_confidence': char_conf,
            "readability_score": readability,
        }
        self.image_data["ocr_quality"] = quality

        return quality

    def set_image_data(self) -> dict[str, Any]:
        """
        Get data about the image
        TODO: Can i get name?
        """
        data = {}
        try:
            osd = pytesseract.image_to_osd(self.image)
        except pytesseract.TesseractError as e:
            if "Too few characters" in str(e):
                try:
                    osd = pytesseract.image_to_osd(self.image, config="--psm 0 -c min_characters_to_try=5")
                except pytesseract.TesseractError as ex:
                    logger.error(f"Retry failed with error: {ex.__class__.__name__} - {str(ex)}")
                    return {}
            else:
                logger.error(f"Unexpected TesseractError: {e.__class__.__name__} - {str(e)}")
                osd = None

        osd_dict: dict[str, Any] = {
            i.split(": ")[0]: i.split(": ")[1] for i in osd.split("\n") if len(i.split(": ")) > 1
        }  # pylint: disable=C0301
        data = {
            # "page_num": osd_dict.get("Page number"),
            "rotation": int(osd_dict.get("Rotate", "0")),
            "rotation_to_zero": 360 - int(osd_dict.get("Rotate", "0")),
            "rotation_confidence": float(osd_dict.get("Orientation confidence", "0.0")),
            "script_language": osd_dict.get("Script"),
            "script_confidence": float(osd_dict.get("OrientationScript confidence", "0.0")),
            "format": self.image.format,
            "mode": self.image.mode,
            "filename": self.get_image_filename(),
            "info": self.image.info,
        }

        if self.image.getexif():  # self.image._exif:
            logger.error(f"image exif data: {self.image.getexif()}")
            # data.update(self.image.getexif())

        # logger.info(data)
        self.image_data = data
        return data

    def rotate_image(self, confidence: float = 0.0):
        """
        If we think the image should rotate, do so.
        """
        self.image_data["rotated_for_ocr"] = False
        if self.image_data["rotation"] != 0 and self.image_data["rotation_confidence"] < confidence:
            logger.info(
                f"rotation of {self.image_data["rotation"]} was detected but it confidence of {self.image_data["rotation_confidence"]} did not reach the required confidence of {confidence}"  # pylint: disable=C0301
            )  # pylint: disable=C0301

        if self.image_data["rotation"] != 0 and self.image_data["rotation_confidence"] >= confidence:
            logger.warning("rotating image")
            # self.image = self.image.rotate(angle=self.image_data["rotation"], expand=True)
            self.image = self.image.rotate(angle=self.image_data["rotation_to_zero"], expand=True)
            self.image_data["rotated_for_ocr"] = True

    def get_ocr_text(self):
        """
        Collect the ocr'ed check.
        """
        self.image_data["text"] = pytesseract.image_to_string(self.image).replace("\n", " ")

    def transform_image(self):
        """
        Transformations to apply

        # contrasted_image = ImageOps.autocontrast(image)
        # flipped_image = ImageOps.flip(image)
        # grayscale_image = ImageOps.grayscale(image)
        # inverted_image = ImageOps.invert(image)
        # posterized_image = ImageOps.posterize(image, bits=3)

        # # Display the original and transformed images
        # image.show(title="Original Image")
        # contrasted_image.show(title="Autocontrast Image")
        # flipped_image.show(title="Flipped Image")
        # grayscale_image.show(title="Grayscale Image")
        # inverted_image.show(title="Inverted Image")
        # posterized_image.show(title="Posterized Image")
        """
        self.image = ImageOps.autocontrast(self.image)
        self.image = ImageOps.posterize(self.image, bits=3)
        self.image = ImageOps.grayscale(self.image)

    def load_and_preprocess_image(self, correct_rotation=True):
        """
        Loads an image from the given path and optionally corrects its rotation.

        :param image_path: Path to the image file.
        :param correct_rotation: Whether to correct the rotation of the image.
        :return: A PIL Image object.

        if pymupdf.pixmap Image.open(io.BytesIO(image.tobytes()))
        """
        self.set_image_data()
        if correct_rotation:
            self.rotate_image()

        self.transform_image()
        # self.image_data["image"] = self.image

    def perform_ocr(self, image: str | pathlib.Path | Image.Image | None = None, file_name: str = "") -> dict[str, Any]:
        """
        Performs OCR on the given PIL Image object and returns the extracted text.
        If an image is provided, attempt to load it.

        :param image: A PIL Image object.
        :return: Extracted text as a string.
        """

        if image:
            self._load_file(image)
        self.load_and_preprocess_image()  # Attempts to correct any potential issues.
        self.get_ocr_text()
        self.ocr_quality(self.image_data["text"], 50)
        self.image_data["file_path"] = f"{file_name}_image_{self.image_data.get("page_num", 0)}"

        # logger.warning(f"{self.image_data}")
        return self.image_data  # ["text"]
