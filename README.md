# DocuParse

DocuParse is a powerful document parsing and analysis tool built with Python. It leverages several complex Python subjects and libraries to provide robust document processing capabilities. This project is designed to be flexible, efficient, and easy to use.

## Features

- **Document Parsing**: Efficiently parse various document formats.
- **Text Analysis**: Perform text analysis using natural language processing techniques.
- **Customizable Pipelines**: Create and customize processing pipelines to suit specific needs.
- **Logging**: Comprehensive logging to monitor and debug the processing.

## Installation

To install DocuParse, clone the repository and install the required dependencies:

```bash
git clone https://github.com/minoad/DocuParse.git
cd DocuParse
python -m pip venv .venv
source .venv/bin/activate
python -m pip install -e .[all]

cd infrastructure/mongodb
docker-compose up -d

# Create a configuration file
cat << EOF > conf/dev.env
PROJECT_NAME=
ENVIRONMENT=
PYTESSERACT_EXE=
MONGO_SERVER=
MONGO_PORT=
MONGO_DATABASE=
MONGO_USER=
MONGO_PASSWORD=
MONGO_COLLECTION=
EOF

```

## Usage

### Python

Here’s a simple example of how to use DocuParse:

```python
from docuparse import DocumentProcessor

# Initialize the processor
processor = DocumentProcessor()

# Process a document
result = processor.process('path/to/documents')

# Print the result
print(result)
```

### Command Line Interface

DocuParse also provides a command-line interface for ease of use. Below is an example:

```bash
python -m docuparse --input path/to/document --output path/to/output
```

### CLI Options

- `--input`: Path to the input document.
- `--output`: Path to the output file.
- `--dry-run`: Run the process without making any changes.
