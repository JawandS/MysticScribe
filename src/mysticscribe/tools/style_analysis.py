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
        """Analyze writing style patterns from the chapters with deep integration focus."""
        
        analysis = f"Analyzing {len(chapters)} previous chapters for deep style integration...\n\n"
        
        # Combine all chapter content for analysis
        all_text = ""
        for chapter_num, content in chapters:
            all_text += content + "\n\n"
        
        total_words = len(all_text.split())
        analysis += f"Total content analyzed: {total_words:,} words across {len(chapters)} chapters\n\n"
        
        # Analyze sentence patterns with more detail
        sentences = re.split(r'[.!?]+', all_text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        
        if sentences:
            short_sentences = [s for s in sentences if len(s.split()) <= 8]
            medium_sentences = [s for s in sentences if 9 <= len(s.split()) <= 20]
            long_sentences = [s for s in sentences if len(s.split()) > 20]
            
            analysis += "=== SENTENCE STRUCTURE PATTERNS (MUST MAINTAIN) ===\n"
            analysis += f"• Short sentences (≤8 words): {len(short_sentences)} ({len(short_sentences)/len(sentences)*100:.1f}%)\n"
            analysis += f"• Medium sentences (9-20 words): {len(medium_sentences)} ({len(medium_sentences)/len(sentences)*100:.1f}%)\n"
            analysis += f"• Long sentences (>20 words): {len(long_sentences)} ({len(long_sentences)/len(sentences)*100:.1f}%)\n"
            
            # Calculate average sentence length
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            analysis += f"• Average sentence length: {avg_sentence_length:.1f} words\n\n"
            
            # Show specific examples to emulate
            if short_sentences:
                analysis += "SHORT SENTENCE STYLE TO EMULATE:\n"
                for example in short_sentences[:3]:
                    analysis += f"  • \"{example.strip()}\"\n"
                analysis += "\n"
            
            if long_sentences:
                analysis += "LONG SENTENCE STYLE TO EMULATE:\n"
                for example in long_sentences[:2]:
                    analysis += f"  • \"{example.strip()}\"\n"
                analysis += "\n"
        
        # Enhanced imagery and metaphor analysis
        analysis += "=== IMAGERY AND METAPHOR PATTERNS (CRITICAL TO MATCH) ===\n"
        metaphor_patterns = []
        
        # Look for common metaphorical constructions with more comprehensive patterns
        metaphor_indicators = [
            r'like a [^,.!?]*',
            r'as [^,.!?]* as',
            r'was a [^,.!?]*(?:of|made|carved|forged)[^,.!?]*',
            r'seemed to [^,.!?]*',
            r'coiled like [^,.!?]*',
            r'carved from [^,.!?]*',
            r'flowed like [^,.!?]*',
            r'moved like [^,.!?]*',
            r'reminded [^,.!?]* of [^,.!?]*'
        ]
        
        all_metaphors = []
        for pattern in metaphor_indicators:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                all_metaphors.extend(matches)
                metaphor_patterns.extend(matches[:1])  # One example per pattern type
        
        metaphor_density = len(all_metaphors) / total_words * 1000 if total_words > 0 else 0
        analysis += f"Metaphor density: {metaphor_density:.1f} metaphors per 1000 words\n"
        
        if metaphor_patterns:
            analysis += "ESTABLISHED METAPHOR STYLES TO REPLICATE:\n"
            for pattern in metaphor_patterns[:5]:
                analysis += f"  • \"{pattern}\"\n"
            analysis += f"→ REQUIREMENT: Include {len(metaphor_patterns)//3 + 1}-{len(metaphor_patterns)//2 + 2} similar metaphors in new content\n\n"
        
        # Enhanced dialogue analysis
        analysis += "=== DIALOGUE STYLE PATTERNS (MAINTAIN CONSISTENCY) ===\n"
        dialogue_lines = re.findall(r'"([^"]*)"', all_text)
        
        if dialogue_lines:
            short_dialogue = [d for d in dialogue_lines if len(d.split()) <= 5]
            medium_dialogue = [d for d in dialogue_lines if 6 <= len(d.split()) <= 15]
            long_dialogue = [d for d in dialogue_lines if len(d.split()) > 15]
            
            avg_dialogue_length = sum(len(d.split()) for d in dialogue_lines) / len(dialogue_lines)
            
            analysis += f"• Total dialogue lines: {len(dialogue_lines)}\n"
            analysis += f"• Average dialogue length: {avg_dialogue_length:.1f} words\n"
            analysis += f"• Short dialogue (≤5 words): {len(short_dialogue)} ({len(short_dialogue)/len(dialogue_lines)*100:.1f}%)\n"
            analysis += f"• Medium dialogue (6-15 words): {len(medium_dialogue)} ({len(medium_dialogue)/len(dialogue_lines)*100:.1f}%)\n"
            analysis += f"• Long dialogue (>15 words): {len(long_dialogue)} ({len(long_dialogue)/len(dialogue_lines)*100:.1f}%)\n"
            
            # Show example dialogue to match tone
            if dialogue_lines:
                analysis += "DIALOGUE TONE EXAMPLES TO MATCH:\n"
                for example in dialogue_lines[:3]:
                    if len(example.split()) >= 4:  # Meaningful examples
                        analysis += f"  • \"{example}\"\n"
                analysis += "\n"
            
            # Look for dialogue tag patterns with more variety
            dialogue_tag_patterns = re.findall(r'"\s*[^"]*"\s*([^.!?]*(?:said|asked|whispered|called|grunted|muttered|crowed|admonished|replied|demanded|urged)[^.!?]*)', all_text, re.IGNORECASE)
            if dialogue_tag_patterns:
                analysis += "ESTABLISHED DIALOGUE TAG STYLES:\n"
                unique_tags = list(set(tag.strip() for tag in dialogue_tag_patterns))[:5]
                for tag in unique_tags:
                    analysis += f"  • {tag}\n"
                analysis += f"→ REQUIREMENT: Use similar variety and style in dialogue tags\n\n"
        
        # Enhanced descriptive techniques analysis
        analysis += "=== DESCRIPTIVE TECHNIQUE PATTERNS (SENSORY BALANCE) ===\n"
        
        # Look for sensory details with expanded patterns
        sensory_patterns = {
            'Visual': [r'gleam', r'glow', r'flicker', r'shimmer', r'shadow', r'light', r'glitter', r'sparkle', r'dark', r'bright', r'pale'],
            'Auditory': [r'whisper', r'echo', r'silence', r'thump', r'shriek', r'vibrated', r'hum', r'buzz', r'crack', r'rustle'],
            'Tactile': [r'cold', r'warm', r'rough', r'smooth', r'sharp', r'soft', r'hard', r'wet', r'dry', r'sticky'],
            'Olfactory': [r'scent', r'smell', r'aroma', r'stench', r'fragrance', r'musty', r'sweet', r'acrid'],
            'Physical': [r'ache', r'pulse', r'tremble', r'shiver', r'burn', r'tingle', r'numb', r'sore', r'tight']
        }
        
        sensory_totals = {}
        sensory_examples = {}
        
        for sense_type, patterns in sensory_patterns.items():
            count = 0
            examples = []
            for pattern in patterns:
                matches = re.findall(rf'[^.!?]*{pattern}[^.!?]*', all_text, re.IGNORECASE)
                count += len(matches)
                if matches:
                    examples.extend(matches[:1])  # One example per pattern
            
            if count > 0:
                density = (count / total_words) * 1000 if total_words > 0 else 0
                sensory_totals[sense_type] = count
                sensory_examples[sense_type] = examples[:2]  # Limit examples
                analysis += f"• {sense_type} details: {count} instances ({density:.1f} per 1000 words)\n"
        
        # Show sensory balance requirements
        if sensory_totals:
            total_sensory = sum(sensory_totals.values())
            analysis += f"\nSENSORY BALANCE TO MAINTAIN:\n"
            for sense_type, count in sensory_totals.items():
                percentage = (count / total_sensory) * 100
                analysis += f"• {sense_type}: {percentage:.1f}% of sensory descriptions\n"
                if sense_type in sensory_examples and sensory_examples[sense_type]:
                    analysis += f"  Example style: \"{sensory_examples[sense_type][0].strip()}\"\n"
        
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
        
        # Analyze opening/closing patterns
        analysis += "=== NARRATIVE TRANSITION PATTERNS ===\n"
        
        # Extract chapter openings and closings
        chapter_openings = []
        chapter_closings = []
        for chapter_num, content in chapters:
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
            if lines:
                # Get first few sentences
                first_sentences = '. '.join(lines[:2])[:200]
                chapter_openings.append(f"Ch{chapter_num}: {first_sentences}")
                
                # Get last few sentences
                last_sentences = '. '.join(lines[-2:])[:200]
                chapter_closings.append(f"Ch{chapter_num}: {last_sentences}")
        
        if chapter_openings:
            analysis += "Chapter opening patterns:\n"
            for opening in chapter_openings[-3:]:  # Show last 3 openings
                analysis += f"  • {opening}...\n"
            analysis += "\n"
        
        if chapter_closings:
            analysis += "Chapter closing patterns:\n"
            for closing in chapter_closings[-3:]:  # Show last 3 closings
                analysis += f"  • {closing}...\n"
            analysis += "\n"
        
        # Analyze pacing and rhythm patterns
        analysis += "=== PACING AND RHYTHM PATTERNS ===\n"
        
        # Look for action sequences vs contemplative passages
        action_indicators = [r'struck', r'leaped', r'rushed', r'charged', r'dodged', r'slammed', r'burst', r'sprinted']
        contemplative_indicators = [r'wondered', r'thought', r'considered', r'realized', r'remembered', r'felt']
        
        action_count = sum(len(re.findall(pattern, all_text, re.IGNORECASE)) for pattern in action_indicators)
        contemplative_count = sum(len(re.findall(pattern, all_text, re.IGNORECASE)) for pattern in contemplative_indicators)
        
        total_words = len(all_text.split())
        if total_words > 0:
            action_density = (action_count / total_words) * 1000
            contemplative_density = (contemplative_count / total_words) * 1000
            
            analysis += f"• Action density: {action_density:.1f} action words per 1000 words\n"
            analysis += f"• Contemplative density: {contemplative_density:.1f} contemplative words per 1000 words\n"
            analysis += f"• Action-to-contemplation ratio: {action_count}:{contemplative_count}\n\n"
        
        # Extract specific stylistic phrases
        analysis += "=== SIGNATURE STYLE PHRASES ===\n"
        
        # Look for repeated stylistic constructions
        style_patterns = [
            r'[A-Z][^.!?]*(?:pulsed|thrummed|hummed|vibrated)[^.!?]*',
            r'[A-Z][^.!?]*(?:coiled|twisted|spiraled|wound)[^.!?]*',
            r'[A-Z][^.!?]*(?:carved|etched|marked|traced)[^.!?]*',
            r'[A-Z][^.!?]*(?:ancient|old|weathered|worn)[^.!?]*'
        ]
        
        signature_phrases = []
        for pattern in style_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                signature_phrases.extend(matches[:2])
        
        if signature_phrases:
            analysis += "Recurring stylistic constructions to maintain:\n"
            for phrase in signature_phrases[:5]:
                analysis += f"  • \"{phrase.strip()}\"\n"
            analysis += "\n"
        
        # Analyze emotional tone patterns
        analysis += "=== EMOTIONAL TONE PATTERNS ===\n"
        
        emotion_words = {
            'tension': [r'tense', r'tight', r'strained', r'coiled', r'rigid'],
            'mystery': [r'shadow', r'hidden', r'secret', r'mystery', r'unknown'],
            'power': [r'energy', r'force', r'power', r'strength', r'might'],
            'elegance': [r'graceful', r'elegant', r'smooth', r'fluid', r'refined']
        }
        
        for emotion, patterns in emotion_words.items():
            count = sum(len(re.findall(pattern, all_text, re.IGNORECASE)) for pattern in patterns)
            if count > 0:
                analysis += f"• {emotion.capitalize()} words: {count} instances\n"
        
        analysis += "\n"
        
        # Extract dialogue voice patterns per character
        analysis += "=== CHARACTER-SPECIFIC DIALOGUE STYLES ===\n"
        
        # More sophisticated dialogue extraction
        dialogue_with_speaker = re.findall(r'([A-Z][a-z]+)[^"]*"([^"]*)"[^.!?]*(?:said|asked|whispered|called|grunted|muttered|replied)', all_text)
        
        if dialogue_with_speaker:
            from collections import defaultdict
            char_dialogue = defaultdict(list)
            for speaker, quote in dialogue_with_speaker:
                if len(quote.split()) >= 3:  # Only meaningful dialogue
                    char_dialogue[speaker].append(quote)
            
            for char, quotes in list(char_dialogue.items())[:3]:  # Top 3 characters
                analysis += f"{char}'s dialogue patterns:\n"
                for quote in quotes[:2]:  # Sample quotes
                    word_count = len(quote.split())
                    analysis += f"  • \"{quote}\" ({word_count} words)\n"
                
                # Analyze this character's speech patterns
                all_char_dialogue = ' '.join(quotes)
                avg_words = sum(len(q.split()) for q in quotes) / len(quotes) if quotes else 0
                analysis += f"  → Average dialogue length: {avg_words:.1f} words\n"
                
                # Look for character-specific speech patterns
                if 'formal' in all_char_dialogue.lower() or 'shall' in all_char_dialogue.lower():
                    analysis += f"  → Formal speech pattern detected\n"
                elif 'gonna' in all_char_dialogue.lower() or 'ain\'t' in all_char_dialogue.lower():
                    analysis += f"  → Informal speech pattern detected\n"
                
                analysis += "\n"
        
        analysis += "=== INTEGRATED STYLE REQUIREMENTS ===\n"
        analysis += "CRITICAL: Maintain these established patterns from previous chapters:\n\n"
        
        # More specific and actionable guidelines
        if sentences:
            short_pct = len(short_sentences)/len(sentences)*100
            medium_pct = len(medium_sentences)/len(sentences)*100
            long_pct = len(long_sentences)/len(sentences)*100
            
            analysis += f"SENTENCE STRUCTURE: Maintain {short_pct:.0f}% short, {medium_pct:.0f}% medium, {long_pct:.0f}% long sentences\n"
        
        if signature_phrases:
            analysis += f"SIGNATURE STYLE: Include similar descriptive constructions (see examples above)\n"
        
        if action_count and contemplative_count:
            analysis += f"PACING BALANCE: Maintain {action_count}:{contemplative_count} action-to-contemplation ratio\n"
        
        if atmosphere_examples:
            analysis += f"ATMOSPHERIC STYLE: Continue using environmental descriptions as mood setters\n"
        
        analysis += f"DIALOGUE CONSISTENCY: Match established character voice patterns (see character analysis)\n"
        
        # Extract and provide specific transition words/phrases that appear frequently
        transition_patterns = re.findall(r'(?:^|\. )([A-Z][^.!?]*(?:then|now|suddenly|meanwhile|however|still|yet)[^.!?]*)', all_text, re.MULTILINE)
        if transition_patterns:
            analysis += f"TRANSITION STYLE: Use similar connecting phrases like: {', '.join(transition_patterns[:3])}\n"
        
        analysis += "\nIMPORTANT: Review the specific examples above and consciously incorporate similar patterns, rhythms, and stylistic choices in the new chapter content."
        
        return analysis
