"""
Main entry point for python -m mysticscribe

This provides module-style access to MysticScribe.
For simplicity, it's recommended to use the root-level mysticscribe.py script instead.
"""

import sys
import os
from pathlib import Path

def main():
    """Run MysticScribe via module import."""
    print("ℹ️  Running MysticScribe via module import")
    print("💡 Tip: For simplicity, use ./mysticscribe.py directly from the project root")
    
    # Get project root (go up from src/mysticscribe to project root)
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent
    
    # Add the project root to sys.path to import the main mysticscribe module
    sys.path.insert(0, str(project_root))
    
    try:
        # Import and run the main mysticscribe module
        import mysticscribe
        mysticscribe.main()
    except ImportError as e:
        print(f"❌ Error importing mysticscribe: {e}")
        print(f"Make sure you're running from the project root: {project_root}")
        sys.exit(1)

if __name__ == "__main__":
    main()
