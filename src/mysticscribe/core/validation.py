"""
Content Validation System

Validates generated chapter content for quality, word count, and common issues.
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ValidationIssue:
    """Represents a validation issue found in content."""
    severity: str  # 'warning', 'error', 'info'
    category: str  # 'word_count', 'ai_patterns', 'formatting', etc.
    message: str
    line_number: Optional[int] = None


class ContentValidator:
    """
    Validates chapter content for quality, structure, and common issues.
    
    This class performs various checks on generated content to ensure
    it meets quality standards and doesn't contain common AI generation artifacts.
    """
    
    # AI patterns that shouldn't appear in final content
    AI_PATTERNS = [
        "The completed Chapter",
        "This chapter",
        "In this chapter", 
        "The following chapter",
        "Chapter Summary:",
        "**Chapter",
        "Here is Chapter",
        "Here's Chapter",
        "The story continues",
        "This story",
        "Our protagonist",
        "Our hero",
        "Our main character"
    ]
    
    # Word count ranges
    MIN_WORD_COUNT = 1800
    TARGET_MIN_WORD_COUNT = 2000
    TARGET_MAX_WORD_COUNT = 4000
    MAX_WORD_COUNT = 4200
    
    def __init__(self):
        """Initialize the Content Validator."""
        pass
    
    def validate_chapter_content(self, content: str) -> List[ValidationIssue]:
        """
        Validate chapter content comprehensively.
        
        Args:
            content: The chapter content to validate
            
        Returns:
            List of validation issues found
        """
        issues = []
        
        # Word count validation
        issues.extend(self._validate_word_count(content))
        
        # AI pattern validation
        issues.extend(self._validate_ai_patterns(content))
        
        # Structure validation
        issues.extend(self._validate_structure(content))
        
        # Content quality validation
        issues.extend(self._validate_content_quality(content))
        
        return issues
    
    def _validate_word_count(self, content: str) -> List[ValidationIssue]:
        """Validate word count is within acceptable range."""
        issues = []
        word_count = len(content.split())
        
        if word_count < self.MIN_WORD_COUNT:
            issues.append(ValidationIssue(
                severity='error',
                category='word_count',
                message=f"Chapter is too short: {word_count} words (minimum {self.MIN_WORD_COUNT})"
            ))
        elif word_count < self.TARGET_MIN_WORD_COUNT:
            issues.append(ValidationIssue(
                severity='warning',
                category='word_count',
                message=f"Chapter is shorter than target: {word_count} words (target minimum {self.TARGET_MIN_WORD_COUNT})"
            ))
        elif word_count > self.MAX_WORD_COUNT:
            issues.append(ValidationIssue(
                severity='error',
                category='word_count',
                message=f"Chapter is too long: {word_count} words (maximum {self.MAX_WORD_COUNT})"
            ))
        elif word_count > self.TARGET_MAX_WORD_COUNT:
            issues.append(ValidationIssue(
                severity='warning',
                category='word_count',
                message=f"Chapter is longer than target: {word_count} words (target maximum {self.TARGET_MAX_WORD_COUNT})"
            ))
        else:
            issues.append(ValidationIssue(
                severity='info',
                category='word_count',
                message=f"Chapter word count: {word_count} words (within target range)"
            ))
        
        return issues
    
    def _validate_ai_patterns(self, content: str) -> List[ValidationIssue]:
        """Check for AI generation patterns that shouldn't be in final content."""
        issues = []
        
        for pattern in self.AI_PATTERNS:
            if pattern.lower() in content.lower():
                # Find line number if possible
                lines = content.split('\n')
                line_num = None
                for i, line in enumerate(lines, 1):
                    if pattern.lower() in line.lower():
                        line_num = i
                        break
                
                issues.append(ValidationIssue(
                    severity='warning',
                    category='ai_patterns',
                    message=f"Found potential AI meta-commentary pattern: '{pattern}'",
                    line_number=line_num
                ))
        
        return issues
    
    def _validate_structure(self, content: str) -> List[ValidationIssue]:
        """Validate basic content structure."""
        issues = []
        
        # Check if content is empty or too short
        if not content.strip():
            issues.append(ValidationIssue(
                severity='error',
                category='structure',
                message="Content is empty"
            ))
            return issues
        
        # Check for basic paragraph structure
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        if len(paragraphs) < 3:
            issues.append(ValidationIssue(
                severity='warning',
                category='structure',
                message=f"Very few paragraphs detected: {len(paragraphs)} (may need better formatting)"
            ))
        
        # Check for dialogue (should have some in most chapters)
        if '"' not in content and "'" not in content:
            issues.append(ValidationIssue(
                severity='info',
                category='structure',
                message="No dialogue detected (may be intentional)"
            ))
        
        return issues
    
    def _validate_content_quality(self, content: str) -> List[ValidationIssue]:
        """Validate content quality indicators."""
        issues = []
        
        # Check for repetitive phrases
        sentences = re.split(r'[.!?]+', content)
        sentence_starts = [s.strip()[:20].lower() for s in sentences if len(s.strip()) > 20]
        
        # Find repeated sentence starts
        start_counts = {}
        for start in sentence_starts:
            start_counts[start] = start_counts.get(start, 0) + 1
        
        repeated_starts = {start: count for start, count in start_counts.items() if count > 2}
        if repeated_starts:
            issues.append(ValidationIssue(
                severity='warning',
                category='quality',
                message=f"Repetitive sentence starts detected: {list(repeated_starts.keys())}"
            ))
        
        # Check for very short sentences (might indicate choppy writing)
        very_short_sentences = [s for s in sentences if len(s.strip().split()) < 4 and len(s.strip()) > 0]
        if len(very_short_sentences) > len(sentences) * 0.3:  # More than 30% very short
            issues.append(ValidationIssue(
                severity='warning',
                category='quality',
                message=f"Many very short sentences detected: {len(very_short_sentences)} out of {len(sentences)}"
            ))
        
        # Check for very long sentences (might indicate run-on sentences)
        very_long_sentences = [s for s in sentences if len(s.strip().split()) > 40]
        if very_long_sentences:
            issues.append(ValidationIssue(
                severity='info',
                category='quality',
                message=f"Very long sentences detected: {len(very_long_sentences)} (check for run-on sentences)"
            ))
        
        return issues
    
    def get_validation_summary(self, issues: List[ValidationIssue]) -> Dict[str, int]:
        """
        Get a summary of validation results.
        
        Args:
            issues: List of validation issues
            
        Returns:
            Dictionary with counts by severity and category
        """
        summary = {
            'total_issues': len(issues),
            'errors': len([i for i in issues if i.severity == 'error']),
            'warnings': len([i for i in issues if i.severity == 'warning']),
            'info': len([i for i in issues if i.severity == 'info'])
        }
        
        # Count by category
        categories = {}
        for issue in issues:
            categories[issue.category] = categories.get(issue.category, 0) + 1
        summary['by_category'] = categories
        
        return summary
    
    def format_validation_report(self, issues: List[ValidationIssue]) -> str:
        """
        Format validation issues into a readable report.
        
        Args:
            issues: List of validation issues
            
        Returns:
            Formatted report string
        """
        if not issues:
            return "✅ Content validation passed - no issues found!"
        
        summary = self.get_validation_summary(issues)
        report = f"📊 Validation Summary: {summary['errors']} errors, {summary['warnings']} warnings, {summary['info']} info\n\n"
        
        # Group by severity
        errors = [i for i in issues if i.severity == 'error']
        warnings = [i for i in issues if i.severity == 'warning']
        info = [i for i in issues if i.severity == 'info']
        
        if errors:
            report += "❌ ERRORS:\n"
            for issue in errors:
                line_info = f" (Line {issue.line_number})" if issue.line_number else ""
                report += f"  - {issue.message}{line_info}\n"
            report += "\n"
        
        if warnings:
            report += "⚠️  WARNINGS:\n"
            for issue in warnings:
                line_info = f" (Line {issue.line_number})" if issue.line_number else ""
                report += f"  - {issue.message}{line_info}\n"
            report += "\n"
        
        if info:
            report += "ℹ️  INFO:\n"
            for issue in info:
                line_info = f" (Line {issue.line_number})" if issue.line_number else ""
                report += f"  - {issue.message}{line_info}\n"
        
        return report
