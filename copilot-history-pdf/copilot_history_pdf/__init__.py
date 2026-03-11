"""
Copilot Chat History to PDF Converter

A Python package to convert GitHub Copilot chat history JSON files to formatted PDF documents,
with a public API for programmatic data extraction.
"""

from .converter import ChatHistoryConverter
from .api import (
    get_all_exchanges,
    get_exchange_by_index,
    get_user_messages,
    get_assistant_responses,
    get_chat_metadata,
    get_exchange_count
)


# Public API
__all__ = [
    'ChatHistoryConverter',
    'get_all_exchanges',
    'get_exchange_by_index',
    'get_user_messages',
    'get_assistant_responses',
    'get_chat_metadata',
    'get_exchange_count'
]

__version__ = '0.1.0'
