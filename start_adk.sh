#!/bin/bash
# Start ADK API Server for Agent Visualization

echo "🤖 Starting Google ADK API Server..."
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
echo "🚀 Starting ADK API Server..."
echo "   Agent File: adk_agent.py"
echo "   API Server: http://localhost:8000"
echo "   CORS: http://localhost:4200"
echo ""
echo "📝 Next steps:"
echo "   1. Keep this terminal running"
echo "   2. In another terminal, start ADK Web:"
echo "      cd /path/to/adk-web"
echo "      npm run serve -- --backend=http://localhost:8000"
echo "   3. Open browser: http://localhost:4200"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start ADK API server
adk api_server \
    --agent_file=adk_agent.py \
    --allow_origins=http://localhost:4200 \
    --host=0.0.0.0 \
    --port=8000
