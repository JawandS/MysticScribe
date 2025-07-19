"""
Complete Workflow

Full end-to-end workflow: architect → writer → editor with approval gates.
"""

from typing import Dict, Any, Optional
from pathlib import Path

from .base_workflow import BaseWorkflow
from .architect_workflow import ArchitectWorkflow


class CompleteWorkflow(BaseWorkflow):
    """
    Complete chapter generation workflow.
    
    This workflow implements the full process:
    1. Architect phase with human approval gates for outline
    2. Writer and editor phases to create final chapter
    """
    
    def execute(self, chapter_number: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        """
        Execute the complete workflow.
        
        Args:
            chapter_number: The chapter number to process
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing workflow results and metadata
        """
        chapter_num = self.get_chapter_number(chapter_number)
        
        # Validate prerequisites
        if not self.validate_prerequisites(chapter_num):
            raise ValueError("Prerequisites not met for complete workflow")
        
        self.log_workflow_start("Complete Chapter Workflow", chapter_num)
        
        try:
            # Step 1: Run architect workflow with approval gates
            print(f"\n=== PHASE 1: ARCHITECT ===")
            architect_workflow = ArchitectWorkflow(self.project_root)
            architect_result = architect_workflow.execute(chapter_num)
            
            if architect_result['approved_outline'] == "Workflow cancelled":
                return {
                    'status': 'cancelled',
                    'chapter_number': chapter_num,
                    'workflow_type': 'complete',
                    'phase_completed': 'architect'
                }
            
            approved_outline = architect_result['approved_outline']
            
            # Step 2: Ask if user wants to continue to writing phase
            print(f"\n=== PHASE 2: WRITER & EDITOR ===")
            
            if not self.get_user_confirmation("Proceed to writing and editing phase?"):
                print("✅ Stopping after outline phase. You can resume later with 'run' command.")
                return {
                    'status': 'paused_after_outline',
                    'chapter_number': chapter_num,
                    'workflow_type': 'complete',
                    'phase_completed': 'architect',
                    'approved_outline': approved_outline
                }
            
            # Step 3: Run the writing and editing phases
            writing_result = self._run_writing_and_editing(chapter_num, approved_outline)
            
            self.log_workflow_complete("Complete Chapter Workflow", chapter_num)
            
            return {
                'status': 'completed',
                'chapter_number': chapter_num,
                'workflow_type': 'complete',
                'phases_completed': ['architect', 'writer', 'editor'],
                'approved_outline': approved_outline,
                'chapter_file': writing_result['chapter_file'],
                'validation_report': writing_result.get('validation_report', '')
            }
            
        except Exception as e:
            self.log_workflow_error("Complete Chapter Workflow", chapter_num, e)
            raise Exception(f"Complete workflow failed: {e}")
    
    def _run_writing_and_editing(self, chapter_number: int, approved_outline: str) -> Dict[str, Any]:
        """
        Run the writing and editing phases.
        
        Args:
            chapter_number: The chapter number being processed
            approved_outline: The approved outline from the architect phase
            
        Returns:
            Dictionary with writing phase results
        """
        from ..crew import Mysticscribe
        
        print(f"📝 Initializing writer and editor agents...")
        crew_instance = Mysticscribe()
        
        # Prepare inputs for the writing and editing phases
        inputs = self.prepare_base_inputs(chapter_number)
        inputs.update({
            'approved_outline': approved_outline,
            'existing_draft': "",  # Clear since we're using the approved outline
            'existing_outline': approved_outline,
            'outline_action': 'use_approved'
        })
        
        print(f"🏃‍♂️ Running writer and editor agents for Chapter {chapter_number}...")
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Process and save the result
        return self._save_chapter_result(chapter_number, result)
    
    def _save_chapter_result(self, chapter_number: int, result) -> Dict[str, Any]:
        """
        Save the chapter result and perform validation.
        
        Args:
            chapter_number: The chapter number
            result: The result from crew execution
            
        Returns:
            Dictionary with save operation results
        """
        # Extract content from the CrewAI result
        content = self._extract_content_from_result(result)
        
        # Save the chapter
        chapter_file = self.chapter_manager.save_chapter_content(
            chapter_number, 
            content, 
            validate=True
        )
        
        # Validate and report
        from ..core.validation import ContentValidator
        validator = ContentValidator()
        validation_issues = validator.validate_chapter_content(content)
        validation_report = validator.format_validation_report(validation_issues)
        
        # Print validation results
        print(f"\n📊 Content Validation Results:")
        print(validation_report)
        
        # Print completion info
        print(f"\n🎉 Complete Chapter Workflow Finished!")
        print(f"📋 Outline: outlines/chapter_{chapter_number}.txt")
        print(f"📖 Chapter: {chapter_file}")
        print(f"✨ Chapter {chapter_number} is ready!")
        
        return {
            'chapter_file': str(chapter_file),
            'validation_report': validation_report,
            'validation_issues': validation_issues
        }
    
    def _extract_content_from_result(self, result) -> str:
        """
        Extract the actual content from the CrewAI result.
        
        Args:
            result: The CrewAI execution result
            
        Returns:
            The extracted content string
        """
        if hasattr(result, 'raw'):
            content = result.raw
            self.logger.debug(f"Saving result.raw content ({len(content)} characters)")
        elif hasattr(result, 'output'):
            content = result.output
            self.logger.debug(f"Saving result.output content ({len(content)} characters)")
        else:
            content = str(result)
            self.logger.debug(f"Saving str(result) content ({len(content)} characters)")
            self.logger.warning(f"Unexpected result type: {type(result)}")
        
        return content
