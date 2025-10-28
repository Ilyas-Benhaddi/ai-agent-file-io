#!/bin/bash
# Start ADK Web Interface - Simple All-in-One

echo "🚀 Starting Google ADK Web Interface..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env from .env.example and add your GOOGLE_API_KEY"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "Activate with: source .venv/bin/activate"
    echo ""
fi

# Check if MinIO is running
echo "🔍 Checking MinIO status..."
if ! curl -s http://localhost:9002/minio/health/live > /dev/null 2>&1; then
    echo "⚠️  Warning: MinIO not responding on port 9002"
    echo "Start MinIO with: docker-compose up -d"
    echo ""
fi

# Check if ADK is installed
if ! python -c "import google.adk" 2>/dev/null; then
    echo "❌ Error: google-adk not installed!"
    echo "Install with: pip install google-adk"
    exit 1
fi

echo "✅ All checks passed!"
echo ""
echo "🌐 Starting ADK Web Interface..."
echo "   Agent File: adk_agent.py"
echo "   Web Interface: http://localhost:8000"
echo ""
echo "📝 Instructions:"
echo "   1. Open browser: http://localhost:8000"
echo "   2. Select 'file_io_agent' from the dropdown (upper right)"
echo "   3. Start chatting with your agent!"
echo ""
echo "💡 Try these commands:"
echo "   - Create a file called notes.txt with my shopping list"
echo "   - What files do I have?"
echo "   - Read the notes.txt file"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start ADK web interface
# Note: adk_agent is now a directory containing the agent configuration
adk web --port 8000 adk_agent
