"""
FastAPI Web Server for AI Agent
Provides REST API and web interface
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
import logging
import os

from src.agent import Agent
from src.storage_service import StorageService
from config.settings import load_settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Agent with File I/O",
    description="Intelligent AI agent with file operations powered by Google Gemini",
    version="1.0.0"
)

# Global variables for agent and storage
agent: Optional[Agent] = None
storage: Optional[StorageService] = None


# Request/Response Models
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None


class FileInfo(BaseModel):
    name: str
    size: Optional[int] = None
    last_modified: Optional[str] = None


class FileListResponse(BaseModel):
    files: list[FileInfo]
    count: int
    success: bool
    error: Optional[str] = None


class FileContentResponse(BaseModel):
    filename: str
    content: str
    size: int
    success: bool
    error: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize agent and storage on startup"""
    global agent, storage

    try:
        logger.info("🚀 Starting AI Agent Web Server...")

        # Load settings
        settings = load_settings()
        logger.info("✅ Configuration loaded")

        # Initialize storage
        storage = StorageService(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            bucket_name=settings.minio_bucket_name,
            secure=settings.minio_secure
        )
        logger.info("✅ Storage connected")

        # Initialize agent
        agent = Agent(settings, storage)
        logger.info("✅ Agent initialized")

        logger.info("🎉 Web server ready!")

    except Exception as e:
        logger.error(f"❌ Failed to initialize: {e}")
        raise


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main web interface"""
    static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "index.html")
    if os.path.exists(static_path):
        return FileResponse(static_path)
    return """
    <html>
        <head><title>AI Agent</title></head>
        <body>
            <h1>AI Agent Server Running</h1>
            <p>API Documentation: <a href="/docs">/docs</a></p>
        </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_initialized": agent is not None,
        "storage_initialized": storage is not None
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the AI agent

    Example:
    ```json
    {
        "message": "Create a file called hello.txt with 'Hello World'"
    }
    ```
    """
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:
        logger.info(f"💬 Chat request: {request.message}")
        response = agent.chat(request.message)

        return ChatResponse(
            response=response,
            success=True
        )
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        return ChatResponse(
            response="",
            success=False,
            error=str(e)
        )


@app.get("/api/files", response_model=FileListResponse)
async def list_files():
    """
    List all files in storage
    """
    if not storage:
        raise HTTPException(status_code=503, detail="Storage not initialized")

    try:
        files = storage.list_files()

        # Get metadata for each file
        file_info_list = []
        for filename in files:
            metadata = storage.get_file_metadata(filename)
            if metadata:
                file_info_list.append(FileInfo(
                    name=metadata["name"],
                    size=metadata["size"],
                    last_modified=str(metadata["last_modified"])
                ))
            else:
                file_info_list.append(FileInfo(name=filename))

        return FileListResponse(
            files=file_info_list,
            count=len(file_info_list),
            success=True
        )
    except Exception as e:
        logger.error(f"❌ Error listing files: {e}")
        return FileListResponse(
            files=[],
            count=0,
            success=False,
            error=str(e)
        )


@app.get("/api/files/{filename}", response_model=FileContentResponse)
async def read_file(filename: str):
    """
    Read a specific file from storage
    """
    if not storage:
        raise HTTPException(status_code=503, detail="Storage not initialized")

    try:
        file_data = storage.download_file(filename)

        if file_data is None:
            raise HTTPException(status_code=404, detail=f"File '{filename}' not found")

        # Try to decode as text
        try:
            content = file_data.decode('utf-8')
        except UnicodeDecodeError:
            content = f"[Binary file, {len(file_data)} bytes]"

        return FileContentResponse(
            filename=filename,
            content=content,
            size=len(file_data),
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error reading file: {e}")
        return FileContentResponse(
            filename=filename,
            content="",
            size=0,
            success=False,
            error=str(e)
        )


@app.delete("/api/files/{filename}")
async def delete_file(filename: str):
    """
    Delete a file from storage
    """
    if not storage:
        raise HTTPException(status_code=503, detail="Storage not initialized")

    try:
        success = storage.delete_file(filename)

        if not success:
            raise HTTPException(status_code=404, detail=f"Failed to delete '{filename}'")

        return {
            "success": True,
            "message": f"File '{filename}' deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Mount static files (CSS, JS, images)
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
