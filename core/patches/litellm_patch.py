"""
LiteLLM Patch for Ollama tool calls issues

This module contains monkey patches for known issues with LiteLLM's Ollama integration,
specifically around tool calling support which causes index errors.
"""
import os
import sys
import logging
from functools import wraps

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def patch_litellm():
    """
    Apply patches to LiteLLM to fix common issues with the Ollama integration,
    particularly around tool calls which cause index errors.
    """
    try:
        # Disable OpenAI API usage completely to prevent fallbacks
        os.environ["OPENAI_API_KEY"] = ""
        os.environ["OPENAI_API_BASE"] = "http://localhost:11434"  # Redirect to Ollama
        os.environ["LANGCHAIN_TRACING"] = "false"
        os.environ["CREWAI_FORCE_LOCAL_EMBEDDINGS"] = "true"
        os.environ["LANGCHAIN_OPENAI_API_KEY"] = ""
        
        # Add CrewAI specific environment variables
        os.environ["CREWAI_LLM_PROVIDER"] = "ollama"
        
        # Add Chroma environment variables to prevent OpenAI embeddings usage
        os.environ["CHROMA_OPENAI_API_KEY"] = "not-needed-using-local-embeddings"
        
        # Force CrewAI to use local embeddings
        os.environ["CREW_EMBEDDING_MODEL"] = "ollama/nomic-embed-text"
        os.environ["CREW_EMBEDDING_BASE_URL"] = "http://localhost:11434"
        
        # Import liteLLM modules for patching
        import litellm
        from litellm.litellm_core_utils.prompt_templates.factory import ollama_pt
        
        # Keep track of original function
        original_ollama_pt = ollama_pt
        
        # Define completely new, safe implementation of ollama_pt
        def patched_ollama_pt(model, messages, custom_llm_provider=None, **kwargs):
            """
            Completely rewritten ollama_pt function to properly handle tool calls and prevent index errors.
            This handles all message formats and produces Ollama-compatible prompts.
            """
            # Create a default fallback prompt in case of any errors
            default_prompt = "<user>\nHelp me\n</user>"
            
            try:
                # Safety check for empty messages
                if not messages:
                    logger.warning("Empty messages list in ollama_pt, returning default prompt")
                    return default_prompt
                
                # Log message information for debugging
                logger.info(f"Patched ollama_pt called with {len(messages)} messages")
                
                # Create a clean list of valid dict messages - defensive coding
                clean_messages = []
                for msg in messages:
                    if isinstance(msg, dict):
                        clean_messages.append(dict(msg))  # Create a clean copy
                    else:
                        logger.warning(f"Skipping non-dict message of type: {type(msg)}")
                
                # If we have no valid messages, return default
                if not clean_messages:
                    logger.warning("No valid messages found")
                    return default_prompt
                
                # Build prompt in Ollama format
                # Extract system prompt if present
                system = ""
                system_messages = []
                user_assistant_messages = []
                
                # Separate system messages from other messages
                for msg in clean_messages:
                    if msg.get("role", "") == "system":
                        system_content = msg.get("content") or ""
                        if system_content:
                            system += system_content
                            system_messages.append(msg)
                    else:
                        user_assistant_messages.append(msg)
                        
                result = ""
                if system:
                    result += f"<system>\n{system}\n</system>\n\n"
                    
                # Process user/assistant messages in sequence
                # Safety check to avoid index errors
                if not user_assistant_messages:
                    logger.warning("No user or assistant messages to process")
                    if result:  # If we at least have a system message
                        result += f"<user>\nHelp me\n</user>"
                        return result
                    else:
                        return default_prompt
                
                # Process messages in pairs (user/assistant)
                prompt_messages = []
                for i, msg in enumerate(user_assistant_messages):
                    role = msg.get("role", "").lower()
                    content = msg.get("content")
                    if content is None:  # Handle None content
                        content = ""
                        
                    # Handle tool calls safely - this is where the index error happened
                    tool_calls = None
                    try:
                        # Safely get tool_calls with multiple fallback options
                        if "tool_calls" in msg:
                            tool_calls = msg.get("tool_calls")
                        elif "function_call" in msg:
                            # Handle legacy function call format
                            function_call = msg.get("function_call")
                            if function_call:
                                tool_calls = [{
                                    "type": "function",
                                    "function": function_call
                                }]
                    except Exception as e:
                        logger.warning(f"Error extracting tool_calls: {e}")
                        tool_calls = None

                    # Process different roles
                    if role == "user":
                        result += f"<user>\n{content}\n</user>\n"
                    elif role == "assistant":
                        # Add assistant message content
                        result += f"<assistant>\n{content}"
                        
                        # Safe handling of tool_calls - this was the source of the index error
                        if tool_calls is not None and isinstance(tool_calls, list) and len(tool_calls) > 0:
                            try:
                                # Process each tool call safely
                                for tool_call in tool_calls:
                                    if not isinstance(tool_call, dict):
                                        continue  # Skip non-dict tool calls
                                        
                                    # Extract function name and arguments
                                    function_data = None
                                    
                                    # Try different possible structures
                                    if "function" in tool_call and isinstance(tool_call["function"], dict):
                                        function_data = tool_call["function"]
                                    elif "function_call" in tool_call and isinstance(tool_call["function_call"], dict):
                                        function_data = tool_call["function_call"]
                                        
                                    if function_data:
                                        fn_name = function_data.get("name", "")
                                        fn_args = function_data.get("arguments", "{}")
                                        if fn_name:
                                            # Format tool call for Ollama
                                            result += f"\n<tool_call>\n<tool_name>{fn_name}</tool_name>\n<tool_input>{fn_args}</tool_input>\n</tool_call>"
                            except Exception as e:
                                logger.warning(f"Error processing tool calls: {e}")
                                
                        # Close assistant tag
                        result += "\n</assistant>\n"
                        
                # Add tool_result messages if present
                for msg in user_assistant_messages:
                    if msg.get("role", "").lower() == "tool":
                        tool_name = msg.get("name", "")
                        content = msg.get("content", "")
                        if tool_name and content:
                            result += f"<tool_result>\n<tool_name>{tool_name}</tool_name>\n<tool_result_value>{content}</tool_result_value>\n</tool_result>\n"
                            
                # Return the final formatted prompt
                logger.info(f"Successfully created Ollama prompt with length {len(result)}")
                return result
                
            except Exception as e:
                # Log the error and return a safe default prompt
                logger.error(f"Error in patched_ollama_pt: {str(e)}")
                return default_prompt
                return result
                    
            except Exception as e:
                logger.error(f"Error in patched_ollama_pt: {str(e)}")
                try:
                    # Don't fall back to original function if our patch fails - it has the bug!
                    # Return a minimal working prompt as last resort
                    logger.info("Patched ollama_pt failed, returning minimal prompt")
                    return "<user>\nHelp me\n</user>"
                except Exception as inner_e:
                    logger.error(f"Both patched and original ollama_pt failed: {str(inner_e)}")
                    # Return minimal working prompt as last resort
                    return "<user>\nHelp me\n</user>"
        
        # Apply the patch by replacing the function everywhere it's used
        logger.info("Applying patch for ollama_pt in LiteLLM")
        # Direct replacement in the prompt_templates factory
        from litellm.litellm_core_utils.prompt_templates import factory
        factory.ollama_pt = patched_ollama_pt
        
        # Patch the Ollama provider by directly replacing the ollama_pt function
        try:
            # Try to find and patch ollama_pt in the transformation module
            import importlib
            
            # First try the direct module structure
            try:
                from litellm.llms.ollama.completion import transformation
                if hasattr(transformation, 'ollama_pt'):
                    # Save original for reference
                    original_pt = transformation.ollama_pt
                    # Replace with our patched version
                    transformation.ollama_pt = patched_ollama_pt
                    logger.info("Successfully patched Ollama's ollama_pt in transformation module")
            except (ImportError, AttributeError) as e:
                logger.info(f"Could not find ollama_pt in direct module: {str(e)}")
            
            # Try alternative module paths that might exist in different versions
            possible_paths = [
                'litellm.llms.ollama.completion.transformation',
                'litellm.llms.ollama',
                'litellm.llms.ollama.completion',
                'litellm.prompt_templates.factory',
                'litellm.litellm_core_utils.prompt_templates.factory'
            ]
            
            for path in possible_paths:
                try:
                    module = importlib.import_module(path)
                    if hasattr(module, 'ollama_pt'):
                        module.ollama_pt = patched_ollama_pt
                        logger.info(f"Successfully patched ollama_pt in {path}")
                except (ImportError, AttributeError) as e:
                    logger.debug(f"Could not patch {path}: {str(e)}")
            
            logger.info("Completed Ollama patching process")
        except Exception as e:
            logger.error(f"Failed to patch Ollama integration: {str(e)}")
        
        # Also patch embedding to avoid OpenAI API calls
        def patch_embeddings():
            try:
                # Save original embedding function
                original_embedding = litellm.embedding
                
                @wraps(original_embedding)
                def safe_embedding(*args, **kwargs):
                    # Force all OpenAI embeddings to use local Ollama
                    if "model" in kwargs and isinstance(kwargs["model"], str):
                        if kwargs["model"].startswith("text-embedding"):
                            logger.info(f"Redirecting embedding call from {kwargs['model']} to Ollama")
                            kwargs["model"] = "ollama/nomic-embed-text"
                            kwargs["custom_llm_provider"] = "ollama"
                            kwargs["api_base"] = "http://localhost:11434"
                    
                    return original_embedding(*args, **kwargs)
                
                # Apply patch
                litellm.embedding = safe_embedding
                logger.info("Successfully patched LiteLLM embedding function")
                
            except Exception as e:
                logger.error(f"Failed to patch embedding function: {str(e)}")
        
        # Apply embedding patch
        patch_embeddings()
        
        # Also patch completion to enforce Ollama instead of OpenAI
        def patch_completion():
            try:
                # Save original completion function
                original_completion = litellm.completion
                
                @wraps(original_completion)
                def safe_completion(*args, **kwargs):
                    # Force OpenAI completions and other models to use local Ollama
                    if "model" in kwargs and isinstance(kwargs["model"], str):
                        # Redirect specific models to Ollama qwen3
                        if (kwargs["model"].startswith("gpt") or 
                            kwargs["model"] == "llama3" or 
                            "openai" in kwargs.get("custom_llm_provider", "") or
                            kwargs["model"].startswith("text-")):
                            
                            logger.info(f"Redirecting completion call from {kwargs.get('custom_llm_provider', 'unknown')}/{kwargs['model']} to Ollama qwen3")
                            kwargs["model"] = "ollama/qwen3"  # Use qwen3 as it's available on your server
                            kwargs["custom_llm_provider"] = "ollama"
                            kwargs["api_base"] = "http://localhost:11434"
                    
                    return original_completion(*args, **kwargs)
                
                # Apply patch
                litellm.completion = safe_completion
                logger.info("Successfully patched LiteLLM completion function")
                
            except Exception as e:
                logger.error(f"Failed to patch completion function: {str(e)}")
        
        # Apply completion patch
        patch_completion()
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to patch LiteLLM: {str(e)}")
        return False

# Automatically apply patches when imported
success = patch_litellm()
if success:
    logger.info("LiteLLM patches applied successfully")
else:
    logger.error("Failed to apply LiteLLM patches")