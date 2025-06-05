"""
Example ChiefArchitect agent for CrewSurf
This agent handles architecture planning and technology decisions
"""
from crewai import Agent
from langchain_community.tools import DuckDuckGoSearchRun

# Create search tool for research
search_tool = DuckDuckGoSearchRun()

# Create the ChiefArchitect agent
ChiefArchitect = Agent(
    role='Software Architect',
    goal='Design elegant software architecture and plan implementation sprints',
    backstory='You are a visionary software architect with expertise in design patterns and system architecture. You create technical plans that balance innovation with practicality.',
    verbose=True,
    allow_delegation=True,
    # Enable web search for research
    tools=[search_tool]
)
