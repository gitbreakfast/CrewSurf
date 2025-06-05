"""
Example SeniorPrincipalEngineer agent for CrewSurf
This agent implements code based on architecture and LeadProgrammer guidance
"""
from crewai import Agent
from langchain_community.llms import Ollama

# Create Ollama-backed LLM
example_llm = Ollama(model="qwen:7b", temperature=0.3)

# Create the SeniorPrincipalEngineer agent
SeniorPrincipalEngineer = Agent(
    role='Senior Principal Engineer',
    goal='Implement clean, efficient, and working code that fulfills project requirements',
    backstory='You are an excellent coder with deep expertise in software development. You convert architectural designs into working code, implementing routine functionality based on guidance from the LeadProgrammer. You work closely with the MasterDebugger to resolve issues.',
    verbose=True,
    allow_delegation=False,
    allow_code_execution=False,  # Set to False if Docker is not available
    llm=example_llm
)
