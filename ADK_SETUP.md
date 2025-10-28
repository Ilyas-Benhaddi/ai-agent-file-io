# 🚀 Google ADK Web Setup Guide

This guide will help you visualize your AI agent using **Google's Agent Development Kit (ADK) Web** - the official visualization tool for AI agents.

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ Python 3.9+
- ✅ Docker (for MinIO)
- ✅ Google API Key (already in `.env`)
- ✅ Virtual environment activated

---

## 🔧 Setup (3 Simple Steps!)

### Step 1: Install ADK

```bash
# Make sure you're in your virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Google ADK
pip install -r requirements.txt

# Verify installation
python -c "from google.adk.agents import LlmAgent; print('✅ ADK installed!')"
```

### Step 2: Start MinIO (Storage Service)

```bash
# Start MinIO in Docker
docker-compose up -d

# Verify MinIO is running
curl http://localhost:9002/minio/health/live
```

You should see MinIO running on:
- API: http://localhost:9002
- Console: http://localhost:9003

### Step 3: Start ADK Web Interface

```bash
# One simple command to start everything!
./start_adk.sh

# Or manually:
adk web --port 8000 adk_agent
```

**That's it!** The web interface is now running.

---

## 🎉 Access ADK Web

Open your browser to: **http://localhost:8000**

### First Time Setup:
1. **Select Agent**: Click the dropdown in the upper right corner
2. **Choose `file_io_agent`** from the list
3. **Start Chatting!** Type your first message

---

## 💬 Try These Commands

Once the interface loads, try:

```
You: Create a file called notes.txt with my shopping list: milk, eggs, bread
Agent: [Creates the file and confirms]

You: What files do I have?
Agent: [Lists all files in storage]

You: Read the notes.txt file
Agent: [Shows file content]

You: Write a report about AI trends to report.txt
Agent: [Generates and saves the report]
```

---

## 🎨 ADK Web Interface Features

### What You'll See:

**Chat Interface:**
- 💬 Natural conversation with your agent
- 🔧 Real-time tool execution visualization
- 📊 Function call traces
- 📝 Full conversation history

**Agent Dashboard:**
- ⚙️ Agent configuration and settings
- 🛠️ Available tools display
- 📈 Execution statistics
- 🔍 Debug mode for troubleshooting

**Tool Execution View:**
- Watch when `read_file()` is called
- See `write_file()` parameters
- Monitor `list_files()` results
- Debug any errors in real-time

---

## 📁 What Just Happened?

Your setup now has **2 running services**:

| Service | Port | Purpose |
|---------|------|---------|
| **MinIO** | 9002/9003 | File storage backend |
| **ADK Web** | 8000 | Agent + Web UI (all-in-one!) |

```
┌─────────────┐
│   Browser   │ http://localhost:8000
│  (ADK Web)  │
└──────┬──────┘
       │
       ↓
┌─────────────────┐
│  ADK Framework  │ (Python Agent + Web Server)
│  file_io_agent  │
└──────┬──────────┘
       │
       ↓
┌─────────────────┐
│  MinIO Storage  │ http://localhost:9002
│   (File Backend)│
└─────────────────┘
```

**Much simpler than before!** The `adk web` command handles everything.

---

## 🛠️ Troubleshooting

### "adk: command not found"
```bash
# Reinstall ADK
pip install --upgrade google-adk

# Verify PATH
which adk
```

### "ModuleNotFoundError: No module named 'google.adk'"
```bash
# Make sure virtual environment is activated
source .venv/bin/activate
pip install google-adk
```

### "Agent not found"
Make sure you're in the project directory when running:
```bash
cd /path/to/agent_project
./start_adk.sh
```

### MinIO not connecting
```bash
# Check MinIO is running
docker ps | grep minio

# Restart if needed
docker-compose restart
```

### Port 8000 already in use
```bash
# Use different port
adk web --port 8001 adk_agent
```

### Can't see agent in dropdown
- Refresh the page
- Check terminal for errors
- Verify adk_agent.py has `root_agent` defined

---

## 🎯 Quick Start Commands

### Complete Startup:

```bash
# Terminal 1: Start MinIO
docker-compose up -d

# Terminal 2: Start ADK Web
source .venv/bin/activate
./start_adk.sh

# Browser: Open
http://localhost:8000
```

### Quick Stop:
```bash
# Stop ADK (Ctrl+C in terminal)
# Stop MinIO
docker-compose down
```

---

## 🌟 Benefits of ADK Web

✅ **All-in-One** - Single command starts everything
✅ **Official Google Tool** - Built by the Gemini team
✅ **Rich Visualization** - See exactly what your agent is doing
✅ **Debugging Tools** - Trace every step of execution
✅ **Session Management** - Save and replay interactions
✅ **No External Setup** - No need to clone adk-web repo
✅ **Real-Time Updates** - Watch your agent work live

---

## 📖 Learn More

- [ADK Python Docs](https://github.com/google/adk-python)
- [Official ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Codelabs](https://codelabs.developers.google.com/your-first-agent-with-adk)

---

## 💡 Pro Tips

1. **Use the dropdown** in the upper right to select your agent
2. **Check the trace view** to see tool calls in detail
3. **Save sessions** for later review and debugging
4. **Use debug mode** to see full LLM prompts and responses
5. **Try different prompts** to test edge cases

---

**Ready to visualize your agent?** Just run `./start_adk.sh` and go! 🚀
