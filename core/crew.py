from crewai import Crew, Task, Agent, Process
from crewai.tools import tool
import time
import os
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.chains import RetrievalQA

# Use the latest recommended import for Ollama if available
try:
    from langchain_ollama import OllamaLLM as Ollama
except ImportError:
    # Fallback to older import
    from langchain_community.llms import Ollama
from core.config.llm_config import get_ollama_llm, print_model_config
from core.agents.chiefexecutiveofficer import ChiefExecutiveOfficer
from core.agents.director import Director
from core.agents.seniorprincipalengineer import SeniorPrincipalEngineer
from core.agents.softwareengineerintest import SoftwareEngineerInTest
from core.agents.masterdebugger import MasterDebugger
from core.agents.chiefarchitect import ChiefArchitect
from core.agents.headofsoftwarequality import HeadOfSoftwareQuality
from core.agents.technicalwriter import TechnicalWriter
from core.agents.staffengineer import StaffEngineer
from core.agents.seniorprincipalengineer import crewai_llm as senior_engineer_llm
from bridge.cascade_bridge import CascadeLLM

# Get the CascadeLLM instance from the StaffEngineer agent
cascade_llm = StaffEngineer.llm
# Human interaction now handled through WindsurfCustomerTool

# Initialize the search tool for Architect
duck_search = DuckDuckGoSearchRun()

# Create web search tool with the proper CrewAI format
@tool
def web_search(query: str) -> str:
    """Search the web for information on technologies, programming concepts, or other general knowledge."""
    return duck_search.run(query)

# Set the web search tool for reference
web_search_tool = web_search

# We'll add tools later in the run_crewsurfai_pipeline function instead of directly here
# This ensures proper tool assignment compatible with the current CrewAI version

# Define Tasks with clear responsibilities
# Human interaction now handled through WindsurfCustomerTool directly

task_customer_oversight = Task(
    description="Monitor project progress and ensure it meets customer expectations. Report on overall project reputation and customer satisfaction.",
    expected_output="Status report on project reputation and customer satisfaction metrics",
    agent=ChiefExecutiveOfficer
)

task_team_management = Task(
    description="Manage the development team, assign responsibilities, and ensure adherence to customer requirements. Coordinate all activities between team members.",
    expected_output="Team coordination report with task assignments and progress tracking",
    agent=Director
)

task_architecture_planning = Task(
    description="Plan the sprint using agile/kanban methodologies. Define technical architecture, select libraries, and establish development patterns. Research optimal technical solutions.",
    expected_output="Sprint plan, architecture diagrams, and technology stack recommendations",
    agent=ChiefArchitect
    # Tools are now assigned directly to the agent, not to the task
)

task_staff_engineering = Task(
    description="Provide technical leadership, design critical systems, and bridge the gap between architecture vision and implementation. Make key technical decisions and guide the SeniorPrincipalEngineer.",
    expected_output="System design documents, technical specifications, and critical component implementations", 
    agent=StaffEngineer
)

task_code_implementation = Task(
    description="Using the architecture plan from the architect and technical specifications from the StaffEngineer, implement the code needed to fulfill the customer requirements. Focus on clean, efficient, and working code. Work with the debugger to fix any issues.",
    expected_output="Functional code implementation that satisfies the project requirements",
    agent=SeniorPrincipalEngineer
)

task_code_testing = Task(
    description="Create comprehensive test harnesses and testing frameworks. Ensure all functionalities are covered with automated tests including edge cases and regression scenarios.",
    expected_output="Comprehensive test suite and testing framework",
    agent=SoftwareEngineerInTest
)

task_debugging = Task(
    description="Assist with identifying and fixing bugs in the codebase. Perform code review and suggest optimizations. Work closely with Senior Principal Engineer to resolve issues quickly.",
    expected_output="Bug analysis report and fixed issues list",
    agent=MasterDebugger
)

task_quality_assurance = Task(
    description="Ensure the software meets project quality standards. Review code for consistency, performance, and adherence to best practices. Authority to send code back to Chief Architect or Senior Principal Engineer if quality standards are not met.",
    expected_output="Quality assessment report with recommendations",
    agent=HeadOfSoftwareQuality
)

task_documentation = Task(
    description="Create comprehensive documentation for the codebase including inline comments, README files, API references, and usage examples. Take documentation requests from all team members and translate complex technical concepts into accessible language.",
    expected_output="Complete professional project documentation",
    agent=TechnicalWriter
)

