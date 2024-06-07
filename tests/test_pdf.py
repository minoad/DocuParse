from typing import Any

import pytest

from docuparse import config, logger
from docuparse.processors import PDFProcessor

test_cases: dict[str, dict[str, Any]] = {
    "invalid_path": {
        "function": lambda: config.ENVIRONMENT,
        "expected": "dev",
        "expected_exception": None,
    },
    "pdf_test_file": {
        "function": lambda: PDFProcessor().process_file("data/test/pdf/pdf_image_and_text.pdf")[
            "C:\\Users\\Micah\\repos\\DocuParse\\data\\test\\pdf\\pdf_image_and_text.pdf"
        ][1],
        "expected": "300 x 300",
        "expected_exception": None,
    },
}


@pytest.mark.parametrize("name, case", test_cases.items())
def test_pdfs(name, case):
    """
    Generic test cases
    """
    func = case["function"]

    # Handle cases where input might be missing or incorrect
    if case.get("expected_exception", None):
        with pytest.raises(case["expected_exception"]):
            result = func()
    else:
        result = func()
        logger.debug("%s == %s", result, case["expected"])
        assert result == case["expected"], f"Test {name} failed: expected {case['expected']} but got {result}"


if __name__ == "__main__":
    pytest.main()
