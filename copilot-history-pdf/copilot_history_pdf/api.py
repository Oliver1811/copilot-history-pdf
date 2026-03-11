"""
Public API functions for extracting data from Copilot chat history.
"""

from .parsers import (
    load_chat_history,
    extract_text_from_parts,
    extract_response_text,
    extract_model_id
)


def get_all_exchanges(json_path):
    """
    Returns list of all Q&A pairs with metadata.
    
    Args:
        json_path (str): Path to the chat history JSON file
        
    Returns:
        list: List of dicts, each containing:
            - user_message (str): The user's question/message
            - assistant_response (str): The assistant's response
            - timestamp (int): Timestamp in milliseconds
            - exchange_number (int): Exchange number (1-indexed)
            - model_id (str): Model ID used for this exchange
            
    Example:
        >>> exchanges = get_all_exchanges("chat.json")
        >>> for ex in exchanges:
        ...     print(f"Q{ex['exchange_number']}: {ex['user_message'][:50]}")
        ...     print(f"Model: {ex['model_id']}")
    """
    data = load_chat_history(json_path)
    requests = data.get('requests', [])
    
    exchanges = []
    for idx, request_data in enumerate(requests, 1):
        # Extract user message
        message = request_data.get('message', {})
        user_text = message.get('text', '')
        if not user_text and 'parts' in message:
            user_text = extract_text_from_parts(message['parts'])
        
        # Extract assistant response
        response = request_data.get('response', [])
        response_text = extract_response_text(response)
        
        # Extract timestamp
        timestamp = request_data.get('timestamp', 0)
        
        # Extract model ID
        model_id = extract_model_id(request_data)
        
        exchanges.append({
            'user_message': user_text,
            'assistant_response': response_text,
            'timestamp': timestamp,
            'exchange_number': idx,
            'model_id': model_id
        })
    
    return exchanges


def get_exchange_by_index(json_path, idx):
    """
    Get specific exchange by index (0-indexed).
    
    Args:
        json_path (str): Path to the chat history JSON file
        idx (int): Index of the exchange (0-indexed)
        
    Returns:
        dict: Exchange dict with user_message, assistant_response, timestamp, exchange_number, model_id
        
    Raises:
        IndexError: If index is out of range
        
    Example:
        >>> exchange = get_exchange_by_index("chat.json", 0)
        >>> print(exchange['user_message'])
    """
    exchanges = get_all_exchanges(json_path)
    
    if idx < 0 or idx >= len(exchanges):
        raise IndexError(f"Exchange index {idx} out of range (0-{len(exchanges)-1})")
    
    return exchanges[idx]


def get_user_messages(json_path):
    """
    Returns list of all user message strings.
    
    Args:
        json_path (str): Path to the chat history JSON file
        
    Returns:
        list: List of user message strings
        
    Example:
        >>> messages = get_user_messages("chat.json")
        >>> print(f"Student asked {len(messages)} questions")
    """
    exchanges = get_all_exchanges(json_path)
    return [ex['user_message'] for ex in exchanges]


def get_assistant_responses(json_path):
    """
    Returns list of all assistant response strings.
    
    Args:
        json_path (str): Path to the chat history JSON file
        
    Returns:
        list: List of assistant response strings
        
    Example:
        >>> responses = get_assistant_responses("chat.json")
        >>> avg_length = sum(len(r) for r in responses) / len(responses)
    """
    exchanges = get_all_exchanges(json_path)
    return [ex['assistant_response'] for ex in exchanges]


def get_chat_metadata(json_path):
    """
    Returns metadata about the chat history.
    
    Args:
        json_path (str): Path to the chat history JSON file
        
    Returns:
        dict: Metadata containing:
            - responder_username (str): Username of the responder (e.g., "GitHub Copilot")
            - total_exchanges (int): Number of exchanges in the chat
            - model_ids (list): List of unique model IDs used
            - first_timestamp (int): Timestamp of first exchange
            - last_timestamp (int): Timestamp of last exchange
            
    Example:
        >>> meta = get_chat_metadata("chat.json")
        >>> print(f"Models used: {', '.join(meta['model_ids'])}")
    """
    data = load_chat_history(json_path)
    exchanges = get_all_exchanges(json_path)
    
    timestamps = [ex['timestamp'] for ex in exchanges if ex['timestamp'] > 0]
    model_ids = list(set(ex['model_id'] for ex in exchanges))
    
    return {
        'responder_username': data.get('responderUsername', 'Unknown'),
        'total_exchanges': len(exchanges),
        'model_ids': model_ids,
        'first_timestamp': min(timestamps) if timestamps else 0,
        'last_timestamp': max(timestamps) if timestamps else 0
    }


def get_exchange_count(json_path):
    """
    Returns number of exchanges in the chat.
    
    Args:
        json_path (str): Path to the chat history JSON file
        
    Returns:
        int: Number of exchanges
        
    Example:
        >>> count = get_exchange_count("chat.json")
        >>> print(f"Chat has {count} exchanges")
    """
    data = load_chat_history(json_path)
    return len(data.get('requests', []))
