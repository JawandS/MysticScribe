#!/usr/bin/env python3
"""
MysticScribe - AI-Powered Story Chapter Generator

A simple, unified workflow for generating story chapters using AI agents.
Automatically detects the next chapter number and runs the complete workflow.

Usage:
    ./generate_chapter.py [chapter_number]    # Generate a chapter (auto-detects next if not specified)
    ./generate_chapter.py --help              # Show this help message
"""

import sys
import os
import re
import warnings
from datetime import datetime
from pathlib import Path

# Filter out pysbd warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def activate_virtual_environment():
    """Activate the virtual environment if it exists."""
    project_root = Path(__file__).parent
    venv_activate = project_root / ".venv" / "bin" / "activate"
    
    if venv_activate.exists():
        # Check if we're already in a virtual environment
        if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("ℹ️  Virtual environment detected but not activated")
            print(f"💡 Run: source .venv/bin/activate")
            print("   Then try again")
            return False
    return True


def get_next_chapter_number(project_root: Path) -> int:
    """Get the next chapter number by checking existing chapters."""
    chapters_dir = project_root / "chapters"
    
    if not chapters_dir.exists():
        chapters_dir.mkdir(exist_ok=True)
        return 1
    
    # Find all chapter files
    chapter_files = [f for f in chapters_dir.iterdir() if f.name.startswith("chapter_") and f.name.endswith(".md")]
    
    if not chapter_files:
        return 1
    
    # Extract chapter numbers
    chapter_numbers = []
    for file in chapter_files:
        match = re.search(r'chapter_(\d+)\.md', file.name)
        if match:
            chapter_numbers.append(int(match.group(1)))
    
    if not chapter_numbers:
        return 1
    
    return max(chapter_numbers) + 1


def load_knowledge_context(project_root: Path) -> str:
    """Load all knowledge files into a single context string."""
    knowledge_dir = project_root / "knowledge"
    context_parts = []
    
    if knowledge_dir.exists():
        for knowledge_file in knowledge_dir.glob("*.txt"):
            try:
                content = knowledge_file.read_text(encoding='utf-8')
                context_parts.append(f"=== {knowledge_file.name} ===\n{content}")
            except Exception as e:
                print(f"⚠️  Warning: Could not load {knowledge_file.name}: {e}")
    
    return "\n\n".join(context_parts) if context_parts else ""


def get_user_outline_decision(chapter_number: int, project_root: Path) -> tuple[str, str, bool]:
    """
    Check for existing outline and get user's decision on whether to use it or create new.
    Returns (outline_content, action, skip_architect) where:
    - outline_content: existing outline content (if any)
    - action: 'use_existing' or 'create_new'
    - skip_architect: True if architect should be skipped, False otherwise
    """
    outlines_dir = project_root / "outlines"
    outline_file = outlines_dir / f"chapter_{chapter_number}.txt"
    
    if outline_file.exists():
        try:
            content = outline_file.read_text(encoding='utf-8')
            if content.strip():
                print(f"\n📋 Found existing outline for Chapter {chapter_number}")
                print("=" * 60)
                # Show preview of outline (first 300 characters)
                preview = content[:300]
                if len(content) > 300:
                    preview += "..."
                print(f"Preview:\n{preview}\n")
                print("=" * 60)
                
                while True:
                    choice = input("Do you want to:\n[1] Use existing outline (skip to writing)\n[2] Generate new outline\nEnter choice (1 or 2): ").strip()
                    if choice == "1":
                        print("✅ Using existing outline - skipping to writer")
                        return content, 'use_existing', True
                    elif choice == "2":
                        print("📝 Will generate new outline")
                        return '', 'create_new', False
                    else:
                        print("❌ Please enter 1 or 2")
        except Exception as e:
            print(f"⚠️  Warning: Could not read outline file: {e}")
    
    print(f"📝 No existing outline found for Chapter {chapter_number}")
    return '', 'create_new', False


