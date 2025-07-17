# MysticScribe - AI-Powered Chapter Writing System

MysticScribe is a CrewAI-based system that uses three specialized AI agents to create publication-ready chapters for your story. The system reads from a comprehensive knowledge base and follows a structured workflow to produce high-quality narrative content.

## System Overview

### Three-Agent Workflow

1. **Architect Agent** - Analyzes story context, previous chapters, and creates detailed chapter outlines
2. **Writer Agent** - Transforms outlines into engaging prose 
3. **Editor Agent** - Refines and polishes chapters to publication quality (2000-4000 words)

### Knowledge Base

The system uses a comprehensive knowledge base stored in the `knowledge/` directory:

- `chapters.txt` - Chapter structure and progression
- `core_story_elements.txt` - Main story elements
- `cultivation_system.txt` - Power/magic system details
- `plot.txt` - Overall plot structure and arcs
- `regions.txt` - World geography and locations
- `society.txt` - Social structures and cultures
- `government.txt` - Political systems
- `economic.txt` - Economic systems
- `military.txt` - Military structures
- `knowledge_system_overview.txt` - Overview of all systems

### Continuity Features

- The Architect Agent automatically reads previously written chapters to maintain continuity
- Character development, plot threads, and world-building elements are carried forward
- Each new chapter builds meaningfully on what came before

## Installation

1. Ensure you have Python 3.10+ installed
2. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

### Generate a Chapter

```bash
# Generate chapter 1 (default)
python -m mysticscribe.main run

# Generate a specific chapter
python -m mysticscribe.main run 3
```

### Training the System

```bash
# Train with 5 iterations, save to training_data.pkl
python -m mysticscribe.main train 5 training_data.pkl

# Train for a specific chapter
python -m mysticscribe.main train 5 training_data.pkl 2
```

### Testing the System

```bash
# Test with 3 iterations using gpt-4
python -m mysticscribe.main test 3 gpt-4

# Test for a specific chapter
python -m mysticscribe.main test 3 gpt-4 5
```

### Replay Previous Execution

```bash
python -m mysticscribe.main replay <task_id>
```

## Output

Generated chapters are saved as `chapter_X.md` files in the project root directory.

## Workflow Details

### 1. Outliner Agent
- Reads all knowledge base files
- Focuses on the requested chapter number
- Creates detailed scene-by-scene breakdown
- Estimates word counts per section
- Ensures story continuity and progression

### 2. Writer Agent  
- Takes the outline and transforms it into narrative prose
- Focuses on character development and world-building
- Creates engaging dialogue and descriptions
- Maintains consistent voice and style

### 3. Editor Agent
- Reviews the draft chapter
- Ensures 2000-4000 word target length
- Improves prose quality and flow
- Fixes inconsistencies and enhances pacing
- Produces publication-ready content

## Configuration

### Agents
Agent configurations are in `src/mysticscribe/config/agents.yaml`:
- Roles, goals, and backstories for each agent
- Specialized for narrative fiction writing

### Tasks  
Task configurations are in `src/mysticscribe/config/tasks.yaml`:
- Detailed descriptions of what each agent should accomplish
- Expected outputs and quality standards

## Project Structure

```
mysticscribe/
├── src/mysticscribe/
│   ├── main.py              # Entry point and CLI
│   ├── crew.py              # CrewAI setup and coordination
│   ├── config/
│   │   ├── agents.yaml      # Agent definitions
│   │   └── tasks.yaml       # Task definitions
│   └── tools/
│       └── custom_tool.py   # Knowledge lookup tools
├── knowledge/               # Story knowledge base
├── tests/                   # Test files
├── pyproject.toml          # Project dependencies
└── README.md               # This file
```

## Extending the System

### Adding New Knowledge
1. Add new `.txt` files to the `knowledge/` directory
2. Update the `load_knowledge_context()` method in `crew.py` to include new files

### Customizing Agents
1. Modify agent configurations in `config/agents.yaml`
2. Adjust roles, goals, and backstories as needed

### Adding Tools
1. Create new tools in `tools/custom_tool.py`
2. Add tools to agents in `crew.py`

## Tips for Best Results

1. **Chapter Numbers**: Use sequential chapter numbers that match your story structure
2. **Knowledge Base**: Keep knowledge files updated with current story details
3. **Iteration**: Use the training feature to improve output quality over time
4. **Review**: Always review generated content for consistency with your overall story

## Troubleshooting

- Ensure all knowledge files are present and readable
- Check that chapter numbers exist in your `chapters.txt` file
- Verify CrewAI installation if you encounter import errors
- Review generated outlines before proceeding to writing phase Crew

Welcome to the Mysticscribe Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/mysticscribe/config/agents.yaml` to define your agents
- Modify `src/mysticscribe/config/tasks.yaml` to define your tasks
- Modify `src/mysticscribe/crew.py` to add your own logic, tools and specific args
- Modify `src/mysticscribe/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the MysticScribe Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The MysticScribe Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the Mysticscribe Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
