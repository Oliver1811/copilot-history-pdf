"""
PDF styling configuration for chat history documents.
"""

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib import colors


def get_title_style():
    """
    Get the style for the main document title.
    
    Returns:
        ParagraphStyle: Title style configuration
    """
    styles = getSampleStyleSheet()
    return ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E86AB'),
        spaceAfter=30,
        alignment=TA_LEFT
    )


def get_user_style():
    """
    Get the style for user messages.
    
    Returns:
        ParagraphStyle: User message style configuration
    """
    styles = getSampleStyleSheet()
    return ParagraphStyle(
        'UserMessage',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        spaceBefore=12,
        leftIndent=0,
        rightIndent=20,
        backColor=colors.HexColor('#E8F4F8'),
        borderPadding=10
    )


def get_assistant_style():
    """
    Get the style for assistant responses.
    
    Returns:
        ParagraphStyle: Assistant message style configuration
    """
    styles = getSampleStyleSheet()
    return ParagraphStyle(
        'AssistantMessage',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        spaceBefore=12,
        leftIndent=20,
        rightIndent=0,
        backColor=colors.HexColor('#F0F0F0'),
        borderPadding=10
    )


def get_heading_style():
    """
    Get the style for conversation exchange headings.
    
    Returns:
        ParagraphStyle: Heading style configuration
    """
    styles = getSampleStyleSheet()
    return ParagraphStyle(
        'ConversationHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#555555'),
        spaceAfter=10,
        spaceBefore=20
    )


def get_timestamp_style():
    """
    Get the style for timestamps.
    
    Returns:
        ParagraphStyle: Timestamp style configuration
    """
    styles = getSampleStyleSheet()
    return ParagraphStyle(
        'Timestamp',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_RIGHT
    )


def get_all_styles():
    """
    Get all styles as a dictionary for convenience.
    
    Returns:
        dict: Dictionary with all style configurations
    """
    return {
        'title': get_title_style(),
        'user': get_user_style(),
        'assistant': get_assistant_style(),
        'heading': get_heading_style(),
        'timestamp': get_timestamp_style()
    }
