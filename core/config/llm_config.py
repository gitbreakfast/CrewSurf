"""
Ollama LLM Configuration for CrewAI agents

This module provides centralized configuration for LLM models used in different contexts:
1. Direct API usage (OllamaLLM for embeddings, direct calls)
2. CrewAI/LiteLLM usage (requiring provider prefix)
"""
import os
# Use the latest recommended import for Ollama if available
try:
    from langchain_ollama import OllamaLLM as Ollama
except ImportError:
    # Fallback to deprecated import
    from langchain_community.llms import Ollama

# Base configuration
OLLAMA_BASE_URL = "http://localhost:11434"
BASE_MODEL_NAME = 'qwen3'  # Base model name without provider prefix
CREWAI_MODEL_NAME = f"ollama/{BASE_MODEL_NAME}"  # Model name with provider prefix for CrewAI/LiteLLM

# Agent role to temperature mapping
AGENT_TEMPERATURE_MAP = {
    # More creative for architectural and writing tasks
    'ChiefArchitect': 0.8,
    'TechnicalWriter': 0.7,
    
    # More deterministic for coding and testing
    'SeniorPrincipalEngineer': 0.3,
    'SoftwareEngineerInTest': 0.2,
    'MasterDebugger': 0.2,
    'StaffEngineer': 0.3,
    
    # Middle ground for management
    'ChiefExecutiveOfficer': 0.7,
    'Director': 0.5,
    'HeadOfSoftwareQuality': 0.4,
    
    # Default temperature
    'default': 0.5
}

# Cache for LLM instances to avoid recreation
_llm_cache = {}

def get_ollama_llm(role='default', use_provider_prefix=False, override_temperature=None):
    """
    Create an Ollama LLM instance with parameters based on agent role
    
    Args:
        role: Agent role name to determine temperature
        use_provider_prefix: If True, use 'ollama/qwen3' format for LiteLLM compatibility
                           If False, use 'qwen3' format for direct Ollama API calls
        override_temperature: Optionally override the role-based temperature
    
    Returns:
        Configured Ollama LLM instance
    """
    # Cache key includes all parameters that could affect the LLM instance
    cache_key = f"{role}_{use_provider_prefix}_{override_temperature}"
    
    # Return cached instance if available
    if cache_key in _llm_cache:
        return _llm_cache[cache_key]
    
    # Get the appropriate model name based on usage context
    model = CREWAI_MODEL_NAME if use_provider_prefix else BASE_MODEL_NAME
    temperature = override_temperature or AGENT_TEMPERATURE_MAP.get(role, AGENT_TEMPERATURE_MAP['default'])
    
    # Create the Ollama instance with explicit base_url to avoid invalid port errors
    llm = Ollama(
        model=model,
        temperature=temperature,
        base_url=OLLAMA_BASE_URL
    )
    
    # Cache the instance for future use
    _llm_cache[cache_key] = llm
    return llm

def get_all_agent_configs():
    """
    Get model configurations for all agents for CrewAI initialization
    
    Returns:
        Dictionary of agent configurations with model and temperature
    """
    agents_config = {}
    for role in AGENT_TEMPERATURE_MAP:
        if role != 'default':
            agents_config[role] = {
                "model": CREWAI_MODEL_NAME,  # Always use provider prefix for CrewAI
                "temperature": AGENT_TEMPERATURE_MAP[role]
            }
    return agents_config

def print_model_config():
    """Print the current model configuration for all agents"""
    print("\n=== Agent Model Configuration ===")
    for role in sorted([r for r in AGENT_TEMPERATURE_MAP.keys() if r != 'default']):
        temp = AGENT_TEMPERATURE_MAP.get(role, AGENT_TEMPERATURE_MAP['default'])
        print(f"{role}: {CREWAI_MODEL_NAME} (temperature: {temp})")
        
def configure_environment_for_local():
    """Configure environment variables to force local embeddings and prevent OpenAI usage"""
    os.environ["OPENAI_API_KEY"] = "sk-no-openai-usage"
    os.environ["LANGCHAIN_TRACING"] = "false"
    os.environ["CREWAI_FORCE_LOCAL_EMBEDDINGS"] = "true"
    return True
