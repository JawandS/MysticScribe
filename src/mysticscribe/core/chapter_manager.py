"""
Chapter Management System

Handles chapter numbering, file operations, and chapter lifecycle management.
"""

import os
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ChapterInfo:
    """Information about a chapter."""
    number: int
    outline_exists: bool
    draft_exists: bool
    outline_path: Optional[Path] = None
    draft_path: Optional[Path] = None
    word_count: Optional[int] = None


class ChapterManager:
    """
    Manages chapter numbering, file operations, and chapter metadata.
    
    This class provides a centralized way to handle all chapter-related
    file operations, including automatic chapter numbering, validation,
    and file management.
    """
    
    def __init__(self, project_root: Path):
        """
        Initialize the Chapter Manager.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = Path(project_root)
        self.chapters_dir = self.project_root / "chapters"
        self.outlines_dir = self.project_root / "outlines"
        
        # Ensure directories exist
        self.chapters_dir.mkdir(exist_ok=True)
        self.outlines_dir.mkdir(exist_ok=True)
    
    def get_next_chapter_number(self) -> int:
        """
        Get the next chapter number by checking existing outlines.
        
        Returns:
            The next chapter number (highest existing + 1, or 1 if none exist)
        """
        outline_files = list(self.outlines_dir.glob("chapter_*.txt"))
        
        if not outline_files:
            return 1
        
        # Extract chapter numbers
        chapter_numbers = []
        for file_path in outline_files:
            match = re.search(r'chapter_(\d+)\.txt', file_path.name)
            if match:
                chapter_numbers.append(int(match.group(1)))
        
        return max(chapter_numbers, default=0) + 1
    
    def get_chapter_info(self, chapter_number: int) -> ChapterInfo:
        """
        Get comprehensive information about a chapter.
        
        Args:
            chapter_number: The chapter number to analyze
            
        Returns:
            ChapterInfo object containing all available information
        """
        outline_path = self.outlines_dir / f"chapter_{chapter_number}.txt"
        draft_path = self.chapters_dir / f"chapter_{chapter_number}.md"
        
        word_count = None
        if draft_path.exists():
            try:
                with open(draft_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    word_count = len(content.split())
            except Exception as e:
                logger.warning(f"Could not read chapter {chapter_number} for word count: {e}")
        
        return ChapterInfo(
            number=chapter_number,
            outline_exists=outline_path.exists(),
            draft_exists=draft_path.exists(),
            outline_path=outline_path if outline_path.exists() else None,
            draft_path=draft_path if draft_path.exists() else None,
            word_count=word_count
        )
    
    def list_chapters(self) -> List[ChapterInfo]:
        """
        List all chapters with their information.
        
        Returns:
            List of ChapterInfo objects for all discovered chapters
        """
        # Get all chapter numbers from both outlines and drafts
        all_numbers = set()
        
        # From outlines
        for file_path in self.outlines_dir.glob("chapter_*.txt"):
            match = re.search(r'chapter_(\d+)\.txt', file_path.name)
            if match:
                all_numbers.add(int(match.group(1)))
        
        # From drafts
        for file_path in self.chapters_dir.glob("chapter_*.md"):
            match = re.search(r'chapter_(\d+)\.md', file_path.name)
            if match:
                all_numbers.add(int(match.group(1)))
        
        # Get info for all chapters and sort
        chapters = [self.get_chapter_info(num) for num in sorted(all_numbers)]
        return chapters
    
    def save_chapter_content(self, chapter_number: int, content: str, validate: bool = True) -> Path:
        """
        Save chapter content to file.
        
        Args:
            chapter_number: The chapter number
            content: The chapter content to save
            validate: Whether to validate content before saving
            
        Returns:
            Path to the saved file
            
        Raises:
            ValueError: If content validation fails
        """
        output_path = self.chapters_dir / f"chapter_{chapter_number}.md"
        
        if validate:
            from .validation import ContentValidator
            validator = ContentValidator()
            issues = validator.validate_chapter_content(content)
            if issues:
                logger.warning(f"Content validation issues for Chapter {chapter_number}: {issues}")
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Chapter {chapter_number} saved to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to save chapter {chapter_number}: {e}")
            raise
    
    def load_chapter_content(self, chapter_number: int) -> str:
        """
        Load chapter content from file.
        
        Args:
            chapter_number: The chapter number to load
            
        Returns:
            The chapter content
            
        Raises:
            FileNotFoundError: If the chapter file doesn't exist
        """
        chapter_path = self.chapters_dir / f"chapter_{chapter_number}.md"
        
        if not chapter_path.exists():
            raise FileNotFoundError(f"Chapter {chapter_number} not found at {chapter_path}")
        
        with open(chapter_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def save_outline(self, chapter_number: int, outline: str) -> Path:
        """
        Save chapter outline to file.
        
        Args:
            chapter_number: The chapter number
            outline: The outline content to save
            
        Returns:
            Path to the saved outline file
        """
        outline_path = self.outlines_dir / f"chapter_{chapter_number}.txt"
        
        try:
            with open(outline_path, 'w', encoding='utf-8') as f:
                f.write(outline)
            logger.info(f"Outline for Chapter {chapter_number} saved to: {outline_path}")
            return outline_path
        except Exception as e:
            logger.error(f"Failed to save outline for chapter {chapter_number}: {e}")
            raise
    
    def load_outline(self, chapter_number: int) -> str:
        """
        Load chapter outline from file.
        
        Args:
            chapter_number: The chapter number to load outline for
            
        Returns:
            The outline content
            
        Raises:
            FileNotFoundError: If the outline file doesn't exist
        """
        outline_path = self.outlines_dir / f"chapter_{chapter_number}.txt"
        
        if not outline_path.exists():
            raise FileNotFoundError(f"Outline for Chapter {chapter_number} not found at {outline_path}")
        
        with open(outline_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def outline_exists(self, chapter_number: int) -> bool:
        """
        Check if an outline exists for the given chapter.
        
        Args:
            chapter_number: The chapter number to check
            
        Returns:
            True if outline exists, False otherwise
        """
        outline_path = self.outlines_dir / f"chapter_{chapter_number}.txt"
        return outline_path.exists()
    
    def chapter_exists(self, chapter_number: int) -> bool:
        """
        Check if a chapter draft exists for the given chapter.
        
        Args:
            chapter_number: The chapter number to check
            
        Returns:
            True if chapter exists, False otherwise
        """
        chapter_path = self.chapters_dir / f"chapter_{chapter_number}.md"
        return chapter_path.exists()
