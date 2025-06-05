import os
import glob
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from crew import run_interactive_crew
from config.llm_config import print_model_config

# Load environment variables from .env file (for API keys)
load_dotenv()

def scan_codebase(directory="./", file_extensions=[".py", ".js", ".html", ".css", ".md", ".txt", ".yaml", ".yml"]):
    """Scan and index the entire codebase for enhanced memory"""
    print("Scanning codebase for memory indexing...")
    code_files = []
    for ext in file_extensions:
        code_files.extend(glob.glob(f"{directory}/**/*{ext}", recursive=True))
    
    # Read all code files
    code_contents = []
    for file_path in code_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                code_contents.append({"path": file_path, "content": content})
            print(f"Indexed: {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return code_contents

def create_memory_store(code_contents):
    """Create a vector store for code memory using Ollama locally"""
    # Prepare documents
    documents = []
    for item in code_contents:
        documents.append(f"File: {item['path']}\n\n{item['content']}")
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )
    texts = text_splitter.create_documents(documents)
    
    # Create vector store using Ollama embeddings
    try:
        # Use Ollama for embeddings with your local qwen3 model
        embeddings = OllamaEmbeddings(model="qwen3")
        vector_store = Chroma.from_documents(texts, embeddings, persist_directory="./chroma_db")
        print(f"Memory store created with {len(texts)} chunks of code using Ollama")
        return vector_store
    except Exception as e:
        print(f"Error creating memory store: {e}")
        print("Proceeding without vector memory...")
        return None

# Main entry point
if __name__ == "__main__":
    print("\nCrewAI Enhanced Memory Setup")
    
    # Print the model configuration being used
    print_model_config()
    
    # Scan codebase for memory
    code_contents = scan_codebase()
    print(f"Scanned {len(code_contents)} code files")
    
    # Create memory store using Ollama (no API key required)
    memory_store = None
    try:
        memory_store = create_memory_store(code_contents)
    except Exception as e:
        print(f"Error initializing Ollama memory store: {e}")
        print("Make sure Ollama is installed and running locally.")
    
    # Run the interactive crew simulation
    print("\nStarting CrewAI with enhanced memory...")
    run_interactive_crew(memory_store)
