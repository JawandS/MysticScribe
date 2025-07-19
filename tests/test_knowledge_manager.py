"""
Test the refactored Knowledge Manager functionality.
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from src.mysticscribe.core import KnowledgeManager


class TestKnowledgeManager:
    """Test suite for KnowledgeManager class."""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create a temporary project directory with test knowledge files."""
        temp_dir = Path(tempfile.mkdtemp())
        knowledge_dir = temp_dir / "knowledge"
        knowledge_dir.mkdir()
        
        # Create test knowledge files
        test_files = {
            "core_story_elements.txt": "Main character: Hero\nTheme: Good vs Evil",
            "plot.txt": "Act 1: Setup\nAct 2: Conflict\nAct 3: Resolution",
            "cultivation_system.txt": "Power Level 1: Novice\nPower Level 2: Advanced",
        }
        
        for filename, content in test_files.items():
            (knowledge_dir / filename).write_text(content)
        
        yield temp_dir
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def knowledge_manager(self, temp_project_root):
        """Create a KnowledgeManager instance for testing."""
        return KnowledgeManager(temp_project_root)
    
    def test_initialization(self, knowledge_manager, temp_project_root):
        """Test KnowledgeManager initialization."""
        assert knowledge_manager.project_root == temp_project_root
        assert knowledge_manager.knowledge_dir == temp_project_root / "knowledge"
    
    def test_load_knowledge_file_existing(self, knowledge_manager):
        """Test loading an existing knowledge file."""
        content = knowledge_manager.load_knowledge_file("core_story_elements.txt")
        assert content is not None
        assert "Main character: Hero" in content
        assert "Theme: Good vs Evil" in content
    
    def test_load_knowledge_file_nonexistent(self, knowledge_manager):
        """Test loading a non-existent knowledge file."""
        content = knowledge_manager.load_knowledge_file("nonexistent.txt")
        assert content is None
    
    def test_get_available_files(self, knowledge_manager):
        """Test getting list of available knowledge files."""
        available = knowledge_manager.get_available_files()
        
        # Should include files that exist from our test setup
        assert "core_story_elements.txt" in available
        assert "plot.txt" in available
        assert "cultivation_system.txt" in available
        
        # Should not include files that don't exist
        assert "nonexistent.txt" not in available
    
    def test_get_missing_files(self, knowledge_manager):
        """Test getting list of missing knowledge files."""
        missing = knowledge_manager.get_missing_files()
        
        # Should include files from KNOWLEDGE_FILES that don't exist
        assert "chapters.txt" in missing  # This wasn't created in our test setup
        assert "regions.txt" in missing
        
        # Should not include files that do exist
        assert "core_story_elements.txt" not in missing
    
    def test_validate_knowledge_base(self, knowledge_manager):
        """Test validating the knowledge base completeness."""
        status = knowledge_manager.validate_knowledge_base()
        
        assert isinstance(status, dict)
        assert status["core_story_elements.txt"] is True
        assert status["plot.txt"] is True
        assert status["cultivation_system.txt"] is True
        assert status["chapters.txt"] is False  # Doesn't exist in test setup
    
    def test_get_knowledge_summary(self, knowledge_manager):
        """Test getting knowledge base summary."""
        summary = knowledge_manager.get_knowledge_summary()
        
        assert isinstance(summary, dict)
        assert "total_files" in summary
        assert "available_files" in summary
        assert "missing_files" in summary
        assert "completeness_percentage" in summary
        
        # We have 3 out of 10 total files
        assert summary["available_files"] == 3
        assert summary["missing_files"] == 7
        assert summary["completeness_percentage"] == 30.0
    
    def test_load_all_knowledge(self, knowledge_manager):
        """Test loading all knowledge into a formatted context."""
        context = knowledge_manager.load_all_knowledge()
        
        assert "=== STORY KNOWLEDGE BASE ===" in context
        assert "=== CORE_STORY_ELEMENTS ===" in context
        assert "=== PLOT ===" in context
        assert "Main character: Hero" in context
        assert "Act 1: Setup" in context
    
    def test_search_knowledge(self, knowledge_manager):
        """Test searching across knowledge files."""
        # Search for existing term
        results = knowledge_manager.search_knowledge("Hero")
        assert len(results) > 0
        assert "core_story_elements.txt" in results
        
        # Search for non-existent term
        results = knowledge_manager.search_knowledge("NonexistentTerm")
        assert len(results) == 0
        
        # Case-insensitive search
        results = knowledge_manager.search_knowledge("hero", case_sensitive=False)
        assert len(results) > 0
        
        results = knowledge_manager.search_knowledge("hero", case_sensitive=True)
        assert len(results) == 0  # "hero" != "Hero"
    
    def test_empty_knowledge_directory(self):
        """Test behavior with empty knowledge directory."""
        temp_dir = Path(tempfile.mkdtemp())
        try:
            # Don't create knowledge directory
            knowledge_manager = KnowledgeManager(temp_dir)
            
            # Should handle missing directory gracefully
            assert knowledge_manager.get_available_files() == []
            assert len(knowledge_manager.get_missing_files()) == len(KnowledgeManager.KNOWLEDGE_FILES)
            
            context = knowledge_manager.load_all_knowledge()
            assert context == "=== STORY KNOWLEDGE BASE ===\n\n"
            
        finally:
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__])
