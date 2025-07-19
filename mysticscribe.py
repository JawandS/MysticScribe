#!/usr/bin/env python3
"""
MysticScribe Entry Point Script

This script provides a simple interface to the MysticScribe chapter writing system.
It automatically detects the next chapter number and runs the workflow.

Usage:
    ./mysticscribe.py [chapter_number]    # Run complete workflow
    ./mysticscribe.py --help              # Show help message
"""

import sys
import os
from pathlib import Path

def main():
    """Run MysticScribe with simplified command line interface."""
    
    # Get the directory where this script is located (project root)
    project_root = Path(__file__).parent.absolute()
    
    # Add the src directory to Python path so we can import mysticscribe
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    try:
        # Import the new main function directly from the module
        import mysticscribe.main_refactored as main_module
        from mysticscribe.main_refactored import MysticScribeRunner, print_help_message
        
        # Change to project root directory
        os.chdir(project_root)
        
        # Check if help requested
        if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
            print_help_message()
            return
        
        # Create runner instance
        runner = MysticScribeRunner(project_root)
        
        # Get chapter number if provided
        chapter_number = None
        if len(sys.argv) > 1:
            try:
                chapter_number = int(sys.argv[1])
            except ValueError:
                print(f"❌ Error: '{sys.argv[1]}' is not a valid chapter number")
                sys.exit(1)
        
        # Auto-detect chapter number if not provided
        if chapter_number is None:
            chapter_number = runner.chapter_manager.get_next_chapter_number()
            print(f"ℹ️ Auto-detecting next chapter: Chapter {chapter_number}")
        
        # Run the complete workflow (architect + writer + editor)
        print(f"🚀 Starting MysticScribe for Chapter {chapter_number}")
        runner.run_complete_workflow(chapter_number)
        
    except ImportError as e:
        print(f"❌ Error: Could not import MysticScribe modules: {e}")
        print("Make sure you're running this from the project root and dependencies are installed.")
        print("Debug info:")
        print(f"  Project root: {project_root}")
        print(f"  Source path: {src_path}")
        print(f"  Source exists: {src_path.exists()}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Command interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
