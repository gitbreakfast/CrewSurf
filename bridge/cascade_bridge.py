"""
Example Cascade Bridge integration for CrewSurf
This file demonstrates how to connect CrewAI agents to Windsurf/Cascade
"""
import os
import requests
import logging
import time
from typing import Dict, Any, Optional, List
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from pydantic import Extra, Field, root_validator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('CascadeLLM')

class CascadeLLM(LLM):
    """
    LLM wrapper for Cascade Bridge integration.
    
    This acts as a bridge between CrewAI agents and Windsurf/Cascade,
    allowing agents to communicate with the human user through
    the Windsurf IDE.
    """
    
    bridge_url: str = Field(default="http://localhost:8089")
    agent_role: str = Field(default="Assistant")
    timeout: int = Field(default=120)
    
    class Config:
        """Configuration for this pydantic object."""
        extra = Extra.forbid

    @root_validator(skip_on_failure=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that bridge server appears to be running."""
        try:
            bridge_url = values["bridge_url"]
            response = requests.get(f"{bridge_url}/health", timeout=5)
            if response.status_code == 200:
                logger.info(f"Successfully configured Cascade Bridge for role: {values['agent_role']}")
            else:
                logger.warning(f"Cascade Bridge health check failed: {response.status_code}")
        except Exception as e:
            logger.warning(f"Failed to connect to Cascade Bridge: {e}")
            logger.warning("Bridge server might not be running - continuing with setup anyway")
        
        return values

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "cascade_bridge"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the Cascade Bridge API."""
        try:
            # Prepare the payload
            payload = {
                "prompt": prompt,
                "role": self.agent_role,
                "stop": stop or [],
            }
            
            # Send request to bridge
            response = requests.post(
                f"{self.bridge_url}/generate", 
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                error_message = f"Bridge server error: {response.status_code} - {response.text}"
                logger.error(error_message)
                return f"[ERROR: {error_message}]"
                
        except Exception as e:
            error_message = f"Exception calling Cascade Bridge: {str(e)}"
            logger.error(error_message)
            return f"[ERROR: {error_message}]"
