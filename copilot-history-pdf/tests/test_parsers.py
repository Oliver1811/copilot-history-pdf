"""
Tests for the parsers module.
"""

import unittest
import json
from pathlib import Path

from copilot_history_pdf.parsers import (
    load_chat_history,
    extract_text_from_parts,
    extract_response_text,
    extract_model_id,
    sanitize_text
)


class TestParsers(unittest.TestCase):
    """Test cases for parser functions."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixture_path = Path(__file__).parent / "fixtures" / "sample_chat.json"
        with open(cls.fixture_path, 'r') as f:
            cls.test_data = json.load(f)
    
    def test_load_chat_history(self):
        """Test loading chat history from JSON file."""
        data = load_chat_history(self.fixture_path)
        
        self.assertIsInstance(data, dict)
        self.assertIn('responderUsername', data)
        self.assertIn('requests', data)
        self.assertEqual(data['responderUsername'], 'GitHub Copilot')
    
    def test_extract_text_from_parts_with_text_field(self):
        """Test extracting text from parts with 'text' field."""
        parts = [{'text': 'Hello'}, {'text': 'World'}]
        result = extract_text_from_parts(parts)
        
        self.assertEqual(result, 'Hello World')
    
    def test_extract_text_from_parts_with_value_field(self):
        """Test extracting text from parts with 'value' field."""
        parts = [{'value': 'Hello'}, {'value': 'World'}]
        result = extract_text_from_parts(parts)
        
        self.assertEqual(result, 'Hello World')
    
    def test_extract_text_from_parts_empty(self):
        """Test extracting text from empty parts."""
        result = extract_text_from_parts([])
        self.assertEqual(result, '')
    
    def test_extract_text_from_parts_with_replacements(self):
        """Test text extraction with replacements applied."""
        parts = [{'text': 'Hello oliver'}]
        replacements = {'oliver': 'student'}
        result = extract_text_from_parts(parts, replacements)
        
        self.assertEqual(result, 'Hello student')
    
    def test_extract_response_text(self):
        """Test extracting response text from response items."""
        response_items = [
            {'value': {'value': 'First response'}},
            {'value': {'value': 'Second response'}}
        ]
        result = extract_response_text(response_items)
        
        self.assertIn('First response', result)
        self.assertIn('Second response', result)
    
    def test_extract_response_text_empty(self):
        """Test extracting response text from empty items."""
        result = extract_response_text([])
        self.assertEqual(result, '')
    
    def test_extract_model_id(self):
        """Test extracting model ID from request."""
        request = self.test_data['requests'][0]
        model_id = extract_model_id(request)
        
        self.assertEqual(model_id, 'copilot/gpt-4')
    
    def test_extract_model_id_missing(self):
        """Test extracting model ID when missing."""
        request = {}
        model_id = extract_model_id(request)
        
        self.assertEqual(model_id, 'Unknown')
    
    def test_sanitize_text(self):
        """Test text sanitization with replacements."""
        text = "Hello oliver, how are you Oliver?"
        replacements = {'oliver': 'student', 'Oliver': 'Student'}
        result = sanitize_text(text, replacements)
        
        self.assertEqual(result, 'Hello student, how are you Student?')
    
    def test_sanitize_text_no_replacements(self):
        """Test sanitization without replacements."""
        text = "Hello world"
        result = sanitize_text(text)
        
        self.assertEqual(result, 'Hello world')


if __name__ == '__main__':
    unittest.main()
