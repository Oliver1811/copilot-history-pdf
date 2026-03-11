# Examples

This directory contains example usage of the `copilot-history-pdf` package.

## Files

### api_usage.py
Demonstrates how to use the Python API to programmatically extract and analyze data from Copilot chat history files.

**Features demonstrated:**
- Getting chat metadata (total exchanges, models used, timestamps)
- Retrieving all exchanges with full details
- Accessing specific exchanges by index
- Extracting only user messages
- Extracting only assistant responses
- Getting exchange count
- Generating PDFs with custom configuration

**How to run:**
```bash
# Edit the json_file path in the script first
python api_usage.py
```

### cli_usage.sh
Shows various command-line interface usage patterns for the `copilot-to-pdf` command.

**Features demonstrated:**
- Basic conversion with defaults
- Custom output filename
- Adding custom titles
- Limiting response length
- Text replacements from config
- Disabling timestamps
- Page size options (letter/a4)
- Full configuration example
- Version and help commands

**How to run:**
```bash
# Make the script executable
chmod +x cli_usage.sh

# View the examples (they won't actually run without a real JSON file)
./cli_usage.sh
```

### replacements.json
Sample configuration file for text replacements. Use this to redact sensitive information before generating PDFs.

**Use cases:**
- Removing personal information (names, emails)
- Redacting API keys and passwords
- Replacing file paths
- Hiding IP addresses
- Anonymizing company names

**How to use:**
```bash
copilot-to-pdf chat_history.json --replacements replacements.json
```

Or with the Python API:
```python
import copilot_history_pdf as chp

converter = chp.ChatHistoryConverter(
    json_path="chat_history.json",
    output_path="output.pdf",
    config={'replacements': "replacements.json"}
)
converter.convert()
```

## Quick Start

1. **Install the package:**
   ```bash
   pip install copilot-history-pdf
   ```

2. **Try the CLI:**
   ```bash
   copilot-to-pdf your_chat_history.json
   ```

3. **Try the Python API:**
   ```python
   import copilot_history_pdf as chp
   
   # Get metadata
   metadata = chp.get_chat_metadata("your_chat_history.json")
   print(metadata)
   
   # Generate PDF
   converter = chp.ChatHistoryConverter(
       json_path="your_chat_history.json",
       output_path="output.pdf"
   )
   converter.convert()
   ```

## Getting Your Chat History JSON

To export your GitHub Copilot chat history:
1. Open VS Code
2. Open the Copilot Chat view
3. Click the "..." menu in the chat panel
4. Select "Export Chat" or use the command palette: "Copilot: Export Chat History"
5. Save the JSON file

## Tips

- **For Students:** Use `--title` to add your name and course information to the PDF header
- **For Privacy:** Use the `replacements.json` approach to redact sensitive information
- **For Submissions:** Use `--no-timestamps` if timestamps aren't required
- **For Analysis:** Use the Python API functions to extract specific data points for reports
- **For Long Chats:** Use `--max-response-length` to limit file size by truncating responses

## Need Help?

- Check the main [README.md](../README.md) for full documentation
- Run `copilot-to-pdf --help` for CLI options
- Visit the [GitHub repository](https://github.com/Oliver1811/copilot-history-pdf) for issues and discussions
