from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os


class PreviousChapterReaderInput(BaseModel):
    """Input schema for PreviousChapterReaderTool."""
    target_chapter: str = Field(
        ..., 
        description="The chapter number you are currently planning. The tool will read all previous chapters (e.g. if you specify '3', it will read chapters 1 and 2)."
    )

class PreviousChapterReaderTool(BaseTool):
    name: str = "Previous Chapter Reader"
    description: str = (
        "Read and analyze all previously written chapters up to the target chapter number. Use this to maintain continuity, reference past events, and build upon character development from earlier chapters."
    )
    args_schema: Type[BaseModel] = PreviousChapterReaderInput

    def _run(self, target_chapter: str) -> str:
        try:
            # Convert target chapter to integer
            target_chapter_num = int(target_chapter)
            
            if target_chapter_num <= 1:
                return "No previous chapters to read for Chapter 1."
                
            # Get the chapters directory path
            current_dir = os.path.dirname(__file__)
            chapters_dir = os.path.join(current_dir, '..', '..', '..', 'chapters')
            
            if not os.path.exists(chapters_dir):
                return "Chapters directory not found."
            
            previous_chapters = []
            
            # Collect all previous chapters
            for chapter_num in range(1, target_chapter_num):
                chapter_file = os.path.join(chapters_dir, f'chapter_{chapter_num}.md')
                
                if os.path.exists(chapter_file):
                    with open(chapter_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    previous_chapters.append((chapter_num, content))
            
            if not previous_chapters:
                return f"No previous chapters found for Chapter {target_chapter}."
            
            # Format the response
            result = f"=== PREVIOUS CHAPTERS ANALYSIS FOR PLANNING CHAPTER {target_chapter} ===\n\n"
            
            for chapter_num, content in previous_chapters:
                result += f"--- CHAPTER {chapter_num} ---\n\n"
                result += content
                result += "\n\n"
            
            result += "=== PREVIOUS CHAPTERS SUMMARY ===\n\n"
            result += f"Found and analyzed {len(previous_chapters)} previous chapters before Chapter {target_chapter}.\n"
            result += "Use this information to maintain continuity, reference past events, build upon established character development, and ensure narrative progression."
            
            return result
                
        except Exception as e:
            return f"Error reading previous chapters: {str(e)}"
