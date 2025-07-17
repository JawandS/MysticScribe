#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from mysticscribe.crew import Mysticscribe

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew to generate a chapter.
    Usage: python main.py run [chapter_number]
    """
    chapter_number = sys.argv[2] if len(sys.argv) > 2 else "1"
    
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
        print(f"\n=== Chapter {chapter_number} Generation Complete ===")
        print(f"Output saved to: chapter_{chapter_number}.md")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    Usage: python main.py train <n_iterations> <filename> [chapter_number]
    """
    chapter_number = sys.argv[4] if len(sys.argv) > 4 else "1"
    
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
    chapter_number = sys.argv[4] if len(sys.argv) > 4 else "1"
    
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
