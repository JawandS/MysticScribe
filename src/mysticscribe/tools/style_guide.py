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
• Prioritize character thoughts and reactions over scenic exposition

INNER MONOLOGUE INTEGRATION:
• Include main character's thoughts regularly (every few paragraphs)
• Keep thoughts brief and natural-sounding
• Use thoughts to show character motivation, concerns, and reactions
• Balance inner voice with external action and dialogue
• Let thoughts reveal character personality and growth

SENTENCE STRUCTURE:
• Vary length organically - mix short, punchy sentences with flowing, complex ones
• Avoid repetitive patterns (don't start multiple sentences the same way)
• Use active voice for action scenes, passive voice sparingly for atmosphere
• Break up long paragraphs naturally based on thought shifts or scene changes
• Add delimiters (/* /* /*) between major sections for clarity

SCENIC WRITING BALANCE:
• Limit pure description to 2-3 sentences before adding character reaction
• Filter all descriptions through the main character's perspective
• Cut scenic details that don't serve character development or plot
• Use the "so what?" test - if a description doesn't matter to the character, cut it

HUMAN WRITING PATTERNS:
• Include minor imperfections and natural rhythms
• Vary paragraph lengths based on content and pacing needs
• Use contractions in dialogue for natural speech
• Include small details and observations that feel organically human
• Prioritize character engagement over elaborate scene-setting
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
• Drop "said" when context is clear or if it's being overused
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
• Use strong, specific verbs rather than weak verbs with adverbs
            """,
            
            "description": """
=== DESCRIPTIVE WRITING GUIDELINES ===

AVOIDING SCENIC OVERLOAD:
• Limit pure description to 2-3 sentences before adding action or dialogue
• Focus on details that serve the story or reveal character
• Cut descriptions that don't advance plot or develop character
• Use the "rule of three" - pick 3 key details maximum per scene
• Weave description into action rather than stopping for description blocks

WORLD-BUILDING INTEGRATION:
• Weave world details naturally into the narrative
• Avoid info-dumping - reveal world details through character interaction
• Use all five senses to create immersive scenes
• Filter descriptions through the main character's perspective and concerns

ATMOSPHERIC DETAILS:
• Choose details that enhance mood and tone
• Use specific, concrete images rather than vague descriptions
• Balance description with action and dialogue
• Make descriptions focus: "The windy valley" vs. "The valley was windy"

SHOW DON'T TELL:
• Reveal character emotions through actions and physical reactions
• Let readers infer meaning rather than explicitly stating everything
• Use metaphors and comparisons that fit the fantasy world
• Trust readers to understand subtle implications

PACING CONSIDERATIONS:
• Vary descriptive density based on scene importance
• Use shorter, punchier descriptions during action sequences
• Allow for fuller descriptions during quieter character moments
• When in doubt, cut description in favor of character thoughts/dialogue
            """,
            
            "emotion": """
=== EMOTIONAL WRITING GUIDELINES ===

AUTHENTIC EMOTION:
• Show emotions through physical reactions and behavior
• Avoid stating emotions directly ("he was angry" vs. "his jaw clenched")
• Use internal monologue sparingly and naturally
• Make emotional reactions fit the character's personality

INNER MONOLOGUE BEST PRACTICES:
• Keep internal thoughts concise and purposeful (1-2 sentences max usually)
• Use italics sparingly - often regular text works better
• Make thoughts feel natural, not forced or exposition-heavy
• Balance internal thoughts with external action and dialogue
• Use inner monologue to reveal character motivation and conflict
• Let thoughts interrupt action naturally: "He raised his sword. This has to work. The blade gleamed..."

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
