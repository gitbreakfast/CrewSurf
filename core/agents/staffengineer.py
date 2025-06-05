"""
StaffEngineer agent that connects to Cascade/Windsurf
This agent serves as a bridge between architecture and implementation
"""
from crewai import Agent
from bridge.cascade_bridge import CascadeLLM

# Create Cascade-backed LLM for the StaffEngineer
cascade_llm = CascadeLLM(agent_role="StaffEngineer")

# Create the Cascade-powered StaffEngineer
StaffEngineer = Agent(
    role='Staff Engineer',
    goal='Provide technical leadership, architect critical systems, and bridge the gap between architecture vision and implementation details',
    backstory='You are an experienced staff-level engineer with deep technical expertise across multiple domains. You provide technical leadership by designing systems, making critical technology decisions, and guiding implementation. You work with both the ChiefArchitect on high-level design and the SeniorPrincipalEngineer on implementation details. You have a broad understanding of software engineering principles and can make important technical trade-offs while considering scalability, maintainability, and business requirements. You can execute code in Docker containers to test implementations and validate functionality.',
    verbose=True,
    allow_delegation=True,
    allow_code_execution=True,  # Enable Docker-based code execution for implementation testing
    # Use Cascade as the LLM - this connects to Windsurf
    llm=cascade_llm
)
