"""
Environment setup script for running CrewAI with local Ollama models
This sets the necessary environment variables and runs the application
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set all required environment variables for local LLM and embeddings"""
    logger.info("Setting up environment for local embeddings and LLM")
    
    # Disable OpenAI API usage completely to prevent fallbacks
    os.environ["OPENAI_API_KEY"] = ""
    os.environ["OPENAI_API_BASE"] = "http://localhost:11434"
    os.environ["LANGCHAIN_TRACING"] = "false"
    os.environ["CREWAI_FORCE_LOCAL_EMBEDDINGS"] = "true"
    os.environ["LANGCHAIN_OPENAI_API_KEY"] = ""
    
    # Remove any other OpenAI-related variables that might trigger API calls
    if "OPENAI_API_TYPE" in os.environ:
        del os.environ["OPENAI_API_TYPE"]
    if "OPENAI_ORGANIZATION" in os.environ:
        del os.environ["OPENAI_ORGANIZATION"]
    
    # Add CrewAI specific environment variables
    os.environ["CREWAI_LLM_PROVIDER"] = "ollama"
    
    # Add Chroma environment variables to prevent OpenAI embeddings usage
    os.environ["CHROMA_OPENAI_API_KEY"] = "dummy-key-for-local-usage"
    # Remove any existing CHROMA_API_IMPL if present as it causes errors
    if "CHROMA_API_IMPL" in os.environ:
        del os.environ["CHROMA_API_IMPL"]
    
    # Force CrewAI to use local embeddings
    os.environ["CREWAI_EMBEDDINGS"] = "ollama"
    os.environ["CREW_EMBEDDING_MODEL"] = "nomic-embed-text" # Without provider prefix
    os.environ["CREW_EMBEDDING_BASE_URL"] = "http://localhost:11434"
    
    # Additional CrewAI environment variables
    os.environ["LANGCHAIN_TRACING_V2"] = "false"
    os.environ["LANGCHAIN_ENDPOINT"] = ""
    os.environ["LANGCHAIN_API_KEY"] = ""
    os.environ["LANGCHAIN_PROJECT"] = ""
    
    # Set debug mode for litellm if needed
    # os.environ["LITELLM_DEBUG"] = "true"
    
    logger.info("Environment variables set successfully")

if __name__ == "__main__":
    setup_environment()
    
    # Import the patch first to ensure it's applied before any LiteLLM usage
    from core.patches.litellm_patch import patch_litellm
    patch_litellm()
    
    # Run the main application
    from core.run_with_cascade import run_modified_crew
    logger.info("Starting CrewSurf AI with local LLM and embeddings")
    
    # Patch sys.argv if no arguments are provided
    if len(sys.argv) <= 1:
        sys.argv = [sys.argv[0], "--scan-codebase"]
    
    # Run the modified crew function that's already imported
    # First scan the codebase to create memory store
    from core.run_with_cascade import scan_codebase
    from core.config.project_config import PROJECT_DIR
    
    # Use project directory from config
    print(f"Scanning codebase at: {PROJECT_DIR}")
    memory_store = scan_codebase(PROJECT_DIR)
    
    # Now run the modified crew with the memory store
    run_modified_crew(memory_store)