# Define delegation permissions - who can delegate to whom
delegation_map = {
    # HeadOfSoftwareQuality can send work back to ChiefArchitect and SeniorPrincipalEngineer
    HeadOfSoftwareQuality: [ChiefArchitect, SeniorPrincipalEngineer],
    
    # MasterDebugger works closely with SeniorPrincipalEngineer
    MasterDebugger: [SeniorPrincipalEngineer],
    SeniorPrincipalEngineer: [MasterDebugger],
    
    # StaffEngineer can delegate to SeniorPrincipalEngineer and TechnicalWriter
    StaffEngineer: [SeniorPrincipalEngineer, TechnicalWriter],
    
    # Everyone can delegate to the TechnicalWriter
    ChiefExecutiveOfficer: [TechnicalWriter],
    Director: [TechnicalWriter],
    ChiefArchitect: [TechnicalWriter],
    SeniorPrincipalEngineer: [TechnicalWriter],
    SoftwareEngineerInTest: [TechnicalWriter],
    MasterDebugger: [TechnicalWriter],
    HeadOfSoftwareQuality: [TechnicalWriter]
}

# NOTE: Direct delegation setting is no longer supported in newer CrewAI versions
# Delegation is now handled through the Crew configuration and the delegation parameter
# when creating tasks

# Resource weights control how much computation time each agent gets
resource_weights = {
    "ChiefExecutiveOfficer": 0.5,   # Executive overview doesn't need much computation
    "Director": 0.7,               # Coordination is important but not computation-heavy
    "ChiefArchitect": 1.0,        # Architecture planning is critical 
    "StaffEngineer": 1.0,         # Technical leadership is high-priority
    "SeniorPrincipalEngineer": 1.0, # Core implementation needs full resources
    "SoftwareEngineerInTest": 0.8, # Testing needs significant resources
    "MasterDebugger": 1.0,        # Debugging is critical and needs full resources
    "HeadOfSoftwareQuality": 0.8, # Quality assurance is important
    "TechnicalWriter": 0.4        # Documentation gets lower priority when resources are constrained
}

# Task types and their resource requirements
task_resource_priority = {
    "architecture": 1.0,           # Architecture tasks need full resources
    "implementation": 1.0,        # Implementation tasks need full resources 
    "testing": 0.9,              # Testing is high priority
    "debugging": 1.0,            # Debugging must have full resources
    "quality": 0.8,              # Quality assessment is important
    "documentation": 0.5,        # Documentation can work with fewer resources
    "management": 0.6,           # Management tasks are less compute-intensive
    "customer": 0.7              # Customer interaction is important but not compute-heavy
}

# Map tasks to their resource category
task_category_map = {
    task_architecture_planning: "architecture",
    task_staff_engineering: "implementation",
    task_code_implementation: "implementation",
    task_code_testing: "testing",
    task_debugging: "debugging",
    task_quality_assurance: "quality",
    task_documentation: "documentation",
    task_team_management: "management",
    task_customer_oversight: "customer"
}

def balance_agent_resources(agent, task=None):
    """Balance resources for agents to ensure fair distribution
    
    Args:
        agent: The CrewAI agent that's about to run
        task: The current task (optional)
        
    Returns:
        resource_factor: A factor (0-1) to apply to this agent's execution
    """
    # Get base weight for this agent
    agent_role = agent.role.replace(' ', '')
    if hasattr(agent, "__class__") and hasattr(agent.__class__, "__name__"):
        agent_class = agent.__class__.__name__
    else:
        agent_class = "TechnicalWriter"  # Default to TechnicalWriter (lowest) if unknown
        
    base_weight = resource_weights.get(agent_class, 0.7)  # Default to 0.7 if not specified
    
    # If task is provided, adjust weight based on task type
    task_factor = 1.0
    if task:
        task_category = task_category_map.get(task, "documentation")
        task_factor = task_resource_priority.get(task_category, 0.7)
    
    # Special handling for TechnicalWriter to prevent overuse when high-priority agents are active
    if agent_class == "TechnicalWriter":
        # Use agent.metadata to track Writer's usage
        if not hasattr(agent, "metadata"):
            agent.metadata = {"last_run": 0, "run_count": 0, "night_mode": False}
            
        current_time = time.time()
        
        # Check if we're in "night mode" (lead programmer offline)
        # This is determined by checking active agents or through a configuration
        night_mode = agent.metadata.get("night_mode", False)
        
        # Night mode can be triggered via configuration or by checking time periods
        # This allows Writer to catch up when other resources are offline
        if night_mode:
            # During night mode, Writer gets more resources
            base_weight = 0.9  # Increased priority during off-hours
            print(f"[Resource Manager] TechnicalWriter in night mode - increased resources")
        else:
            # Normal daytime operation - manage resources carefully
            # If Writer was recently used, reduce its priority further
            if current_time - agent.metadata.get("last_run", 0) < 60:  # Within last minute
                agent.metadata["run_count"] = agent.metadata.get("run_count", 0) + 1
                # Exponentially reduce resources if Writer is used repeatedly
                if agent.metadata["run_count"] > 3:
                    task_factor *= 0.5  # Halve the resources after 3 consecutive uses
            else:
                # Reset counter if enough time has passed
                agent.metadata["run_count"] = 1
                
        agent.metadata["last_run"] = current_time
    
    # Calculate final resource factor
    resource_factor = base_weight * task_factor
    
    # Apply any system-level adjustments
    # For example, check system load and adjust if necessary
    
    return resource_factor

