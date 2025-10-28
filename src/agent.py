"""
AI Agent Module
Integrates Google Gemini with file tools
"""
import google.generativeai as genai
from typing import Dict, Any, List
import json
import logging

from src.file_tools import FileTools
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

        # Create tool functions that the model can call
        def read_file(filename: str) -> str:
            """
            Read a file from storage

            Args:
                filename: Name of the file to read (e.g., 'document.txt', 'data.csv')

            Returns:
                The file content as a string
            """
            result = self.file_tools.read_file(filename)
            return json.dumps(result)

        def write_file(filename: str, content: str) -> str:
            """
            Write a file to storage

            Args:
                filename: Name for the new file (e.g., 'report.txt', 'summary.json')
                content: Content to write to the file

            Returns:
                Success message with file details
            """
            result = self.file_tools.write_file(filename, content)
            return json.dumps(result)

        def list_files() -> str:
            """
            List all files in storage

            Returns:
                List of all available files
            """
            result = self.file_tools.list_files()
            return json.dumps(result)

        # Store tool functions
        self.tool_functions = {
            'read_file': read_file,
            'write_file': write_file,
            'list_files': list_files
        }

        # Initialize model with tools
        self.model = genai.GenerativeModel(
            model_name=settings.agent_model,
            tools=[read_file, write_file, list_files]
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
            # Start chat session with automatic function calling
            # The SDK will automatically call the tool functions we provided
            chat = self.model.start_chat(enable_automatic_function_calling=True)

            # Send message - tools will be called automatically by the SDK
            response = chat.send_message(message)

            # Get final text response
            final_response = response.text
            logger.info(f"🤖 Agent: {final_response[:100]}...")

            return final_response

        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return f"I encountered an error: {error_msg}"
