# AI Agent with File I/O

An intelligent AI agent powered by Google Gemini that can read, write, and manage files using MinIO (S3-compatible) storage.

## 🌟 Features

- 🤖 **AI-Powered Agent**: Uses Google Gemini 1.5 Flash for natural language understanding
- 📁 **File Operations**: Read, write, and list files through natural language commands
- 🗄️ **S3-Compatible Storage**: MinIO for reliable, scalable file storage
- 🔧 **Function Calling**: AI automatically uses tools to complete tasks
- 💬 **Interactive Chat**: Chat interface for seamless interaction

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

# Interactive mode
python test_agent_interactive.py
```

## 📋 Usage Examples

### Interactive Chat
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
│   ├── file_tools.py         # File operation tools
│   └── storage_service.py    # MinIO integration
├── config/
│   └── settings.py           # Configuration management
├── docker-compose.yml        # MinIO setup
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── test_storage.py          # Storage tests
├── test_agent.py            # Agent tests
└── test_agent_interactive.py # Interactive chat
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

### MinIO Ports

- **API**: http://localhost:9002
- **Console**: http://localhost:9003
  - Username: `minioadmin`
  - Password: `minioadmin123`

## 🧪 Testing
```bash
# Test storage service
python test_storage.py

# Test AI agent
python test_agent.py

# Interactive mode
python test_agent_interactive.py
```

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
