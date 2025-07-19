"""
MysticScribe - AI-Powered Chapter Writing System

A sophisticated AI-powered system that automates the process of writing story chapters
using a team of specialized AI agents built on the CrewAI framework.

Main Components:
- Core: Chapter management, knowledge management, and content validation
- Workflows: Different workflow implementations (architect, complete, legacy)
- Tools: Specialized AI tools for content creation and analysis
- Utils: Utility functions for logging, file operations, and text processing

Usage:
    from mysticscribe import MysticScribeRunner
    from mysticscribe.workflows import CompleteWorkflow
    from mysticscribe.core import ChapterManager
"""

from .core import ChapterManager, KnowledgeManager, ContentValidator
from .workflows import ArchitectWorkflow, CompleteWorkflow, LegacyWorkflow
from .main_refactored import MysticScribeRunner, main

# For backwards compatibility
from .crew import Mysticscribe
from .main import run as legacy_run

__version__ = "1.0.0"

__all__ = [
    # Main interfaces
    'MysticScribeRunner',
    'main',
    
    # Core components
    'ChapterManager',
    'KnowledgeManager',
    'ContentValidator',
    
    # Workflows
    'ArchitectWorkflow',
    'CompleteWorkflow', 
    'LegacyWorkflow',
    
    # Legacy compatibility
    'Mysticscribe',
    'legacy_run'
]