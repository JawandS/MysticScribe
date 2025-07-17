#!/usr/bin/env python3
"""
Example usage of MysticScribe
This script demonstrates how to use the three-agent system to generate chapters.
"""

import sys
import os
from datetime import datetime

# Add the src directory to the path so we can import mysticscribe
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def example_chapter_generation():
    """Example of generating a chapter"""
    try:
        from mysticscribe.crew import Mysticscribe
        
        print("🚀 Starting MysticScribe Chapter Generation Example")
        print("=" * 50)
        
        # Create crew instance
        crew_instance = Mysticscribe()
        
        # Load knowledge context
        print("📚 Loading knowledge context...")
        knowledge_context = crew_instance.load_knowledge_context()
        print(f"✅ Loaded {len(knowledge_context)} characters of context")
        
        # Set up inputs for chapter 1
        chapter_number = "1"
        inputs = {
            'chapter_number': chapter_number,
            'current_year': str(datetime.now().year),
            'knowledge_context': knowledge_context
        }
        
        print(f"📝 Generating Chapter {chapter_number}...")
        print("This will involve:")
        print("  1. 🎯 Outliner Agent: Creating detailed chapter outline")
        print("  2. ✍️  Writer Agent: Converting outline to prose")
        print("  3. 📖 Editor Agent: Polishing to 2000-4000 words")
        
        # Run the crew
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        print(f"\n🎉 Chapter {chapter_number} generation complete!")
        print(f"📄 Output saved to: chapter_{chapter_number}.md")
        
        return result
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install dependencies with: pip install -e .")
        return None
    except Exception as e:
        print(f"❌ Error during chapter generation: {e}")
        return None

def show_usage():
    """Show usage examples"""
    print("MysticScribe Usage Examples")
    print("=" * 30)
    print()
    print("1. Generate Chapter 1 (default):")
    print("   python -m mysticscribe.main run")
    print()
    print("2. Generate specific chapter:")
    print("   python -m mysticscribe.main run 3")
    print()
    print("3. Train the system:")
    print("   python -m mysticscribe.main train 5 training_data.pkl")
    print()
    print("4. Test the system:")
    print("   python -m mysticscribe.main test 3 gpt-4")
    print()
    print("5. Run this example:")
    print("   python example.py")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--usage":
        show_usage()
    else:
        example_chapter_generation()
