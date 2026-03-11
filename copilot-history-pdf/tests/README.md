# Tests

Unit and integration tests for copilot-history-pdf package.

## Running Tests

### Run all tests:
```bash
python -m pytest tests/
```

Or using unittest:
```bash
python -m unittest discover tests/
```

### Run specific test file:
```bash
python -m pytest tests/test_parsers.py
```

### Run with coverage:
```bash
pip install pytest pytest-cov
python -m pytest --cov=copilot_history_pdf tests/
```

## Test Structure

- `test_parsers.py` - Tests for JSON parsing functions
- `test_api.py` - Tests for public API functions
- `test_utils.py` - Tests for utility functions
- `test_converter.py` - Integration tests for PDF conversion
- `fixtures/` - Test data files
  - `sample_chat.json` - Sample chat history for testing

## Test Coverage

The test suite covers:
- ✅ JSON parsing and text extraction
- ✅ Model ID extraction and formatting
- ✅ Text sanitization and replacements
- ✅ All 6 public API functions
- ✅ HTML escaping and timestamp formatting
- ✅ Text truncation
- ✅ PDF generation (basic and with config)
- ✅ Error handling (invalid files, out of range indices)
