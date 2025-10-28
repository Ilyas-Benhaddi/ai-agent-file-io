"""
ADK-Compatible Agent
AI Agent integrated with Google Agent Development Kit
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from src.storage_service import StorageService
from config.settings import load_settings
from typing import Dict, Any

# Initialize storage service globally
settings = load_settings()
storage = StorageService(
    endpoint=settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    bucket_name=settings.minio_bucket_name,
    secure=settings.minio_secure
)


def read_file(filename: str) -> Dict[str, Any]:
    """
    Read a file from storage

    Args:
        filename: Name of the file to read (e.g., 'document.txt', 'data.csv')

    Returns:
        dict: Result with file content or error
    """
    try:
        file_data = storage.download_file(filename)

        if file_data is None:
            return {
                "success": False,
                "error": f"File '{filename}' not found"
            }

        try:
            content = file_data.decode('utf-8')
        except UnicodeDecodeError:
            content = f"[Binary file, {len(file_data)} bytes]"

        return {
            "success": True,
            "filename": filename,
            "content": content,
            "size": len(file_data)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def write_file(filename: str, content: str) -> Dict[str, Any]:
    """
    Write a file to storage

    Args:
        filename: Name for the new file (e.g., 'report.txt', 'summary.json')
        content: Content to write to the file

    Returns:
        dict: Result with file info or error
    """
    try:
        file_data = content.encode('utf-8')

        content_type = "text/plain"
        if filename.endswith('.json'):
            content_type = "application/json"
        elif filename.endswith('.html'):
            content_type = "text/html"
        elif filename.endswith('.csv'):
            content_type = "text/csv"

        result = storage.upload_file(
            file_data=file_data,
            object_name=filename,
            content_type=content_type
        )

        if result["success"]:
            return {
                "success": True,
                "filename": filename,
                "size": result["size"],
                "s3_key": result["s3_key"]
            }
        else:
            return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def list_files() -> Dict[str, Any]:
    """
    List all files currently in storage

    Returns:
        dict: List of files or error
    """
    try:
        files = storage.list_files()
        return {
            "success": True,
            "files": files,
            "count": len(files)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Create the ADK agent with file tools
file_agent = LlmAgent(
    name="file_io_agent",
    model="gemini-1.5-flash",
    description="An AI agent that can read, write, and manage files using MinIO storage. "
                "I can help you create files, read file contents, and list all available files.",
    instruction="""You are a helpful AI assistant with file I/O capabilities.

You have access to three tools:
1. read_file(filename) - Read the contents of a file
2. write_file(filename, content) - Create or write a new file
3. list_files() - List all files in storage

When users ask you to:
- Create, write, or save a file -> use write_file()
- Read, view, or check a file -> use read_file()
- List, show, or check what files exist -> use list_files()

Always be helpful and execute the file operations as requested.
After writing a file, confirm what you created.
When listing files, present them in a user-friendly format.""",
    tools=[read_file, write_file, list_files]
)


# Export for ADK to discover
root_agent = file_agent


if __name__ == "__main__":
    print("✅ ADK Agent initialized!")
    print(f"   Name: {file_agent.name}")
    print(f"   Model: {file_agent.model}")
    print(f"   Tools: {len(file_agent.tools)}")
    print("\nTo run with ADK web:")
    print("   adk api_server --allow_origins=http://localhost:4200 --host=0.0.0.0")
