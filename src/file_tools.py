"""
File Tools for AI Agent
Provides read and write capabilities
"""
import json
from typing import Dict, Any
from src.storage_service import StorageService
import logging

logger = logging.getLogger(__name__)


class FileTools:
    """Tools for file operations that the agent can use"""
    
    def __init__(self, storage_service: StorageService):
        self.storage = storage_service
    
    def read_file(self, filename: str) -> Dict[str, Any]:
        """
        Read a file from storage
        
        Args:
            filename: Name of the file to read
            
        Returns:
            dict: Result with file content or error
        """
        logger.info(f"🔍 Reading file: {filename}")
        
        try:
            # Download file from storage
            file_data = self.storage.download_file(filename)
            
            if file_data is None:
                return {
                    "success": False,
                    "error": f"File '{filename}' not found"
                }
            
            # Try to decode as text
            try:
                content = file_data.decode('utf-8')
            except UnicodeDecodeError:
                content = f"[Binary file, {len(file_data)} bytes]"
            
            logger.info(f"✅ Successfully read file: {filename}")
            return {
                "success": True,
                "filename": filename,
                "content": content,
                "size": len(file_data)
            }
            
        except Exception as e:
            logger.error(f"❌ Error reading file: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def write_file(self, filename: str, content: str) -> Dict[str, Any]:
        """
        Write a file to storage
        
        Args:
            filename: Name for the new file
            content: Content to write
            
        Returns:
            dict: Result with file info or error
        """
        logger.info(f"✍️  Writing file: {filename}")
        
        try:
            # Convert content to bytes
            file_data = content.encode('utf-8')
            
            # Determine content type
            content_type = "text/plain"
            if filename.endswith('.json'):
                content_type = "application/json"
            elif filename.endswith('.html'):
                content_type = "text/html"
            elif filename.endswith('.csv'):
                content_type = "text/csv"
            
            # Upload to storage
            result = self.storage.upload_file(
                file_data=file_data,
                object_name=filename,
                content_type=content_type
            )
            
            if result["success"]:
                logger.info(f"✅ Successfully wrote file: {filename}")
                return {
                    "success": True,
                    "filename": filename,
                    "size": result["size"],
                    "s3_key": result["s3_key"]
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"❌ Error writing file: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_files(self) -> Dict[str, Any]:
        """
        List all files in storage
        
        Returns:
            dict: List of files or error
        """
        logger.info("📋 Listing files")
        
        try:
            files = self.storage.list_files()
            logger.info(f"✅ Found {len(files)} file(s)")
            return {
                "success": True,
                "files": files,
                "count": len(files)
            }
        except Exception as e:
            logger.error(f"❌ Error listing files: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Tool definitions for Google Gemini function calling
READ_FILE_TOOL = {
    "name": "read_file",
    "description": "Read the contents of a file from storage. Use this when the user asks to read, view, or analyze a file.",
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The name of the file to read (e.g., 'document.txt', 'data.csv')"
            }
        },
        "required": ["filename"]
    }
}

WRITE_FILE_TOOL = {
    "name": "write_file",
    "description": "Write content to a new file in storage. Use this when the user asks to create, generate, or save a file.",
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The name for the new file (e.g., 'report.txt', 'summary.json')"
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file"
            }
        },
        "required": ["filename", "content"]
    }
}

LIST_FILES_TOOL = {
    "name": "list_files",
    "description": "List all files currently in storage. Use this when the user asks what files are available.",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}
