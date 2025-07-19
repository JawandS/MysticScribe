"""
MysticScribe - AI-Powered Chapter Writing System

A simplified AI-powered system that automates the process of writing story chapters
using a team of specialized AI agents built on the CrewAI framework.

Main Components:
- Core: Chapter management, knowledge management, and content validation
- Tools: Specialized AI tools for content creation and analysis
- Utils: Utility functions for logging, file operations, and text processing

Usage:
    from mysticscribe.crew import Mysticscribe
    
    # Initialize and run
    crew = Mysticscribe()
    result = crew.crew().kickoff(inputs=your_inputs)
"""

from .core import ChapterManager, KnowledgeManager

# Main crew interface
from .crew import Mysticscribe

__version__ = "1.0.0"

__all__ = [
    # Main interfaces
    "Mysticscribe",
    "ChapterManager", 
    "KnowledgeManager",
]