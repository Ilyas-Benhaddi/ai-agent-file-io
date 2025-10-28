"""
Interactive AI Agent Test
Chat with the AI agent in real-time
"""
import sys
sys.path.append('.')

from src.agent import Agent
from src.storage_service import StorageService
from config.settings import load_settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run interactive agent chat"""

    print("=" * 60)
    print("🤖 AI Agent - Interactive Chat Mode")
    print("=" * 60)
    print()

    # Load settings
    print("📋 Loading configuration...")
    try:
        settings = load_settings()
        print("✅ Configuration loaded\n")
    except ValueError as e:
        print(f"❌ {e}")
        print("\n📝 Please add your GOOGLE_API_KEY to .env file")
        print("   Get your key from: https://makersuite.google.com/app/apikey\n")
        return

    # Initialize storage
    print("🗄️  Connecting to storage...")
    try:
        storage = StorageService(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            bucket_name=settings.minio_bucket_name,
            secure=settings.minio_secure
        )
        print("✅ Storage connected\n")
    except Exception as e:
        print(f"❌ Error connecting to storage: {e}")
        print("\n💡 Make sure MinIO is running:")
        print("   docker-compose up -d\n")
        return

    # Initialize agent
    print("🤖 Initializing AI agent...")
    try:
        agent = Agent(settings, storage)
        print("✅ Agent ready!\n")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}\n")
        return

    # Interactive loop
    print("=" * 60)
    print("💬 Chat with the agent (type 'exit' or 'quit' to end)")
    print("=" * 60)
    print()
    print("Examples:")
    print("  - Create a file called notes.txt with my shopping list")
    print("  - Read the notes.txt file")
    print("  - What files do I have?")
    print("  - Write a report about AI trends to report.txt")
    print()

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("\n👋 Goodbye! Thanks for chatting!\n")
                break

            # Process with agent
            print()
            response = agent.chat(user_input)
            print(f"\n🤖 Agent: {response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for chatting!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            continue


if __name__ == "__main__":
    main()
