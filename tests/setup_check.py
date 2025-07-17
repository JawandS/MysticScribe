#!/usr/bin/env python3
"""
Setup verification script for MysticScribe
Run this to check if everything is properly configured.
"""

import os
import sys
from pathlib import Path

def check_knowledge_files():
    """Check if all required knowledge files exist"""
    knowledge_dir = Path(__file__).parent / "knowledge"
    required_files = [
        'chapters.txt',
        'core_story_elements.txt', 
        'cultivation_system.txt',
        'economic.txt',
        'government.txt',
        'knowledge_system_overview.txt',
        'military.txt',
        'plot.txt',
        'regions.txt',
        'society.txt'
    ]
    
    missing_files = []
    for file in required_files:
        file_path = knowledge_dir / file
        if not file_path.exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing knowledge files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All knowledge files present")
        return True

def check_project_structure():
    """Check if project structure is correct"""
    base_dir = Path(__file__).parent
    required_paths = [
        "src/mysticscribe/__init__.py",
        "src/mysticscribe/main.py", 
        "src/mysticscribe/crew.py",
        "src/mysticscribe/config/agents.yaml",
        "src/mysticscribe/config/tasks.yaml",
        "src/mysticscribe/tools/__init__.py",
        "src/mysticscribe/tools/custom_tool.py",
        "pyproject.toml"
    ]
    
    missing_paths = []
    for path in required_paths:
        full_path = base_dir / path
        if not full_path.exists():
            missing_paths.append(path)
    
    if missing_paths:
        print("❌ Missing project files:")
        for path in missing_paths:
            print(f"   - {path}")
        return False
    else:
        print("✅ Project structure is correct")
        return True

def check_dependencies():
    """Check if required dependencies can be imported"""
    try:
        import crewai
        print("✅ CrewAI is installed")
        return True
    except ImportError:
        print("❌ CrewAI not installed. Run: pip install -e .")
        return False

def main():
    """Main setup check function"""
    print("MysticScribe Setup Verification")
    print("=" * 40)
    
    checks = [
        check_project_structure(),
        check_knowledge_files(),
        check_dependencies()
    ]
    
    if all(checks):
        print("\n🎉 Setup verification complete! MysticScribe is ready to use.")
        print("\nTry running:")
        print("  python -m mysticscribe.main run")
    else:
        print("\n⚠️  Some issues found. Please address them before using MysticScribe.")
        sys.exit(1)

if __name__ == "__main__":
    main()
