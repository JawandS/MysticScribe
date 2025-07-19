"""
Legacy Workflow

Simple linear workflow that runs all agents without approval gates.
"""

from typing import Dict, Any, Optional

from .base_workflow import BaseWorkflow


class LegacyWorkflow(BaseWorkflow):
    """
    Legacy workflow for backwards compatibility.
    
    This workflow runs all agents sequentially without interactive
    approval gates, maintaining compatibility with older usage patterns.
    """
    
    def execute(self, chapter_number: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        """
        Execute the legacy workflow.
        
        Args:
            chapter_number: The chapter number to process
            **kwargs: Additional parameters (unused)
            
        Returns:
            Dictionary containing workflow results and metadata
        """
        chapter_num = self.get_chapter_number(chapter_number)
        
        # Validate prerequisites
        if not self.validate_prerequisites(chapter_num):
            raise ValueError("Prerequisites not met for legacy workflow")
        
        self.log_workflow_start("Legacy Workflow", chapter_num)
        print("ℹ️  Note: This skips the interactive outline approval. Use 'workflow' for full control.")
        
        try:
            from ..crew import Mysticscribe
            
            # Initialize crew
            crew_instance = Mysticscribe()
            
            # Prepare inputs
            inputs = self._prepare_legacy_inputs(chapter_num)
            
            print(f"🚀 Running all agents sequentially...")
            result = crew_instance.crew().kickoff(inputs=inputs)
            
            # Save and validate the result
            save_result = self._save_chapter_result(chapter_num, result)
            
            print(f"\n=== Chapter {chapter_num} Generation Complete ===")
            print(f"📖 Output saved to: {save_result['chapter_file']}")
            print(f"💡 Tip: Use 'workflow' command for interactive outline approval")
            
            self.log_workflow_complete("Legacy Workflow", chapter_num)
            
            return {
                'status': 'completed',
                'chapter_number': chapter_num,
                'workflow_type': 'legacy',
                'chapter_file': save_result['chapter_file'],
                'validation_report': save_result.get('validation_report', '')
            }
            
        except Exception as e:
            self.log_workflow_error("Legacy Workflow", chapter_num, e)
            raise Exception(f"Legacy workflow failed: {e}")
    
    def _prepare_legacy_inputs(self, chapter_number: int) -> Dict[str, Any]:
        """
        Prepare inputs for the legacy workflow.
        
        Args:
            chapter_number: The chapter number being processed
            
        Returns:
            Dictionary with all inputs needed for legacy execution
        """
        inputs = self.prepare_base_inputs(chapter_number)
        
        # Check for existing draft material
        existing_draft = self._check_existing_draft(chapter_number)
        inputs['existing_draft'] = existing_draft
        
        if existing_draft:
            print(f"📖 Found existing draft material for Chapter {chapter_number}")
        
        # Check for existing outline - if it exists, use it as approved
        existing_outline, outline_action = self._check_existing_outline(chapter_number)
        inputs['existing_outline'] = existing_outline
        inputs['approved_outline'] = existing_outline  # Use as approved in legacy mode
        inputs['outline_action'] = outline_action
        
        return inputs
    
    def _check_existing_draft(self, chapter_number: int) -> str:
        """Check for existing draft material."""
        try:
            from ..tools.custom_tool import ChapterAnalysisTool
            chapter_tool = ChapterAnalysisTool()
            existing_draft = chapter_tool._run(str(chapter_number))
            
            if "not found" not in existing_draft.lower():
                return existing_draft
            return ""
        except Exception as e:
            self.logger.warning(f"Error checking existing draft: {e}")
            return ""
    
    def _check_existing_outline(self, chapter_number: int) -> tuple[str, str]:
        """
        Check for existing outline.
        
        Returns:
            Tuple of (existing_outline, outline_action)
        """
        try:
            from ..tools.custom_tool import OutlineManagementTool
            outline_tool = OutlineManagementTool()
            outline_check = outline_tool._run(str(chapter_number), "check")
            
            if "EXISTS" in outline_check:
                existing_outline = outline_tool._run(str(chapter_number), "load")
                print(f"📋 Using existing outline for Chapter {chapter_number}")
                return existing_outline, 'use_existing'
            else:
                print(f"🆕 Will create new outline for Chapter {chapter_number}")
                return "", 'create_new'
        except Exception as e:
            self.logger.warning(f"Error checking existing outline: {e}")
            return "", 'create_new'
    
    def _save_chapter_result(self, chapter_number: int, result) -> Dict[str, Any]:
        """
        Save the chapter result with validation.
        
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
        
        return {
            'chapter_file': str(chapter_file),
            'validation_report': validation_report,
            'validation_issues': validation_issues
        }
    
    def _extract_content_from_result(self, result) -> str:
        """Extract content from CrewAI result."""
        if hasattr(result, 'raw'):
            content = result.raw
            print(f"📝 Saving result.raw content ({len(content)} characters)")
        elif hasattr(result, 'output'):
            content = result.output
            print(f"📝 Saving result.output content ({len(content)} characters)")
        else:
            content = str(result)
            print(f"📝 Saving str(result) content ({len(content)} characters)")
            print(f"⚠️  Result type: {type(result)}")
        
        return content
