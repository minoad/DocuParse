#!./venv/bin/python

"""
Module Docstring
"""
import sys

from docuparse import logger
from docuparse.containers import FileDataDirectory

#  from pathlib import Path

#  from docuparse.ocr import OCREngine


def main() -> int:
    """
    main thread

    Returns:
        0 int if good.  int > 0 if some error.
    """
    logger.debug("begin run")
    # m = OCREngine()
    # m.perform_ocr("data/test/screenshots/47d68d48a450545f76f85cc34aee9da8c7f93798.jpeg")
    # n = FileDataDirectory("data/plats/CAP ROCK ESTATES")
    n = FileDataDirectory("data/test/pdf/")
    # n = FileDataDirectory("data/plats/GRAND MESA")
    # n = FileDataDirectory("data/plats/BLUFFS")
    # # n = FileDataDirectory("data/test/plats")
    # n = FileDataDirectory("data/plats/TOWNHOMES")
    n.process_files(force=True)
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
    sys.exit(main())


# def _process_image(self, image: pymupdf.Pixmap, file_name: str = "") -> dict[str, Any]:

#         try:
#             with Image.open(io.BytesIO()) as pil_image:
#                 if image.mode != "RGB":
#                     pil_image = pil_image.convert("RGB")
#                 # ocr_image = self.ocr_image(pil_image)
#                 image_text = self.ocr_engine.perform_ocr(pil_image, file_name)
#                 # image_text = re.sub(r"[^A-Za-z0-9]+", " ", ocr_image)
#         except (OSError, RuntimeError, ValueError, IOError, UnidentifiedImageError) as e:   # FzErrorArgument
#             if "unsupported colorspace for" in str(e):
#                 logger.error(f"{e}")
#                 return {}
#             logger.error(e)
#             return {}
#             # raise e

#         return image_text
