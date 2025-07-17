#!/usr/bin/env python3
"""
Simple runner script for MysticScribe commands.
Place this in the project root for easy access.
"""

import sys
import subprocess
import os
import re
from pathlib import Path

def get_next_chapter_number(project_root):
    """
    Get the next chapter number by checking existing outlines.
    Returns the highest outline number + 1, or 1 if no outlines exist.
    """
    outlines_dir = project_root / "outlines"
    
    # Create outlines directory if it doesn't exist
    if not outlines_dir.exists():
        outlines_dir.mkdir(parents=True, exist_ok=True)
        return "1"
    
    # Find all outline files
    outline_files = [f for f in os.listdir(outlines_dir) if f.startswith("chapter_") and f.endswith(".txt")]
    
    if not outline_files:
        return "1"
    
    # Extract chapter numbers
    chapter_numbers = []
    for filename in outline_files:
        match = re.search(r'chapter_(\d+)\.txt', filename)
        if match:
            chapter_numbers.append(int(match.group(1)))
    
    if not chapter_numbers:
        return "1"
    
    return str(max(chapter_numbers) + 1)

def main():
    """Run MysticScribe commands with simplified syntax."""
    
    # Get the directory where this script is located (project root)
    project_root = Path(__file__).parent.absolute()
    main_script = project_root / "src" / "mysticscribe" / "main.py"
    
    if not main_script.exists():
        print("❌ Error: MysticScribe main.py not found!")
        print(f"Expected location: {main_script}")
        sys.exit(1)

    # Pass arguments to the main script, always using workflow mode
    cmd = [sys.executable, str(main_script), "workflow"]
    
    # Check if the user provided an argument and if it's a chapter number
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        # If user provided a chapter number, use it
        cmd.append(sys.argv[1])
        chapter_number = sys.argv[1]
    else:
        # Otherwise, automatically determine the next chapter number
        chapter_number = get_next_chapter_number(project_root)
        cmd.append(chapter_number)
        print(f"ℹ️ Auto-detecting next chapter: Chapter {chapter_number}")
    
    try:
        # Change to project root directory
        os.chdir(project_root)
        
        # Run the command
        result = subprocess.run(cmd, cwd=project_root)
        sys.exit(result.returncode)
        
    except KeyboardInterrupt:
        print("\n⏹️  Command interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running command: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
