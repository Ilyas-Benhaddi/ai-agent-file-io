#!/bin/bash
# Start the AI Agent Web Server

echo "🚀 Starting AI Agent Web Server..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env from .env.example and add your GOOGLE_API_KEY"
    echo ""
    echo "  cp .env.example .env"
    echo "  # Edit .env and add your API key"
    echo ""
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

echo "✅ Starting web server on http://localhost:8000"
echo ""
echo "📊 Dashboard: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start the server
python src/api.py