def get_user_approval_for_outline(chapter_number: int, project_root: Path) -> bool:
    """
    Wait for user to review and approve the generated outline.
    Returns True if approved, False if user wants to regenerate.
    """
    outlines_dir = project_root / "outlines"
    outline_file = outlines_dir / f"chapter_{chapter_number}.txt"
    
    print(f"\n⏸️  OUTLINE GENERATED - APPROVAL GATE")
    print("=" * 60)
    print(f"📋 Chapter {chapter_number} outline has been generated and saved to:")
    print(f"   {outline_file}")
    print("\nPlease review the outline and make any edits if needed.")
    print("=" * 60)
    
    while True:
        choice = input("Outline ready? Choose:\n[1] Approve outline and continue to writing\n[2] Regenerate outline\nEnter choice (1 or 2): ").strip()
        if choice == "1":
            print("✅ Outline approved - continuing to writer")
            return True
        elif choice == "2":
            print("🔄 Will regenerate outline")
            return False
        else:
            print("❌ Please enter 1 or 2")


def get_previous_chapter_context(chapter_number: int, project_root: Path) -> str:
    """Load context from the previous chapter for continuity."""
    if chapter_number <= 1:
        return "This is Chapter 1 - no previous chapters to reference."
    
    previous_chapter_file = project_root / "chapters" / f"chapter_{chapter_number - 1}.md"
    
    if previous_chapter_file.exists():
        try:
            content = previous_chapter_file.read_text(encoding='utf-8')
            # Take the last 1000 characters for context
            if len(content) > 1000:
                content = "..." + content[-1000:]
            return f"=== Previous Chapter ({chapter_number - 1}) Context ===\n{content}"
        except Exception as e:
            return f"Could not load previous chapter context: {e}"
    
    return f"Chapter {chapter_number - 1} file not found - no previous context available."


def validate_chapter_content(content: str, chapter_number: int) -> None:
    """Validate the generated chapter content."""
    word_count = len(content.split())
    
    print(f"📊 Chapter {chapter_number} Statistics:")
    print(f"   Word count: {word_count}")
    
    if word_count < 1800:
        print(f"⚠️  WARNING: Chapter is only {word_count} words (recommended: 2000-4000)")
    elif word_count > 4200:
        print(f"⚠️  WARNING: Chapter is {word_count} words (recommended: 2000-4000)")
    else:
        print(f"✅ Word count within recommended range")
    
    # Check for AI meta-commentary patterns
    ai_patterns = [
        "The completed Chapter",
        "This chapter",
        "In this chapter", 
        "The following chapter",
        "Chapter Summary:",
        "**Chapter"
    ]
    
    found_patterns = [pattern for pattern in ai_patterns if pattern.lower() in content.lower()]
    if found_patterns:
        print(f"⚠️  WARNING: Found potential AI meta-commentary: {found_patterns}")
        print("   Content may need manual review")
    else:
        print("✅ No AI meta-commentary detected")


