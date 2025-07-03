"""Text processing utilities for the Nova AI Assistant."""

def apply_all_filters(text: str) -> str:
    """
    Apply all text processing filters to the input text.
    
    Args:
        text (str): The input text to process
        
    Returns:
        str: The processed text
    """
    if not text:
        return text
        
    # Apply each filter in sequence
    text = text.strip()
    
    # Ensure the text ends with a single newline
    text = text.rstrip('\n') + '\n'
    
    return text

def clean_whitespace(text: str) -> str:
    """Clean up whitespace in the text."""
    if not text:
        return text
    return ' '.join(text.split())

def remove_extra_newlines(text: str) -> str:
    """Remove extra newlines, keeping at most two in a row."""
    if not text:
        return text
    import re
    return re.sub(r'\n{3,}', '\n\n', text)

# Add more text processing functions as needed
