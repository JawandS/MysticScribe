from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os


class KnowledgeLookupInput(BaseModel):
    """Input schema for KnowledgeLookupTool."""
    knowledge_file: str = Field(
        ..., 
        description="Name of the knowledge file to read. Available files: chapters.txt, core_story_elements.txt, cultivation_system.txt, economic.txt, government.txt, knowledge_system_overview.txt, military.txt, plot.txt, regions.txt, society.txt"
    )

class KnowledgeLookupTool(BaseTool):
    name: str = "Knowledge Lookup"
    description: str = (
        "Read specific knowledge files from the story knowledge base. Use this to get detailed information about specific aspects of the story world, characters, plot, or systems."
    )
    args_schema: Type[BaseModel] = KnowledgeLookupInput

    def _run(self, knowledge_file: str) -> str:
        try:
            # Get the knowledge directory path
            current_dir = os.path.dirname(__file__)
            knowledge_dir = os.path.join(current_dir, '..', '..', '..', 'knowledge')
            file_path = os.path.join(knowledge_dir, knowledge_file)
            
            if not os.path.exists(file_path):
                return f"Knowledge file '{knowledge_file}' not found. Available files: chapters.txt, core_story_elements.txt, cultivation_system.txt, economic.txt, government.txt, knowledge_system_overview.txt, military.txt, plot.txt, regions.txt, society.txt"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return f"=== {knowledge_file.upper()} ===\n\n{content}"
                
        except Exception as e:
            return f"Error reading knowledge file: {str(e)}"


class ChapterAnalysisInput(BaseModel):
    """Input schema for ChapterAnalysisTool."""
    chapter_number: str = Field(..., description="The chapter number to analyze (e.g., '1', '2', etc.)")

class ChapterAnalysisTool(BaseTool):
    name: str = "Chapter Analysis"
    description: str = (
        "Analyze the chapter structure and get specific details about a particular chapter from the chapters.txt file."
    )
    args_schema: Type[BaseModel] = ChapterAnalysisInput

    def _run(self, chapter_number: str) -> str:
        try:
            # Get the knowledge directory path
            current_dir = os.path.dirname(__file__)
            knowledge_dir = os.path.join(current_dir, '..', '..', '..', 'knowledge')
            file_path = os.path.join(knowledge_dir, 'chapters.txt')
            
            if not os.path.exists(file_path):
                return "chapters.txt file not found in knowledge directory"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for the specific chapter in the content
            lines = content.split('\n')
            chapter_content = []
            in_target_chapter = False
            
            for line in lines:
                if f"Chapter {chapter_number}:" in line or f"#### Chapter {chapter_number}:" in line:
                    in_target_chapter = True
                    chapter_content.append(line)
                elif in_target_chapter and line.startswith(('#### Chapter', '### Chapter')) and f"Chapter {chapter_number}" not in line:
                    break
                elif in_target_chapter:
                    chapter_content.append(line)
            
            if chapter_content:
                return f"=== CHAPTER {chapter_number} DETAILS ===\n\n" + '\n'.join(chapter_content)
            else:
                return f"Chapter {chapter_number} not found in chapters.txt. Please check the chapter number or refer to the full chapters.txt file."
                
        except Exception as e:
            return f"Error analyzing chapter: {str(e)}"


class OutlineManagementInput(BaseModel):
    """Input schema for OutlineManagementTool."""
    chapter_number: str = Field(..., description="The chapter number (e.g., '1', '2', etc.)")
    action: str = Field(..., description="Action to perform: 'check', 'load', or 'save'")
    outline_content: str = Field(default="", description="Outline content to save (only used with 'save' action)")

class OutlineManagementTool(BaseTool):
    name: str = "Outline Management"
    description: str = (
        "Manage chapter outlines: check if an outline exists, load existing outline, or save a new outline to the outlines directory."
    )
    args_schema: Type[BaseModel] = OutlineManagementInput

    def _run(self, chapter_number: str, action: str, outline_content: str = "") -> str:
        try:
            # Get the outlines directory path
            current_dir = os.path.dirname(__file__)
            outlines_dir = os.path.join(current_dir, '..', '..', '..', 'outlines')
            
            # Ensure outlines directory exists
            if not os.path.exists(outlines_dir):
                os.makedirs(outlines_dir)
            
            outline_file = os.path.join(outlines_dir, f'chapter_{chapter_number}.txt')
            
            if action == 'check':
                exists = os.path.exists(outline_file)
                return f"Outline for chapter {chapter_number}: {'EXISTS' if exists else 'NOT FOUND'}"
            
            elif action == 'load':
                if not os.path.exists(outline_file):
                    return f"No existing outline found for chapter {chapter_number}"
                
                with open(outline_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                return f"=== EXISTING OUTLINE FOR CHAPTER {chapter_number} ===\n\n{content}"
            
            elif action == 'save':
                if not outline_content.strip():
                    return "Cannot save empty outline content"
                
                with open(outline_file, 'w', encoding='utf-8') as f:
                    f.write(outline_content)
                return f"Outline saved successfully to: {outline_file}"
            
            else:
                return f"Invalid action '{action}'. Use 'check', 'load', or 'save'"
                
        except Exception as e:
            return f"Error in outline management: {str(e)}"
