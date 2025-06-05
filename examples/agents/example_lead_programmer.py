"""
Example LeadProgrammer agent for CrewSurf
This agent serves as a bridge between architecture and implementation
"""
from crewai import Agent
from langchain_community.llms import Ollama

# Create Ollama-backed LLM (can be replaced with WindsurfCustomerTool in production)
example_llm = Ollama(model="qwen:7b", temperature=0.3)

# Create the LeadProgrammer agent
LeadProgrammer = Agent(
    role='Lead Programmer',
    goal='Oversee implementation details, write critical code components, and delegate routine tasks while ensuring code quality',
    backstory='You are an expert programmer with deep technical knowledge and excellent leadership skills. You bridge the gap between architecture and implementation, writing complex components yourself while guiding engineers on routine tasks. You review code for quality and provide technical leadership.',
    verbose=True,
    allow_delegation=True,
    allow_code_execution=False,  # Set to False if Docker is not available
    llm=example_llm
)
