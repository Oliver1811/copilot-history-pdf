"""
Example: Using the Python API to extract data from Copilot chat history

This example demonstrates how to use the copilot_history_pdf API functions
to programmatically access and analyze chat data.
"""

import copilot_history_pdf as chp

# Path to your chat history JSON file
json_file = "path/to/your/chat_history.json"

# Example 1: Get basic chat metadata
print("=" * 60)
print("Example 1: Chat Metadata")
print("=" * 60)
metadata = chp.get_chat_metadata(json_file)
print(f"Total exchanges: {metadata['total_exchanges']}")
print(f"Models used: {', '.join(metadata['model_ids'])}")
print(f"First message: {metadata['first_timestamp']}")
print(f"Last message: {metadata['last_timestamp']}")
print()

# Example 2: Get all exchanges with full details
print("=" * 60)
print("Example 2: All Exchanges")
print("=" * 60)
exchanges = chp.get_all_exchanges(json_file)
for exchange in exchanges:
    print(f"\n--- Exchange {exchange['exchange_number']} ---")
    print(f"Model: {exchange['model_id']}")
    print(f"User: {exchange['user_message'][:100]}...")
    print(f"Assistant: {exchange['assistant_response'][:100]}...")
    print(f"Timestamp: {exchange['timestamp']}")
print()

# Example 3: Get a specific exchange by index (0-based)
print("=" * 60)
print("Example 3: Specific Exchange")
print("=" * 60)
try:
    exchange = chp.get_exchange_by_index(json_file, 0)  # First exchange
    print(f"Exchange #{exchange['exchange_number']}")
    print(f"User question: {exchange['user_message']}")
    print(f"Assistant response: {exchange['assistant_response'][:200]}...")
except IndexError as e:
    print(f"Error: {e}")
print()

# Example 4: Get only user messages
print("=" * 60)
print("Example 4: User Messages Only")
print("=" * 60)
user_messages = chp.get_user_messages(json_file)
for i, message in enumerate(user_messages, 1):
    print(f"{i}. {message[:80]}...")
print()

# Example 5: Get only assistant responses
print("=" * 60)
print("Example 5: Assistant Responses Only")
print("=" * 60)
assistant_responses = chp.get_assistant_responses(json_file)
for i, response in enumerate(assistant_responses, 1):
    print(f"{i}. {response[:80]}...")
print()

# Example 6: Get count of exchanges
print("=" * 60)
print("Example 6: Exchange Count")
print("=" * 60)
count = chp.get_exchange_count(json_file)
print(f"Total number of exchanges: {count}")
print()

# Example 7: Generate PDF with custom configuration
print("=" * 60)
print("Example 7: Generate PDF")
print("=" * 60)
converter = chp.ChatHistoryConverter(
    json_path=json_file,
    output_path="output.pdf",
    config={
        'custom_title': 'My Copilot Chat History',
        'max_response_length': 1000,
        'include_timestamps': True,
        'page_size': 'letter'
    }
)
converter.convert()
print("PDF generated successfully!")
