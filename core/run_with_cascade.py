import os
import sys
import glob
import time
import logging
from datetime import datetime
from pathlib import Path

# Apply patches early to fix LiteLLM Ollama integration issues
from core.patches.litellm_patch import patch_litellm
logging.info("Applying LiteLLM patches for Ollama integration")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

try:
    # Use the new langchain-ollama package
    from langchain_ollama import OllamaEmbeddings
except ImportError:
    # Fallback to deprecated import
    from langchain_community.embeddings import OllamaEmbeddings

# Use our centralized LLM configuration
from core.config.llm_config import get_ollama_llm, get_all_agent_configs, configure_environment_for_local, print_model_config
from langchain_core.vectorstores import VectorStore
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.tools import DuckDuckGoSearchRun

# Import local modules
from core.crew import run_crewsurfai_pipeline
from bridge.cascade_bridge import CascadeLLM

def scan_codebase(source_dir):
    """Scan the codebase for relevant files and build embeddings
    
    Args:
        source_dir: Directory to scan for code files
        
    Returns:
        Vector store with code embeddings
    """
    # Import project configuration
    try:
        from core.config.project_config import INCLUDED_FILE_TYPES, EXCLUDED_DIRS, PROJECT_LANGUAGE
        # Use config values
        file_types = INCLUDED_FILE_TYPES
        exclude_dirs = EXCLUDED_DIRS
        print(f"Scanning codebase for {PROJECT_LANGUAGE} files...")
    except ImportError:
        # Default values if config not found
        file_types = [".java", ".kt", ".gradle", ".xml", ".json", ".md", ".txt", ".py"]
        exclude_dirs = [".git", "build", "bin", ".gradle", "__pycache__", "venv"]
        print("\nScanning codebase for relevant files...")
    
    code_files = []
    for root, dirs, files in os.walk(source_dir):
        # Skip any excluded directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in exclude_dirs]
        
        for file in files:
            # Check if file has one of the included extensions
            if any(file.endswith(ext) for ext in file_types):
                full_path = os.path.join(root, file)
                code_files.append(full_path)
    
    print(f"Scanned {len(code_files)} code files")
    
    # Create embeddings from the code files
    documents = []
    for file_path in code_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                content = f.read()
                # Create a document with the code content and metadata
                documents.append({
                    "page_content": content,
                    "metadata": {
                        "source": file_path,
                        "filename": os.path.basename(file_path)
                    }
                })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    # Create vector store using Chroma with Ollama embeddings
    try:
        # Use embedded model name and base_url from config
        from core.config.llm_config import BASE_MODEL_NAME, OLLAMA_BASE_URL
        
        # Configure Ollama embeddings with base_url to avoid port format errors
        ollama_embeddings = OllamaEmbeddings(
            model=BASE_MODEL_NAME,  # Use base model name (no provider prefix) for direct API calls
            base_url=OLLAMA_BASE_URL  # Explicit base URL to avoid port format errors
        )
        
        # Create FAISS vector store with the embeddings
        vectorstore = FAISS.from_documents(
            documents=[Document(**doc) for doc in documents],
            embedding=ollama_embeddings
        )
        
        # Save index for future use if needed
        vectorstore.save_local("./faiss_index")
        
        print(f"Memory store created with {len(documents)} chunks of code using FAISS and Ollama embeddings")
        return vectorstore
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None

def create_memory_tool(memory_store, ollama_llm):
    """Creates a retrieval tool for searching code in memory"""
    # Set up retriever
    retriever = memory_store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=ollama_llm,
        chain_type="stuff",
        retriever=retriever
    )
    
    # Import the tool decorator from crewai
    from crewai.tools import tool
    
    # Create a tool using the decorator pattern
    @tool
    def codebase_memory(query: str) -> str:
        """Search the codebase for relevant code snippets, patterns, or information."""
        return qa_chain.run(query)
    
    return codebase_memory

def run_modified_crew(memory_store):
    """Run the CrewSurfAI pipeline with memory tools"""
    # Create web search tool
    web_search_tool = DuckDuckGoSearchRun()
    
    # Create memory tool with Ollama using our centralized config
    ollama_llm = get_ollama_llm(role="SeniorPrincipalEngineer", use_provider_prefix=True)
    memory_tool = create_memory_tool(memory_store, ollama_llm)
    
    # Run the CrewSurfAI pipeline
    tools_dict = {
        "web_search": web_search_tool,
        "memory_tool": memory_tool
    }
    
    # The SeniorPrincipalEngineer is already configured to use Cascade
    # in its agent definition file
    
    # Run the CrewSurfAI pipeline
    print("\nCrewAI Enhanced with Cascade Integration")
    print("✅ Cascade Bridge is running!")
    
    # Configure environment to avoid OpenAI API usage
    configure_environment_for_local()
    
    # Set up the list of available models using our centralized config
    agents_config = get_all_agent_configs()
    print_model_config()
    
    run_crewsurfai_pipeline(tools_dict)

if __name__ == "__main__":
    # Show provider list
    print("\nProvider List: https://docs.litellm.ai/docs/providers\n")
    
    # Scan codebase and set up vector store directly
    memory_store = scan_codebase("./")
    
    if memory_store is None:
        print("Failed to create memory store. Exiting.")
        sys.exit(1)
    
    # Run the modified crew with memory tools
    run_modified_crew(memory_store)
