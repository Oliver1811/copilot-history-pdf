"""
Helper utility functions for chat history processing.
"""

from datetime import datetime
import html


def escape_html(text):
    """
    Escape HTML/XML special characters for use in reportlab Paragraphs.
    
    Args:
        text (str): Text to escape
        
    Returns:
        str: Escaped text safe for XML/HTML
    """
    if not text:
        return ""
    
    # Replace special characters that can break XML/HTML
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    
    return text


def format_timestamp(timestamp_ms, format_str='%Y-%m-%d %H:%M:%S'):
    """
    Convert millisecond timestamp to readable format.
    
    Args:
        timestamp_ms (int): Timestamp in milliseconds since epoch
        format_str (str): strftime format string (default: '%Y-%m-%d %H:%M:%S')
        
    Returns:
        str: Formatted timestamp string
        
    Raises:
        ValueError: If timestamp is invalid
    """
    try:
        dt = datetime.fromtimestamp(timestamp_ms / 1000)
        return dt.strftime(format_str)
    except (ValueError, OSError) as e:
        raise ValueError(f"Invalid timestamp: {timestamp_ms}") from e


def validate_json_structure(data):
    """
    Verify that the JSON data has the expected Copilot chat history structure.
    
    Args:
        data (dict): Parsed JSON data
        
    Returns:
        bool: True if structure is valid
        
    Raises:
        ValueError: If structure is invalid with details about what's missing
    """
    if not isinstance(data, dict):
        raise ValueError("JSON data must be a dictionary")
    
    if 'requests' not in data:
        raise ValueError("JSON must contain 'requests' field")
    
    if not isinstance(data['requests'], list):
        raise ValueError("'requests' field must be a list")
    
    # Check if we have at least one request with proper structure
    if len(data['requests']) > 0:
        first_request = data['requests'][0]
        
        if not isinstance(first_request, dict):
            raise ValueError("Each request must be a dictionary")
        
        if 'message' not in first_request:
            raise ValueError("Each request must have a 'message' field")
    
    return True


def truncate_text(text, max_length=5000, suffix="... [truncated]"):
    """
    Truncate text to a maximum length with a suffix.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length before truncation (default: 5000)
        suffix (str): String to append when truncated (default: "... [truncated]")
        
    Returns:
        str: Truncated text with suffix if needed, original text otherwise
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length] + suffix


def load_replacements_config(config_path):
    """
    Load text replacement configuration from a JSON file.
    
    Args:
        config_path (str): Path to JSON config file
        
    Returns:
        dict: Dictionary of text replacements
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is not valid JSON
    """
    import json
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Extract replacements from config
    if 'replacements' in config:
        replacements_list = config['replacements']
        # Convert list format [{"find": "x", "replace": "y"}] to dict {"x": "y"}
        if isinstance(replacements_list, list):
            return {item['find']: item['replace'] for item in replacements_list}
        return replacements_list
    
    return config


def format_model_name(model_id):
    """
    Format a model ID for display (clean up the raw ID string).
    
    Args:
        model_id (str): Raw model ID (e.g., "copilot/claude-sonnet-4.5")
        
    Returns:
        str: Human-readable model name (e.g., "Claude Sonnet 4.5")
    """
    if not model_id or model_id == "Unknown":
        return "Unknown Model"
    
    # Remove "copilot/" prefix if present
    if model_id.startswith("copilot/"):
        model_id = model_id[8:]
    
    # Convert to title case and handle common patterns
    # e.g., "claude-sonnet-4.5" -> "Claude Sonnet 4.5"
    # e.g., "gpt-4" -> "GPT-4"
    
    parts = model_id.split('-')
    formatted_parts = []
    
    for part in parts:
        # Keep version numbers as-is
        if part.replace('.', '').isdigit():
            formatted_parts.append(part)
        # Uppercase known acronyms
        elif part.lower() in ['gpt', 'llm', 'ai']:
            formatted_parts.append(part.upper())
        # Title case everything else
        else:
            formatted_parts.append(part.capitalize())
    
    return ' '.join(formatted_parts)
