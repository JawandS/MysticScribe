# MysticScribe - AI-Powered Chapter Writing System

MysticScribe is a simplified AI-powered system that automates the process of writing story chapters. Built on the CrewAI framework, it uses a team of specialized AI agents to create publication-ready chapters from a knowledge base of world-building and plot elements.

## 🚀 Quick Start

```bash
# 1. Activate virtual environment (REQUIRED)
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate a chapter
./mysticscribe.py [chapter_number]

# 4. Run tests (optional)
./run_tests.py
```

The system will automatically detect the next chapter number if one isn't provided, based on existing chapters in the `chapters/` directory.

## 📋 System Overview

MysticScribe employs a three-agent workflow to create high-quality narrative content:

1. **Architect Agent** - Creates detailed chapter outlines based on knowledge context and previous chapters
2. **Writer Agent** - Transforms approved outlines into engaging prose (2000-4000 words)  
3. **Editor Agent** - Polishes the draft to publication quality with consistent style and flow

### Single Unified Workflow

The system runs a single, unified workflow that executes all three agents sequentially:
- Loads story knowledge and previous chapter context
- Creates/uses chapter outlines automatically
- Writes the complete chapter
- Edits and polishes the final content
- Validates word count and content quality

## 🗂️ Project Structure

```
MysticScribe/
├── mysticscribe.py              # 🌟 Main entry point script
├── run_tests.py                 # Test runner script  
├── pyproject.toml               # Project dependencies and configuration
├── README.md                    # Documentation (this file)
├── chapters/                    # Generated chapter output files
│   ├── chapter_1.md
│   └── chapter_2.md
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
├── outlines/                    # Stored chapter outlines (optional)
│   ├── chapter_1.txt
│   └── chapter_2.txt
├── src/mysticscribe/           # Main source code
│   ├── __init__.py             # Package initialization
│   ├── __main__.py             # Module entry point
│   ├── crew.py                 # CrewAI agent definitions
│   ├── core/                   # Core functionality modules
│   │   ├── __init__.py
│   │   ├── chapter_manager.py  # Chapter file management
│   │   ├── knowledge_manager.py # Knowledge base management
│   │   └── validation.py       # Content validation
│   ├── tools/                  # AI agent tools
│   │   ├── __init__.py
│   │   ├── custom_tool.py      # Knowledge and chapter tools
│   │   ├── previous_chapter_reader.py # Chapter continuity
│   │   ├── style_analysis.py   # Style analysis tools
│   │   └── style_guide.py      # Style consistency
│   ├── utils/                  # Utility modules
│   │   ├── __init__.py
│   │   ├── logging_config.py   # Logging configuration
│   │   ├── file_utils.py       # File operation utilities
│   │   └── text_utils.py       # Text processing utilities
│   └── config/                 # Configuration files
│       ├── agents.yaml         # Agent configurations
│       └── tasks.yaml          # Task configurations
├── styles/                     # Writing style guides
│   ├── casual.txt
│   ├── formal.txt
│   └── traditional.txt
└── tests/                      # Test suite
    ├── conftest.py
    ├── test_mysticscribe.py     # Main functionality tests
    └── [other test files]
```

## 💡 Usage

### Simple Usage

```bash
# Generate the next chapter automatically
./mysticscribe.py

# Generate a specific chapter 
./mysticscribe.py 5

# Get help
./mysticscribe.py --help
```

### Module Interface (Alternative)

```bash
# Run via Python module
python -m mysticscribe
```

### Python API

```python
from mysticscribe.crew import Mysticscribe

# Initialize the crew
crew = Mysticscribe()

# Prepare inputs
inputs = {
    'chapter_number': '1',
    'current_year': '2024',
    'knowledge_context': crew.load_knowledge_context(),
    'previous_chapter_context': 'This is Chapter 1...'
}

# Generate chapter
result = crew.crew().kickoff(inputs=inputs)
```

## 🧩 Architecture Overview

### Core Components

- **`crew.py`** - Main CrewAI agent definitions (Architect, Writer, Editor)
- **`core/chapter_manager.py`** - Chapter numbering, file operations, and metadata
- **`core/knowledge_manager.py`** - Knowledge base management and access
- **`core/validation.py`** - Content quality validation and reporting

### Agent Tools

- **Knowledge Tools** - Access story knowledge base and previous chapters
- **Chapter Analysis** - Analyze existing chapters for continuity
- **Style Tools** - Maintain consistent writing style across chapters
- **Outline Management** - Create and manage chapter outlines

## 🔄 Workflow Process

1. **Context Loading** - Load knowledge base and previous chapter context
2. **Outline Creation** - Architect agent creates detailed chapter outline
3. **Chapter Writing** - Writer agent transforms outline into engaging prose
4. **Content Editing** - Editor agent polishes for quality and consistency
5. **Validation** - Automated quality checks and content validation
6. **Output** - Final chapter saved as Markdown file

## ✅ Content Validation

The system includes comprehensive validation:

- **Word Count** - Ensures chapters meet target length (2000-4000 words)
- **AI Pattern Detection** - Identifies common AI-generated text patterns
- **Quality Metrics** - Analyzes readability and content quality

## 🧪 Testing

```bash
# Run all tests
./run_tests.py

# Or with specific test runner
python -m pytest tests/
python tests/test_mysticscribe.py
```

## 🔧 Setup & Prerequisites

### Prerequisites

- Python 3.10+ (< 3.14)
- Virtual environment (recommended)

### Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Required before running

# Install dependencies
pip install -r requirements.txt

# Verify installation
./mysticscribe.py --help
```

### Knowledge Base Setup

Populate the `knowledge/` directory with your story elements:

1. **Required Files:**
   - `core_story_elements.txt` - Main characters, themes, tone
   - `plot.txt` - Story structure and major plot points

2. **Optional World-Building Files:**
   - `cultivation_system.txt` - Magic/power systems
   - `regions.txt` - Geographic locations
   - `society.txt` - Social structures and cultures
   - Additional system files as needed

## 💡 Tips

- Always run `source .venv/bin/activate` before using MysticScribe
- Start with simple knowledge files and expand as needed
- Review and edit generated chapters for your specific style
- The system works best with consistent chapter numbering

---

*For advanced usage and development details, see the source code documentation.*