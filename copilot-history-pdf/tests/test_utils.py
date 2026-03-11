"""
Tests for utility functions.
"""

import unittest
from datetime import datetime

from copilot_history_pdf.utils import (
    escape_html,
    format_timestamp,
    truncate_text,
    format_model_name,
    validate_json_structure
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_escape_html_ampersand(self):
        """Test HTML escaping of ampersand."""
        result = escape_html("Tom & Jerry")
        self.assertEqual(result, "Tom &amp; Jerry")
    
    def test_escape_html_less_than(self):
        """Test HTML escaping of less than sign."""
        result = escape_html("x < y")
        self.assertEqual(result, "x &lt; y")
    
    def test_escape_html_greater_than(self):
        """Test HTML escaping of greater than sign."""
        result = escape_html("x > y")
        self.assertEqual(result, "x &gt; y")
    
    def test_escape_html_combined(self):
        """Test HTML escaping of multiple characters."""
        result = escape_html("if x < 5 && y > 3")
        self.assertEqual(result, "if x &lt; 5 &amp;&amp; y &gt; 3")
    
    def test_escape_html_empty(self):
        """Test HTML escaping of empty string."""
        result = escape_html("")
        self.assertEqual(result, "")
    
    def test_format_timestamp(self):
        """Test timestamp formatting."""
        # 1700000000000 ms = Nov 14, 2023
        result = format_timestamp(1700000000000)
        
        # Just check it returned a date string
        self.assertIsInstance(result, str)
        self.assertIn('2023', result)
    
    def test_format_timestamp_custom_format(self):
        """Test timestamp with custom format."""
        result = format_timestamp(1700000000000, '%Y-%m-%d')
        self.assertEqual(result, '2023-11-14')
    
    def test_format_timestamp_invalid(self):
        """Test invalid timestamp."""
        # Use a timestamp that exceeds valid range (year 10000+)
        with self.assertRaises(ValueError):
            format_timestamp(999999999999999)
    
    def test_truncate_text_short(self):
        """Test truncating text that's already short."""
        text = "Short text"
        result = truncate_text(text, 100)
        self.assertEqual(result, "Short text")
    
    def test_truncate_text_long(self):
        """Test truncating long text."""
        text = "a" * 1000
        result = truncate_text(text, 100)
        
        self.assertTrue(len(result) < 150)
        self.assertIn("[truncated]", result)
    
    def test_truncate_text_custom_suffix(self):
        """Test truncating with custom suffix."""
        text = "a" * 100
        result = truncate_text(text, 50, suffix="...")
        
        self.assertTrue(result.endswith("..."))
        self.assertEqual(len(result), 53)  # 50 + len("...")
    
    def test_format_model_name_copilot_prefix(self):
        """Test formatting model name with copilot prefix."""
        result = format_model_name("copilot/claude-sonnet-4.5")
        self.assertEqual(result, "Claude Sonnet 4.5")
    
    def test_format_model_name_gpt(self):
        """Test formatting GPT model name."""
        result = format_model_name("copilot/gpt-4")
        self.assertEqual(result, "GPT 4")
    
    def test_format_model_name_unknown(self):
        """Test formatting unknown model."""
        result = format_model_name("Unknown")
        self.assertEqual(result, "Unknown Model")
    
    def test_format_model_name_empty(self):
        """Test formatting empty model name."""
        result = format_model_name("")
        self.assertEqual(result, "Unknown Model")
    
    def test_validate_json_structure_valid(self):
        """Test validating a valid JSON structure."""
        valid_data = {
            "responderUsername": "GitHub Copilot",
            "requests": [
                {
                    "message": {"text": "test"}
                }
            ]
        }
        
        self.assertTrue(validate_json_structure(valid_data))
    
    def test_validate_json_structure_not_dict(self):
        """Test validating non-dict structure."""
        with self.assertRaises(ValueError):
            validate_json_structure([])
    
    def test_validate_json_structure_no_requests(self):
        """Test validating structure without requests field."""
        invalid_data = {"responderUsername": "Test"}
        
        with self.assertRaises(ValueError):
            validate_json_structure(invalid_data)
    
    def test_validate_json_structure_requests_not_list(self):
        """Test validating structure with non-list requests."""
        invalid_data = {"requests": "not a list"}
        
        with self.assertRaises(ValueError):
            validate_json_structure(invalid_data)


if __name__ == '__main__':
    unittest.main()
