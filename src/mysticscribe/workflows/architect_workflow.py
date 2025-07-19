"""
Architect Workflow

Interactive outline creation workflow with human approval gates.
"""

from typing import Dict, Any, Optional
from pathlib import Path

from .base_workflow import BaseWorkflow


class ArchitectWorkflow(BaseWorkflow):
    """
    Architect workflow for interactive outline creation.
    
    This workflow implements the outline creation process with human approval gates:
    1. Context Check: Load story context and previous chapters
    2. Outline Handling: Check for existing outlines, expand or create new
    3. Generate/Expand: Use architect agent to create/improve outline
    4. Save & Pause: Save outline and pause for human review
    5. User Approval Gate: Wait for explicit user approval
    """
    
    def execute(self, chapter_number: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        """
        Execute the architect workflow with human approval gates.
        
        Args:
            chapter_number: The chapter number to process
            **kwargs: Additional parameters (unused in this workflow)
            
        Returns:
            Dictionary containing the approved outline and workflow metadata
        """
        chapter_num = self.get_chapter_number(chapter_number)
        
        # Validate prerequisites
        if not self.validate_prerequisites(chapter_num):
            raise ValueError("Prerequisites not met for architect workflow")
        
        self.log_workflow_start("Architect Workflow", chapter_num)
        
        try:
            # Initialize crew and prepare inputs
            from ..crew import Mysticscribe
            crew_instance = Mysticscribe()
            
            # Prepare base inputs
            inputs = self.prepare_base_inputs(chapter_num)
            
            # Step 1: Context Check
            print(f"\n📚 Step 1: Context Check - Loading story context for Chapter {chapter_num}...")
            self._log_context_status(chapter_num)
            
            # Check for existing draft material
            existing_draft = self._check_existing_draft(chapter_num)
            inputs['existing_draft'] = existing_draft
            
            # Step 2: Outline Handling
            print(f"\n📋 Step 2: Outline Handling - Checking for existing outline...")
            outline_action, existing_outline = self._handle_existing_outline(chapter_num)
            
            if outline_action == 'use_as_is':
                approved_outline = existing_outline.replace(
                    "=== EXISTING OUTLINE FOR CHAPTER", 
                    "=== APPROVED OUTLINE FOR CHAPTER"
                )
                self.log_workflow_complete("Architect Workflow", chapter_num)
                return {
                    'approved_outline': approved_outline,
                    'chapter_number': chapter_num,
                    'workflow_type': 'architect',
                    'action_taken': 'used_existing'
                }
            
            inputs['existing_outline'] = existing_outline
            inputs['outline_action'] = outline_action
            
            # Step 3: Generate/Expand outline
            action_text = "Expanding" if outline_action == 'expand' else "Creating"
            print(f"\n🏗️  Step 3: {action_text} outline using architect agent...")
            
            outline_result = self._generate_outline(crew_instance, inputs)
            
            # Step 4: Save outline and pause for review
            print(f"\n💾 Step 4: Saving outline for human review...")
            outline_file = self._save_and_show_outline(chapter_num, outline_result)
            
            # Step 5: User Approval Gate
            print(f"\n🔍 Step 5: User Approval Gate - Waiting for approval...")
            approved_outline = self._get_user_approval(chapter_num, outline_file)
            
            self.log_workflow_complete("Architect Workflow", chapter_num)
            
            return {
                'approved_outline': approved_outline,
                'chapter_number': chapter_num,
                'workflow_type': 'architect',
                'action_taken': outline_action,
                'outline_file': str(outline_file)
            }
            
        except Exception as e:
            self.log_workflow_error("Architect Workflow", chapter_num, e)
            raise Exception(f"Architect workflow failed: {e}")
    
    def _log_context_status(self, chapter_number: int):
        """Log the context loading status."""
        if chapter_number > 1:
            print(f"📖 Loaded previous chapter context for continuity")
        else:
            print(f"📝 Chapter 1 - no previous chapters to reference")
    
    def _check_existing_draft(self, chapter_number: int) -> str:
        """Check for existing draft material in chapters.txt."""
        from ..tools.custom_tool import ChapterAnalysisTool
        
        try:
            chapter_tool = ChapterAnalysisTool()
            existing_draft = chapter_tool._run(str(chapter_number))
            
            if "not found" not in existing_draft.lower():
                print(f"📖 Found existing draft material for Chapter {chapter_number}")
                return existing_draft
            else:
                print(f"📝 No existing draft found for Chapter {chapter_number}")
                return ""
        except Exception as e:
            self.logger.warning(f"Error checking existing draft: {e}")
            return ""
    
    def _handle_existing_outline(self, chapter_number: int) -> tuple[str, str]:
        """
        Handle existing outline logic.
        
        Returns:
            Tuple of (action, existing_outline)
        """
        from ..tools.custom_tool import OutlineManagementTool
        
        outline_tool = OutlineManagementTool()
        outline_check = outline_tool._run(str(chapter_number), "check")
        
        if "EXISTS" not in outline_check:
            print(f"📝 No existing outline found for Chapter {chapter_number}")
            print("🆕 Will create new outline")
            return 'create_new', ""
        
        # Existing outline found
        print(f"📄 Found existing outline for Chapter {chapter_number}")
        existing_outline = outline_tool._run(str(chapter_number), "load")
        print(f"📖 Loaded existing outline")
        
        # Ask user what to do
        options = {
            '1': 'Expand and improve existing outline',
            '2': 'Create a completely new outline', 
            '3': 'Use existing outline as-is'
        }
        
        choice = self.get_user_choice(
            f"Found existing outline for Chapter {chapter_number}. What would you like to do?",
            options
        )
        
        if choice == '1':
            print("📈 Will expand existing outline")
            return 'expand', existing_outline
        elif choice == '2':
            print("🆕 Will create new outline")
            return 'create_new', ""
        else:  # choice == '3'
            print(f"✅ Using existing outline as-is")
            return 'use_as_is', existing_outline
    
    def _generate_outline(self, crew_instance, inputs: Dict[str, Any]) -> str:
        """Generate or expand the outline using the architect agent."""
        from crewai import Crew, Process
        
        # Create a minimal crew with just the architect and outline task
        architect = crew_instance.architect()
        outline_task = crew_instance.outline_task()
        
        outline_crew = Crew(
            agents=[architect],
            tasks=[outline_task],
            process=Process.sequential,
            verbose=True
        )
        
        print(f"🤖 Architect agent is working on the outline...")
        self.logger.debug(f"Executing outline_crew.kickoff with inputs: {list(inputs.keys())}")
        
        try:
            outline_result = outline_crew.kickoff(inputs=inputs)
            
            if not outline_result:
                raise ValueError("Empty outline result returned from crew execution")
                
            return str(outline_result)
            
        except Exception as e:
            self.logger.error(f"Error during outline crew execution: {e}")
            raise
    
    def _save_and_show_outline(self, chapter_number: int, outline_result: str) -> Path:
        """Save the outline and show information to user."""
        from ..tools.custom_tool import OutlineManagementTool
        
        # Save the outline
        outline_tool = OutlineManagementTool()
        save_result = outline_tool._run(str(chapter_number), "save", outline_result)
        print(save_result)
        
        # Get the outline file path for user reference
        outline_file = self.project_root / "outlines" / f"chapter_{chapter_number}.txt"
        
        print(f"\n⏸️  PAUSE FOR HUMAN REVIEW")
        print(f"📁 Outline saved to: {outline_file}")
        print(f"📝 Please review and edit the outline file as needed.")
        print(f"💡 You can modify the outline directly in your editor.")
        print(f"🔧 Make any changes you want to the structure, pacing, or content.")
        
        return outline_file
    
    def _get_user_approval(self, chapter_number: int, outline_file: Path) -> str:
        """Get user approval for the outline."""
        from ..tools.custom_tool import OutlineManagementTool
        
        while True:
            approval = input(f"\nHave you reviewed and approved the outline for Chapter {chapter_number}? (y/n/q): ").strip().lower()
            
            if approval == 'q':
                print("❌ Workflow cancelled by user")
                raise InterruptedError("Workflow cancelled by user")
            elif approval == 'y':
                print("✅ Outline approved! Ready for writer and editor agents...")
                break
            elif approval == 'n':
                print("📝 Please continue editing the outline file and return when ready.")
                print(f"📂 File location: {outline_file}")
            else:
                print("Please enter 'y' (yes), 'n' (not yet), or 'q' (quit)")
        
        # Load the final approved outline
        print(f"\n📖 Step 6: Loading final approved outline...")
        outline_tool = OutlineManagementTool()
        approved_outline = outline_tool._run(str(chapter_number), "load")
        
        print(f"📋 Approved outline is ready for writer and editor agents")
        return approved_outline
