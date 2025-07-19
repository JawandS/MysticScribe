"""
Test the simplified MysticScribe system.

This tests the main mysticscribe.py entry point and core functionality.
"""

import tempfile
import shutil
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Optional pytest import
try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False
    # Create a minimal pytest fixture decorator for compatibility
    def pytest_fixture(func):
        return func
    pytest = type('pytest', (), {'fixture': staticmethod(pytest_fixture)})()

# Add the project root to sys.path to import mysticscribe
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import mysticscribe


class TestMysticScribeCore:
    """Test core MysticScribe functionality."""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create a temporary project directory."""
        temp_dir = Path(tempfile.mkdtemp())
        
        # Create required directories
        (temp_dir / "chapters").mkdir()
        (temp_dir / "knowledge").mkdir()
        (temp_dir / "src").mkdir()
        
        # Create knowledge files
        knowledge_dir = temp_dir / "knowledge"
        (knowledge_dir / "core_story_elements.txt").write_text("Test story elements")
        (knowledge_dir / "plot.txt").write_text("Test plot")
        
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_get_next_chapter_number_empty_directory(self, temp_project_root):
        """Test chapter number detection with no existing chapters."""
        result = mysticscribe.get_next_chapter_number(temp_project_root)
        assert result == 1
    
    def test_get_next_chapter_number_with_existing_chapters(self, temp_project_root):
        """Test chapter number detection with existing chapters."""
        chapters_dir = temp_project_root / "chapters"
        
        # Create some chapter files
        (chapters_dir / "chapter_1.md").write_text("Chapter 1 content")
        (chapters_dir / "chapter_3.md").write_text("Chapter 3 content")
        (chapters_dir / "chapter_5.md").write_text("Chapter 5 content")
        
        result = mysticscribe.get_next_chapter_number(temp_project_root)
        assert result == 6  # Should be highest (5) + 1
    
    def test_load_knowledge_context(self, temp_project_root):
        """Test loading knowledge context from files."""
        result = mysticscribe.load_knowledge_context(temp_project_root)
        
        assert "core_story_elements.txt" in result
        assert "plot.txt" in result
        assert "Test story elements" in result
        assert "Test plot" in result
    
    def test_get_previous_chapter_context_chapter_1(self, temp_project_root):
        """Test previous chapter context for Chapter 1."""
        result = mysticscribe.get_previous_chapter_context(1, temp_project_root)
        assert "This is Chapter 1" in result
        assert "no previous chapters" in result
    
    def test_get_previous_chapter_context_with_previous(self, temp_project_root):
        """Test previous chapter context with existing previous chapter."""
        chapters_dir = temp_project_root / "chapters"
        (chapters_dir / "chapter_1.md").write_text("Previous chapter content here")
        
        result = mysticscribe.get_previous_chapter_context(2, temp_project_root)
        assert "Previous chapter content here" in result
        assert "Previous Chapter (1)" in result
    
    def test_validate_chapter_content(self, capsys):
        """Test chapter content validation."""
        # Test normal content
        normal_content = " ".join(["word"] * 2500)  # 2500 words
        mysticscribe.validate_chapter_content(normal_content, 1)
        
        captured = capsys.readouterr()
        assert "Word count within recommended range" in captured.out
        
        # Test short content
        short_content = " ".join(["word"] * 1000)  # 1000 words
        mysticscribe.validate_chapter_content(short_content, 2)
        
        captured = capsys.readouterr()
        assert "WARNING" in captured.out
        assert "1000 words" in captured.out
    
    def test_validate_chapter_content_ai_patterns(self, capsys):
        """Test AI pattern detection in content validation."""
        content_with_ai_patterns = "The completed Chapter 1 shows great promise. This chapter introduces..."
        
        mysticscribe.validate_chapter_content(content_with_ai_patterns, 1)
        
        captured = capsys.readouterr()
        assert "WARNING" in captured.out
        assert "AI meta-commentary" in captured.out


class TestMysticScribeIntegration:
    """Integration tests that require mocking external dependencies."""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create a temporary project directory with full structure."""
        temp_dir = Path(tempfile.mkdtemp())
        
        # Create full directory structure
        (temp_dir / "chapters").mkdir()
        (temp_dir / "knowledge").mkdir()
        (temp_dir / "src" / "mysticscribe").mkdir(parents=True)
        
        # Create knowledge files
        knowledge_dir = temp_dir / "knowledge"
        (knowledge_dir / "core_story_elements.txt").write_text("Test story elements")
        (knowledge_dir / "plot.txt").write_text("Test plot")
        
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @patch('mysticscribe.sys.path')
    def test_run_workflow_import_setup(self, mock_sys_path, temp_project_root):
        """Test that run_workflow sets up imports correctly."""
        with patch('mysticscribe.Mysticscribe') as mock_crew_class:
            mock_crew_instance = Mock()
            mock_crew_class.return_value = mock_crew_instance
            mock_crew_instance.crew().kickoff.return_value.raw = "Test chapter content"
            
            try:
                mysticscribe.run_workflow(1, temp_project_root)
            except Exception:
                pass  # We expect this to fail due to mocking, but we want to test the setup
            
            # Check that src path was added to sys.path
            src_path = temp_project_root / "src"
            mock_sys_path.insert.assert_called_with(0, str(src_path))


if __name__ == "__main__":
    # Simple test runner if pytest is not available
    import unittest
    
    # Convert pytest fixtures to unittest setUp
    class TestMysticScribeSimple(unittest.TestCase):
        
        def setUp(self):
            self.temp_dir = Path(tempfile.mkdtemp())
            (self.temp_dir / "chapters").mkdir()
            (self.temp_dir / "knowledge").mkdir()
            
            knowledge_dir = self.temp_dir / "knowledge"
            (knowledge_dir / "core_story_elements.txt").write_text("Test story elements")
            (knowledge_dir / "plot.txt").write_text("Test plot")
        
        def tearDown(self):
            shutil.rmtree(self.temp_dir)
        
        def test_get_next_chapter_number(self):
            result = mysticscribe.get_next_chapter_number(self.temp_dir)
            self.assertEqual(result, 1)
        
        def test_load_knowledge_context(self):
            result = mysticscribe.load_knowledge_context(self.temp_dir)
            self.assertIn("Test story elements", result)
            self.assertIn("Test plot", result)
    
    unittest.main()
