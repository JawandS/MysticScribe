from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class StyleGuideInput(BaseModel):
    """Input schema for StyleGuideTool."""
    focus_area: str = Field(
        default="general", 
        description="The specific style area to focus on: 'general', 'dialogue', 'action', 'description', 'emotion', or 'worldbuilding'"
    )

class StyleGuideTool(BaseTool):
    name: str = "Style Guide"
    description: str = (
        "Get specific style guidelines for fantasy/xianxia literature to ensure consistent, professional prose quality. Use this to understand genre conventions and human writing patterns."
    )
    args_schema: Type[BaseModel] = StyleGuideInput

    def _run(self, focus_area: str = "general") -> str:
        """Return style guidelines based on the focus area."""
        
        guidelines = {
            "general": """
=== GENERAL FANTASY/XIANXIA STYLE GUIDELINES ===

OVERALL TONE:
• Balance epic scope with intimate character moments
• Use language that feels both timeless and accessible
• Maintain immersive atmosphere without overwrought purple prose
• Create natural flow between action, dialogue, and description

SENTENCE STRUCTURE:
• Vary length organically - mix short, punchy sentences with flowing, complex ones
• Avoid repetitive patterns (don't start multiple sentences the same way)
• Use active voice for action scenes, passive voice sparingly for atmosphere
• Break up long paragraphs naturally based on thought shifts or scene changes

HUMAN WRITING PATTERNS:
• Include minor imperfections and natural rhythms
• Vary paragraph lengths based on content and pacing needs
• Use contractions in dialogue for natural speech
• Include small details and observations that feel organically human
            """,
            
            "dialogue": """
=== DIALOGUE STYLE GUIDELINES ===

NATURAL SPEECH PATTERNS:
• Characters should have distinct voices based on personality and background
• Include interruptions, hesitations, and realistic speech rhythms
• Use contractions and informal language where appropriate
• Avoid overly formal or exposition-heavy dialogue

DIALOGUE TAGS:
• Use "said" most often - it's invisible to readers
• Vary occasionally with "asked," "whispered," "called," but sparingly
• Include action beats instead of dialogue tags when possible
• Avoid adverbs with dialogue tags (don't write "she said angrily")

CHARACTER VOICE:
• Each character should speak differently based on their background
• Consider education level, cultural background, personality
• Maintain consistency in how each character speaks
• Use dialect/accent subtly if at all - don't overdo it
            """,
            
            "action": """
=== ACTION SCENE STYLE GUIDELINES ===

PACING AND FLOW:
• Use shorter sentences during intense moments
• Vary sentence length to control rhythm and tension
• Focus on visceral, immediate details rather than clinical descriptions
• Move between character actions and internal reactions naturally

SENSORY DETAILS:
• Include sounds, smells, physical sensations
• Make readers feel the weight of weapons, the heat of fire, the impact of blows
• Use specific details rather than generic descriptions
• Balance action with character emotion and thought

CLARITY:
• Keep action sequences clear and easy to follow
• Avoid overly complex choreography that confuses readers
• Focus on the most important moments and impacts
• Use strong, specific verbs rather than weak verbs with adverbs
            """,
            
            "description": """
=== DESCRIPTIVE WRITING GUIDELINES ===

WORLD-BUILDING INTEGRATION:
• Weave world details naturally into the narrative
• Avoid info-dumping - reveal world details through character interaction
• Use all five senses to create immersive scenes
• Make descriptions serve character development or plot advancement

ATMOSPHERIC DETAILS:
• Choose details that enhance mood and tone
• Use specific, concrete images rather than vague descriptions
• Include small details that make scenes feel lived-in and real
• Balance description with action and dialogue

SHOW DON'T TELL:
• Reveal character emotions through actions and physical reactions
• Let readers infer meaning rather than explicitly stating everything
• Use metaphors and comparisons that fit the fantasy world
• Trust readers to understand subtle implications
            """,
            
            "emotion": """
=== EMOTIONAL WRITING GUIDELINES ===

AUTHENTIC EMOTION:
• Show emotions through physical reactions and behavior
• Avoid stating emotions directly ("he was angry" vs. "his jaw clenched")
• Use internal monologue sparingly and naturally
• Make emotional reactions fit the character's personality

SUBTLETY:
• Not every emotion needs to be dramatic or intense
• Include quiet moments and subtle emotional shifts
• Let emotions build naturally rather than jumping to extremes
• Use understatement for powerful effect

CHARACTER DEVELOPMENT:
• Emotions should reflect character growth and change
• Consider how past events affect current emotional reactions
• Make emotional responses consistent with character history
• Allow characters to be complex and sometimes contradictory
            """,
            
            "worldbuilding": """
=== WORLD-BUILDING STYLE GUIDELINES ===

NATURAL INTEGRATION:
• Introduce world elements through character experience
• Avoid exposition dumps - reveal world details gradually
• Use familiar concepts as bridges to unfamiliar ones
• Make world-building serve the story, not dominate it

CONSISTENCY:
• Maintain established rules and world logic
• Keep terminology and naming conventions consistent
• Reference previously established world elements
• Ensure new details don't contradict existing world-building

IMMERSION:
• Use world-specific details in casual, natural ways
• Include mundane world details alongside fantastic elements
• Make magical/cultivation systems feel lived-in rather than academic
• Let characters take their world for granted - don't over-explain
            """
        }
        
        if focus_area.lower() in guidelines:
            return guidelines[focus_area.lower()]
        else:
            # Return general guidelines if focus area not found
            available_areas = ", ".join(guidelines.keys())
            return f"Available focus areas: {available_areas}\n\n{guidelines['general']}"
