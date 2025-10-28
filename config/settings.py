"""
Configuration Module
Loads and validates environment variables
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Settings:
    """Application settings loaded from environment"""
    
    # Google AI
    google_api_key: str
    agent_model: str = "gemini-1.5-flash-latest"
    
    # MinIO Storage
    minio_endpoint: str = "localhost:9002"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin123"
    minio_bucket_name: str = "agent-files"
    minio_secure: bool = False
    
    # Agent Config
    max_file_size_mb: int = 10
    
    def __post_init__(self):
        """Validate required settings"""
        if not self.google_api_key or self.google_api_key == "your_google_ai_studio_api_key_here":
            logger.error("GOOGLE_API_KEY not set in .env file!")
            raise ValueError(
                "Please set GOOGLE_API_KEY in .env file. "
                "Get your key from: https://makersuite.google.com/app/apikey"
            )
        logger.info("✅ Configuration loaded successfully")


def load_settings() -> Settings:
    """Load settings from environment variables"""
    return Settings(
        google_api_key=os.getenv("GOOGLE_API_KEY", ""),
        agent_model=os.getenv("AGENT_MODEL", "gemini-1.5-flash-latest"),
        minio_endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9002"),
        minio_access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        minio_secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin123"),
        minio_bucket_name=os.getenv("MINIO_BUCKET_NAME", "agent-files"),
        minio_secure=os.getenv("MINIO_SECURE", "False").lower() == "true",
        max_file_size_mb=int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    )
