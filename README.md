# MysticScribe - AI-Powered Chapter Writing System

MysticScribe is a sophisticated AI-powered system that automates the process of writing story chapters. Built on the CrewAI framework, it uses a team of specialized AI agents to create publication-ready chapters from a knowledge base of world-building and plot elements.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -e .

# Generate a chapter (interactive workflow)
python mysticscribe.py [chapter_number]
```

The system will automatically detect the next chapter number if one isn't provided, based on existing outlines in the `outlines/` directory.

## 📋 System Overview

MysticScribe employs a three-agent workflow to create high-quality narrative content:

1. **Architect Agent** - Creates detailed chapter outlines based on knowledge context and previous chapters
2. **Writer Agent** - Transforms approved outlines into engaging prose (2000-4000 words)
3. **Editor Agent** - Polishes the draft to publication quality with consistent style and flow

The system guides you through an interactive workflow with approval gates:
- Review and approve outlines before writing begins
- Make edits to outlines before final chapter generation
- Final chapters are saved as Markdown files in the `chapters/` directory

## 🗂️ Project Structure

```
MysticScribe/
├── mysticscribe.py              # Entry point script with simplified interface
├── pyproject.toml               # Project dependencies and configuration
├── README.md                    # Documentation (this file)
├── chapters/                    # Generated chapter output files
│   └── chapter_1.md             # Example generated chapter
├── knowledge/                   # Knowledge base for story elements
│   ├── chapters.txt             # Chapter structure and progression
│   ├── core_story_elements.txt  # Main story elements
│   ├── cultivation_system.txt   # Power/magic system details
│   ├── economic.txt             # Economic systems
│   ├── government.txt           # Political systems
│   ├── knowledge_system_overview.txt  # Overview of all systems
│   ├── military.txt             # Military structures
│   ├── plot.txt                 # Overall plot structure and arcs
│   ├── regions.txt              # World geography and locations
│   └── society.txt              # Social structures and cultures
├── outlines/                    # Stored chapter outlines
│   └── chapter_1.txt            # Example chapter outline
├── src/                         # Source code
│   └── mysticscribe/            # Main package
│       ├── __init__.py          # Package initialization
│       ├── crew.py              # CrewAI setup and agent coordination
│       ├── main.py              # Main application logic and CLI
│       ├── config/              # Configuration files
│       │   ├── agents.yaml      # Agent definitions
│       │   └── tasks.yaml       # Task definitions
│       └── tools/               # Custom tools for agents
│           ├── __init__.py      # Package initialization
│           ├── custom_tool.py   # Knowledge lookup tools
│           └── previous_chapter_reader.py  # Tool for reading previous chapters
└── tests/                       # Test files
    ├── setup_check.py           # Environment setup tests
    ├── test_architect_workflow.py  # Tests for architect workflow
    └── test_crew.py             # Tests for crew functionality
```

## 📚 Detailed Component Walkthrough

### 1. Runner Script (`mysticscribe.py`)

The runner script provides a simplified interface to the main application. It:
- Locates the main application script
- Automatically determines the next chapter number based on existing outlines
- Forwards commands to the main script with the workflow mode
- Provides user-friendly error handling

### 2. Crew Setup (`src/mysticscribe/crew.py`)

The crew file defines the agent structure and workflow:
- Agent definitions with specific roles and tools
- Task configurations for each step in the workflow
- Knowledge context loading from the knowledge base
- Agent-task relationships and execution flow

### 3. Main Application (`src/mysticscribe/main.py`)

The main script implements the workflow logic:
- Chapter number handling and sequence management
- Interactive workflow with user approval gates
- Outline creation, review, and approval process
- Chapter generation with writer and editor agents
- Output file management and saving

### 4. Agent Configuration (`src/mysticscribe/config/agents.yaml`)

Agent configurations define each agent's:
- Role and objective
- Specialized skills and knowledge
- Response format and style
- Decision-making parameters

### 5. Task Configuration (`src/mysticscribe/config/tasks.yaml`)

Task configurations define:
- Specific objectives for each agent
- Input and output specifications
- Dependencies between tasks
- Expected deliverables

### 6. Custom Tools (`src/mysticscribe/tools/`)

Custom tools provide specialized capabilities:
- `KnowledgeLookupTool`: Retrieves information from the knowledge base
- `ChapterAnalysisTool`: Analyzes chapter structure and content
- `OutlineManagementTool`: Manages outline creation and storage
- `PreviousChapterReaderTool`: Reads previous chapters for continuity

## 🔄 Interactive Workflow Process

### Phase 1: Architect (Outline Creation)

1. **Context Loading**
   - System loads all knowledge base files
   - Retrieves information about previous chapters
   - Checks for existing drafts or outlines

2. **Outline Creation/Expansion**
   - If an outline exists, you can choose to:
     - Expand the existing outline
     - Create a new outline
     - Use the existing outline as-is
   - Architect agent creates or expands the outline

3. **Human Review and Approval**
   - Outline is saved to `outlines/chapter_X.txt`
   - You can review and edit the outline
   - You must explicitly approve the outline to continue

### Phase 2: Writer & Editor (Chapter Generation)

4. **Chapter Writing**
   - Writer agent transforms the approved outline into prose
   - Creates engaging narrative based on outline structure
   - Maintains consistency with world-building elements

5. **Chapter Editing**
   - Editor agent refines the draft for quality
   - Ensures proper pacing, flow, and word count
   - Produces publication-ready content

6. **Output Generation**
   - Final chapter is saved to `chapters/chapter_X.md`
   - System provides links to both outline and chapter files

## 📝 Extending the Knowledge Base

The system reads from text files in the `knowledge/` directory. To expand the knowledge base:

1. Create new `.txt` files in the `knowledge/` directory
2. Add the filenames to the `knowledge_files` list in `src/mysticscribe/crew.py`
3. Organize information in a clear, structured format

Example knowledge file format:
```
=== SECTION TITLE ===
Key information about this aspect of the story.

=== ANOTHER SECTION ===
More details relevant to the story world.
```

## 🔧 Troubleshooting

Common issues and solutions:

1. **Missing Dependencies**
   - Ensure you've installed all required packages with `pip install -e .`
   - Check that CrewAI is properly installed

2. **Chapter Generation Issues**
   - Verify that all knowledge files exist and are properly formatted
   - Check for errors in the outline or approval process
   - Ensure chapter numbers are consistent with your knowledge base

3. **Output Quality Issues**
   - Review and refine your knowledge base files
   - Provide more detailed outlines during the approval process
   - Adjust agent configurations in `config/agents.yaml` for different writing styles

## 🌟 Best Practices

For optimal results with MysticScribe:

1. **Knowledge Base Maintenance**
   - Keep knowledge files updated with current story details
   - Organize information clearly with headings and sections
   - Ensure consistency between knowledge files

2. **Outline Development**
   - Take time to review and edit outlines before approval
   - Add specific details about scenes, character motivations, and key events
   - Include notes about tone, pacing, and important revelations

3. **Chapter Sequence**
   - Generate chapters in sequence for best continuity
   - Reference previous chapters explicitly in your knowledge base
   - Update plot and character information as the story progresses