"""
AI Agent Module
Integrates Google Gemini with file tools
"""
import google.generativeai as genai
from typing import Dict, Any, List
import json
import logging

from src.file_tools import FileTools, READ_FILE_TOOL, WRITE_FILE_TOOL, LIST_FILES_TOOL
from src.storage_service import StorageService
from config.settings import Settings

logger = logging.getLogger(__name__)


class Agent:
    """AI Agent with file I/O capabilities"""
    
    def __init__(self, settings: Settings, storage_service: StorageService):
        """
        Initialize the AI agent
        
        Args:
            settings: Application settings
            storage_service: Storage service instance
        """
        self.settings = settings
        self.storage = storage_service
        self.file_tools = FileTools(storage_service)
        
        # Configure Google AI
        genai.configure(api_key=settings.google_api_key)
        
        # Initialize model with tools
        self.model = genai.GenerativeModel(
            model_name=settings.agent_model,
            tools=[READ_FILE_TOOL, WRITE_FILE_TOOL, LIST_FILES_TOOL]
        )
        
        logger.info(f"✅ Agent initialized with model: {settings.agent_model}")
    
    def chat(self, message: str) -> str:
        """
        Process a user message and return response
        
        Args:
            message: User's message
            
        Returns:
            str: Agent's response
        """
        logger.info(f"💬 User: {message}")
        
        try:
            # Start chat session
            chat = self.model.start_chat(enable_automatic_function_calling=True)
            
            # Send message
            response = chat.send_message(message)
            
            # Execute any tool calls
            while response.candidates[0].content.parts:
                part = response.candidates[0].content.parts[0]
                
                # Check if this is a function call
                if hasattr(part, 'function_call'):
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = dict(function_call.args)
                    
                    logger.info(f"🔧 Calling tool: {function_name}")
                    logger.info(f"   Args: {function_args}")
                    
                    # Execute the tool
                    result = self._execute_tool(function_name, function_args)
                    
                    # Send result back to model
                    response = chat.send_message({
                        "function_response": {
                            "name": function_name,
                            "response": result
                        }
                    })
                else:
                    # Regular text response
                    break
            
            # Get final text response
            final_response = response.text
            logger.info(f"🤖 Agent: {final_response[:100]}...")
            
            return final_response
            
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return f"I encountered an error: {error_msg}"
    
    def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool function
        
        Args:
            tool_name: Name of the tool to execute
            args: Arguments for the tool
            
        Returns:
            dict: Tool execution result
        """
        try:
            if tool_name == "read_file":
                return self.file_tools.read_file(args["filename"])
            
            elif tool_name == "write_file":
                return self.file_tools.write_file(
                    args["filename"],
                    args["content"]
                )
            
            elif tool_name == "list_files":
                return self.file_tools.list_files()
            
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}"
                }
                
        except Exception as e:
            logger.error(f"❌ Error executing tool {tool_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
