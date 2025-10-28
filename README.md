# AI Agent with File I/O

An intelligent AI agent powered by Google Gemini that can read, write, and manage files using MinIO (S3-compatible) storage.

## 🌟 Features

- 🤖 **AI-Powered Agent**: Uses Google Gemini 1.5 Flash for natural language understanding
- 📁 **File Operations**: Read, write, and list files through natural language commands
- 🗄️ **S3-Compatible Storage**: MinIO for reliable, scalable file storage
- 🔧 **Function Calling**: AI automatically uses tools to complete tasks
- 💬 **Interactive Chat**: Chat interface for seamless interaction
- 🌐 **Web Dashboard**: Beautiful web interface for agent interaction and file management
- 🎨 **Real-Time UI**: Live updates and modern, responsive design
- 🚀 **Google ADK Integration**: Visualize your agent with Google's official Agent Development Kit Web UI

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Google AI Studio API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd agent_project
```

2. **Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

5. **Start MinIO**
```bash
docker-compose up -d
```

6. **Test the setup**
```bash
# Test storage
python test_storage.py

# Test agent
python test_agent.py

# Interactive mode (CLI)
python test_agent_interactive.py

# Web interface
python src/api.py
# Then open http://localhost:8000 in your browser

# Google ADK Web (Recommended for visualization!)
./start_adk.sh
# See ADK_SETUP.md for complete instructions
```

## 📋 Usage Examples

### 🚀 Google ADK Web (Official Visualization - Recommended!)

The best way to visualize and debug your agent is using Google's official Agent Development Kit Web UI.

**Super simple - just one command!**

```bash
# 1. Install ADK
pip install google-adk

# 2. Start MinIO
docker-compose up -d

# 3. Start ADK Web (all-in-one!)
./start_adk.sh
# Or: adk web --port 8000 adk_agent

# 4. Open http://localhost:8000
# 5. Select 'file_io_agent' from dropdown (upper right)
# 6. Start chatting!
```

**See [ADK_SETUP.md](ADK_SETUP.md) for complete setup instructions.**

ADK Web Features:
- 📊 **Visual Agent Dashboard** - See agent configuration and status
- 💬 **Interactive Chat** - Talk with your agent in real-time
- 🔧 **Tool Execution View** - Watch tools being called
- 📈 **Execution Traces** - Debug every step
- 📝 **Session History** - Save and replay conversations
- ✨ **All-in-One** - No need to clone separate repos!

### 🌐 Web Dashboard (Custom UI)

Start the web server:
```bash
python src/api.py
# Or with uvicorn directly:
# uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

Then open your browser to: **http://localhost:8000**

Features:
- 💬 **Real-time chat** with the AI agent
- 📁 **File browser** with view/delete operations
- 📊 **Storage statistics** (file count, total size)
- 🎨 **Beautiful dark-themed UI** with smooth animations
- 📱 **Responsive design** works on mobile and desktop

### Interactive CLI Chat
```bash
python test_agent_interactive.py
```

Example conversations:
```
You: Create a file called notes.txt with my shopping list: milk, eggs, bread
Agent: I've created notes.txt with your shopping list!

You: Read the notes.txt file
Agent: The file contains: milk, eggs, bread

You: What files do I have?
Agent: You have 1 file: notes.txt
```

### Programmatic Usage
```python
from src.agent import Agent
from src.storage_service import StorageService
from config.settings import load_settings

# Initialize
settings = load_settings()
storage = StorageService(
    endpoint=settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    bucket_name=settings.minio_bucket_name
)
agent = Agent(settings, storage)

# Chat with the agent
response = agent.chat("Create a report about project status")
print(response)
```

## 🏗️ Architecture
```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ↓
┌─────────────────────────────────┐
│     AI Agent (Gemini 1.5)       │
│  ┌──────────────────────────┐   │
│  │  File Tools              │   │
│  │  - read_file()           │   │
│  │  - write_file()          │   │
│  │  - list_files()          │   │
│  └──────────┬───────────────┘   │
└─────────────┼───────────────────┘
              │
              ↓
┌─────────────────────────────────┐
│   Storage Service (MinIO)       │
│   - S3-compatible API           │
│   - Docker containerized        │
└─────────────────────────────────┘
```

