#!/usr/bin/env python
import sys
import warnings
import os
import re

from datetime import datetime

from mysticscribe.crew import Mysticscribe

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

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

def run():
    """
    Run the crew to generate a chapter.
    Usage: python main.py run [chapter_number]
    """
    chapter_number = str(get_next_chapter_number())
    
    inputs = {
        'chapter_number': chapter_number,
        'current_year': str(datetime.now().year)
    }
    
    try:
        crew_instance = Mysticscribe()
        # Load knowledge context and add to inputs
        knowledge_context = crew_instance.load_knowledge_context()
        inputs['knowledge_context'] = knowledge_context
        
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Get the chapters directory path
        chapters_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chapters")
        output_file = os.path.join(chapters_dir, f"chapter_{chapter_number}.md")
        
        print(f"\n=== Chapter {chapter_number} Generation Complete ===")
        print(f"Output saved to: {output_file}")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


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
        
        crew_instance.crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py run [chapter_number]")
        print("  python main.py train <n_iterations> <filename> [chapter_number]") 
        print("  python main.py replay <task_id>")
        print("  python main.py test <n_iterations> <eval_llm> [chapter_number]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "run":
        run()
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
