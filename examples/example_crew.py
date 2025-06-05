"""
Example CrewSurf team setup with sophisticated agent structure
This showcases the hierarchical workflow and delegation patterns
"""
from crewai import Crew, Task, Process
from langchain_community.tools import DuckDuckGoSearchRun

# Import example agents
from agents.example_chief_architect import ChiefArchitect
from agents.example_lead_programmer import LeadProgrammer
from agents.example_senior_engineer import SeniorPrincipalEngineer

# Create a search tool for web research
web_search_tool = DuckDuckGoSearchRun()

# Define tasks for our agent team with clear goals and expectations
task_architecture_planning = Task(
    description="Create a technical architecture plan based on customer requirements. Research relevant technologies and design patterns. Produce a clear plan for implementation.",
    expected_output="Comprehensive architecture document with technology choices and implementation strategy",
    agent=ChiefArchitect,
    tools=[web_search_tool]
)

task_lead_programming = Task(
    description="Oversee code implementation, write critical components, and delegate routine tasks to the SeniorPrincipalEngineer. Ensure code quality and adherence to architecture.",
    expected_output="High-quality code implementation and technical leadership report", 
    agent=LeadProgrammer
)

task_code_implementation = Task(
    description="Using the architecture plan and direction from the LeadProgrammer, implement the code needed to fulfill requirements. Focus on clean, efficient, and working code.",
    expected_output="Functional code implementation that satisfies the project requirements",
    agent=SeniorPrincipalEngineer
)

# Create a crew with hierarchical delegation
crew = Crew(
    agents=[ChiefArchitect, LeadProgrammer, SeniorPrincipalEngineer],
    tasks=[
        task_architecture_planning, 
        task_lead_programming,
        task_code_implementation
    ],
    verbose=True,
    process=Process.hierarchical,  # Enable hierarchical workflow
    memory=True,                   # Enable memory to maintain context
    cache=True                     # Cache results for better performance
)

def run_interactive_crew(memory_store=None):
    """Run the crew with interactive customer feedback and memory access
    
    Args:
        memory_store: The vector store containing indexed codebase (optional)
    """
    global crew
    
    # Each task delegated through the hierarchy
    result = crew.kickoff()
    
    print("\n🏄 CrewSurf Result:")
    print(result)
    return result

if __name__ == "__main__":
    print("Running CrewSurf Example")
    run_interactive_crew()
