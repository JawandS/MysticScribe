from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.llm import LLM
from typing import List
import os
from .tools import KnowledgeLookupTool, ChapterAnalysisTool, OutlineManagementTool, PreviousChapterReaderTool, PreviousChapterEndingTool, StyleGuideTool, StyleAnalysisTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Mysticscribe():
    """Mysticscribe crew - A three-agent system for chapter writing"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def architect(self) -> Agent:
        return Agent(
            config=self.agents_config['architect'], # type: ignore[index]
            # llm=LLM(
                # model="o3", 
                # drop_params=True,           # tell LiteLLM to strip anything not explicitly allowed
                # additional_drop_params=["stop", "temperature", "top_p"]
            # ),
            llm=LLM(model="gpt-4.1"),
            tools=[
                KnowledgeLookupTool(), 
                ChapterAnalysisTool(), 
                PreviousChapterReaderTool(),
                PreviousChapterEndingTool(),
                OutlineManagementTool()
            ],
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'], # type: ignore[index]
            llm=LLM(model="gpt-4o", temperature=0.8),  # High creativity for vivid scene writing
            tools=[
                KnowledgeLookupTool(), 
                PreviousChapterReaderTool(),
                PreviousChapterEndingTool()
            ],
            verbose=True
        )

    @agent  
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'], # type: ignore[index]
            llm=LLM(model="gpt-4.1"),  # Higher creativity for natural style variation
            tools=[
                PreviousChapterReaderTool(),  # For comprehensive previous chapter content and continuity checking
                PreviousChapterEndingTool(),  # For checking how previous chapter ended
                StyleAnalysisTool(),  # For detailed style pattern analysis from previous chapters
                StyleGuideTool(),  # For general style guidelines
                KnowledgeLookupTool()  # For world-building and tone consistency
            ],
            verbose=True
        )



    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def outline_task(self) -> Task:
        return Task(
            config=self.tasks_config['outline_task'], # type: ignore[index]
            agent=self.architect()  # Explicitly assign agent to task
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'], # type: ignore[index]
            context=[self.outline_task()],  # Use output from outline_task
            agent=self.writer()
        )

    @task
    def editing_task(self) -> Task:
        return Task(
            config=self.tasks_config['editing_task'], # type: ignore[index]
            context=[self.writing_task()],  # Use output from writing_task  
            agent=self.editor()
        )



    @crew
    def crew(self) -> Crew:
        """Creates the Mysticscribe crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

    def load_knowledge_context(self) -> str:
        """Load all knowledge files to provide context to agents"""
        knowledge_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'knowledge')
        context = "=== STORY KNOWLEDGE BASE ===\n\n"
        
        knowledge_files = [
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
        
        for filename in knowledge_files:
            file_path = os.path.join(knowledge_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    context += f"=== {filename.upper().replace('.TXT', '')} ===\n"
                    context += f.read()
                    context += "\n\n"
        
        return context
