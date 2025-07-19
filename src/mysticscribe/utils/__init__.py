"""
Utility functions and classes for MysticScribe.

This module contains helper functions, configuration management,
and other utility classes used throughout the system.
"""

from .logging_config import setup_logging, get_logger
from .file_utils import ensure_directory, safe_read_file, safe_write_file
from .text_utils import extract_word_count, clean_text, truncate_text

__all__ = [
    'setup_logging',
    'get_logger',
    'ensure_directory',
    'safe_read_file', 
    'safe_write_file',
    'extract_word_count',
    'clean_text',
    'truncate_text'
]
