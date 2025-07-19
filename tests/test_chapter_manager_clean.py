"""
Test the refactored Chapter Manager functionality.
"""

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    
import tempfile
import shutil
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mysticscribe.core import ChapterManager

if PYTEST_AVAILABLE:
    class TestChapterManager:
        """Test suite for ChapterManager class."""
        
        def test_initialization(self, temp_project_root):
            """Test ChapterManager initialization."""
            manager = ChapterManager(temp_project_root)
            
            assert manager.project_root == temp_project_root
            assert manager.chapters_dir.exists()
            assert manager.outlines_dir.exists()
        
        def test_get_next_chapter_number(self, temp_project_root):
            """Test next chapter number detection."""
            manager = ChapterManager(temp_project_root)
            
            # Should be 1 with no chapters
            assert manager.get_next_chapter_number() == 1
            
            # Create some chapters
            (temp_project_root / "chapters" / "chapter_1.md").write_text("Chapter 1")
            (temp_project_root / "chapters" / "chapter_3.md").write_text("Chapter 3")
            
            # Should be 4 (next after highest)
            assert manager.get_next_chapter_number() == 4
        
        def test_save_and_load_chapter(self, temp_project_root):
            """Test chapter save and load operations."""
            manager = ChapterManager(temp_project_root)
            
            test_content = "# Test Chapter\n\nThis is test content."
            
            # Save chapter
            result = manager.save_chapter(5, test_content)
            assert result is True
            
            # Load chapter
            loaded_content = manager.load_chapter(5)
            assert test_content in loaded_content
        
        def test_get_chapter_info(self, temp_project_root, sample_chapters):
            """Test chapter info retrieval."""
            manager = ChapterManager(temp_project_root)
            
            # Test existing chapter
            info = manager.get_chapter_info(1)
            assert info['number'] == 1
            assert info['exists'] is True
            assert info['word_count'] > 0
            
            # Test non-existing chapter
            info = manager.get_chapter_info(99)
            assert info['number'] == 99
            assert info['exists'] is False
            assert info['word_count'] == 0
        
        def test_chapter_management(self, temp_project_root):
            """Test comprehensive chapter management."""
            manager = ChapterManager(temp_project_root)
            
            # Create multiple chapters
            chapters = {
                1: "# Chapter 1\n\nFirst chapter content.",
                2: "# Chapter 2\n\nSecond chapter content.",
                3: "# Chapter 3\n\nThird chapter content."
            }
            
            for num, content in chapters.items():
                manager.save_chapter(num, content)
            
            # Test all chapters exist
            for num in chapters.keys():
                info = manager.get_chapter_info(num)
                assert info['exists'] is True
                assert info['word_count'] > 0
            
            # Test next chapter number
            assert manager.get_next_chapter_number() == 4

else:
    # Fallback tests without pytest
    def test_chapter_manager_standalone():
        """Standalone test for ChapterManager without pytest."""
        temp_dir = Path(tempfile.mkdtemp())
        
        try:
            # Create directory structure
            (temp_dir / "chapters").mkdir()
            (temp_dir / "outlines").mkdir()
            
            manager = ChapterManager(temp_dir)
            
            # Test initialization
            assert manager.project_root == temp_dir
            assert manager.chapters_dir.exists()
            
            # Test save and load
            test_content = "# Test Chapter\n\nTest content"
            manager.save_chapter(1, test_content)
            loaded = manager.load_chapter(1)
            assert test_content in loaded
            
            # Test next chapter number
            assert manager.get_next_chapter_number() == 2
            
            print("✅ ChapterManager standalone tests passed")
            return True
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__" and not PYTEST_AVAILABLE:
    test_chapter_manager_standalone()
