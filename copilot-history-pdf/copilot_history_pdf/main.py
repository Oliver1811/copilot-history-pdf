"""
Command-line interface for converting Copilot chat history to PDF.
"""

import argparse
import sys
import json
from pathlib import Path

from .converter import ChatHistoryConverter
from .utils import load_replacements_config


def parse_page_size(size_str):
    """
    Parse page size string to reportlab page size tuple.
    
    Args:
        size_str (str): Page size name ('letter', 'a4', etc.)
        
    Returns:
        tuple: Page size tuple (width, height) in points
    """
    from reportlab.lib.pagesizes import letter, A4
    
    sizes = {
        'letter': letter,
        'a4': A4,
    }
    
    size_lower = size_str.lower()
    if size_lower not in sizes:
        raise argparse.ArgumentTypeError(
            f"Invalid page size '{size_str}'. Must be one of: {', '.join(sizes.keys())}"
        )
    
    return sizes[size_lower]


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Convert GitHub Copilot chat history JSON to PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  copilot-to-pdf chat.json
  
  # Custom output path
  copilot-to-pdf chat.json -o report.pdf
  
  # With text replacements
  copilot-to-pdf chat.json --replacements config.json
  
  # Custom title and no timestamps
  copilot-to-pdf chat.json --title "Student Submission" --no-timestamps
        """
    )
    
    # Required arguments
    parser.add_argument(
        'input',
        help='Path to the input JSON file containing chat history'
    )
    
    # Optional arguments
    parser.add_argument(
        '-o', '--output',
        default='chat_history.pdf',
        help='Output PDF file path (default: chat_history.pdf)'
    )
    
    parser.add_argument(
        '--title',
        help='Custom title for the PDF document'
    )
    
    parser.add_argument(
        '--max-response-length',
        type=int,
        default=5000,
        help='Maximum length for assistant responses before truncation (default: 5000)'
    )
    
    parser.add_argument(
        '--replacements',
        help='Path to JSON file containing text replacements (e.g., {"oliver": "finan"})'
    )
    
    parser.add_argument(
        '--no-timestamps',
        action='store_true',
        help='Omit timestamps from the PDF'
    )
    
    parser.add_argument(
        '--page-size',
        type=parse_page_size,
        default='letter',
        help='Page size for the PDF (letter, a4) (default: letter)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.1.2'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        return 1
    
    # Load replacements if provided
    replacements = None
    if args.replacements:
        try:
            replacements = load_replacements_config(args.replacements)
            print(f"Loaded text replacements from {args.replacements}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading replacements: {e}", file=sys.stderr)
            return 1
    
    # Build configuration
    config = {
        'replacements': replacements,
        'max_response_length': args.max_response_length,
        'page_size': args.page_size,
        'include_timestamps': not args.no_timestamps,
        'custom_title': args.title
    }
    
    # Perform conversion
    try:
        print(f"Converting {args.input} to PDF...")
        converter = ChatHistoryConverter(args.input, args.output, config)
        output_path = converter.convert()
        
        # Show exchange count
        exchange_count = len(converter.chat_data.get('requests', []))
        print(f"✓ PDF created successfully: {output_path}")
        print(f"  Processed {exchange_count} exchange(s)")
        return 0
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file - {e}", file=sys.stderr)
        return 1
    
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
