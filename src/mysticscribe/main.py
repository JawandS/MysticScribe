#!/usr/bin/env python
import sys
import warnings
import os
import re

from datetime import datetime
from pathlib import Path

from mysticscribe.crew import Mysticscribe

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def get_previous_chapter_context(chapter_number: str):
    """
    Load the context from previous chapters, with special focus on the immediate previous chapter.
    Returns formatted context that emphasizes continuity requirements.
    """
    try:
        chapter_num = int(chapter_number)
        if chapter_num <= 1:
            return "This is Chapter 1 - no previous chapters to reference."
        
        print(f"📖 Loading previous chapter context for continuity...")
        
        # Use the Previous Chapter Reader Tool to get comprehensive context
        from mysticscribe.tools.previous_chapter_reader import PreviousChapterReaderTool
        previous_reader = PreviousChapterReaderTool()
        previous_context = previous_reader._run(chapter_number)
        
        print(f"✅ Previous chapter context loaded - focusing on continuity from Chapter {chapter_num - 1}")
        
        return previous_context
        
    except Exception as e:
        print(f"⚠️ Could not load previous chapter context: {str(e)}")
        return f"Could not load previous chapter context: {str(e)}"


def get_next_chapter_number():
    """
    Get the next chapter number by checking existing chapters in the chapters directory.
    Returns the highest chapter number + 1, or 1 if no chapters exist.
    """
    chapters_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chapters")
    
    # Create chapters directory if it doesn't exist
    if not os.path.exists(chapters_dir):
        os.makedirs(chapters_dir)
        return 1
    
    # Find all chapter files
    chapter_files = [f for f in os.listdir(chapters_dir) if f.startswith("chapter_") and f.endswith(".md")]
    
    if not chapter_files:
        return 1
    
    # Extract chapter numbers
    chapter_numbers = []
    for filename in chapter_files:
        match = re.search(r'chapter_(\d+)\.md', filename)
        if match:
            chapter_numbers.append(int(match.group(1)))
    
    if not chapter_numbers:
        return 1
    
    return max(chapter_numbers) + 1

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run_architect_workflow(chapter_number: str = None):
    """
    Run the architect workflow with human approval gates.
    This implements the iterative, user-guided outline creation process.
    
    Workflow Steps:
    1. Context Check: Load all available story context, including chapters.txt and previous chapter files
    2. Outline Handling: Check for existing outline, expand or create new
    3. Generate/Expand: Use architect agent to create/improve outline
    4. Save & Pause: Save outline and pause for human review
    5. User Approval Gate: Wait for explicit user approval
    6. Return approved outline for next workflow stages
    """
    if chapter_number is None:
        chapter_number = str(get_next_chapter_number())
    
    print(f"\n=== Starting Architect Workflow for Chapter {chapter_number} ===")
    
    # Initialize crew and load knowledge context
    crew_instance = Mysticscribe()
    knowledge_context = crew_instance.load_knowledge_context()
    
    # Load previous chapter context for continuity
    previous_chapter_context = get_previous_chapter_context(chapter_number)
    
    # Step 1: Context Check - Load all available story context
    print(f"\n📚 Step 1: Context Check - Loading story context for Chapter {chapter_number}...")
    
    if int(chapter_number) > 1:
        print(f"📖 Loaded previous chapter context for continuity")
    else:
        print(f"📝 Chapter 1 - no previous chapters to reference")
    
    # Check if a draft already exists in chapters.txt via the ChapterAnalysisTool
    from mysticscribe.tools.custom_tool import ChapterAnalysisTool, OutlineManagementTool
    chapter_tool = ChapterAnalysisTool()
    existing_draft = chapter_tool._run(chapter_number)
    
    if "not found" not in existing_draft.lower():
        print(f"📖 Found existing draft material for Chapter {chapter_number}")
    else:
        print(f"📝 No existing draft found for Chapter {chapter_number}")
        existing_draft = ""
    
    # Step 2: Outline Handling - Check for existing outline
    print(f"\n📋 Step 2: Outline Handling - Checking for existing outline...")
    
    outline_tool = OutlineManagementTool()
    outline_check = outline_tool._run(chapter_number, "check")
    
    existing_outline = ""
    outline_action = "create_new"
    
    if "EXISTS" in outline_check:
        print(f"📄 Found existing outline for Chapter {chapter_number}")
        existing_outline = outline_tool._run(chapter_number, "load")
        print(f"📖 Loaded existing outline")
        
        # Ask if user wants to expand existing outline or create new one
        print(f"\nFound existing outline for Chapter {chapter_number}.")
        print("Options:")
        print("1. Expand and improve existing outline")
        print("2. Create a completely new outline")
        print("3. Use existing outline as-is")
        
        while True:
            choice = input("Choose option (1-3): ").strip()
            if choice in ['1', '2', '3']:
                break
            print("Please enter 1, 2, or 3")
        
        if choice == '1':
            outline_action = 'expand'
            print("📈 Will expand existing outline")
        elif choice == '2':
            existing_outline = ""
            outline_action = 'create_new'
            print("🆕 Will create new outline")
        else:  # choice == '3'
            print(f"✅ Using existing outline as-is")
            return existing_outline.replace("=== EXISTING OUTLINE FOR CHAPTER", "=== APPROVED OUTLINE FOR CHAPTER")
    else:
        print(f"📝 No existing outline found for Chapter {chapter_number}")
        print("🆕 Will create new outline")
    
    # Step 3: Generate/Expand outline using architect agent
    action_text = "Expanding" if outline_action == 'expand' else "Creating"
    print(f"\n🏗️  Step 3: {action_text} outline using architect agent...")
    
    # Prepare inputs for the architect agent
    inputs = {
        'chapter_number': chapter_number,
        'knowledge_context': knowledge_context,
        'previous_chapter_context': previous_chapter_context,
        'existing_draft': existing_draft,
        'existing_outline': existing_outline,
        'outline_action': outline_action,
        'current_year': str(datetime.now().year)
    }
    
    try:
        # Create a minimal crew with just the architect and outline task
        from crewai import Crew, Process, Task
        
        architect = crew_instance.architect()
        outline_task = crew_instance.outline_task()
        
        # Create a minimal crew for just the outline task
        outline_crew = Crew(
            agents=[architect],
            tasks=[outline_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the outline task
        print(f"🤖 Architect agent is working on the outline...")
        try:
            print(f"Debug: Executing outline_crew.kickoff with inputs: {inputs.keys()}")
            outline_result = outline_crew.kickoff(inputs=inputs)
            print(f"Debug: Outline result type: {type(outline_result)}")
            if not outline_result:
                print(f"Debug: Empty outline result")
                raise ValueError("Empty outline result returned from crew execution")
        except Exception as e:
            print(f"Debug: Error during outline crew execution: {str(e)}")
            raise
        
        # Step 4: Save outline and pause for human review
        print(f"\n💾 Step 4: Saving outline for human review...")
        
        # Save the outline
        save_result = outline_tool._run(chapter_number, "save", str(outline_result))
        print(save_result)
        
        # Get the outline file path for user reference
        outlines_dir = Path(__file__).parent.parent.parent / "outlines"
        outline_file = outlines_dir / f"chapter_{chapter_number}.txt"
        
        print(f"\n⏸️  PAUSE FOR HUMAN REVIEW")
        print(f"📁 Outline saved to: {outline_file}")
        print(f"📝 Please review and edit the outline file as needed.")
        print(f"💡 You can modify the outline directly in your editor.")
        print(f"🔧 Make any changes you want to the structure, pacing, or content.")
        
        # Step 5: User Approval Gate
        print(f"\n🔍 Step 5: User Approval Gate - Waiting for approval...")
        
        while True:
            approval = input(f"\nHave you reviewed and approved the outline for Chapter {chapter_number}? (y/n/q): ").strip().lower()
            
            if approval == 'q':
                print("❌ Workflow cancelled by user")
                return "Workflow cancelled"
            elif approval == 'y':
                print("✅ Outline approved! Ready for writer and editor agents...")
                break
            elif approval == 'n':
                print("📝 Please continue editing the outline file and return when ready.")
                print(f"📂 File location: {outline_file}")
            else:
                print("Please enter 'y' (yes), 'n' (not yet), or 'q' (quit)")
        
        # Step 6: Load the final approved outline
        print(f"\n📖 Step 6: Loading final approved outline...")
        approved_outline = outline_tool._run(chapter_number, "load")
        
        print(f"\n✅ Architect workflow complete for Chapter {chapter_number}")
        print(f"📋 Approved outline is ready for writer and editor agents")
        
        return approved_outline
        
    except Exception as e:
        print(f"❌ Error in architect workflow: {str(e)}")
        raise Exception(f"Architect workflow failed: {e}")


def run():
    """
    Run the crew to generate a chapter (legacy method).
    This skips the interactive architect workflow and runs all agents sequentially.
    Usage: python main.py run [chapter_number]
    """
    chapter_number = str(get_next_chapter_number())
    
    print(f"\n📚 Running Legacy Workflow for Chapter {chapter_number}")
    print("ℹ️  Note: This skips the interactive outline approval. Use 'workflow' for full control.")
    
    inputs = {
        'chapter_number': chapter_number,
        'current_year': str(datetime.now().year)
    }
    
    try:
        crew_instance = Mysticscribe()
        # Load knowledge context and add to inputs
        knowledge_context = crew_instance.load_knowledge_context()
        inputs['knowledge_context'] = knowledge_context
        
        # Load previous chapter context for continuity
        previous_chapter_context = get_previous_chapter_context(chapter_number)
        inputs['previous_chapter_context'] = previous_chapter_context
        
        # Check for existing draft material
        from mysticscribe.tools.custom_tool import ChapterAnalysisTool, OutlineManagementTool
        chapter_tool = ChapterAnalysisTool()
        existing_draft = chapter_tool._run(chapter_number)
        
        if "not found" not in existing_draft.lower():
            inputs['existing_draft'] = existing_draft
            print(f"📖 Found existing draft material for Chapter {chapter_number}")
        else:
            inputs['existing_draft'] = ""
        
        # Check for existing outline - if it exists, use it as approved
        outline_tool = OutlineManagementTool()
        outline_check = outline_tool._run(chapter_number, "check")
        
        if "EXISTS" in outline_check:
            existing_outline = outline_tool._run(chapter_number, "load")
            inputs['existing_outline'] = existing_outline
            inputs['approved_outline'] = existing_outline
            inputs['outline_action'] = 'use_existing'
            print(f"📋 Using existing outline for Chapter {chapter_number}")
        else:
            inputs['existing_outline'] = ""
            inputs['approved_outline'] = ""
            inputs['outline_action'] = 'create_new'
            print(f"🆕 Will create new outline for Chapter {chapter_number}")
        
        print(f"🚀 Running all agents sequentially...")
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Get the chapters directory path
        chapters_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chapters")
        output_file = os.path.join(chapters_dir, f"chapter_{chapter_number}.md")
        
        # Save the result to the file with validation
        os.makedirs(chapters_dir, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            # Extract the actual content from the CrewAI result
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
            
            # Validate content before saving
            word_count = len(content.split())
            if word_count < 1800:
                print(f"⚠️  WARNING: Chapter is only {word_count} words (minimum 2000 recommended)")
            elif word_count > 4200:
                print(f"⚠️  WARNING: Chapter is {word_count} words (maximum 4000 recommended)")
            else:
                print(f"✅ Chapter word count: {word_count} words (within target range)")
            
            # Check for AI patterns that shouldn't be there
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
                print(f"⚠️  WARNING: Found potential AI patterns: {found_patterns}")
                print("❌ Content may need manual review")
            else:
                print("✅ No AI meta-commentary patterns detected")
            
            f.write(content)
        
        print(f"\n=== Chapter {chapter_number} Generation Complete ===")
        print(f"📖 Output saved to: {output_file}")
        print(f"💡 Tip: Use 'python main.py workflow' for interactive outline approval")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def run_full_workflow(chapter_number: str = None):
    """
    Run the complete workflow: architect -> writer -> editor with approval gates.
    Usage: python main.py workflow [chapter_number]
    
    This implements the full iterative process:
    1. Architect phase with human approval gates for outline
    2. Writer and editor phases to create final chapter
    """
    if chapter_number is None:
        chapter_number = str(get_next_chapter_number())
    
    print(f"\n🚀 Starting Complete Chapter Workflow for Chapter {chapter_number}")
    
    try:
        # Step 1: Run architect workflow with approval gates
        print(f"\n=== PHASE 1: ARCHITECT ===")
        approved_outline = run_architect_workflow(chapter_number)
        
        if approved_outline == "Workflow cancelled":
            return "Workflow cancelled by user"
        
        # Step 2: Ask if user wants to continue to writing phase
        print(f"\n=== PHASE 2: WRITER & EDITOR ===")
        continue_writing = input("Proceed to writing and editing phase? (y/n): ").strip().lower()
        
        if continue_writing != 'y':
            print("✅ Stopping after outline phase. You can resume later with 'run' command.")
            return approved_outline
        
        # Step 3: Run the full crew with the approved outline
        print(f"📝 Initializing writer and editor agents...")
        crew_instance = Mysticscribe()
        knowledge_context = crew_instance.load_knowledge_context()
        
        # Load previous chapter context for continuity
        previous_chapter_context = get_previous_chapter_context(chapter_number)
        
        # Prepare inputs for the writing and editing phases
        inputs = {
            'chapter_number': chapter_number,
            'knowledge_context': knowledge_context,
            'previous_chapter_context': previous_chapter_context,
            'current_year': str(datetime.now().year),
            'approved_outline': approved_outline,
            'existing_draft': "",  # Clear since we're using the approved outline
            'existing_outline': approved_outline,
            'outline_action': 'use_approved'
        }
        
        print(f"🏃‍♂️ Running writer and editor agents for Chapter {chapter_number}...")
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Get the chapters directory path
        chapters_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chapters")
        output_file = os.path.join(chapters_dir, f"chapter_{chapter_number}.md")
        
        # Save the result to the file with validation
        os.makedirs(chapters_dir, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            # Extract the actual content from the CrewAI result
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
            
            # Validate content before saving
            word_count = len(content.split())
            if word_count < 1800:
                print(f"⚠️  WARNING: Chapter is only {word_count} words (minimum 2000 recommended)")
            elif word_count > 4200:
                print(f"⚠️  WARNING: Chapter is {word_count} words (maximum 4000 recommended)")
            else:
                print(f"✅ Chapter word count: {word_count} words (within target range)")
            
            # Check for AI patterns that shouldn't be there
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
                print(f"⚠️  WARNING: Found potential AI patterns: {found_patterns}")
                print("❌ Content may need manual review")
            else:
                print("✅ No AI meta-commentary patterns detected")
            
            f.write(content)
        
        print(f"\n🎉 Complete Chapter Workflow Finished!")
        print(f"📋 Outline: outlines/chapter_{chapter_number}.txt")
        print(f"📖 Chapter: {output_file}")
        print(f"✨ Chapter {chapter_number} is ready!")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in full workflow: {str(e)}")
        raise Exception(f"Full workflow failed: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    Usage: python main.py train <n_iterations> <filename> [chapter_number]
    """
    if len(sys.argv) > 4:
        chapter_number = sys.argv[4]
    else:
        chapter_number = str(get_next_chapter_number())
    
    inputs = {
        "chapter_number": chapter_number,
        'current_year': str(datetime.now().year)
    }
    
    try:
        crew_instance = Mysticscribe()
        # Load knowledge context and add to inputs
        knowledge_context = crew_instance.load_knowledge_context()
        inputs['knowledge_context'] = knowledge_context
        
        # Load previous chapter context for continuity
        previous_chapter_context = get_previous_chapter_context(chapter_number)
        inputs['previous_chapter_context'] = previous_chapter_context
        
        crew_instance.crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Mysticscribe().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    Usage: python main.py test <n_iterations> <eval_llm> [chapter_number]
    """
    if len(sys.argv) > 4:
        chapter_number = sys.argv[4]
    else:
        chapter_number = str(get_next_chapter_number())
    
    inputs = {
        "chapter_number": chapter_number,
        "current_year": str(datetime.now().year)
    }
    
    try:
        crew_instance = Mysticscribe()
        # Load knowledge context and add to inputs
        knowledge_context = crew_instance.load_knowledge_context()
        inputs['knowledge_context'] = knowledge_context
        
        # Load previous chapter context for continuity
        previous_chapter_context = get_previous_chapter_context(chapter_number)
        inputs['previous_chapter_context'] = previous_chapter_context
        
        crew_instance.crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("🏗️  MysticScribe Chapter Generation System")
        print("=" * 50)
        print("\nWorkflow Commands:")
        print("  python main.py workflow [chapter_number]               # 🌟 RECOMMENDED: Full interactive workflow")
        print("                                                          #     with outline approval gates")
        print("  python main.py architect [chapter_number]              # 📋 Outline creation only with approval")
        print("  python main.py run [chapter_number]                    # ⚡ Legacy: Skip outline approval")
        print("\nTraining & Testing:")
        print("  python main.py train <n_iterations> <filename> [chapter_number]") 
        print("  python main.py replay <task_id>")
        print("  python main.py test <n_iterations> <eval_llm> [chapter_number]")
        print("\nWorkflow Descriptions:")
        print("  📋 'architect' - Creates/expands outlines with human review and approval")
        print("  🌟 'workflow'  - Complete process: architect → user approval → writer → editor")
        print("  ⚡ 'run'       - Legacy mode: runs all agents without outline approval pause")
        print("\n💡 Tip: Use 'workflow' for best results with human oversight!")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "run":
        chapter_num = sys.argv[2] if len(sys.argv) > 2 else None
        if chapter_num:
            # Run with specific chapter number
            chapter_number = chapter_num
            inputs = {
                'chapter_number': chapter_number,
                'current_year': str(datetime.now().year)
            }
            
            try:
                print(f"\n📚 Running Legacy Workflow for Chapter {chapter_number}")
                print("ℹ️  Note: This skips the interactive outline approval. Use 'workflow' for full control.")
                
                crew_instance = Mysticscribe()
                knowledge_context = crew_instance.load_knowledge_context()
                inputs['knowledge_context'] = knowledge_context
                
                # Load previous chapter context for continuity
                previous_chapter_context = get_previous_chapter_context(chapter_number)
                inputs['previous_chapter_context'] = previous_chapter_context
                
                # Check for existing draft material
                from mysticscribe.tools.custom_tool import ChapterAnalysisTool, OutlineManagementTool
                chapter_tool = ChapterAnalysisTool()
                existing_draft = chapter_tool._run(chapter_number)
                
                if "not found" not in existing_draft.lower():
                    inputs['existing_draft'] = existing_draft
                    print(f"📖 Found existing draft material for Chapter {chapter_number}")
                else:
                    inputs['existing_draft'] = ""
                
                # Check for existing outline
                outline_tool = OutlineManagementTool()
                outline_check = outline_tool._run(chapter_number, "check")
                
                if "EXISTS" in outline_check:
                    existing_outline = outline_tool._run(chapter_number, "load")
                    inputs['existing_outline'] = existing_outline
                    inputs['approved_outline'] = existing_outline
                    inputs['outline_action'] = 'use_existing'
                    print(f"📋 Using existing outline for Chapter {chapter_number}")
                else:
                    inputs['existing_outline'] = ""
                    inputs['approved_outline'] = ""
                    inputs['outline_action'] = 'create_new'
                    print(f"🆕 Will create new outline for Chapter {chapter_number}")
                
                print(f"🚀 Running all agents sequentially...")
                result = crew_instance.crew().kickoff(inputs=inputs)
                
                chapters_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chapters")
                output_file = os.path.join(chapters_dir, f"chapter_{chapter_number}.md")
                
                # Save the result to the file with validation
                os.makedirs(chapters_dir, exist_ok=True)
                with open(output_file, 'w', encoding='utf-8') as f:
                    # Extract the actual content from the CrewAI result
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
                    
                    # Validate content before saving
                    word_count = len(content.split())
                    if word_count < 1800:
                        print(f"⚠️  WARNING: Chapter is only {word_count} words (minimum 2000 recommended)")
                    elif word_count > 4200:
                        print(f"⚠️  WARNING: Chapter is {word_count} words (maximum 4000 recommended)")
                    else:
                        print(f"✅ Chapter word count: {word_count} words (within target range)")
                    
                    # Check for AI patterns that shouldn't be there
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
                        print(f"⚠️  WARNING: Found potential AI patterns: {found_patterns}")
                        print("❌ Content may need manual review")
                    else:
                        print("✅ No AI meta-commentary patterns detected")
                    
                    f.write(content)
                
                print(f"\n=== Chapter {chapter_number} Generation Complete ===")
                print(f"📖 Output saved to: {output_file}")
                print(f"💡 Tip: Use 'python main.py workflow' for interactive outline approval")
            except Exception as e:
                raise Exception(f"An error occurred while running the crew: {e}")
        else:
            run()
    elif command == "architect":
        chapter_num = sys.argv[2] if len(sys.argv) > 2 else None
        run_architect_workflow(chapter_num)
    elif command == "workflow":
        chapter_num = sys.argv[2] if len(sys.argv) > 2 else None
        run_full_workflow(chapter_num)
    elif command == "train":
        if len(sys.argv) < 4:
            print("Usage: python main.py train <n_iterations> <filename> [chapter_number]")
            sys.exit(1)
        train()
    elif command == "replay":
        if len(sys.argv) < 3:
            print("Usage: python main.py replay <task_id>")
            sys.exit(1)
        replay()
    elif command == "test":
        if len(sys.argv) < 4:
            print("Usage: python main.py test <n_iterations> <eval_llm> [chapter_number]")
            sys.exit(1)
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
