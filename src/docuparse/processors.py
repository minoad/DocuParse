import io
import pathlib
from typing import Any, Dict, Protocol

import pymupdf
import pytesseract
from PIL import Image

from docuparse import logger


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
        doc = pymupdf.open(file_path)

        text_dat = []
        for page in doc:
            text_dat.append(page.get_text())
            for image in page.get_images():
                pix = pymupdf.Pixmap(doc, image[0])
                pil_image: Image.Image = Image.open(io.BytesIO(pix.tobytes()))
                if pil_image.mode != "RGB":
                    pil_image = pil_image.convert("RGB")
                text_dat.append(self.ocr_image(pil_image))

        logger.debug(f"{file_path} has {len(text_dat)} instances of extracted text.")

        return {"text_data": text_dat}

    def ocr_image(self, image_dat: pathlib.Path | str | Image.Image) -> str:
        """
        run ocr on the image
        """
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if isinstance(image_dat, (str, pathlib.Path)):
            image_dat = Image.open(image_dat)
        # TODO: do some rotations or other enhancements to improve results.
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


# from typing import Dict, Any
# import pathlib
# import fitz  # PyMuPDF
# from PIL import Image
# import pytesseract

# class PDFProcessor:
#     def process(self, file_path: pathlib.Path) -> Dict[str, Any]:
#         doc = fitz.open(file_path)
#         text = ""
#         for page in doc:
#             text += page.get_text()
#         images = [img for img in doc.get_images(full=True)]
#         return {"text": text, "images": images}

# class ImageProcessor:
#     def ocr_image(self, image_path: pathlib.Path) -> str:
#         image = Image.open(image_path)
#         text = pytesseract.image_to_string(image)
#         return text

#     def process(self, file_path: pathlib.Path) -> Dict[str, Any]:
#         text = self.ocr_image(file_path)
#         return {"text": text}
