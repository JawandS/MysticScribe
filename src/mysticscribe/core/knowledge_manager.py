"""
Knowledge Management System

Handles loading and managing the knowledge base for story generation.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class KnowledgeManager:
    """
    Manages the story knowledge base and provides access to world-building information.
    
    This class centralizes access to all knowledge files and provides
    structured access to story elements, world-building details, and plot information.
    """
    
    # Available knowledge files in order of loading priority
    KNOWLEDGE_FILES = [
        'knowledge_system_overview.txt',
        'core_story_elements.txt', 
        'plot.txt',
        'chapters.txt',
        'cultivation_system.txt',
        'regions.txt',
        'society.txt',
        'government.txt',
        'economic.txt',
        'military.txt'
    ]
    
    def __init__(self, project_root: Path):
        """
        Initialize the Knowledge Manager.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = Path(project_root)
        self.knowledge_dir = self.project_root / "knowledge"
        
        if not self.knowledge_dir.exists():
            logger.warning(f"Knowledge directory not found at: {self.knowledge_dir}")
            self.knowledge_dir.mkdir(parents=True, exist_ok=True)
    
    def load_all_knowledge(self) -> str:
        """
        Load all knowledge files into a single formatted context string.
        
        Returns:
            Formatted string containing all knowledge base content
        """
        context = "=== STORY KNOWLEDGE BASE ===\n\n"
        
        for filename in self.KNOWLEDGE_FILES:
            file_content = self.load_knowledge_file(filename)
            if file_content:
                context += f"=== {filename.upper().replace('.TXT', '')} ===\n"
                context += file_content
                context += "\n\n"
        
        return context
    
    def load_knowledge_file(self, filename: str) -> Optional[str]:
        """
        Load a specific knowledge file.
        
        Args:
            filename: Name of the knowledge file to load
            
        Returns:
            Content of the file, or None if file doesn't exist
        """
        file_path = self.knowledge_dir / filename
        
        if not file_path.exists():
            logger.warning(f"Knowledge file not found: {filename}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    logger.debug(f"Loaded knowledge file: {filename}")
                    return content
                else:
                    logger.warning(f"Knowledge file is empty: {filename}")
                    return None
        except Exception as e:
            logger.error(f"Error reading knowledge file {filename}: {e}")
            return None
    
    def get_available_files(self) -> List[str]:
        """
        Get list of available knowledge files.
        
        Returns:
            List of available knowledge file names
        """
        available = []
        for filename in self.KNOWLEDGE_FILES:
            file_path = self.knowledge_dir / filename
            if file_path.exists():
                available.append(filename)
        return available
    
    def get_missing_files(self) -> List[str]:
        """
        Get list of missing knowledge files.
        
        Returns:
            List of missing knowledge file names
        """
        missing = []
        for filename in self.KNOWLEDGE_FILES:
            file_path = self.knowledge_dir / filename
            if not file_path.exists():
                missing.append(filename)
        return missing
    
    def validate_knowledge_base(self) -> Dict[str, bool]:
        """
        Validate the knowledge base completeness.
        
        Returns:
            Dictionary mapping filenames to existence status
        """
        status = {}
        for filename in self.KNOWLEDGE_FILES:
            file_path = self.knowledge_dir / filename
            status[filename] = file_path.exists()
        return status
    
    def get_knowledge_summary(self) -> Dict[str, any]:
        """
        Get a summary of the knowledge base.
        
        Returns:
            Dictionary with knowledge base statistics and information
        """
        total_files = len(self.KNOWLEDGE_FILES)
        available_files = self.get_available_files()
        missing_files = self.get_missing_files()
        
        total_size = 0
        for filename in available_files:
            file_path = self.knowledge_dir / filename
            if file_path.exists():
                total_size += file_path.stat().st_size
        
        return {
            'total_files': total_files,
            'available_files': len(available_files),
            'missing_files': len(missing_files),
            'missing_file_names': missing_files,
            'total_size_bytes': total_size,
            'completeness_percentage': (len(available_files) / total_files) * 100
        }
    
    def search_knowledge(self, search_term: str, case_sensitive: bool = False) -> Dict[str, List[str]]:
        """
        Search for a term across all knowledge files.
        
        Args:
            search_term: Term to search for
            case_sensitive: Whether search should be case sensitive
            
        Returns:
            Dictionary mapping filenames to lists of matching lines
        """
        results = {}
        
        for filename in self.get_available_files():
            content = self.load_knowledge_file(filename)
            if not content:
                continue
            
            matches = []
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                search_line = line if case_sensitive else line.lower()
                search_target = search_term if case_sensitive else search_term.lower()
                
                if search_target in search_line:
                    matches.append(f"Line {line_num}: {line.strip()}")
            
            if matches:
                results[filename] = matches
        
        return results
