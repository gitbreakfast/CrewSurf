"""
Example main entry point for CrewSurf
This demonstrates codebase scanning with vector memory
"""
import os
import glob
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.tools import Tool
from langchain_community.llms import Ollama

from example_crew import run_interactive_crew

# Print a welcome message
def print_welcome():
    print("\n" + "="*50)
    print("🏄‍♂️ CrewSurf - Advanced AI Development Team")
    print("="*50)
    print("Initializing your AI team...")
    print_model_config()

# Configuration for the LLM models
def print_model_config():
    """Print the model configuration for all agents."""
    print("\n=== Agent Model Configuration ===")
    print("ChiefArchitect: qwen:7b (temperature: 0.8)")
    print("LeadProgrammer: qwen:7b (temperature: 0.5)")
    print("SeniorPrincipalEngineer: qwen:7b (temperature: 0.3)")
    
def get_ollama_llm():
    """Create and return an Ollama LLM instance."""
    return Ollama(model="qwen:7b")

def scan_codebase(directory_path):
    """
    Scan a codebase and extract content from relevant files
    
    Args:
        directory_path: Path to the directory containing the codebase
        
    Returns:
        List of documents containing code snippets
    """
    code_files = []
    code_extensions = ['.py', '.js', '.java', '.c', '.cpp', '.h', '.cs', '.ts', '.html', '.css']
    
    # Find all files with code extensions
    for ext in code_extensions:
        files = glob.glob(os.path.join(directory_path, f'**/*{ext}'), recursive=True)
        code_files.extend(files)
    
    print(f"Scanned {len(code_files)} code files")
    
    documents = []
    for file_path in code_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                relative_path = os.path.relpath(file_path, directory_path)
                documents.append({
                    'content': content,
                    'path': relative_path
                })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return documents

def create_vector_store(documents):
    """
    Create a vector store from code documents
    
    Args:
        documents: List of documents containing code
        
    Returns:
        Chroma vector store instance
    """
    # Initialize Ollama embeddings
    try:
        print("Creating vector embeddings with Ollama...")
        embeddings = OllamaEmbeddings(model="qwen:7b")
        
        # Create texts and metadata
        texts = [doc['content'] for doc in documents]
        metadatas = [{'path': doc['path']} for doc in documents]
        
        # Create vector store
        vector_store = Chroma.from_texts(
            texts=texts, 
            embedding=embeddings,
            metadatas=metadatas,
            persist_directory="./chroma_db"
        )
        
        print(f"Memory store created with {len(texts)} chunks of code using Ollama")
        return vector_store
        
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None

def create_memory_tool(vector_store):
    """
    Create a tool to query the code memory
    
    Args:
        vector_store: Vector store containing code embeddings
        
    Returns:
        Tool for querying code memory
    """
    if not vector_store:
        return None
        
    # Create retriever from vector store
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # Create Ollama LLM for the QA chain
    ollama_llm = get_ollama_llm()
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=ollama_llm,
        chain_type="stuff",
        retriever=retriever
    )
    
    # Create a tool that wraps the retrieval chain
    memory_tool = Tool(
        name="CodebaseMemory",
        func=qa_chain.run,
        description="Useful for searching through the codebase memory."
    )
    
    return memory_tool

if __name__ == "__main__":
    print_welcome()
    
    # Step 1: Scan the codebase (use your project path or current directory)
    project_path = os.getcwd() 
    documents = scan_codebase(project_path)
    
    # Step 2: Create vector store for code memory
    memory_store = create_vector_store(documents)
    
    # Step 3: Create memory tool for agents to use
    if memory_store:
        memory_tool = create_memory_tool(memory_store)
    
    # Step 4: Run the interactive crew with memory access
    run_interactive_crew(memory_store)
