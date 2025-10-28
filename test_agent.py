"""
Test script for AI Agent
Tests agent with file operations
"""
import sys
sys.path.append('.')

from src.agent import Agent
from src.storage_service import StorageService
from config.settings import load_settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_agent():
    """Test the AI agent with various prompts"""
    
    print("🤖 Testing AI Agent...\n")
    
    # Load settings
    print("1️⃣ Loading configuration...")
    try:
        settings = load_settings()
        print("✅ Configuration loaded\n")
    except ValueError as e:
        print(f"❌ {e}")
        print("\n📝 Please add your GOOGLE_API_KEY to .env file")
        print("   Get your key from: https://makersuite.google.com/app/apikey\n")
        return
    
    # Initialize storage
    print("2️⃣ Connecting to storage...")
    storage = StorageService(
        endpoint=settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        bucket_name=settings.minio_bucket_name,
        secure=settings.minio_secure
    )
    print("✅ Storage connected\n")
    
    # Initialize agent
    print("3️⃣ Initializing AI agent...")
    agent = Agent(settings, storage)
    print("✅ Agent ready\n")
    
    # Test 1: Create a file
    print("=" * 50)
    print("TEST 1: Ask agent to create a file")
    print("=" * 50)
    response = agent.chat(
        "Create a file called 'greeting.txt' with the content: 'Hello from the AI agent! This is a test file created by AI.'"
    )
    print(f"\n🤖 Agent response:\n{response}\n")
    
    # Test 2: Read the file
    print("=" * 50)
    print("TEST 2: Ask agent to read the file")
    print("=" * 50)
    response = agent.chat("Read the greeting.txt file and tell me what it says")
    print(f"\n🤖 Agent response:\n{response}\n")
    
    # Test 3: List files
    print("=" * 50)
    print("TEST 3: Ask agent to list files")
    print("=" * 50)
    response = agent.chat("What files do we have in storage?")
    print(f"\n🤖 Agent response:\n{response}\n")
    
    # Test 4: Create a more complex file
    print("=" * 50)
    print("TEST 4: Create a report")
    print("=" * 50)
    response = agent.chat(
        "Create a file called 'report.txt' with a brief report about the weather today. "
        "Make it sound professional."
    )
    print(f"\n🤖 Agent response:\n{response}\n")
    
    print("=" * 50)
    print("🎉 All agent tests completed!")
    print("=" * 50)
    print("\n💡 Try interactive mode next: python test_agent_interactive.py")


if __name__ == "__main__":
    test_agent()
