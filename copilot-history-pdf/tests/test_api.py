"""
Tests for the public API functions.
"""

import unittest
from pathlib import Path

from copilot_history_pdf import (
    get_all_exchanges,
    get_exchange_by_index,
    get_user_messages,
    get_assistant_responses,
    get_chat_metadata,
    get_exchange_count
)


class TestAPI(unittest.TestCase):
    """Test cases for public API functions."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixture_path = Path(__file__).parent / "fixtures" / "sample_chat.json"
    
    def test_get_all_exchanges(self):
        """Test getting all exchanges."""
        exchanges = get_all_exchanges(str(self.fixture_path))
        
        self.assertIsInstance(exchanges, list)
        self.assertEqual(len(exchanges), 2)
        
        # Check first exchange structure
        first = exchanges[0]
        self.assertIn('user_message', first)
        self.assertIn('assistant_response', first)
        self.assertIn('timestamp', first)
        self.assertIn('exchange_number', first)
        self.assertIn('model_id', first)
        
        # Verify content
        self.assertIn('Python function', first['user_message'])
        self.assertEqual(first['exchange_number'], 1)
        self.assertEqual(first['model_id'], 'copilot/gpt-4')
    
    def test_get_exchange_by_index(self):
        """Test getting a specific exchange by index."""
        exchange = get_exchange_by_index(str(self.fixture_path), 0)
        
        self.assertIsInstance(exchange, dict)
        self.assertIn('Python function', exchange['user_message'])
        self.assertEqual(exchange['exchange_number'], 1)
    
    def test_get_exchange_by_index_second(self):
        """Test getting the second exchange."""
        exchange = get_exchange_by_index(str(self.fixture_path), 1)
        
        self.assertIn('example', exchange['user_message'])
        self.assertEqual(exchange['exchange_number'], 2)
        self.assertEqual(exchange['model_id'], 'copilot/claude-sonnet-4.5')
    
    def test_get_exchange_by_index_out_of_range(self):
        """Test getting exchange with invalid index."""
        with self.assertRaises(IndexError):
            get_exchange_by_index(str(self.fixture_path), 10)
    
    def test_get_user_messages(self):
        """Test getting all user messages."""
        messages = get_user_messages(str(self.fixture_path))
        
        self.assertIsInstance(messages, list)
        self.assertEqual(len(messages), 2)
        self.assertIn('Python function', messages[0])
        self.assertIn('example', messages[1])
    
    def test_get_assistant_responses(self):
        """Test getting all assistant responses."""
        responses = get_assistant_responses(str(self.fixture_path))
        
        self.assertIsInstance(responses, list)
        self.assertEqual(len(responses), 2)
        self.assertIn('def keyword', responses[0])
        self.assertIn('greet', responses[1])
    
    def test_get_chat_metadata(self):
        """Test getting chat metadata."""
        meta = get_chat_metadata(str(self.fixture_path))
        
        self.assertIsInstance(meta, dict)
        self.assertIn('responder_username', meta)
        self.assertIn('total_exchanges', meta)
        self.assertIn('model_ids', meta)
        self.assertIn('first_timestamp', meta)
        self.assertIn('last_timestamp', meta)
        
        # Verify values
        self.assertEqual(meta['responder_username'], 'GitHub Copilot')
        self.assertEqual(meta['total_exchanges'], 2)
        self.assertIn('copilot/gpt-4', meta['model_ids'])
        self.assertIn('copilot/claude-sonnet-4.5', meta['model_ids'])
    
    def test_get_exchange_count(self):
        """Test getting exchange count."""
        count = get_exchange_count(str(self.fixture_path))
        
        self.assertEqual(count, 2)


if __name__ == '__main__':
    unittest.main()
