from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import re


class StyleAnalysisInput(BaseModel):
    """Input schema for StyleAnalysisTool."""
    target_chapter: str = Field(
        ..., 
        description="The chapter number you are currently polishing (e.g., '2', '3', etc.). The tool will analyze the style of all previous chapters."
    )

class StyleAnalysisTool(BaseTool):
    name: str = "Style Analysis"
    description: str = (
        "Analyze the specific writing style, patterns, and techniques used in previous chapters to ensure stylistic consistency. Provides detailed analysis of sentence structures, imagery patterns, dialogue styles, and atmospheric techniques."
    )
    args_schema: Type[BaseModel] = StyleAnalysisInput

    def _run(self, target_chapter: str) -> str:
        try:
            # Convert target chapter to integer
            target_chapter_num = int(target_chapter)
            
            if target_chapter_num <= 1:
                return "No previous chapters to analyze for Chapter 1."
                
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
                return f"No previous chapters found for style analysis."
            
            # Analyze style patterns
            style_analysis = self._analyze_writing_style(previous_chapters)
            
            return f"=== STYLE ANALYSIS FOR CHAPTER {target_chapter} POLISHING ===\n\n{style_analysis}"
                
        except Exception as e:
            return f"Error analyzing writing style: {str(e)}"
    
    def _analyze_writing_style(self, chapters):
        """Analyze writing style patterns from the chapters."""
        
        analysis = ""
        
        # Combine all chapter content for analysis
        all_text = ""
        for chapter_num, content in chapters:
            all_text += content + "\n\n"
        
        # Analyze sentence patterns
        sentences = re.split(r'[.!?]+', all_text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        
        if sentences:
            short_sentences = [s for s in sentences if len(s.split()) <= 8]
            medium_sentences = [s for s in sentences if 9 <= len(s.split()) <= 20]
            long_sentences = [s for s in sentences if len(s.split()) > 20]
            
            analysis += "=== SENTENCE STRUCTURE PATTERNS ===\n"
            analysis += f"• Short sentences (≤8 words): {len(short_sentences)} ({len(short_sentences)/len(sentences)*100:.1f}%)\n"
            analysis += f"• Medium sentences (9-20 words): {len(medium_sentences)} ({len(medium_sentences)/len(sentences)*100:.1f}%)\n"
            analysis += f"• Long sentences (>20 words): {len(long_sentences)} ({len(long_sentences)/len(sentences)*100:.1f}%)\n\n"
            
            if short_sentences:
                analysis += "Short sentence examples:\n"
                for example in short_sentences[:3]:
                    analysis += f"  • \"{example.strip()}\"\n"
                analysis += "\n"
        
        # Analyze imagery and metaphor patterns
        analysis += "=== IMAGERY AND METAPHOR PATTERNS ===\n"
        metaphor_patterns = []
        
        # Look for common metaphorical constructions
        metaphor_indicators = [
            r'like a [^,.!?]*',
            r'as [^,.!?]* as',
            r'was a [^,.!?]*',
            r'seemed to [^,.!?]*',
            r'coiled like [^,.!?]*',
            r'carved from [^,.!?]*'
        ]
        
        for pattern in metaphor_indicators:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                metaphor_patterns.extend(matches[:2])  # Limit examples
        
        if metaphor_patterns:
            analysis += "Metaphor/simile patterns found:\n"
            for pattern in metaphor_patterns[:5]:
                analysis += f"  • \"{pattern}\"\n"
            analysis += "\n"
        
        # Analyze dialogue patterns
        analysis += "=== DIALOGUE STYLE PATTERNS ===\n"
        dialogue_lines = re.findall(r'"([^"]*)"', all_text)
        
        if dialogue_lines:
            short_dialogue = [d for d in dialogue_lines if len(d.split()) <= 5]
            analysis += f"• Total dialogue lines: {len(dialogue_lines)}\n"
            analysis += f"• Short dialogue (≤5 words): {len(short_dialogue)} ({len(short_dialogue)/len(dialogue_lines)*100:.1f}%)\n"
            
            # Look for dialogue tag patterns
            dialogue_tag_patterns = re.findall(r'"\s*[^"]*"\s*([^.!?]*(?:said|asked|whispered|called|grunted|muttered|crowed|admonished)[^.!?]*)', all_text, re.IGNORECASE)
            if dialogue_tag_patterns:
                analysis += "Common dialogue tag patterns:\n"
                for tag in dialogue_tag_patterns[:3]:
                    analysis += f"  • {tag.strip()}\n"
            analysis += "\n"
        
        # Analyze descriptive techniques
        analysis += "=== DESCRIPTIVE TECHNIQUE PATTERNS ===\n"
        
        # Look for sensory details
        sensory_patterns = {
            'Visual': [r'gleam', r'glow', r'flicker', r'shimmer', r'shadow', r'light'],
            'Auditory': [r'whisper', r'echo', r'silence', r'thump', r'shriek', r'vibrated'],
            'Tactile': [r'cold', r'warm', r'rough', r'smooth', r'sharp', r'soft'],
            'Olfactory': [r'scent', r'smell', r'aroma', r'stench', r'fragrance'],
            'Physical': [r'ache', r'pulse', r'tremble', r'shiver', r'burn']
        }
        
        for sense_type, patterns in sensory_patterns.items():
            count = 0
            for pattern in patterns:
                count += len(re.findall(pattern, all_text, re.IGNORECASE))
            if count > 0:
                analysis += f"• {sense_type} details: {count} instances\n"
        
        analysis += "\n"
        
        # Analyze atmospheric elements
        analysis += "=== ATMOSPHERIC TECHNIQUE PATTERNS ===\n"
        
        # Look for weather/environment descriptions
        atmospheric_elements = [
            r'wind[^.!?]*',
            r'mist[^.!?]*', 
            r'dawn[^.!?]*',
            r'dusk[^.!?]*',
            r'shadow[^.!?]*',
            r'air[^.!?]*'
        ]
        
        atmosphere_examples = []
        for pattern in atmospheric_elements:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                atmosphere_examples.extend(matches[:1])
        
        if atmosphere_examples:
            analysis += "Atmospheric description examples:\n"
            for example in atmosphere_examples[:3]:
                analysis += f"  • \"{example.strip()}\"\n"
            analysis += "\n"
        
        # Analyze paragraph structure
        paragraphs = [p.strip() for p in all_text.split('\n\n') if p.strip()]
        if paragraphs:
            short_paras = [p for p in paragraphs if len(p.split()) <= 30]
            medium_paras = [p for p in paragraphs if 31 <= len(p.split()) <= 100]
            long_paras = [p for p in paragraphs if len(p.split()) > 100]
            
            analysis += "=== PARAGRAPH STRUCTURE PATTERNS ===\n"
            analysis += f"• Short paragraphs (≤30 words): {len(short_paras)} ({len(short_paras)/len(paragraphs)*100:.1f}%)\n"
            analysis += f"• Medium paragraphs (31-100 words): {len(medium_paras)} ({len(medium_paras)/len(paragraphs)*100:.1f}%)\n"
            analysis += f"• Long paragraphs (>100 words): {len(long_paras)} ({len(long_paras)/len(paragraphs)*100:.1f}%)\n\n"
        
        # Character voice analysis
        analysis += "=== CHARACTER VOICE PATTERNS ===\n"
        
        # Look for character-specific dialogue patterns
        character_patterns = re.findall(r'([A-Z][a-z]+)(?:\s+[a-z]*)*[^.!?]*(?:said|asked|whispered|called|grunted|muttered|crowed|admonished)', all_text)
        if character_patterns:
            from collections import Counter
            char_counts = Counter(character_patterns)
            analysis += "Characters with dialogue:\n"
            for char, count in char_counts.most_common(5):
                analysis += f"  • {char}: {count} instances\n"
            analysis += "\n"
        
        analysis += "=== STYLE CONSISTENCY GUIDELINES ===\n"
        analysis += "Based on the analysis above, maintain these patterns:\n"
        analysis += "• Use similar sentence length variation and rhythm\n"
        analysis += "• Employ similar metaphorical and imagery techniques\n"
        analysis += "• Keep dialogue patterns consistent with established character voices\n"
        analysis += "• Maintain the same level of sensory detail and atmospheric description\n"
        analysis += "• Use similar paragraph structure and pacing\n"
        analysis += "• Preserve the established balance between action, dialogue, and description\n"
        
        return analysis
