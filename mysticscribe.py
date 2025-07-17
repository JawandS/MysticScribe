#!/usr/bin/env python3
"""
Simple runner script for MysticScribe commands.
Place this in the project root for easy access.
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    """Run MysticScribe commands with simplified syntax."""
    
    # Get the directory where this script is located (project root)
    project_root = Path(__file__).parent.absolute()
    main_script = project_root / "src" / "mysticscribe" / "main.py"
    
    if not main_script.exists():
        print("❌ Error: MysticScribe main.py not found!")
        print(f"Expected location: {main_script}")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("🏗️  MysticScribe Chapter Generation System")
        print("=" * 50)
        print("\n🚀 Easy Commands:")
        print("  python mysticscribe.py workflow [chapter_number]    # 🌟 RECOMMENDED: Full interactive workflow")
        print("  python mysticscribe.py architect [chapter_number]   # 📋 Outline creation only")
        print("  python mysticscribe.py run [chapter_number]         # ⚡ Legacy: Skip outline approval")
        print("\n📚 Training & Testing:")
        print("  python mysticscribe.py train <n_iterations> <filename> [chapter_number]")
        print("  python mysticscribe.py replay <task_id>")
        print("  python mysticscribe.py test <n_iterations> <eval_llm> [chapter_number]")
        sys.exit(0)
    
    # Pass all arguments to the main script
    cmd = [sys.executable, str(main_script)] + sys.argv[1:]
    
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
