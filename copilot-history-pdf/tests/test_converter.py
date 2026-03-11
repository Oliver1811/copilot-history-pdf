"""
Integration tests for the PDF converter.
"""

import unittest
import tempfile
import os
from pathlib import Path

from copilot_history_pdf import ChatHistoryConverter


class TestConverter(unittest.TestCase):
    """Test cases for ChatHistoryConverter."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixture_path = Path(__file__).parent / "fixtures" / "sample_chat.json"
    
    def test_converter_basic(self):
        """Test basic PDF conversion."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            output_path = tmp.name
        
        try:
            converter = ChatHistoryConverter(
                str(self.fixture_path),
                output_path
            )
            result = converter.convert()
            
            # Check PDF was created
            self.assertTrue(os.path.exists(output_path))
            self.assertEqual(result, output_path)
            
            # Check file has content
            file_size = os.path.getsize(output_path)
            self.assertGreater(file_size, 0)
        
        finally:
            # Clean up
            if os.path.exists(output_path):
                os.remove(output_path)
    
    def test_converter_with_config(self):
        """Test PDF conversion with custom configuration."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            output_path = tmp.name
        
        try:
            config = {
                'custom_title': 'Test Chat History',
                'max_response_length': 1000,
                'include_timestamps': False,
                'replacements': {'function': 'method'}
            }
            
            converter = ChatHistoryConverter(
                str(self.fixture_path),
                output_path,
                config
            )
            result = converter.convert()
            
            # Check PDF was created
            self.assertTrue(os.path.exists(output_path))
            
            # Check file has content
            file_size = os.path.getsize(output_path)
            self.assertGreater(file_size, 0)
        
        finally:
            # Clean up
            if os.path.exists(output_path):
                os.remove(output_path)
    
    def test_converter_invalid_json_path(self):
        """Test converter with invalid JSON file path."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            output_path = tmp.name
        
        try:
            converter = ChatHistoryConverter(
                "nonexistent.json",
                output_path
            )
            
            with self.assertRaises(FileNotFoundError):
                converter.convert()
        
        finally:
            # Clean up
            if os.path.exists(output_path):
                os.remove(output_path)


if __name__ == '__main__':
    unittest.main()