## 📁 Project Structure
```
agent_project/
├── src/
│   ├── agent.py              # AI agent core
│   ├── api.py                # FastAPI web server
│   ├── file_tools.py         # File operation tools
│   └── storage_service.py    # MinIO integration
├── static/
│   ├── index.html            # Web dashboard UI
│   ├── style.css             # Dashboard styling
│   └── app.js                # Frontend JavaScript
├── config/
│   └── settings.py           # Configuration management
├── docker-compose.yml        # MinIO setup
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── test_storage.py          # Storage tests
├── test_agent.py            # Agent tests
└── test_agent_interactive.py # Interactive CLI chat
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google AI Studio API key | Required |
| `AGENT_MODEL` | Gemini model to use | gemini-1.5-flash-latest |
| `MINIO_ENDPOINT` | MinIO server endpoint | localhost:9002 |
| `MINIO_ACCESS_KEY` | MinIO access key | minioadmin |
| `MINIO_SECRET_KEY` | MinIO secret key | minioadmin123 |
| `MINIO_BUCKET_NAME` | Storage bucket name | agent-files |

### Ports

**Web Dashboard:**
- **Dashboard**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

**MinIO:**
- **API**: http://localhost:9002
- **Console**: http://localhost:9003
  - Username: `minioadmin`
  - Password: `minioadmin123`

## 🧪 Testing

### Automated Tests
```bash
# Test storage service
python test_storage.py

# Test AI agent
python test_agent.py
```

### Interactive Testing
```bash
# CLI mode
python test_agent_interactive.py

# Web interface (Best experience!)
python src/api.py
# Open http://localhost:8000
```

### API Testing
```bash
# Start the server
python src/api.py

# Test endpoints with curl
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a file called test.txt with hello world"}'
curl http://localhost:8000/api/files
```

## 🔌 API Reference

The web server provides a REST API for programmatic access:

### Endpoints

**POST /api/chat**
- Chat with the AI agent
- Body: `{"message": "your message"}`
- Response: `{"response": "agent response", "success": true}`

**GET /api/files**
- List all files in storage
- Response: `{"files": [...], "count": N, "success": true}`

**GET /api/files/{filename}**
- Read a specific file
- Response: `{"filename": "...", "content": "...", "size": N, "success": true}`

**DELETE /api/files/{filename}**
- Delete a file
- Response: `{"success": true, "message": "..."}`

**GET /health**
- Health check
- Response: `{"status": "healthy", "agent_initialized": true, "storage_initialized": true}`

**Interactive API Documentation**: http://localhost:8000/docs

## 🛠️ Development

### Adding New Tools

1. Create tool function in `src/file_tools.py`
2. Define tool schema
3. Add to agent's tool list in `src/agent.py`
4. Implement tool execution in `agent._execute_tool()`

### Extending the Agent

The agent can be extended with additional capabilities:
- Image analysis
- Code generation
- Data analysis
- Web scraping
- And more!

## 📝 License

MIT License - feel free to use this project for learning and development!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🆘 Troubleshooting

### MinIO won't start
```bash
# Check if ports are in use
lsof -i :9002
lsof -i :9003

# View logs
docker-compose logs minio
```

### Agent errors
- Ensure `GOOGLE_API_KEY` is set in `.env`
- Check MinIO is running: `docker ps`
- Verify model name is correct: `gemini-1.5-flash-latest`

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 📚 Resources

- [Google AI Studio](https://makersuite.google.com/)
- [MinIO Documentation](https://min.io/docs/minio/linux/index.html)
- [Gemini API Docs](https://ai.google.dev/docs)

## ✨ Acknowledgments

Built with:
- Google Gemini AI
- MinIO Object Storage
- Python 3.13
- Docker

---

**Ready to build intelligent file-based applications!** 🚀
