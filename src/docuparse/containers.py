import pathlib
from dataclasses import dataclass, field

from docuparse import logger
from docuparse.error_handlers import handle_file_exceptions
from docuparse.ocr import OCREngine
from docuparse.processors import FileProcessor, ImageProcessor, PDFProcessor

ocr = OCREngine()
DEFAULT_PROCESSORS: dict[str, FileProcessor | ImageProcessor] = {
    ".pdf": PDFProcessor(ocr),  # Instantiate PDFProcessor
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
    processors: dict[str, FileProcessor | ImageProcessor] = field(default_factory=dict)
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
        if not self.directory.is_dir():  # type: ignore
            raise ValueError(f"The path {self.directory} is not a valid directory.")

        for file_path in self.directory.iterdir():  # type: ignore
            if file_path.suffix.lower() in self.processors:
                processor = self.processors[file_path.suffix.lower()]
                try:
                    data = processor.process_file(file_path=file_path)
                except (OSError, RuntimeError, ValueError) as e:
                    handle_file_exceptions(e, str(file_path.resolve()))
                logger.info(data)
                self.data.extend(data)
