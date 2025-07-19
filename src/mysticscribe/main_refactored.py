"""
Refactored Main Entry Point

Clean, modular main script with proper separation of concerns.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# Import our modular components
from .workflows import ArchitectWorkflow, CompleteWorkflow, LegacyWorkflow
from .utils import setup_logging, get_logger
from .core import ChapterManager

logger = get_logger(__name__)


class MysticScribeRunner:
    """
    Main runner for MysticScribe workflows.
    
    This class provides a clean interface for executing different
    workflow types and managing the overall application lifecycle.
    """
    
    def __init__(self, project_root: Path):
        """
        Initialize the MysticScribe runner.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = Path(project_root)
        self.chapter_manager = ChapterManager(project_root)
        
        # Set up logging
        setup_logging("INFO")
        self.logger = get_logger(__name__)
    
    def run_architect_workflow(self, chapter_number: Optional[int] = None) -> Dict[str, Any]:
        """
        Run the architect workflow (outline creation only).
        
        Args:
            chapter_number: Chapter number to process
            
        Returns:
            Workflow execution results
        """
        workflow = ArchitectWorkflow(self.project_root)
        return workflow.execute(chapter_number)
    
    def run_complete_workflow(self, chapter_number: Optional[int] = None) -> Dict[str, Any]:
        """
        Run the complete workflow (architect + writer + editor).
        
        Args:
            chapter_number: Chapter number to process
            
        Returns:
            Workflow execution results
        """
        workflow = CompleteWorkflow(self.project_root)
        return workflow.execute(chapter_number)
    
    def run_legacy_workflow(self, chapter_number: Optional[int] = None) -> Dict[str, Any]:
        """
        Run the legacy workflow (all agents without approval gates).
        
        Args:
            chapter_number: Chapter number to process
            
        Returns:
            Workflow execution results
        """
        workflow = LegacyWorkflow(self.project_root)
        return workflow.execute(chapter_number)
    
    def train_crew(self, n_iterations: int, filename: str, chapter_number: Optional[int] = None):
        """
        Train the crew for a given number of iterations.
        
        Args:
            n_iterations: Number of training iterations
            filename: Filename to save training results
            chapter_number: Chapter number for training
        """
        from .crew import Mysticscribe
        
        if chapter_number is None:
            chapter_number = self.chapter_manager.get_next_chapter_number()
        
        # Prepare inputs for training
        workflow = LegacyWorkflow(self.project_root)  # Use legacy for base inputs
        inputs = workflow.prepare_base_inputs(chapter_number)
        
        try:
            crew_instance = Mysticscribe()
            crew_instance.crew().train(
                n_iterations=n_iterations, 
                filename=filename, 
                inputs=inputs
            )
            self.logger.info(f"Training completed: {n_iterations} iterations, saved to {filename}")
        except Exception as e:
            self.logger.error(f"Training failed: {e}")
            raise
    
    def replay_crew(self, task_id: str):
        """
        Replay the crew execution from a specific task.
        
        Args:
            task_id: ID of the task to replay from
        """
        try:
            from .crew import Mysticscribe
            crew_instance = Mysticscribe()
            crew_instance.crew().replay(task_id=task_id)
            self.logger.info(f"Replay completed for task: {task_id}")
        except Exception as e:
            self.logger.error(f"Replay failed: {e}")
            raise
    
    def test_crew(self, n_iterations: int, eval_llm: str, chapter_number: Optional[int] = None):
        """
        Test the crew execution and return results.
        
        Args:
            n_iterations: Number of test iterations
            eval_llm: LLM to use for evaluation
            chapter_number: Chapter number for testing
        """
        from .crew import Mysticscribe
        
        if chapter_number is None:
            chapter_number = self.chapter_manager.get_next_chapter_number()
        
        # Prepare inputs for testing
        workflow = LegacyWorkflow(self.project_root)  # Use legacy for base inputs
        inputs = workflow.prepare_base_inputs(chapter_number)
        
        try:
            crew_instance = Mysticscribe()
            crew_instance.crew().test(
                n_iterations=n_iterations, 
                eval_llm=eval_llm, 
                inputs=inputs
            )
            self.logger.info(f"Testing completed: {n_iterations} iterations with {eval_llm}")
        except Exception as e:
            self.logger.error(f"Testing failed: {e}")
            raise
    
    def show_status(self):
        """Show current project status and chapter information."""
        chapters = self.chapter_manager.list_chapters()
        next_chapter = self.chapter_manager.get_next_chapter_number()
        
        print("\n📚 MysticScribe Project Status")
        print("=" * 50)
        print(f"📁 Project Root: {self.project_root}")
        print(f"🔢 Next Chapter: {next_chapter}")
        print(f"📖 Total Chapters: {len(chapters)}")
        
        if chapters:
            print("\n📋 Chapter Status:")
            for chapter_info in chapters[-5:]:  # Show last 5 chapters
                outline_status = "✅" if chapter_info.outline_exists else "❌"
                draft_status = "✅" if chapter_info.draft_exists else "❌"
                word_count = f" ({chapter_info.word_count} words)" if chapter_info.word_count else ""
                print(f"  Chapter {chapter_info.number}: Outline {outline_status} | Draft {draft_status}{word_count}")
        
        # Knowledge base status
        from .core import KnowledgeManager
        knowledge_manager = KnowledgeManager(self.project_root)
        knowledge_summary = knowledge_manager.get_knowledge_summary()
        
        print(f"\n📚 Knowledge Base:")
        print(f"  Available Files: {knowledge_summary['available_files']}/{knowledge_summary['total_files']}")
        print(f"  Completeness: {knowledge_summary['completeness_percentage']:.1f}%")
        
        if knowledge_summary['missing_files'] > 0:
            print(f"  Missing Files: {', '.join(knowledge_summary['missing_file_names'])}")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="MysticScribe - AI-Powered Chapter Writing System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s workflow           # Interactive workflow with approval gates
  %(prog)s architect 3        # Create outline for Chapter 3
  %(prog)s run               # Legacy workflow without approval gates
  %(prog)s status            # Show project status
  %(prog)s train 5 model.pkl  # Train crew for 5 iterations
        """
    )
    
    parser.add_argument(
        'command',
        choices=['workflow', 'architect', 'run', 'train', 'replay', 'test', 'status'],
        help='Command to execute'
    )
    
    parser.add_argument(
        'chapter_number',
        nargs='?',
        type=int,
        help='Chapter number to process (auto-detected if not provided)'
    )
    
    # Training/testing arguments
    parser.add_argument(
        '--iterations', '-i',
        type=int,
        help='Number of iterations for train/test commands'
    )
    
    parser.add_argument(
        '--filename', '-f',
        help='Filename for train command output'
    )
    
    parser.add_argument(
        '--eval-llm',
        help='LLM to use for test command evaluation'
    )
    
    parser.add_argument(
        '--task-id',
        help='Task ID for replay command'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser


def main():
    """Main entry point for the MysticScribe system."""
    parser = create_argument_parser()
    
    # Handle case where no arguments provided
    if len(sys.argv) == 1:
        print_help_message()
        return
    
    args = parser.parse_args()
    
    # Set up logging level
    if args.verbose:
        setup_logging("DEBUG")
    
    # Initialize runner
    project_root = Path(__file__).parent.parent.parent
    runner = MysticScribeRunner(project_root)
    
    try:
        # Execute the requested command
        if args.command == 'workflow':
            runner.run_complete_workflow(args.chapter_number)
        
        elif args.command == 'architect':
            runner.run_architect_workflow(args.chapter_number)
        
        elif args.command == 'run':
            runner.run_legacy_workflow(args.chapter_number)
        
        elif args.command == 'status':
            runner.show_status()
        
        elif args.command == 'train':
            if not args.iterations or not args.filename:
                print("❌ Error: train command requires --iterations and --filename")
                return
            runner.train_crew(args.iterations, args.filename, args.chapter_number)
        
        elif args.command == 'replay':
            if not args.task_id:
                print("❌ Error: replay command requires --task-id")
                return
            runner.replay_crew(args.task_id)
        
        elif args.command == 'test':
            if not args.iterations or not args.eval_llm:
                print("❌ Error: test command requires --iterations and --eval-llm")
                return
            runner.test_crew(args.iterations, args.eval_llm, args.chapter_number)
    
    except KeyboardInterrupt:
        print("\n⏹️  Command interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Command failed: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


def print_help_message():
    """Print a helpful usage message when no arguments are provided."""
    print("🏗️  MysticScribe Chapter Generation System")
    print("=" * 50)
    print("\nWorkflow Commands:")
    print("  python -m mysticscribe workflow [chapter_number]      # 🌟 RECOMMENDED: Full interactive workflow")
    print("                                                        #     with outline approval gates")
    print("  python -m mysticscribe architect [chapter_number]     # 📋 Outline creation only with approval")
    print("  python -m mysticscribe run [chapter_number]           # ⚡ Legacy: Skip outline approval")
    print("  python -m mysticscribe status                         # 📊 Show project status")
    print("\nTraining & Testing:")
    print("  python -m mysticscribe train --iterations N --filename FILE.pkl [chapter_number]") 
    print("  python -m mysticscribe replay --task-id TASK_ID")
    print("  python -m mysticscribe test --iterations N --eval-llm MODEL [chapter_number]")
    print("\nWorkflow Descriptions:")
    print("  📋 'architect' - Creates/expands outlines with human review and approval")
    print("  🌟 'workflow'  - Complete process: architect → user approval → writer → editor")
    print("  ⚡ 'run'       - Legacy mode: runs all agents without outline approval pause")
    print("  📊 'status'    - Show current project status and chapter information")
    print("\n💡 Tip: Use 'workflow' for best results with human oversight!")
    print("\nFor more help: python -m mysticscribe --help")


# Legacy function names for backwards compatibility
def run():
    """Legacy function - use main() instead."""
    print("⚠️  Warning: run() is deprecated, use main() instead")
    main()


# Support for old-style execution
if __name__ == "__main__":
    main()
