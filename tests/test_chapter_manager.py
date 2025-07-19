"""
Test the refactored Chapter Manager functionality.
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from src.mysticscribe.core import ChapterManager


class TestChapterManager:
    """Test suite for ChapterManager class."""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create a temporary project directory."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def chapter_manager(self, temp_project_root):
        """Create a ChapterManager instance for testing."""
        return ChapterManager(temp_project_root)
    
    def test_initialization(self, chapter_manager, temp_project_root):
        """Test ChapterManager initialization."""
        assert chapter_manager.project_root == temp_project_root
        assert chapter_manager.chapters_dir == temp_project_root / "chapters"
        assert chapter_manager.outlines_dir == temp_project_root / "outlines"
        
        # Directories should be created automatically
        assert chapter_manager.chapters_dir.exists()
        assert chapter_manager.outlines_dir.exists()
    
    def test_get_next_chapter_number_empty(self, chapter_manager):
        """Test getting next chapter number when no outlines exist."""
        assert chapter_manager.get_next_chapter_number() == 1
    
    def test_get_next_chapter_number_with_outlines(self, chapter_manager):
        """Test getting next chapter number with existing outlines."""
        # Create some outline files
        (chapter_manager.outlines_dir / "chapter_1.txt").touch()
        (chapter_manager.outlines_dir / "chapter_3.txt").touch()
        (chapter_manager.outlines_dir / "chapter_2.txt").touch()
        
        assert chapter_manager.get_next_chapter_number() == 4
    
    def test_save_and_load_chapter_content(self, chapter_manager):
        """Test saving and loading chapter content."""
        content = "This is test chapter content with multiple paragraphs.\n\nSecond paragraph here."
        chapter_number = 1
        
        # Save content
        saved_path = chapter_manager.save_chapter_content(chapter_number, content, validate=False)
        assert saved_path.exists()
        assert saved_path.name == "chapter_1.md"
        
        # Load content
        loaded_content = chapter_manager.load_chapter_content(chapter_number)
        assert loaded_content == content
    
    def test_save_and_load_outline(self, chapter_manager):
        """Test saving and loading outline content."""
        outline = "Chapter 1 Outline\n\n1. Introduction\n2. Rising action\n3. Climax"
        chapter_number = 1
        
        # Save outline
        saved_path = chapter_manager.save_outline(chapter_number, outline)
        assert saved_path.exists()
        assert saved_path.name == "chapter_1.txt"
        
        # Load outline
        loaded_outline = chapter_manager.load_outline(chapter_number)
        assert loaded_outline == outline
    
    def test_chapter_exists(self, chapter_manager):
        """Test checking if chapter exists."""
        assert not chapter_manager.chapter_exists(1)
        
        # Create a chapter
        chapter_manager.save_chapter_content(1, "Test content", validate=False)
        assert chapter_manager.chapter_exists(1)
    
    def test_outline_exists(self, chapter_manager):
        """Test checking if outline exists."""
        assert not chapter_manager.outline_exists(1)
        
        # Create an outline
        chapter_manager.save_outline(1, "Test outline")
        assert chapter_manager.outline_exists(1)
    
    def test_get_chapter_info(self, chapter_manager):
        """Test getting comprehensive chapter information."""
        chapter_number = 1
        
        # Initially no chapter or outline
        info = chapter_manager.get_chapter_info(chapter_number)
        assert info.number == chapter_number
        assert not info.outline_exists
        assert not info.draft_exists
        assert info.outline_path is None
        assert info.draft_path is None
        assert info.word_count is None
        
        # Create outline
        chapter_manager.save_outline(chapter_number, "Test outline")
        info = chapter_manager.get_chapter_info(chapter_number)
        assert info.outline_exists
        assert info.outline_path is not None
        
        # Create chapter
        chapter_content = "This is a test chapter with some words to count."
        chapter_manager.save_chapter_content(chapter_number, chapter_content, validate=False)
        info = chapter_manager.get_chapter_info(chapter_number)
        assert info.draft_exists
        assert info.draft_path is not None
        assert info.word_count == 11  # Word count of the test content
    
    def test_list_chapters(self, chapter_manager):
        """Test listing all chapters."""
        # Initially empty
        chapters = chapter_manager.list_chapters()
        assert len(chapters) == 0
        
        # Create some chapters and outlines
        chapter_manager.save_outline(1, "Outline 1")
        chapter_manager.save_chapter_content(1, "Chapter 1 content", validate=False)
        chapter_manager.save_outline(3, "Outline 3")
        
        chapters = chapter_manager.list_chapters()
        assert len(chapters) == 2
        
        # Should be sorted by chapter number
        assert chapters[0].number == 1
        assert chapters[1].number == 3
        
        # Check chapter 1 info
        assert chapters[0].outline_exists
        assert chapters[0].draft_exists
        
        # Check chapter 3 info
        assert chapters[1].outline_exists
        assert not chapters[1].draft_exists
    
    def test_load_nonexistent_files(self, chapter_manager):
        """Test loading files that don't exist."""
        with pytest.raises(FileNotFoundError):
            chapter_manager.load_chapter_content(999)
        
        with pytest.raises(FileNotFoundError):
            chapter_manager.load_outline(999)


if __name__ == "__main__":
    pytest.main([__file__])
