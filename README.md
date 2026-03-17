# UE AI Plugin

AI-powered copilot plugin for Unreal Engine 5.5+ that enables natural language interaction for creating and editing 3D assets, materials, and animations.

## Features

- 🎯 Natural language interface to Unreal Engine
- 🤖 Integration with multiple AI services (Meshy.ai, CSM.ai, Kaedim, TripoSR)
- 🎨 Procedural material generation and refinement
- 🖼️ Live viewport feed for scene understanding
- ⚡ Real-time gRPC communication
- 🐳 Docker-based backend

## Architecture

```
┌─────────────────┐     gRPC      ┌──────────────────┐
│  Unreal Engine  │◄─────────────►│  Local Backend   │
│     Plugin      │               │  (Docker)        │
└─────────────────┘               └────────┬─────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │  AI Services    │
                                  │ (Meshy, CSM,    │
                                  │  Kaedim, etc.)  │
                                  └─────────────────┘
```

## Status

🚧 Under active development

## Components

- **UE Plugin** - C++/Python plugin for Unreal Editor
- **Backend Server** - gRPC server with AI service integrations
- **Claude Integration** - Natural language processing and task execution

---

Built for Hollywood/AAA quality asset creation with AI augmentation.