def run_workflow(chapter_number: int, project_root: Path) -> None:
    """Run the unified MysticScribe workflow with approval gates."""
    print(f"\n🚀 MysticScribe Workflow - Chapter {chapter_number}")
    print("=" * 60)
    
    # Add src to Python path
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    try:
        # Import MysticScribe crew
        from mysticscribe.crew import Mysticscribe
        
        print(f"📚 Loading story context...")
        
        # Check for existing outline and get user decision
        existing_outline, outline_action, skip_architect = get_user_outline_decision(chapter_number, project_root)
        
        # If using existing outline, skip directly to writer
        if skip_architect:
            print(f"🤖 Initializing AI agents...")
            crew_instance = Mysticscribe()
            
            # Prepare inputs for writer (skipping architect)
            inputs = {
                'chapter_number': str(chapter_number),
                'current_year': str(datetime.now().year),
                'knowledge_context': load_knowledge_context(project_root),
                'previous_chapter_context': get_previous_chapter_context(chapter_number, project_root),
                'existing_draft': '',
                'existing_outline': existing_outline,
                'outline_action': 'use_existing',
                'approved_outline': existing_outline
            }
            
            print(f"✍️  Skipping to writer - using existing outline...")
            
            # Create a workflow with only writer and editor
            from crewai import Crew, Process
            writing_task = crew_instance.create_writing_task_with_context()
            editing_task = crew_instance.create_editing_task_with_context()
            
            limited_crew = Crew(
                agents=[crew_instance.writer(), crew_instance.editor()],
                tasks=[writing_task, editing_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = limited_crew.kickoff(inputs=inputs)
        else:
            # Full workflow with outline generation and approval
            outline_approved = False
            while not outline_approved:
                print(f"🤖 Initializing AI agents...")
                crew_instance = Mysticscribe()
                
                # Prepare initial inputs
                inputs = {
                    'chapter_number': str(chapter_number),
                    'current_year': str(datetime.now().year),
                    'knowledge_context': load_knowledge_context(project_root),
                    'previous_chapter_context': get_previous_chapter_context(chapter_number, project_root),
                    'existing_draft': '',
                    'existing_outline': existing_outline,
                    'outline_action': outline_action,
                    'approved_outline': ''  # Will be set after approval
                }
                
                print(f"📋 Generating outline for Chapter {chapter_number}...")
                
                # Run only the outline task
                from crewai import Crew, Process
                outline_crew = Crew(
                    agents=[crew_instance.architect()],
                    tasks=[crew_instance.outline_task()],
                    process=Process.sequential,
                    verbose=True
                )
                
                outline_result = outline_crew.kickoff(inputs=inputs)
                
                # Extract and save the outline
                if hasattr(outline_result, 'raw'):
                    outline_content = outline_result.raw
                elif hasattr(outline_result, 'output'):
                    outline_content = outline_result.output
                else:
                    outline_content = str(outline_result)
                
                # Save outline to file
                outlines_dir = project_root / "outlines"
                outlines_dir.mkdir(exist_ok=True)
                outline_file = outlines_dir / f"chapter_{chapter_number}.txt"
                outline_file.write_text(outline_content, encoding='utf-8')
                
                # Get user approval
                outline_approved = get_user_approval_for_outline(chapter_number, project_root)
                
                if not outline_approved:
                    existing_outline = ''  # Clear existing outline for regeneration
                    outline_action = 'create_new'
            
            # Now run writer and editor with approved outline
            print(f"✍️  Continuing with writer and editor...")
            
            # Update inputs with approved outline
            inputs['approved_outline'] = outline_content
            inputs['existing_outline'] = outline_content
            
            # Create crew for writing and editing
            writing_task = crew_instance.create_writing_task_with_context()
            editing_task = crew_instance.create_editing_task_with_context()
            
            writing_crew = Crew(
                agents=[crew_instance.writer(), crew_instance.editor()],
                tasks=[writing_task, editing_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = writing_crew.kickoff(inputs=inputs)
        
        # Save the final result
        chapters_dir = project_root / "chapters"
        chapters_dir.mkdir(exist_ok=True)
        output_file = chapters_dir / f"chapter_{chapter_number}.md"
        
        # Extract content from CrewAI result
        if hasattr(result, 'raw'):
            content = result.raw
        elif hasattr(result, 'output'):
            content = result.output
        else:
            content = str(result)
        
        # Save to file
        output_file.write_text(content, encoding='utf-8')
        
        # Validate the content
        validate_chapter_content(content, chapter_number)
        
        print(f"\n🎉 Chapter {chapter_number} Complete!")
        print(f"📖 Saved to: {output_file}")
        print(f"✨ Ready for review and editing!")
        
    except ImportError as e:
        print(f"❌ Error: Could not import MysticScribe modules: {e}")
        print("Make sure dependencies are installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Workflow interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during workflow execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def print_help():
    """Print help message."""
    print(__doc__)
    print("\nExamples:")
    print("  ./generate_chapter.py           # Generate next chapter automatically")
    print("  ./generate_chapter.py 5         # Generate chapter 5 specifically")
    print("\nPrerequisites:")
    print("  1. Activate virtual environment: source .venv/bin/activate")
    print("  2. Install dependencies: pip install -r requirements.txt")
    print("  3. Set up your story knowledge in the 'knowledge/' directory")


def main():
    """Main entry point for MysticScribe."""
    
    # Get project root
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)
    
    # Check for help request
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print_help()
        return
    
    # Check virtual environment
    if not activate_virtual_environment():
        sys.exit(1)
    
    # Get chapter number
    chapter_number = None
    if len(sys.argv) > 1:
        try:
            chapter_number = int(sys.argv[1])
            if chapter_number < 1:
                print("❌ Error: Chapter number must be positive")
                sys.exit(1)
        except ValueError:
            print(f"❌ Error: '{sys.argv[1]}' is not a valid chapter number")
            print("Use a positive integer or no argument for auto-detection")
            sys.exit(1)
    
    # Auto-detect chapter number if not provided
    if chapter_number is None:
        chapter_number = get_next_chapter_number(project_root)
        print(f"🔍 Auto-detected next chapter: Chapter {chapter_number}")
    
    try:
        # Run the workflow
        run_workflow(chapter_number, project_root)
        
    except KeyboardInterrupt:
        print("\n⏹️  Workflow interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
