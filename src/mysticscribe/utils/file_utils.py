"""
File Utilities

Utility functions for safe file operations.
"""

import os
from pathlib import Path
from typing import Optional, Union
import logging

logger = logging.getLogger(__name__)


def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Path to the directory
        
    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def safe_read_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> Optional[str]:
    """
    Safely read a file, returning None on error.
    
    Args:
        file_path: Path to the file to read
        encoding: File encoding
        
    Returns:
        File contents or None if error occurred
    """
    try:
        path = Path(file_path)
        if not path.exists():
            logger.warning(f"File does not exist: {path}")
            return None
        
        with open(path, 'r', encoding=encoding) as f:
            content = f.read()
            logger.debug(f"Successfully read file: {path} ({len(content)} characters)")
            return content
            
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None


def safe_write_file(
    file_path: Union[str, Path], 
    content: str, 
    encoding: str = 'utf-8',
    create_dirs: bool = True
) -> bool:
    """
    Safely write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write
        encoding: File encoding
        create_dirs: Whether to create parent directories
        
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        
        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
        
        logger.debug(f"Successfully wrote file: {path} ({len(content)} characters)")
        return True
        
    except Exception as e:
        logger.error(f"Error writing file {file_path}: {e}")
        return False


def get_file_stats(file_path: Union[str, Path]) -> Optional[dict]:
    """
    Get statistics for a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary with file statistics or None if error
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return None
        
        stat = path.stat()
        return {
            'size_bytes': stat.st_size,
            'modified_time': stat.st_mtime,
            'created_time': stat.st_ctime,
            'is_file': path.is_file(),
            'is_dir': path.is_dir(),
            'name': path.name,
            'stem': path.stem,
            'suffix': path.suffix
        }
        
    except Exception as e:
        logger.error(f"Error getting file stats for {file_path}: {e}")
        return None


def find_files_by_pattern(directory: Union[str, Path], pattern: str) -> list[Path]:
    """
    Find files matching a glob pattern in a directory.
    
    Args:
        directory: Directory to search in
        pattern: Glob pattern to match
        
    Returns:
        List of matching file paths
    """
    try:
        dir_path = Path(directory)
        if not dir_path.exists() or not dir_path.is_dir():
            logger.warning(f"Directory does not exist or is not a directory: {directory}")
            return []
        
        matches = list(dir_path.glob(pattern))
        logger.debug(f"Found {len(matches)} files matching pattern '{pattern}' in {directory}")
        return matches
        
    except Exception as e:
        logger.error(f"Error finding files with pattern '{pattern}' in {directory}: {e}")
        return []


def backup_file(file_path: Union[str, Path], backup_suffix: str = '.backup') -> Optional[Path]:
    """
    Create a backup copy of a file.
    
    Args:
        file_path: Path to the file to backup
        backup_suffix: Suffix to add to backup file
        
    Returns:
        Path to backup file or None if error
    """
    try:
        path = Path(file_path)
        if not path.exists():
            logger.warning(f"Cannot backup non-existent file: {path}")
            return None
        
        backup_path = path.with_suffix(path.suffix + backup_suffix)
        
        # Read and write to create backup
        content = safe_read_file(path)
        if content is not None and safe_write_file(backup_path, content):
            logger.info(f"Created backup: {backup_path}")
            return backup_path
        else:
            logger.error(f"Failed to create backup of {path}")
            return None
            
    except Exception as e:
        logger.error(f"Error creating backup of {file_path}: {e}")
        return None
