# 🚀 Google ADK Web Setup Guide

This guide will help you visualize your AI agent using **Google's Agent Development Kit (ADK) Web** - the official visualization tool for AI agents.

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ Python 3.9+
- ✅ Node.js and npm (for ADK web UI)
- ✅ Docker (for MinIO)
- ✅ Google API Key (already in `.env`)

---

## 🔧 Step 1: Install ADK Python Package

```bash
# Make sure you're in your virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Google ADK
pip install -r requirements.txt

# Verify installation
python -c "from google.adk.agents import LlmAgent; print('✅ ADK installed!')"
```

---

## 🗄️ Step 2: Start MinIO (Storage Service)

```bash
# Start MinIO in Docker
docker-compose up -d

# Verify MinIO is running
curl http://localhost:9002/minio/health/live
```

You should see MinIO running on:
- API: http://localhost:9002
- Console: http://localhost:9003

---

## 🤖 Step 3: Test the ADK Agent

Test that your agent works before launching the UI:

```bash
# Test the ADK agent
python adk_agent.py
```

You should see:
```
✅ ADK Agent initialized!
   Name: file_io_agent
   Model: gemini-1.5-flash
   Tools: 3
```

---

## 🚀 Step 4: Start ADK API Server

In one terminal, start the ADK API server:

```bash
# Navigate to your project directory
cd /path/to/agent_project

# Activate virtual environment
source .venv/bin/activate

# Start ADK API server
adk api_server \
    --agent_file=adk_agent.py \
    --allow_origins=http://localhost:4200 \
    --host=0.0.0.0 \
    --port=8000
```

**Important Notes:**
- The `--agent_file` points to your ADK agent file
- The `--allow_origins` enables CORS for the web UI
- Keep this terminal running!

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🌐 Step 5: Install and Run ADK Web UI

In a **NEW terminal** (keep the API server running):

```bash
# Clone ADK web repository
git clone https://github.com/google/adk-web.git
cd adk-web

# Install dependencies (first time only)
npm install

# Start the web UI
npm run serve -- --backend=http://localhost:8000
```

**Note:** This may take a few minutes the first time.

You should see:
```
** Angular Live Development Server is listening on localhost:4200 **
✔ Compiled successfully.
```

---

## 🎉 Step 6: Access ADK Web

Open your browser to: **http://localhost:4200**

You'll see the Google ADK Web interface with:
- 📊 **Agent Dashboard** - View agent information
- 💬 **Chat Interface** - Interact with your agent
- 🔧 **Tool Execution View** - See when tools are called
- 📈 **Execution Traces** - Debug agent behavior
- 📝 **Session History** - Review past interactions

---

## 🎯 Using Your Agent in ADK Web

Once the UI loads:

1. **Select Agent**: Choose `file_io_agent` from the dropdown
2. **Start Chatting**: Type messages like:
   - "Create a file called notes.txt with my shopping list"
   - "Read the notes.txt file"
   - "What files do I have?"
   - "Write a report about AI trends to report.txt"

3. **Watch Tool Execution**:
   - See when your agent calls `read_file()`, `write_file()`, or `list_files()`
   - View the responses in real-time
   - Debug any issues with the trace viewer

---

## 📁 What Just Happened?

Your setup now has **3 running services**:

| Service | Port | Purpose |
|---------|------|---------|
| **MinIO** | 9002/9003 | File storage backend |
| **ADK API** | 8000 | Agent runtime server |
| **ADK Web** | 4200 | Visualization UI |

```
┌─────────────┐
│   Browser   │ http://localhost:4200
│  (ADK Web)  │
└──────┬──────┘
       │
       ↓
┌─────────────────┐
│  ADK API Server │ http://localhost:8000
│  (Python Agent) │
└──────┬──────────┘
       │
       ↓
┌─────────────────┐
│  MinIO Storage  │ http://localhost:9002
│   (S3-compatible)│
└─────────────────┘
```

---

## 🛠️ Troubleshooting

### "adk: command not found"
```bash
# Reinstall ADK
pip install --upgrade google-adk

# Or use python -m
python -m google.adk.cli.main api_server --agent_file=adk_agent.py
```

### "ModuleNotFoundError: No module named 'google.adk'"
```bash
# Make sure virtual environment is activated
source .venv/bin/activate
pip install google-adk
```

### "CORS error" in browser
Make sure you started the API server with:
```bash
--allow_origins=http://localhost:4200
```

### MinIO not connecting
```bash
# Check MinIO is running
docker ps | grep minio

# Restart if needed
docker-compose restart
```

### Port 8000 or 4200 already in use
```bash
# For API server, use different port:
adk api_server --agent_file=adk_agent.py --port=8001

# For web UI, change in adk-web/.angular.json or use different backend
```

---

## 🎨 ADK Web Features You Can Use

### 1. **Chat Interface**
- Natural conversation with your agent
- See tool calls in real-time
- View formatted responses

### 2. **Execution Trace**
- Step-by-step execution view
- See LLM prompts and responses
- Debug tool calls and errors

### 3. **Session Management**
- Save conversation sessions
- Load previous sessions
- Compare different runs

### 4. **Agent Configuration**
- View agent settings
- See available tools
- Check model configuration

---

## 📚 Additional Commands

### Stop Services
```bash
# Stop MinIO
docker-compose down

# Stop ADK API (Ctrl+C in that terminal)

# Stop ADK Web (Ctrl+C in that terminal)
```

### Clean Restart
```bash
# Restart everything
docker-compose restart
# Then restart ADK API and Web
```

### Update ADK
```bash
pip install --upgrade google-adk
```

---

## 🎯 Quick Start Commands

### Terminal 1: MinIO
```bash
docker-compose up -d
```

### Terminal 2: ADK API
```bash
source .venv/bin/activate
adk api_server --agent_file=adk_agent.py --allow_origins=http://localhost:4200 --host=0.0.0.0
```

### Terminal 3: ADK Web
```bash
cd ../adk-web  # Navigate to adk-web repo
npm run serve -- --backend=http://localhost:8000
```

### Browser
```
http://localhost:4200
```

---

## 🌟 Benefits of Using ADK Web

✅ **Official Google Tool** - Built by the Gemini team
✅ **Rich Visualization** - See exactly what your agent is doing
✅ **Debugging Tools** - Trace every step of agent execution
✅ **Session Management** - Save and replay interactions
✅ **Multi-Agent Support** - Visualize agent hierarchies
✅ **Real-Time Updates** - Watch your agent work live

---

## 📖 Learn More

- [ADK Python Docs](https://github.com/google/adk-python)
- [ADK Web Docs](https://github.com/google/adk-web)
- [Official ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Codelabs](https://codelabs.developers.google.com/your-first-agent-with-adk)

---

**Ready to visualize your agent?** Follow the steps above and enjoy the official Google ADK experience! 🚀
