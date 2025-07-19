"""
Test the Content Validation functionality.
"""

import pytest
from src.mysticscribe.core import ContentValidator, ValidationIssue


class TestContentValidator:
    """Test suite for ContentValidator class."""
    
    @pytest.fixture
    def validator(self):
        """Create a ContentValidator instance for testing."""
        return ContentValidator()
    
    def test_validation_issue_creation(self):
        """Test creating ValidationIssue objects."""
        issue = ValidationIssue(
            severity="warning",
            category="word_count", 
            message="Chapter is too short",
            line_number=5
        )
        
        assert issue.severity == "warning"
        assert issue.category == "word_count"
        assert issue.message == "Chapter is too short"
        assert issue.line_number == 5
    
    def test_word_count_validation_success(self, validator):
        """Test word count validation within target range."""
        # Create content with around 2500 words (target range)
        content = " ".join(["word"] * 2500)
        issues = validator._validate_word_count(content)
        
        # Should have one info issue about word count being in range
        assert len(issues) == 1
        assert issues[0].severity == "info"
        assert issues[0].category == "word_count"
        assert "within target range" in issues[0].message
    
    def test_word_count_validation_too_short(self, validator):
        """Test word count validation for too short content."""
        # Create content with 1000 words (below minimum)
        content = " ".join(["word"] * 1000)
        issues = validator._validate_word_count(content)
        
        assert len(issues) == 1
        assert issues[0].severity == "error"
        assert issues[0].category == "word_count"
        assert "too short" in issues[0].message
    
    def test_word_count_validation_too_long(self, validator):
        """Test word count validation for too long content."""
        # Create content with 5000 words (above maximum)
        content = " ".join(["word"] * 5000)
        issues = validator._validate_word_count(content)
        
        assert len(issues) == 1
        assert issues[0].severity == "error"
        assert issues[0].category == "word_count"
        assert "too long" in issues[0].message
    
    def test_ai_pattern_detection(self, validator):
        """Test detection of AI-generated patterns."""
        content_with_patterns = """
        This chapter introduces our protagonist who faces challenges.
        The completed Chapter will show character development.
        Here is Chapter 5 of our story.
        """
        
        issues = validator._validate_ai_patterns(content_with_patterns)
        
        # Should detect multiple AI patterns
        assert len(issues) >= 2
        for issue in issues:
            assert issue.severity == "warning"
            assert issue.category == "ai_patterns"
            assert "AI meta-commentary pattern" in issue.message
    
    def test_ai_pattern_detection_clean_content(self, validator):
        """Test AI pattern detection on clean content."""
        clean_content = """
        Sarah walked through the forest, her footsteps echoing on the path.
        The wind whispered through the leaves above her head.
        "Where am I going?" she wondered aloud.
        """
        
        issues = validator._validate_ai_patterns(clean_content)
        assert len(issues) == 0
    
    def test_structure_validation_empty_content(self, validator):
        """Test structure validation on empty content."""
        issues = validator._validate_structure("")
        
        assert len(issues) == 1
        assert issues[0].severity == "error"
        assert issues[0].category == "structure"
        assert "empty" in issues[0].message
    
    def test_structure_validation_few_paragraphs(self, validator):
        """Test structure validation on content with few paragraphs."""
        content = "Short paragraph one.\n\nShort paragraph two."
        issues = validator._validate_structure(content)
        
        # Should warn about few paragraphs
        paragraph_issues = [i for i in issues if "paragraphs" in i.message]
        assert len(paragraph_issues) >= 1
        assert paragraph_issues[0].severity == "warning"
    
    def test_structure_validation_no_dialogue(self, validator):
        """Test structure validation on content without dialogue."""
        content = "This is a chapter without any dialogue. It has multiple paragraphs.\n\nSecond paragraph continues the narrative.\n\nThird paragraph concludes."
        issues = validator._validate_structure(content)
        
        # Should note lack of dialogue
        dialogue_issues = [i for i in issues if "dialogue" in i.message]
        assert len(dialogue_issues) == 1
        assert dialogue_issues[0].severity == "info"
    
    def test_content_quality_validation(self, validator):
        """Test content quality validation."""
        # Content with repetitive sentence starts
        repetitive_content = """
        The hero walked forward. The hero looked around. The hero stopped suddenly.
        The hero walked forward again. The hero was confused. The hero decided to rest.
        """
        
        issues = validator._validate_content_quality(repetitive_content)
        
        # Should detect repetitive patterns
        repetitive_issues = [i for i in issues if "repetitive" in i.message.lower()]
        assert len(repetitive_issues) >= 1
        assert repetitive_issues[0].severity == "warning"
        assert repetitive_issues[0].category == "quality"
    
    def test_comprehensive_validation(self, validator):
        """Test comprehensive validation on good content."""
        good_content = """
        Sarah emerged from the shadows of the ancient forest, her breath visible in the cold morning air. The path ahead wound between towering oaks whose branches formed a natural cathedral overhead. She had been walking for hours, following the cryptic directions from the mysterious letter.

        "This must be the place," she whispered, stopping before a moss-covered stone archway. Strange symbols were carved into its surface, glowing faintly with an inner light. The air hummed with magical energy, making her skin tingle with anticipation.

        As she stepped through the archway, the world around her shifted. The forest transformed into a vast meadow filled with luminescent flowers that chimed softly in the breeze. In the distance, she could see a crystal tower reaching toward the sky, its faceted walls reflecting rainbow patterns across the landscape.

        Her journey to find the Lost Library of Arcanum had finally begun. Whatever challenges lay ahead, she knew there was no turning back now. The fate of her village depended on the knowledge hidden within those ancient halls.
        """ * 12  # Repeat to get good word count
        
        issues = validator.validate_chapter_content(good_content)
        
        # Should have minimal issues, mostly just info about word count
        error_issues = [i for i in issues if i.severity == "error"]
        assert len(error_issues) == 0
        
        # Should have info about word count being good
        info_issues = [i for i in issues if i.severity == "info" and "word count" in i.message]
        assert len(info_issues) >= 1
    
    def test_validation_summary(self, validator):
        """Test validation summary generation."""
        issues = [
            ValidationIssue("error", "word_count", "Too short"),
            ValidationIssue("warning", "ai_patterns", "Pattern found"),
            ValidationIssue("warning", "quality", "Repetitive"),
            ValidationIssue("info", "structure", "No dialogue"),
        ]
        
        summary = validator.get_validation_summary(issues)
        
        assert summary["total_issues"] == 4
        assert summary["errors"] == 1
        assert summary["warnings"] == 2
        assert summary["info"] == 1
        
        assert summary["by_category"]["word_count"] == 1
        assert summary["by_category"]["ai_patterns"] == 1
        assert summary["by_category"]["quality"] == 1
        assert summary["by_category"]["structure"] == 1
    
    def test_format_validation_report(self, validator):
        """Test formatting validation report."""
        issues = [
            ValidationIssue("error", "word_count", "Too short", 1),
            ValidationIssue("warning", "ai_patterns", "Pattern found", 5),
            ValidationIssue("info", "structure", "No dialogue"),
        ]
        
        report = validator.format_validation_report(issues)
        
        assert "❌ ERRORS:" in report
        assert "⚠️  WARNINGS:" in report
        assert "ℹ️  INFO:" in report
        assert "Too short (Line 1)" in report
        assert "Pattern found (Line 5)" in report
        assert "No dialogue" in report
    
    def test_format_validation_report_no_issues(self, validator):
        """Test formatting validation report with no issues."""
        report = validator.format_validation_report([])
        assert "✅ Content validation passed" in report


if __name__ == "__main__":
    pytest.main([__file__])
