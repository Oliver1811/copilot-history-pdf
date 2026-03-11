#!/bin/bash
# Example CLI usage for copilot-to-pdf command

echo "======================================================================"
echo "Example 1: Basic conversion with default settings"
echo "======================================================================"
copilot-to-pdf chat_history.json
echo "Output: chat_history.pdf (default name)"
echo ""

echo "======================================================================"
echo "Example 2: Specify output filename"
echo "======================================================================"
copilot-to-pdf chat_history.json -o my_submission.pdf
echo "Output: my_submission.pdf"
echo ""

echo "======================================================================"
echo "Example 3: Add a custom title"
echo "======================================================================"
copilot-to-pdf chat_history.json --title "CS101 Final Project Chat History"
echo "Output: PDF with custom title"
echo ""

echo "======================================================================"
echo "Example 4: Limit response length to 500 characters"
echo "======================================================================"
copilot-to-pdf chat_history.json --max-response-length 500
echo "Output: Long responses truncated to 500 chars"
echo ""

echo "======================================================================"
echo "Example 5: Apply text replacements from config file"
echo "======================================================================"
copilot-to-pdf chat_history.json --replacements replacements.json
echo "Output: Text replaced according to config"
echo ""

echo "======================================================================"
echo "Example 6: Disable timestamps"
echo "======================================================================"
copilot-to-pdf chat_history.json --no-timestamps
echo "Output: PDF without timestamp information"
echo ""

echo "======================================================================"
echo "Example 7: Use A4 page size (default is letter)"
echo "======================================================================"
copilot-to-pdf chat_history.json --page-size a4
echo "Output: PDF with A4 page dimensions"
echo ""

echo "======================================================================"
echo "Example 8: Full configuration example"
echo "======================================================================"
copilot-to-pdf chat_history.json \
    -o "submission.pdf" \
    --title "My Copilot Chat Session" \
    --max-response-length 800 \
    --replacements replacements.json \
    --no-timestamps \
    --page-size letter
echo "Output: submission.pdf with all custom settings"
echo ""

echo "======================================================================"
echo "Example 9: Check version"
echo "======================================================================"
copilot-to-pdf --version
echo ""

echo "======================================================================"
echo "Example 10: Get help"
echo "======================================================================"
copilot-to-pdf --help
