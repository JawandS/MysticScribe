"""
Text Processing Utilities

Utility functions for text processing and analysis.
"""

import re
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def extract_word_count(text: str) -> int:
    """
    Extract word count from text.
    
    Args:
        text: Text to count words in
        
    Returns:
        Number of words in the text
    """
    if not text:
        return 0
    
    # Split on whitespace and filter out empty strings
    words = [word for word in text.split() if word.strip()]
    return len(words)


def clean_text(text: str, remove_extra_whitespace: bool = True) -> str:
    """
    Clean text by removing common formatting issues.
    
    Args:
        text: Text to clean
        remove_extra_whitespace: Whether to normalize whitespace
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    cleaned = text
    
    # Remove BOM if present
    cleaned = cleaned.replace('\ufeff', '')
    
    # Normalize line endings
    cleaned = cleaned.replace('\r\n', '\n').replace('\r', '\n')
    
    if remove_extra_whitespace:
        # Replace multiple spaces with single space
        cleaned = re.sub(r' +', ' ', cleaned)
        
        # Replace multiple newlines with double newlines (paragraph breaks)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        # Strip leading/trailing whitespace from each line
        lines = cleaned.split('\n')
        cleaned = '\n'.join(line.rstrip() for line in lines)
    
    return cleaned.strip()


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length (including suffix)
        suffix: Suffix to add when truncating
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    if len(suffix) >= max_length:
        return suffix[:max_length]
    
    truncated_length = max_length - len(suffix)
    return text[:truncated_length] + suffix


def extract_sentences(text: str) -> List[str]:
    """
    Extract sentences from text using basic punctuation rules.
    
    Args:
        text: Text to extract sentences from
        
    Returns:
        List of sentences
    """
    if not text:
        return []
    
    # Split on sentence ending punctuation
    sentences = re.split(r'[.!?]+', text)
    
    # Clean up and filter empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences


def extract_paragraphs(text: str) -> List[str]:
    """
    Extract paragraphs from text.
    
    Args:
        text: Text to extract paragraphs from
        
    Returns:
        List of paragraphs
    """
    if not text:
        return []
    
    # Split on double newlines (paragraph breaks)
    paragraphs = text.split('\n\n')
    
    # Clean up and filter empty paragraphs
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    return paragraphs


def find_dialogue(text: str) -> List[str]:
    """
    Find dialogue in text (quoted speech).
    
    Args:
        text: Text to search for dialogue
        
    Returns:
        List of dialogue strings
    """
    if not text:
        return []
    
    dialogue = []
    
    # Find double quotes dialogue
    double_quote_pattern = r'"([^"]*)"'
    double_quotes = re.findall(double_quote_pattern, text)
    dialogue.extend([f'"{quote}"' for quote in double_quotes if quote.strip()])
    
    # Find single quote dialogue (but avoid contractions)
    single_quote_pattern = r"'([^']{10,}?)'"  # At least 10 chars to avoid contractions
    single_quotes = re.findall(single_quote_pattern, text)
    dialogue.extend([f"'{quote}'" for quote in single_quotes if quote.strip()])
    
    return dialogue


def analyze_text_stats(text: str) -> dict:
    """
    Analyze text and return comprehensive statistics.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with text statistics
    """
    if not text:
        return {
            'word_count': 0,
            'character_count': 0,
            'sentence_count': 0,
            'paragraph_count': 0,
            'dialogue_count': 0,
            'avg_sentence_length': 0,
            'avg_paragraph_length': 0
        }
    
    words = extract_word_count(text)
    characters = len(text)
    sentences = extract_sentences(text)
    paragraphs = extract_paragraphs(text)
    dialogue = find_dialogue(text)
    
    avg_sentence_length = words / len(sentences) if sentences else 0
    avg_paragraph_length = words / len(paragraphs) if paragraphs else 0
    
    return {
        'word_count': words,
        'character_count': characters,
        'sentence_count': len(sentences),
        'paragraph_count': len(paragraphs),
        'dialogue_count': len(dialogue),
        'avg_sentence_length': round(avg_sentence_length, 2),
        'avg_paragraph_length': round(avg_paragraph_length, 2)
    }


def search_text(text: str, search_term: str, case_sensitive: bool = False) -> List[Tuple[int, str]]:
    """
    Search for a term in text and return matches with line numbers.
    
    Args:
        text: Text to search in
        search_term: Term to search for
        case_sensitive: Whether search should be case sensitive
        
    Returns:
        List of tuples (line_number, line_content) for matches
    """
    if not text or not search_term:
        return []
    
    matches = []
    lines = text.split('\n')
    
    search_target = search_term if case_sensitive else search_term.lower()
    
    for line_num, line in enumerate(lines, 1):
        search_line = line if case_sensitive else line.lower()
        if search_target in search_line:
            matches.append((line_num, line))
    
    return matches


def format_text_for_display(text: str, max_width: int = 80, indent: int = 0) -> str:
    """
    Format text for display with word wrapping and indentation.
    
    Args:
        text: Text to format
        max_width: Maximum line width
        indent: Number of spaces to indent
        
    Returns:
        Formatted text
    """
    if not text:
        return ""
    
    import textwrap
    
    # Clean the text first
    cleaned_text = clean_text(text)
    
    # Apply indentation
    indent_str = " " * indent
    
    # Wrap and format
    wrapped = textwrap.fill(
        cleaned_text,
        width=max_width - indent,
        initial_indent=indent_str,
        subsequent_indent=indent_str
    )
    
    return wrapped
