"""
Core PDF conversion logic for chat history documents.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from .parsers import (
    load_chat_history,
    extract_text_from_parts,
    extract_response_text,
    extract_model_id,
    sanitize_text
)
from .styles import get_all_styles
from .utils import escape_html, format_timestamp, truncate_text, format_model_name


class ChatHistoryConverter:
    """
    Converts Copilot chat history JSON to formatted PDF documents.
    """
    
    def __init__(self, json_path, output_path, config=None):
        """
        Initialize the converter.
        
        Args:
            json_path (str): Path to the input JSON file
            output_path (str): Path for the output PDF file
            config (dict, optional): Configuration options:
                - replacements (dict): Text replacements to apply
                - max_response_length (int): Max length for responses (default: 5000)
                - page_size (tuple): Page size (default: letter)
                - include_timestamps (bool): Include timestamps (default: True)
                - custom_title (str): Custom document title
        """
        self.json_path = json_path
        self.output_path = output_path
        self.config = config or {}
        
        # Extract configuration options
        self.replacements = self.config.get('replacements', None)
        self.max_response_length = self.config.get('max_response_length', 5000)
        self.page_size = self.config.get('page_size', letter)
        self.include_timestamps = self.config.get('include_timestamps', True)
        self.custom_title = self.config.get('custom_title', None)
        
        # Load styles
        self.styles = get_all_styles()
        
        # Data will be loaded during conversion
        self.chat_data = None
    
    def _build_title(self):
        """
        Build the document title.
        
        Returns:
            Paragraph: Title paragraph element
        """
        if self.custom_title:
            title_text = self.custom_title
        else:
            responder = self.chat_data.get('responderUsername', 'Unknown')
            title_text = f"Chat History - {responder}"
        
        # Apply replacements to title
        if self.replacements:
            title_text = sanitize_text(title_text, self.replacements)
        
        return Paragraph(title_text, self.styles['title'])
    
    def _build_exchange(self, request_data, index):
        """
        Build PDF elements for a single conversation exchange.
        
        Args:
            request_data (dict): Single request/response data
            index (int): Exchange number (1-indexed)
            
        Returns:
            list: List of reportlab flowable elements
        """
        elements = []
        
        # Extract model ID and format it
        model_id = extract_model_id(request_data)
        model_name = format_model_name(model_id)
        
        # Add exchange heading with model info
        heading_text = f"<b>Exchange {index}</b> · <i>{model_name}</i>"
        elements.append(Paragraph(heading_text, self.styles['heading']))
        
        # Extract and add user message
        message = request_data.get('message', {})
        user_text = message.get('text', '')
        
        if not user_text and 'parts' in message:
            user_text = extract_text_from_parts(message['parts'], self.replacements)
        
        # Apply replacements to user text if not already done
        if user_text and self.replacements:
            user_text = sanitize_text(user_text, self.replacements)
        
        if user_text:
            user_text_cleaned = escape_html(user_text)
            elements.append(Paragraph(f"<b>User:</b> {user_text_cleaned}", self.styles['user']))
        
        # Extract and add assistant response
        response = request_data.get('response', [])
        response_text = extract_response_text(response, self.replacements)
        
        if response_text:
            # Truncate very long responses
            response_text = truncate_text(response_text, self.max_response_length)
            
            # Clean for XML/HTML
            response_text_cleaned = escape_html(response_text)
            
            elements.append(Paragraph(f"<b>Assistant:</b> {response_text_cleaned}", self.styles['assistant']))
        
        # Add timestamp if enabled and available
        if self.include_timestamps:
            timestamp = request_data.get('timestamp')
            if timestamp:
                time_str = format_timestamp(timestamp)
                elements.append(Paragraph(f"<i>{time_str}</i>", self.styles['timestamp']))
        
        # Add spacing after exchange
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def convert(self):
        """
        Perform the conversion from JSON to PDF.
        
        Returns:
            str: Path to the generated PDF file
            
        Raises:
            FileNotFoundError: If input JSON file doesn't exist
            ValueError: If JSON structure is invalid
        """
        # Load the chat history
        self.chat_data = load_chat_history(self.json_path)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=self.page_size,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Add title
        elements.append(self._build_title())
        elements.append(Spacer(1, 0.2*inch))
        
        # Process each request/response pair
        requests = self.chat_data.get('requests', [])
        
        for idx, request_data in enumerate(requests, 1):
            exchange_elements = self._build_exchange(request_data, idx)
            elements.extend(exchange_elements)
        
        # Build PDF
        doc.build(elements)
        
        return self.output_path
