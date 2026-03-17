# UE AI Plugin - Quick Start (Mac/Python)

AI-powered copilot for Unreal Engine 5.5+. Natural language interface for creating and editing 3D assets, materials, and animations.

## Quick Start

### 1. Enable Python Startup Script

Open Unreal Editor and go to:
- **Edit → Editor Preferences**
- Search "Python"
- Enable "Python Script Plugin"
- Set "Run Startup Script" = ON
- Set "Python Script File" to:
  ```
  /Volumes/SERENADA_2/_elliott/Unreal Projects/UEAI-Plugin-Test/Content/Python/init_unreal.py
  ```
- Click "Set" and restart Unreal Editor

### 2. Start the Backend

```bash
cd ~/repos/ue-ai-plugin
docker-compose up
```

### 3. Use the AI Chat

In Unreal Editor, open **Output Log → Python** tab:

```python
# Chat with AI
ai_chat.send("Create a red cube at position 0,0,100")
ai_chat.send("Make a blue material called Water")
ai_chat.send("Spawn a sphere")

# Quick commands
ai_chat.create_cube("MyCube", (100, 100, 100))
ai_chat.create_material("RedMat", (1.0, 0.0, 0.0))

# View history
ai_chat.history()

# Clear history
ai_chat.clear()
```

## Features

- 💬 Natural language chat interface
- 🤖 AI integration via z.ai (glm-4.7 model)
- 🎨 Create materials with natural language
- 🧊 Spawn actors and shapes
- 📊 Chat history
- ⚙️ Configurable backend

## Architecture (Python/Blueprint)

```
┌──────────────────────┐
│  Unreal Editor       │
│  ┌────────────────┐  │
│  │ Python Module  │  │
│  │ (ai_chat)      │  │
│  └────────┬───────┘  │
└───────────┼──────────┘
            │ HTTP
┌───────────▼──────────┐
│  Backend Server      │
│  (FastAPI + z.ai)    │
│  localhost:8000      │
└──────────────────────┘
```

## Troubleshooting

### "ai_chat not found"
- Enable Python Script Plugin in Edit → Plugins
- Set startup script in Editor Preferences
- Restart Unreal Editor

### "Cannot connect to backend"
- Make sure Docker is running: `docker-compose up`
- Check backend is at http://localhost:8000
- Test: `curl http://localhost:8000/health`

### Plugin not enabled
- Go to Edit → Plugins
- Search "UE AI Plugin"
- Click "Enabled"
- Restart Unreal Editor

## Requirements

- Unreal Engine 5.5+
- Python Script Plugin (built-in)
- Docker (for backend server)
- 4GB RAM minimum

## License

MIT License
