"""
Main entry point for CrewSurf AI system with Cascade integration
"""

import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Import the run_with_cascade module and run it
if __name__ == "__main__":
    print("Starting CrewSurf AI with Cascade integration...")
    from core.run_with_cascade import scan_codebase_for_memory, setup_memory_storage, run_modified_crew
    
    # Scan codebase for Python files
    code_files = scan_codebase_for_memory()
    print(f"Scanned {len(code_files)} code files")
    
    # Set up memory storage
    memory_store, _ = setup_memory_storage(code_files)
    
    # Run the modified crew with memory tools
    run_modified_crew(memory_store)