# Create an Ollama LLM for the manager using the SeniorPrincipalEngineer's LLM
manager_llm = senior_engineer_llm

# Import Ollama embeddings for explicit configuration
from langchain_community.embeddings import OllamaEmbeddings
from core.config.llm_config import BASE_MODEL_NAME, OLLAMA_BASE_URL

# Create explicit embeddings configuration to override ChromaDB defaults
ollama_embed = OllamaEmbeddings(
    model=BASE_MODEL_NAME,  # Use base model name for direct Ollama API
    base_url=OLLAMA_BASE_URL  # Explicit base URL to avoid port format errors
)

# Create Crew with hierarchical workflow and customer interaction
crew = Crew(
    agents=[ChiefExecutiveOfficer, Director, ChiefArchitect, StaffEngineer, SeniorPrincipalEngineer, 
            SoftwareEngineerInTest, MasterDebugger, HeadOfSoftwareQuality, TechnicalWriter],
    tasks=[
        task_architecture_planning, 
        task_staff_engineering,
        task_code_implementation,
        task_code_testing,
        task_debugging,
        task_quality_assurance,
        task_documentation,
        task_team_management,
        task_customer_oversight
    ],
    verbose=True,
    process=Process.hierarchical,
    manager=Director,  # Director manages the workflow
    manager_llm=manager_llm,  # Added manager_llm as required by newer CrewAI versions
    memory=False,  # Disable CrewAI's built-in memory system
    cache=True    # Cache results for better performance
    # We'll implement our own memory system using FAISS instead of CrewAI's internal memory
)


def get_customer_input():
    """Function to get input from the customer during the process"""
    print("\n[CUSTOMER INPUT] Enter your feedback or press Enter to continue: ")
    return input()

def run_interactive_crew(memory_store=None):
    """Run the crew with interactive customer feedback and access to codebase memory
    
    Args:
        memory_store: The vector store containing indexed codebase (optional)
    """
    global crew
    
    # If memory store is provided, enhance agents with codebase memory
    if memory_store:
        print("Enhancing agents with codebase memory capabilities...")
        for agent in crew.agents:
            # Add memory tools to each agent
            agent.tools.append(create_memory_tool(memory_store))
            
    # Add resource balancing to agents
    for agent in crew.agents:
        # Store original _llm_completion method
        if not hasattr(agent, '_original_run'):
            agent._original_run = agent.run
            
            # Override run method with resource-balanced version
            def resource_balanced_run(self, *args, **kwargs):
                # Get current task if available
                current_task = kwargs.get('task', None)
                
                # Apply resource balancing
                resource_factor = balance_agent_resources(self, current_task)
                
                # Log resource allocation if verbose
                if self.verbose:
                    print(f"\n[Resource Manager] Allocating {resource_factor:.2f} resources to {self.role}")
                    
                # Special case for Writer - add documentation cycle management
                if self.__class__.__name__ == "Writer":
                    if not hasattr(self, "doc_cycle"):
                        self.doc_cycle = 0
                    self.doc_cycle += 1
                    
                    # Check if we should enable night mode (when Lead Programmer is inactive)
                    # This could be time-based, activity-based, or configuration-based
                    current_hour = time.localtime().tm_hour
                    if current_hour < 6 or current_hour > 22:  # Between 10PM and 6AM
                        if hasattr(self, "metadata"):
                            self.metadata["night_mode"] = True
                            print("[Resource Manager] Enabling Writer night mode - Lead Programmer offline")
                            # During night mode, Writer can do full documentation
                    else:
                        if hasattr(self, "metadata"):
                            self.metadata["night_mode"] = False
                    
                    # Only do full documentation during night mode or every 3rd cycle
                    night_mode = getattr(self, "metadata", {}).get("night_mode", False)
                    if not night_mode and self.doc_cycle % 3 != 0:
                        print("[Resource Manager] Writer performing incremental documentation only")
                        # Adjust scope of documentation based on cycle
                        if 'task' in kwargs and kwargs['task']:
                            kwargs['task'].description = kwargs['task'].description.replace(
                                "Create comprehensive documentation", 
                                "Update critical documentation for recent changes"
                            )
                
                # Call original run method
                return self._original_run(*args, **kwargs)
                
            # Bind the new method to the agent instance
            import types
            agent.run = types.MethodType(resource_balanced_run, agent)
    
    print("\nStarting CrewAI Interactive Simulation with Enhanced Memory...")
    conversation_history = []
    
    # Initial kickoff
    initial_result = crew.kickoff()
    conversation_history.append({"type": "result", "content": initial_result})
    print("\nInitial work completed. Result:")
    print(initial_result)
    
    # Allow for ongoing customer input
    while True:
        customer_input = get_customer_input()
        if not customer_input.strip():
            print("No additional input. Simulation ended.")
            break
            
        # Add to conversation history
        conversation_history.append({"type": "customer_input", "content": customer_input})
        print("\nProcessing your feedback...")
        
        # Create a new customer feedback task with access to conversation history
        feedback_task = Task(
            description=f"Process customer feedback: {customer_input}",
            expected_output="Updated work based on customer feedback",
            agent=Director,  # Director receives customer feedback first
            context=[f"Previous conversation: {conversation_history}"]  # Give context of previous interactions
        )
        
        # Add task to crew and process
        crew.tasks.append(feedback_task)
        result = crew.kickoff()
        
        # Add result to conversation history
        conversation_history.append({"type": "result", "content": result})
        print("\nFeedback processed. Result:")
        print(result)

