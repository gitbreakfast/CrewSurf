"""
CrewSurf - Seamless integration between CrewAI agents, local LLMs, and interactive development environments

This module provides the core functionality for connecting CrewAI with Windsurf/Cascade,
local LLMs via Ollama, and environment management like conda.
"""

__version__ = '0.1.0'

# Import core components for easy access
from .windsurf_integration import WindsurfCustomerTool, CondaEnvironmentHandler

# Export main classes for easier imports
__all__ = ['WindsurfCustomerTool', 'CondaEnvironmentHandler']
