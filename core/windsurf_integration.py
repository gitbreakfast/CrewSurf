"""
WindsurfAI Integration Module

This module provides integration with WindsurfAI for enhanced conversational capabilities in CrewSurf.
It enables customer interactions with the AI crew through a custom tool interface.
"""

import logging
import requests
import json
from typing import List, Optional, Dict, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime

class WindsurfCustomerTool(BaseTool):
    """
    Tool for integrating customer interaction with WindsurfAI.
    
    This tool allows agents to interact with the customer by sending messages
    and receiving responses through a custom integration bridge.
    """
    
    name: str = "WindsurfCustomerTool"
    description: str = (
        "Use this tool to ask the customer questions or provide information. "
        "Pass your message to the customer, and they will reply."
    )
    
    def __init__(self, bridge_url: str = "http://localhost:8089/message", **kwargs):
        """Initialize the WindsurfCustomerTool with a bridge URL."""
        super().__init__(**kwargs)
        self.bridge_url = bridge_url
        self.conversation_history = []
        self.logger = logging.getLogger(__name__)
        
    def _run(self, message: str) -> str:
        """Run the tool to interact with the customer."""
        self.logger.info(f"Sending message to customer: {message}")
        
        # Add message to conversation history
        self.conversation_history.append({
            "role": "agent",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Send message to bridge service
        try:
            response = requests.post(
                self.bridge_url,
                json={"message": message},
                headers={"Content-Type": "application/json"},
                timeout=120  # Extended timeout for longer conversations
            )
            
            if response.status_code == 200:
                customer_response = response.json().get("response", "No response received")
                self.logger.info(f"Received customer response: {customer_response}")
                
                # Add customer response to conversation history
                self.conversation_history.append({
                    "role": "customer",
                    "content": customer_response,
                    "timestamp": datetime.now().isoformat()
                })
                
                return customer_response
            else:
                error_msg = f"Error communicating with bridge: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                return error_msg
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to connect to bridge: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
    
    def _arun(self, message: str) -> str:
        """Async version of _run (not implemented)."""
        raise NotImplementedError("Async version not implemented yet")
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Return the conversation history between agent and customer."""
        return self.conversation_history


# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create tool instance
    customer_tool = WindsurfCustomerTool()
    
    # Test interaction
    response = customer_tool.run("Hello customer! What can I help you with today?")
    print(f"Customer response: {response}")
