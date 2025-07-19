"""
Base Workflow Class

Abstract base class for all MysticScribe workflows.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
import logging

from ..core import ChapterManager, KnowledgeManager

logger = logging.getLogger(__name__)


class BaseWorkflow(ABC):
    """
    Abstract base class for MysticScribe workflows.
    
    This class provides the common structure and utilities that all
    workflow implementations need, ensuring consistency across different
    workflow types.
    """
    
    def __init__(self, project_root: Path):
        """
        Initialize the base workflow.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = Path(project_root)
        self.chapter_manager = ChapterManager(project_root)
        self.knowledge_manager = KnowledgeManager(project_root)
        
        # Set up logging
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    def execute(self, chapter_number: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        """
        Execute the workflow.
        
        Args:
            chapter_number: The chapter number to process (auto-detected if None)
            **kwargs: Additional workflow-specific parameters
            
        Returns:
            Dictionary containing workflow results and metadata
        """
        pass
    
    def get_chapter_number(self, chapter_number: Optional[int] = None) -> int:
        """
        Get the chapter number to use, auto-detecting if not provided.
        
        Args:
            chapter_number: Explicit chapter number, or None for auto-detection
            
        Returns:
            The chapter number to use
        """
        if chapter_number is not None:
            return int(chapter_number)
        return self.chapter_manager.get_next_chapter_number()
    
    def prepare_base_inputs(self, chapter_number: int) -> Dict[str, Any]:
        """
        Prepare the base input dictionary that all workflows need.
        
        Args:
            chapter_number: The chapter number being processed
            
        Returns:
            Dictionary with base inputs for crew execution
        """
        from datetime import datetime
        
        inputs = {
            'chapter_number': str(chapter_number),
            'current_year': str(datetime.now().year),
            'knowledge_context': self.knowledge_manager.load_all_knowledge(),
        }
        
        # Add previous chapter context for continuity
        if chapter_number > 1:
            try:
                inputs['previous_chapter_context'] = self._get_previous_chapter_context(chapter_number)
                self.logger.info(f"Loaded previous chapter context for continuity")
            except Exception as e:
                self.logger.warning(f"Could not load previous chapter context: {e}")
                inputs['previous_chapter_context'] = f"Could not load previous chapter context: {e}"
        else:
            inputs['previous_chapter_context'] = "This is Chapter 1 - no previous chapters to reference."
        
        return inputs
    
    def _get_previous_chapter_context(self, chapter_number: int) -> str:
        """
        Load context from previous chapters for continuity.
        
        Args:
            chapter_number: Current chapter number
            
        Returns:
            Formatted previous chapter context
        """
        if chapter_number <= 1:
            return "This is Chapter 1 - no previous chapters to reference."
        
        try:
            # Use the Previous Chapter Reader Tool to get comprehensive context
            from ..tools.previous_chapter_reader import PreviousChapterReaderTool
            previous_reader = PreviousChapterReaderTool()
            previous_context = previous_reader._run(str(chapter_number))
            
            self.logger.debug(f"Previous chapter context loaded - focusing on continuity from Chapter {chapter_number - 1}")
            return previous_context
            
        except Exception as e:
            self.logger.error(f"Error loading previous chapter context: {e}")
            return f"Could not load previous chapter context: {str(e)}"
    
    def validate_prerequisites(self, chapter_number: int) -> bool:
        """
        Validate that prerequisites for workflow execution are met.
        
        Args:
            chapter_number: The chapter number to validate
            
        Returns:
            True if prerequisites are met, False otherwise
        """
        # Check knowledge base
        knowledge_summary = self.knowledge_manager.get_knowledge_summary()
        if knowledge_summary['available_files'] == 0:
            self.logger.error("No knowledge files found - cannot proceed")
            return False
        
        # Warn about missing knowledge files
        if knowledge_summary['missing_files'] > 0:
            self.logger.warning(
                f"Missing {knowledge_summary['missing_files']} knowledge files: "
                f"{knowledge_summary['missing_file_names']}"
            )
        
        return True
    
    def log_workflow_start(self, workflow_name: str, chapter_number: int):
        """
        Log the start of a workflow.
        
        Args:
            workflow_name: Name of the workflow being executed
            chapter_number: Chapter number being processed
        """
        self.logger.info(f"Starting {workflow_name} for Chapter {chapter_number}")
        print(f"\n=== Starting {workflow_name} for Chapter {chapter_number} ===")
    
    def log_workflow_complete(self, workflow_name: str, chapter_number: int):
        """
        Log the completion of a workflow.
        
        Args:
            workflow_name: Name of the workflow that completed
            chapter_number: Chapter number that was processed
        """
        self.logger.info(f"{workflow_name} complete for Chapter {chapter_number}")
        print(f"\n✅ {workflow_name} complete for Chapter {chapter_number}")
    
    def log_workflow_error(self, workflow_name: str, chapter_number: int, error: Exception):
        """
        Log a workflow error.
        
        Args:
            workflow_name: Name of the workflow that failed
            chapter_number: Chapter number being processed
            error: The exception that occurred
        """
        self.logger.error(f"{workflow_name} failed for Chapter {chapter_number}: {error}")
        print(f"❌ {workflow_name} failed for Chapter {chapter_number}: {error}")
    
    def get_user_confirmation(self, prompt: str, default: str = "n") -> bool:
        """
        Get user confirmation for workflow actions.
        
        Args:
            prompt: The prompt to show the user
            default: Default response if user just presses enter
            
        Returns:
            True if user confirmed, False otherwise
        """
        while True:
            response = input(f"{prompt} (y/n) [{default}]: ").strip().lower()
            if not response:
                response = default
            
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' (yes) or 'n' (no)")
    
    def get_user_choice(self, prompt: str, options: Dict[str, str], default: str = None) -> str:
        """
        Get user choice from multiple options.
        
        Args:
            prompt: The prompt to show the user
            options: Dictionary mapping option keys to descriptions
            default: Default option if user just presses enter
            
        Returns:
            The selected option key
        """
        print(f"\n{prompt}")
        for key, description in options.items():
            default_marker = " [default]" if key == default else ""
            print(f"  {key}. {description}{default_marker}")
        
        while True:
            response = input("Choose option: ").strip()
            if not response and default:
                return default
            
            if response in options:
                return response
            else:
                valid_options = ", ".join(options.keys())
                print(f"Please enter one of: {valid_options}")
