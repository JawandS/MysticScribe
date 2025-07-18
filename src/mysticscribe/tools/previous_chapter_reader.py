from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import re


class PreviousChapterReaderInput(BaseModel):
    """Input schema for PreviousChapterReaderTool."""
    target_chapter: str = Field(
        ..., 
        description="The chapter number you are currently planning. The tool will read all previous chapters (e.g. if you specify '3', it will read chapters 1 and 2)."
    )

class PreviousChapterReaderTool(BaseTool):
    name: str = "Previous Chapter Reader"
    description: str = (
        "Read and analyze all previously written chapters up to the target chapter number. Use this to maintain continuity, reference past events, and build upon character development from earlier chapters. Provides special focus on how the previous chapter ended to ensure seamless continuation."
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
            
            # Get the immediate previous chapter (most recent) for special focus
            immediate_previous = previous_chapters[-1] if previous_chapters else None
            
            # Extract the ending of the immediate previous chapter for continuity focus
            def extract_chapter_ending(content: str, paragraphs: int = 3) -> str:
                """Extract the last few paragraphs of a chapter to focus on how it ended."""
                # Split into paragraphs and get the last few non-empty ones
                paragraphs_list = [p.strip() for p in content.split('\n\n') if p.strip()]
                if len(paragraphs_list) >= paragraphs:
                    return '\n\n'.join(paragraphs_list[-paragraphs:])
                else:
                    return '\n\n'.join(paragraphs_list)
            
            # Format the response with special focus on continuity
            result = f"=== PREVIOUS CHAPTERS ANALYSIS FOR CHAPTER {target_chapter} ===\n\n"
            
            if immediate_previous:
                chapter_num, content = immediate_previous
                ending = extract_chapter_ending(content)
                result += f"=== IMMEDIATE PREVIOUS CHAPTER ({chapter_num}) ENDING - CRITICAL FOR CONTINUITY ===\n\n"
                result += ending
                result += "\n\n=== CONTINUITY REQUIREMENTS ===\n"
                result += f"• Chapter {target_chapter} must begin where Chapter {chapter_num} ended\n"
                result += "• Address any cliffhangers, unresolved tensions, or character states from the ending\n"
                result += "• Maintain the emotional tone and momentum established at the end of the previous chapter\n"
                result += "• Reference the immediate situation, location, and character states from the previous chapter's conclusion\n\n"
            
            # Include summaries of all previous chapters for broader context
            result += "=== ALL PREVIOUS CHAPTERS SUMMARY ===\n\n"
            
            for chapter_num, content in previous_chapters:
                # Extract key plot points and character moments
                words = content.split()
                if len(words) > 100:
                    # Create a condensed summary focusing on key events
                    result += f"--- CHAPTER {chapter_num} KEY POINTS ---\n"
                    
                    # Try to extract the first and last paragraphs plus any dialogue for context
                    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                    
                    if len(paragraphs) >= 3:
                        result += f"Opening: {paragraphs[0][:200]}...\n\n"
                        
                        # Look for key dialogue or action sequences
                        key_moments = []
                        for p in paragraphs[1:-1]:
                            if '"' in p or any(action in p.lower() for action in ['said', 'shouted', 'whispered', 'fought', 'attacked', 'discovered']):
                                key_moments.append(p[:150] + "...")
                        
                        if key_moments:
                            result += "Key moments:\n"
                            for moment in key_moments[:3]:  # Limit to 3 key moments
                                result += f"• {moment}\n"
                            result += "\n"
                        
                        result += f"Ending: {paragraphs[-1][:200]}...\n\n"
                    else:
                        result += content[:300] + "...\n\n"
                else:
                    result += content + "\n\n"
            
            result += "=== OVERALL STORY CONTINUITY NOTES ===\n\n"
            result += f"Found and analyzed {len(previous_chapters)} previous chapters before Chapter {target_chapter}.\n"
            result += "Key considerations for Chapter " + target_chapter + ":\n"
            result += "• Maintain character development arcs established in previous chapters\n"
            result += "• Reference and build upon plot threads introduced earlier\n"
            result += "• Ensure world-building elements remain consistent\n"
            result += "• Create natural progression from previous events\n"
            result += "• Address any foreshadowing or setup from earlier chapters\n"
            
            if immediate_previous:
                result += f"\nCRITICAL: Pay special attention to how Chapter {immediate_previous[0]} ended. Chapter {target_chapter} should feel like a natural continuation, not a restart."
            
            return result
                
        except Exception as e:
            return f"Error reading previous chapters: {str(e)}"
