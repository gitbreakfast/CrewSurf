"""
Windsurf/Cascade Integration for CrewAI

This module provides tools and utilities for integrating CrewAI with Windsurf/Cascade,
allowing you to directly interact with the CrewAI agents as the customer without
leaving the Windsurf interface.
"""
from crewai import Tool
import os
import time
import json

class WindsurfCustomerTool:
    """
    A tool factory that creates CrewAI tools for getting customer input
    directly through the Windsurf/Cascade interface.
    """
    
    @staticmethod
    def create_customer_input_tool():
        """
        Creates a tool that agents can use to ask the customer (you) questions
        directly through Windsurf.
        
        Returns:
            Tool: A CrewAI Tool instance
        """
        def ask_customer(question):
            """
            Function that asks the customer a question and waits for their response
            in the Windsurf interface.
            
            Args:
                question: The question to ask the customer
                
            Returns:
                str: The customer's response
            """
            print("\n")
            print("="*80)
            print("🔴 CUSTOMER INPUT REQUESTED 🔴")
            print("="*80)
            print(f"\n{question}\n")
            
            # In Windsurf, we just need to prompt the user and wait for their response
            # The CrewAI agent will display the question directly in Windsurf
            # and the user's next input will be captured as the response
            response = input("\nPlease enter your response: ")
            
            print("\n")
            print("-"*80)
            print(f"Response recorded: {response[:50]}{'...' if len(response) > 50 else ''}")
            print("-"*80)
            
            return response
        
        # Create and return the CrewAI tool
        return Tool(
            name="AskCustomer",
            func=ask_customer,
            description="Use this tool whenever you need to ask the customer (human user) a question or get their feedback. The customer will see your question in Windsurf and can respond directly."
        )

class CondaEnvironmentHandler:
    """
    Helper class for working with conda environments in scripts.
    """
    
    @staticmethod
    def get_conda_run_command(env_name="crewai"):
        """
        Get the appropriate command prefix to run a Python script in a conda environment.
        
        Args:
            env_name: Name of the conda environment
            
        Returns:
            str: Command prefix for running Python in the specified conda environment
        """
        if os.name == "nt":  # Windows
            return f"conda run -n {env_name} python"
        else:  # Unix/Linux/Mac
            return f"conda run -n {env_name} python"
    
    @staticmethod
    def get_current_conda_env():
        """
        Get the name of the currently active conda environment.
        
        Returns:
            str: Name of the current conda environment or None if not in a conda env
        """
        return os.environ.get("CONDA_DEFAULT_ENV")
