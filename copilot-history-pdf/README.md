# Copilot Chat History to PDF Converter

A Python package to convert GitHub Copilot chat history JSON files into formatted PDF documents. Perfect for students submitting chat logs for assignments or instructors analyzing student interactions with AI coding assistants.

## Why This Package?

This package was created to solve a real problem: **universities requiring PDF submissions of GitHub Copilot chat histories, but VS Code only exports chats as JSON files.**

Yesterday, my friend struggled to share his GitHub Copilot chat history reliably in VS Code for a university assignment. Our university requires PDF output of all chat input prompts and outputs for academic integrity and assessment purposes. Since Copilot only exports chat histories in JSON format, there was no straightforward way to convert them to the required PDF format. This package bridges that gap, making it easy for students to meet submission requirements while instructors can review AI-assisted work in a readable format.

## Features

- 🎨 **Beautifully Formatted PDFs** - Color-coded user/assistant messages with timestamps
- 🤖 **Model Tracking** - Displays which AI model was used for each exchange
- 🔧 **Customizable** - Text replacements, custom titles, page sizes, and more
- 📊 **Programmatic API** - Extract and analyze chat data in your own Python scripts
- 🚀 **Easy to Use** - Simple CLI for quick conversions

## Installation

### For Students (Simple Usage)

```bash
pip install copilot-history-pdf
```

### For Development

```bash
git clone https://github.com/Oliver1811/copilot-history-pdf.git
cd copilot-history-pdf
pip install -e .
```

## Quick Start

### Command Line Usage

Convert a chat history JSON file to PDF:

```bash
copilot-to-pdf chat_history.json
```

With custom output path:

```bash
copilot-to-pdf chat_history.json -o my_submission.pdf
```

With custom title:

```bash
copilot-to-pdf chat_history.json --title "Assignment 1 - Student Name"
```

### Python API Usage

Extract and analyze chat data programmatically:

```python
import copilot_history_pdf

# Get all exchanges
exchanges = copilot_history_pdf.get_all_exchanges("chat_history.json")

# Print summary
for ex in exchanges:
    print(f"Exchange {ex['exchange_number']}: {ex['model_id']}")
    print(f"Q: {ex['user_message'][:100]}...")
    print(f"A: {ex['assistant_response'][:100]}...")
    print()

# Get metadata
meta = copilot_history_pdf.get_chat_metadata("chat_history.json")
print(f"Total exchanges: {meta['total_exchanges']}")
print(f"Models used: {', '.join(meta['model_ids'])}")
```

## CLI Options

```
usage: copilot-to-pdf [-h] [-o OUTPUT] [--title TITLE] 
                      [--max-response-length MAX_RESPONSE_LENGTH]
                      [--replacements REPLACEMENTS] [--no-timestamps]
                      [--page-size PAGE_SIZE] [-v]
                      input

Convert GitHub Copilot chat history JSON to PDF

positional arguments:
  input                 Path to the input JSON file

optional arguments:
  -h, --help            Show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output PDF file path (default: chat_history.pdf)
  --title TITLE         Custom title for the PDF document
  --max-response-length MAX_RESPONSE_LENGTH
                        Maximum length for responses (default: 5000)
  --replacements REPLACEMENTS
                        JSON file with text replacements
  --no-timestamps       Omit timestamps from the PDF
  --page-size PAGE_SIZE
                        Page size: letter or a4 (default: letter)
  -v, --version         Show program version
```

## Examples

### Text Replacements

Anonymize or replace text in the output:

Create a `replacements.json` file:
```json
{
  "oliver": "student",
  "Oliver": "Student",
  "my-email@example.com": "[redacted]"
}
```

Then run:
```bash
copilot-to-pdf chat.json --replacements replacements.json
```

### Custom PDF Generation

```bash
copilot-to-pdf chat.json \
  -o "Assignment1_JohnDoe.pdf" \
  --title "CS101 Assignment 1 - John Doe" \
  --page-size a4 \
  --no-timestamps
```

## Python API Reference

### Data Extraction Functions

#### `get_all_exchanges(json_path)`
Returns list of all exchanges with user messages, assistant responses, timestamps, and model IDs.

#### `get_exchange_by_index(json_path, idx)`
Get a specific exchange by index (0-indexed).

#### `get_user_messages(json_path)`
Returns list of all user message strings.

#### `get_assistant_responses(json_path)`
Returns list of all assistant response strings.

#### `get_chat_metadata(json_path)`
Returns metadata including total exchanges, model IDs used, and timestamp range.

#### `get_exchange_count(json_path)`
Returns the number of exchanges in the chat.

### Advanced Usage

```python
from copilot_history_pdf import ChatHistoryConverter

# Create custom converter with configuration
config = {
    'replacements': {'oliver': 'student'},
    'max_response_length': 10000,
    'include_timestamps': True,
    'custom_title': 'My Custom Title'
}

converter = ChatHistoryConverter('input.json', 'output.pdf', config)
converter.convert()
```

## Use Cases

### For Students
- Submit chat histories as part of assignment documentation
- Create portfolios showing AI-assisted learning process
- Archive conversations for future reference

### For Instructors
- Review student AI usage patterns
- Grade based on question quality and engagement
- Analyze which models students prefer and why

### For Researchers
- Study human-AI interaction patterns
- Build datasets from chat histories
- Analyze model performance across different tasks

## File Format

The package expects JSON files in GitHub Copilot's chat history export format. The JSON should have this structure:

```json
{
  "responderUsername": "GitHub Copilot",
  "requests": [
    {
      "message": { "text": "user question", "parts": [...] },
      "response": [...],
      "timestamp": 1234567890000,
      "modelId": "copilot/claude-sonnet-4.5"
    }
  ]
}
```

## Requirements

- Python 3.7 or higher
- reportlab >= 3.6.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

For bug reports and feature requests, please open an issue on GitHub.

## Changelog

### Version 0.1.0
- Initial release
- Basic PDF conversion
- CLI interface
- Python API for data extraction
- Model ID display per exchange
- Text replacement support
- Configurable styling options
