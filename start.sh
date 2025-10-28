#!/bin/bash

echo "🚀 Agent Project - Quick Start"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "❗ IMPORTANT: Edit .env and add your GOOGLE_API_KEY"
    echo "   Get your key from: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Press Enter after you've added your API key..."
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start MinIO
echo "🐳 Starting MinIO with Docker Compose..."
docker-compose up -d

# Wait for MinIO to be ready
echo "⏳ Waiting for MinIO to be ready..."
sleep 5

# Check if MinIO is running
if docker ps | grep -q agent_minio; then
    echo "✅ MinIO is running!"
    echo ""
    echo "📊 MinIO Console: http://localhost:9001"
    echo "   Username: minioadmin"
    echo "   Password: minioadmin123"
    echo ""
else
    echo "❌ MinIO failed to start. Check: docker-compose logs"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt --break-system-packages 2>/dev/null || pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🧪 Test the storage service:"
echo "   python test_storage.py"
echo ""
echo "📖 Next steps:"
echo "   1. Test MinIO: python test_storage.py"
echo "   2. Open MinIO Console: http://localhost:9001"
echo "   3. Ready for Step 2: Building the Agent!"
echo ""
