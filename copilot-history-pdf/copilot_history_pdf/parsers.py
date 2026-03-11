"""
JSON parsing functions for extracting data from Copilot chat history.
"""

import json


def load_chat_history(json_file_path):
    """
    Load the chat history JSON file.
    
    Args:
        json_file_path (str): Path to the JSON file
        
    Returns:
        dict: Parsed JSON data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_text_from_parts(parts, replacements=None):
    """
    Extract text from message parts.
    
    Args:
        parts (list): List of message part dictionaries
        replacements (dict, optional): Dictionary of text replacements to apply
        
    Returns:
        str: Extracted and cleaned text
    """
    if not parts:
        return ""
    
    text_parts = []
    for part in parts:
        if isinstance(part, dict):
            if 'text' in part:
                text_parts.append(part['text'])
            elif 'value' in part:
                text_parts.append(str(part['value']))
        elif isinstance(part, str):
            text_parts.append(part)
    
    result = ' '.join(text_parts)
    
    # Apply text replacements if provided
    if replacements:
        for old_text, new_text in replacements.items():
            result = result.replace(old_text, new_text)
    
    return result


def extract_response_text(response_items, replacements=None):
    """
    Extract text from response items.
    
    Args:
        response_items (list): List of response item dictionaries
        replacements (dict, optional): Dictionary of text replacements to apply
        
    Returns:
        str: Extracted response text, or default message if none found
    """
    if not response_items:
        return ""
    
    response_parts = []
    for item in response_items:
        if isinstance(item, dict):
            if 'value' in item and isinstance(item['value'], dict):
                value = item['value']
                if 'value' in value:
                    response_parts.append(str(value['value']))
            elif 'value' in item:
                response_parts.append(str(item['value']))
    
    result = '\n\n'.join(response_parts) if response_parts else "No response text available"
    
    # Apply text replacements if provided
    if replacements:
        for old_text, new_text in replacements.items():
            result = result.replace(old_text, new_text)
    
    return result


def sanitize_text(text, replacements=None):
    """
    Apply text replacements to sanitize/anonymize content.
    
    Args:
        text (str): Text to sanitize
        replacements (dict, optional): Dictionary of text replacements to apply
        
    Returns:
        str: Sanitized text
    """
    if not replacements or not text:
        return text
    
    result = text
    for old_text, new_text in replacements.items():
        result = result.replace(old_text, new_text)
    
    return result


def extract_model_id(request_data):
    """
    Extract the model ID from a request.
    
    Args:
        request_data (dict): A single request dictionary from the chat history
        
    Returns:
        str: Model ID (e.g., "copilot/claude-sonnet-4.5"), or "Unknown" if not found
    """
    if not isinstance(request_data, dict):
        return "Unknown"
    
    return request_data.get('modelId', 'Unknown')
