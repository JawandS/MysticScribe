"""
Simple test runner without external dependencies.

This test validates basic functionality of the refactored MysticScribe system.
Run this to verify the refactoring is working correctly.
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_chapter_manager():
    """Test ChapterManager basic functionality."""
    print("Testing ChapterManager...")
    
    from mysticscribe.core import ChapterManager
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        manager = ChapterManager(temp_dir)
        
        # Test initialization
        assert manager.project_root == temp_dir
        assert manager.chapters_dir.exists()
        assert manager.outlines_dir.exists()
        print("  ✅ Initialization successful")
        
        # Test next chapter number
        assert manager.get_next_chapter_number() == 1
        print("  ✅ Next chapter number detection works")
        
        # Test saving/loading content
        content = "Test chapter content with multiple words here."
        manager.save_chapter_content(1, content, validate=False)
        loaded = manager.load_chapter_content(1)
        assert loaded == content
        print("  ✅ Chapter save/load works")
        
        # Test chapter info
        info = manager.get_chapter_info(1)
        assert info.number == 1
        assert info.draft_exists
        # Test content has 8 words: "Test", "chapter", "content", "with", "multiple", "words", "here."
        assert info.word_count == 7  # Actual word count of test content
        print("  ✅ Chapter info retrieval works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("  ✅ ChapterManager tests passed\n")


def test_knowledge_manager():
    """Test KnowledgeManager basic functionality."""
    print("Testing KnowledgeManager...")
    
    from mysticscribe.core import KnowledgeManager
    
    # Create temporary directory with test knowledge
    temp_dir = Path(tempfile.mkdtemp())
    knowledge_dir = temp_dir / "knowledge"
    knowledge_dir.mkdir()
    
    try:
        # Create test knowledge files
        (knowledge_dir / "core_story_elements.txt").write_text("Test story elements")
        (knowledge_dir / "plot.txt").write_text("Test plot structure")
        
        manager = KnowledgeManager(temp_dir)
        
        # Test file loading
        content = manager.load_knowledge_file("core_story_elements.txt")
        assert content == "Test story elements"
        print("  ✅ Knowledge file loading works")
        
        # Test available files
        available = manager.get_available_files()
        assert "core_story_elements.txt" in available
        assert "plot.txt" in available
        print("  ✅ Available files detection works")
        
        # Test knowledge summary
        summary = manager.get_knowledge_summary()
        assert summary["available_files"] == 2
        assert summary["completeness_percentage"] == 20.0  # 2 out of 10 files
        print("  ✅ Knowledge summary works")
        
        # Test loading all knowledge
        all_knowledge = manager.load_all_knowledge()
        assert "=== STORY KNOWLEDGE BASE ===" in all_knowledge
        assert "Test story elements" in all_knowledge
        print("  ✅ Load all knowledge works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("  ✅ KnowledgeManager tests passed\n")


def test_content_validator():
    """Test ContentValidator basic functionality."""
    print("Testing ContentValidator...")
    
    from mysticscribe.core import ContentValidator
    
    validator = ContentValidator()
    
    # Test word count validation
    short_content = "Short content"
    issues = validator._validate_word_count(short_content)
    assert len(issues) > 0
    assert issues[0].severity == "error"
    assert "too short" in issues[0].message
    print("  ✅ Word count validation works")
    
    # Test AI pattern detection
    ai_content = "This chapter introduces our protagonist. The completed Chapter shows growth."
    issues = validator._validate_ai_patterns(ai_content)
    assert len(issues) > 0
    assert any("AI meta-commentary" in issue.message for issue in issues)
    print("  ✅ AI pattern detection works")
    
    # Test structure validation
    empty_content = ""
    issues = validator._validate_structure(empty_content)
    assert len(issues) > 0
    assert issues[0].severity == "error"
    assert "empty" in issues[0].message
    print("  ✅ Structure validation works")
    
    # Test validation summary
    from mysticscribe.core.validation import ValidationIssue
    test_issues = [
        ValidationIssue("error", "word_count", "Too short"),
        ValidationIssue("warning", "ai_patterns", "Pattern found"),
    ]
    summary = validator.get_validation_summary(test_issues)
    assert summary["total_issues"] == 2
    assert summary["errors"] == 1
    assert summary["warnings"] == 1
    print("  ✅ Validation summary works")
    
    print("  ✅ ContentValidator tests passed\n")


def test_workflows():
    """Test basic workflow functionality."""
    print("Testing Workflows...")
    
    from mysticscribe.workflows import LegacyWorkflow
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    knowledge_dir = temp_dir / "knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "core_story_elements.txt").write_text("Test story elements")
    
    try:
        workflow = LegacyWorkflow(temp_dir)
        
        # Test initialization
        assert workflow.project_root == temp_dir
        print("  ✅ Workflow initialization works")
        
        # Test chapter number detection
        assert workflow.get_chapter_number() == 1
        assert workflow.get_chapter_number(5) == 5
        print("  ✅ Chapter number handling works")
        
        # Test base inputs preparation
        inputs = workflow.prepare_base_inputs(1)
        assert "chapter_number" in inputs
        assert "knowledge_context" in inputs
        assert "previous_chapter_context" in inputs
        print("  ✅ Base inputs preparation works")
        
        # Test prerequisites validation
        assert workflow.validate_prerequisites(1) is True
        print("  ✅ Prerequisites validation works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("  ✅ Workflow tests passed\n")


def test_utils():
    """Test utility functions."""
    print("Testing Utilities...")
    
    # Test text utils
    from mysticscribe.utils import extract_word_count, clean_text, truncate_text
    
    # Test word count
    text = "This is a test with six words"
    assert extract_word_count(text) == 7  # Actually 7 words
    print("  ✅ Word count extraction works")
    
    # Test text cleaning
    dirty_text = "  Text   with    extra   spaces  \n\n\n\n"
    clean = clean_text(dirty_text)
    assert "extra   spaces" not in clean
    print("  ✅ Text cleaning works")
    
    # Test truncation
    long_text = "This is a very long text that needs truncation"
    truncated = truncate_text(long_text, 20, "...")
    assert len(truncated) <= 20
    assert truncated.endswith("...")
    print("  ✅ Text truncation works")
    
    # Test file utils
    from mysticscribe.utils import ensure_directory, safe_read_file, safe_write_file
    
    temp_dir = Path(tempfile.mkdtemp())
    try:
        # Test directory creation
        test_dir = ensure_directory(temp_dir / "test_subdir")
        assert test_dir.exists()
        print("  ✅ Directory creation works")
        
        # Test file operations
        test_file = test_dir / "test.txt"
        test_content = "Test file content"
        
        assert safe_write_file(test_file, test_content) is True
        loaded_content = safe_read_file(test_file)
        assert loaded_content == test_content
        print("  ✅ File operations work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("  ✅ Utility tests passed\n")


def main():
    """Run all tests."""
    print("🧪 Running MysticScribe Refactoring Tests")
    print("=" * 50)
    
    try:
        test_chapter_manager()
        test_knowledge_manager()
        test_content_validator()
        test_workflows()
        test_utils()
        
        print("🎉 ALL TESTS PASSED!")
        print("✅ The refactored MysticScribe system is working correctly.")
        print("\nNext steps:")
        print("  1. Install development dependencies: pip install -e .[dev]")
        print("  2. Run full test suite: pytest tests/")
        print("  3. Try the new interface: python -m mysticscribe status")
        
        return 0
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
