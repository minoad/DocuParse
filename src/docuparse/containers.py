"""
Container objects.  Right now this is only a directory.
"""

import pathlib
from dataclasses import dataclass, field

from docuparse import logger

# from docuparse.error_handlers import handle_file_exceptions
from docuparse.ocr import OCREngine
from docuparse.processors import FileProcessor, ImageProcessor, PDFProcessor
from docuparse.store import DataWriter, MongoDBDataWriter

ocr = OCREngine()
DEFAULT_PROCESSORS: dict[str, FileProcessor | ImageProcessor] = {
    ".pdf": PDFProcessor(ocr),  # Instantiate PDFProcessor
    ".png": ImageProcessor(),  # Instantiate ImageProcessor
    ".jpeg": ImageProcessor(),  # Instantiate ImageProcessor
    ".jpg": ImageProcessor(),  # Instantiate ImageProcessor
    # Add other file processors here
}

DEFAULT_WRITERS = [
    MongoDBDataWriter(),
]


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
    writers: list[DataWriter] = field(default_factory=list)
    data: list[str] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.directory, str):
            self.directory = pathlib.Path(self.directory)

        for k, v in DEFAULT_PROCESSORS.items():
            self.register_processor(extension=k, processor=v)

        for writer in DEFAULT_WRITERS:
            self.register_writer(writer)

    def register_processor(self, extension: str, processor: FileProcessor | ImageProcessor):
        """
        Register a processor for a specific file extension.

        Args:
            extension (str): The file extension (e.g., '.pdf').
            processor (FileProcessor or ImageProcessor): The processor object.
        """
        self.processors[extension.lower()] = processor

    def register_writer(self, writer: DataWriter) -> None:
        """
        register the writers.
        """
        self.writers.append(writer)

    def process_files(self, force: bool = False):
        """
        Process all files in the specified directory using the registered processors.

        Raises:
            ValueError: If the specified directory is not a valid directory.

        TODO: Check if file needs to be processes.
            for each writer, if not force and not exists, write.
        """
        if not self.directory.is_dir():  # type: ignore
            raise ValueError(f"The path {self.directory} is not a valid directory.")

        processed_files = {}
        for file_path in self.directory.iterdir():  # type: ignore
            if file_path.suffix.lower() in self.processors:
                # what writers need to write.
                w: list[DataWriter] = []
                for writer in self.writers:
                    if not writer.exists(str(file_path)) or force:
                        logger.info(f"we are going to write {str(file_path)} for {writer}")
                        w.append(writer)
                    else:
                        logger.info(f"{str(file_path)} exists for {writer}.  Use force=True to force write.")

                logger.info(f"begin processing {file_path}")
                processor = self.processors[file_path.suffix.lower()]
                # try:
                if len(w) > 0:  # only process if we have somewhere to write
                    processed_files[str(file_path)] = processor.process_file(file_path=file_path)
                    for writer in w:
                        writer.write_data(data={str(file_path): processed_files[str(file_path)]}, force=True)
                # except (OSError, RuntimeError, ValueError) as e:
                #    handle_file_exceptions(e, str(file_path.resolve()))
                # self.data.extend(data)
            logger.info(f"completed file {str(file_path)}")
