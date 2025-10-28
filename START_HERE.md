# 🚀 START HERE - Agent Project

## Quick Start

```bash
# 1. Create .env and add your Google AI API key
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key_here

# 2. Start everything
bash start.sh

# 3. Test it works
python test_storage.py
```

## What This Does

You're building an AI agent that can:
- Accept file uploads
- Read and analyze files
- Generate new files
- Store everything in MinIO (S3-compatible storage)
- Use Google Gemini AI for intelligence

## Project Structure

```
agent_project/
├── docker-compose.yml      # MinIO setup
├── requirements.txt        # Python packages
├── .env                    # Your config
├── start.sh               # Quick start
├── test_storage.py        # Test suite
└── src/
    └── storage_service.py # Storage API
```

## Next Steps

After testing works:
1. You're ready for Step 2: Building the AI Agent!
2. Let me know when you want to continue

## Need Help?

- MinIO Console: http://localhost:9001 (minioadmin/minioadmin123)
- Get API Key: https://makersuite.google.com/app/apikey

**Current Status:** Step 1 Complete ✅
**Next:** Build AI Agent Core
