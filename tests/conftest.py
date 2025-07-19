"""
Test configuration and shared fixtures for MysticScribe tests.
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
import os

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

if PYTEST_AVAILABLE:
    @pytest.fixture
    def temp_project_root():
        """Create a temporary project directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        
        # Create basic directory structure
        (temp_dir / "chapters").mkdir()
        (temp_dir / "knowledge").mkdir()
        (temp_dir / "outlines").mkdir()
        (temp_dir / "styles").mkdir()
        
        yield temp_dir
        
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def sample_knowledge_files(temp_project_root):
        """Create sample knowledge files for testing."""
        knowledge_dir = temp_project_root / "knowledge"
        
        # Create minimal knowledge files
        knowledge_files = {
            'core_story_elements.txt': 'Sample story elements for testing.',
            'plot.txt': 'Sample plot information for testing.',
            'cultivation_system.txt': 'Sample cultivation system details.',
            'regions.txt': 'Sample region descriptions.',
            'society.txt': 'Sample society structure.',
            'government.txt': 'Sample government information.',
            'economic.txt': 'Sample economic system.',
            'military.txt': 'Sample military structure.',
            'knowledge_system_overview.txt': 'Sample knowledge overview.',
            'chapters.txt': 'Sample chapter summaries.'
        }
        
        for filename, content in knowledge_files.items():
            (knowledge_dir / filename).write_text(content)
        
        return knowledge_dir

    @pytest.fixture
    def sample_chapters(temp_project_root):
        """Create sample chapter files for testing."""
        chapters_dir = temp_project_root / "chapters"
        
        chapter1_content = """# Chapter 1: Test Chapter

This is a sample chapter for testing purposes. It contains some dialogue.

"Hello there," the character said.

The wind howled through the trees like a wild beast.
"""
        
        chapter2_content = """# Chapter 2: Another Test Chapter

This is another sample chapter. It has different patterns.

"How are you?" she asked softly.

The rain pattered against the window with gentle persistence.
"""
        
        (chapters_dir / "chapter_1.md").write_text(chapter1_content)
        (chapters_dir / "chapter_2.md").write_text(chapter2_content)
        
        return chapters_dir

    def pytest_configure(config):
        """Configure pytest with custom markers."""
        config.addinivalue_line(
            "markers", "integration: mark test as an integration test"
        )
        config.addinivalue_line(
            "markers", "slow: mark test as slow running"
        )
