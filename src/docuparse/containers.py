"""
Container objects.  Right now this is only a directory.
"""

import pathlib
from dataclasses import dataclass, field

from docuparse import get_logger
from docuparse.ocr import OCREngine
from docuparse.processors import FileProcessor, ImageProcessor, PDFProcessor
from docuparse.store import DataWriter, MongoDBDataWriter

logger = get_logger()
# from docuparse.error_handlers import handle_file_exceptions

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

    def files(self, force: bool) -> list[tuple[pathlib.Path, FileProcessor, DataWriter]]:
        """
        returns a list of strings of files to operate on.
        """

        files_with_processor_and_writer = []

        if not self.directory.is_dir():  # type: ignore
            raise ValueError(f"The path {self.directory} is not a valid directory.")

        for writer in self.writers:
            for file_path in self.directory.iterdir():  # type: ignore
                files_with_processor_and_writer.append(
                    (
                        file_path,
                        self.processors.get(file_path.suffix.lower(), False),
                        writer,
                        writer.exists(str(file_path)),
                    )
                )

        if force:  # return all that have a processor.
            return [i for i in files_with_processor_and_writer if i[1]]  # type: ignore
        return [i for i in files_with_processor_and_writer if i[1] and not i[2]]  # type: ignore

    def process_files(self, force: bool = False, dry_run: bool = False) -> None:
        """
        Process all files in the specified directory using the registered processors.

        Raises:
            ValueError: If the specified directory is not a valid directory.

        TODO: Check if file needs to be processes.
            for each writer, if not force and not exists, write.
        """
        files = self.files(force)

        if dry_run:
            for i in files:
                logger.info(f"would execute for {str(i[0])}")
            return None

        if not self.directory.is_dir():  # type: ignore
            raise ValueError(f"The path {self.directory} is not a valid directory.")

        for f in files:
            writer: DataWriter = f[2]
            file: pathlib.Path = f[0]
            processor: FileProcessor = f[1]
            writer.write_data({str(file): processor.process_file(file_path=file)}, force=force)

        return None