def create_memory_tool(memory_store):
    """Create a tool that allows agents to search the codebase memory using Ollama"""
    # Create Ollama LLM instance using our configuration
    ollama_llm = get_ollama_llm(role='ChiefArchitect')  # Using the architect's model for memory
    
    # Create a retrieval chain
    retriever = memory_store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=ollama_llm,  # Use Ollama LLM
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    
    # Create a tool that wraps the QA chain using the decorator pattern
    @tool
    def codebase_memory(query: str) -> str:
        """Search the codebase for relevant code snippets, patterns, or information. Useful for understanding existing code structure and dependencies."""
        return qa_chain({"query": query})["result"]
        
    # Set memory_tool reference
    memory_tool = codebase_memory
    
    return memory_tool

# Make run_interactive_crew available for import in main.py
result = "Run main.py to start the interactive CrewAI simulation"

def run_crewsurfai_pipeline(tools_dict=None):
    """Run the CrewSurfAI pipeline with a team of agents
    
    Args:
        tools_dict: Dictionary of tools to add to agents
    """
    # Override default OpenAI embeddings with Ollama
    try:
        from langchain.globals import set_llm_cache
        from langchain_community.cache import InMemoryCache
        
        # Try to import CrewSettings from different locations based on crewai version
        try:
            # Newer versions of crewai
            from crewai import CrewSettings
        except ImportError:
            try:
                # Older versions of crewai
                from crewai.utilities import CrewSettings
            except ImportError:
                print("Warning: Could not import CrewSettings - local embeddings may not be configured")
                CrewSettings = None
        
        # Disable any OpenAI usage - use local models only
        os.environ["OPENAI_API_KEY"] = "sk-no-openai-usage"
        os.environ["LANGCHAIN_TRACING"] = "false"
        os.environ["CREWAI_FORCE_LOCAL_EMBEDDINGS"] = "true"  # Added explicit environment variable
        
        # Configure CrewAI to use entirely local tools if CrewSettings is available
        if CrewSettings:
            CrewSettings.use_local_embeddings()
        
        # Cache LLM calls to reduce redundant API calls
        set_llm_cache(InMemoryCache())
        
        print("Configured CrewAI to use local embeddings only")
    except Exception as e:
        print(f"Warning: Could not configure local embeddings: {e}")
    
    # Create a manager LLM using the SeniorPrincipalEngineer's LLM
    pipeline_manager_llm = senior_engineer_llm
    
    # First create agents with tools
    
    # Create copies of our agents to avoid modifying the originals
    # Define web search tools to use
    architect_tools = []
    if tools_dict and 'web_search_tool' in tools_dict:
        print("Adding web search tool to ChiefArchitect")
        architect_tools = [tools_dict['web_search_tool']]
    
    chief_architect = Agent(
        role=ChiefArchitect.role,
        goal=ChiefArchitect.goal,
        backstory=ChiefArchitect.backstory,
        verbose=True,
        allow_delegation=True
    )
    
    # Only add tools if we have them
    if architect_tools:
        chief_architect.tools = architect_tools
    
    # First define tools to use
    memory_tools = []
    if tools_dict and 'memory_tool' in tools_dict:
        print("Adding memory tool to SeniorPrincipalEngineer")
        memory_tools = [tools_dict['memory_tool']]
    
    senior_principal_engineer = Agent(
        role=SeniorPrincipalEngineer.role,
        goal=SeniorPrincipalEngineer.goal,
        backstory=SeniorPrincipalEngineer.backstory,
        llm=senior_engineer_llm,  # Use local Ollama
        verbose=True,
        allow_delegation=True
    )
    
    # Only add tools if we have them
    if memory_tools:
        senior_principal_engineer.tools = memory_tools
    
    # Other agents without special tools
    chief_executive_officer = Agent(
        role=ChiefExecutiveOfficer.role,
        goal=ChiefExecutiveOfficer.goal,
        backstory=ChiefExecutiveOfficer.backstory,
        verbose=True,
        allow_delegation=True
    )
    
    director = Agent(
        role=Director.role,
        goal=Director.goal,
        backstory=Director.backstory,
        verbose=True,
        allow_delegation=True
    )
    
    # StaffEngineer uses CascadeLLM to connect to Windsurf
    # This is the agent that the user interacts with directly
    staff_engineer = Agent(
        role=StaffEngineer.role,
        goal=StaffEngineer.goal,
        backstory=StaffEngineer.backstory,
        llm=cascade_llm,  # Use CascadeLLM to connect to Windsurf
        verbose=True,
        allow_delegation=True
    )
    
    software_engineer_in_test = Agent(
        role=SoftwareEngineerInTest.role,
        goal=SoftwareEngineerInTest.goal,
        backstory=SoftwareEngineerInTest.backstory,
        verbose=True,
        allow_delegation=True
    )
    
    master_debugger = Agent(
        role=MasterDebugger.role,
        goal=MasterDebugger.goal,
        backstory=MasterDebugger.backstory,
        verbose=True,
        allow_delegation=True
    )
    
    head_of_software_quality = Agent(
        role=HeadOfSoftwareQuality.role,
        goal=HeadOfSoftwareQuality.goal,
        backstory=HeadOfSoftwareQuality.backstory,
        verbose=True,
        allow_delegation=True
    )
    
    technical_writer = Agent(
        role=TechnicalWriter.role,
        goal=TechnicalWriter.goal,
        backstory=TechnicalWriter.backstory,
        verbose=True,
        allow_delegation=True
    )
    
    # Print tool assignment status
    if tools_dict and 'web_search_tool' in tools_dict:
        print("Added web search tool to ChiefArchitect")
    if tools_dict and 'memory_tool' in tools_dict:
        print("Added memory tool to SeniorPrincipalEngineer")
        
    # Create the Crew with the agents that have tools properly assigned
    crewsurfai_team = Crew(
        agents=[chief_executive_officer, director, chief_architect, 
                senior_principal_engineer, software_engineer_in_test, 
                master_debugger, head_of_software_quality, 
                technical_writer, staff_engineer],
        tasks=[task_customer_oversight, task_team_management, 
               task_architecture_planning, task_code_implementation, 
               task_code_testing, task_debugging, 
               task_quality_assurance, task_documentation],
        process=Process.hierarchical,
        manager=director,
        manager_llm=pipeline_manager_llm,  # Added manager_llm for hierarchical process
        memory=False,  # Disable memory to avoid ChromaDB API issues
        verbose=True
    )
    
    # Print configuration
    print("\n=== CrewSurfAI Team Configuration ===")
    print(f"Team size: {len(crewsurfai_team.agents)} agents")
    print(f"Tasks: {len(crewsurfai_team.tasks)} main workflow tasks")
    print(f"Process: {crewsurfai_team.process}")
    
    # Run the crew and get the result
    try:
        print("\n=== Starting CrewSurfAI Pipeline ===")
        result = crewsurfai_team.kickoff()
        print("\n=== CrewSurfAI Pipeline Complete ===")
        print(f"Result: {result}")
        return result
    except Exception as e:
        print(f"\nError in CrewSurfAI pipeline: {str(e)}")
        raise