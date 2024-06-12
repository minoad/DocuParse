# DocuParse

DocuParse is a powerful document parsing and analysis tool built with Python. It leverages several complex Python subjects and libraries to provide robust document processing capabilities. This project is designed to be flexible, efficient, and easy to use.

## Features

- **Document Parsing**: Efficiently parse various document formats.
- **Text Analysis**: Perform text analysis using natural language processing techniques.
- **Customizable Pipelines**: Create and customize processing pipelines to suit specific needs.
- **Logging**: Comprehensive logging to monitor and debug the processing.

## TODO

1. Unit tests
1. Add coverage requirements to pre-commit.
1. Add image file processor.
1. Add searching to the cli.  Likely will need to seperate the click groups out into their own files.
1. NLTK to the cli.

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

## Mongodb

### Simple Shell testing

```shell
const regex = /(?:\w+\W+){0,5}\w*declarant\w*(?:\W+\w+){0,5}/i;
const regex = /(?:\w+\W+){0,10}\w*drain\w*(?:\W+\w+){0,10}/i;
const regex = /(?:\w+\W+){0,5}\w*pay\w*(?:\W+\w+){0,5}/i;

const cursor = db.test_col.aggregate([
    {
        $match: { merged_text: { $regex: "17.9060", $options: "i" } }
    },
    {
        $project: { _id: 1, merged_text: 1 }
    }
]);

while (cursor.hasNext()) {
    const doc = cursor.next();
    const matches = doc.merged_text.match(regex);
    if (matches) {
        print(`_id: ${doc._id}, context: ${matches}`);
    }
};
```

## Windows download sample data

```powershell
$source = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
$destination = "sample.pdf"

Invoke-WebRequest -Uri $source -OutFile $destination

Write-Host "Sample PDF downloaded successfully to $destination."
# Invoke-WebRequest -Uri https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf -Outfile data\test\
# Invoke-WebRequest -Uri https://file-examples-com.github.io/uploads/2017/10/file-sample_150kB.pdf -Outfile data\test\
```
