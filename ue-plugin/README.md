# UE AI Plugin - Unreal Engine Plugin

AI-powered copilot plugin for Unreal Engine 5.5+ that enables natural language interaction for creating and editing 3D assets, materials, and animations.

## Features

- 💬 Natural language chat interface in Unreal Editor
- 🤖 Integration with AI backend (Claude/z.ai)
- 🎨 Asset generation and material creation
- 📊 Real-time connection status
- ⚙️ Configurable backend server URL

## Installation

### Method 1: Copy to Your Project

1. Copy the `UEAIPlugin` folder to your project's `Plugins` directory
2. Right-click on `.uproject` file → "Generate Visual Studio project files"
3. Open your project in Unreal Editor
4. Go to Edit → Plugins → Enable "UE AI Plugin"
5. Restart Unreal Editor

### Method 2: Marketplace (Future)

Coming soon to the Unreal Engine Marketplace.

## Usage

### Opening the Plugin

1. Open Unreal Editor
2. Go to **Window → AI → UE AI Plugin**
3. The AI assistant panel will open in the editor

### Example Commands

```
"Create a red sphere material"
"Add a point light to the scene"
"Make a simple cube with metallic material"
"Generate a rock mesh"
```

## Configuration

The plugin settings are stored in:

```
Config/DefaultUEAIPlugin.ini
```

### Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `BackendServerURL` | `http://localhost:8000` | URL of the backend AI server |
| `bAutoConnect` | `true` | Auto-connect to backend on startup |
| `ChatHistoryLimit` | `50` | Maximum messages in chat history |
| `ZaiAPIKey` | (empty) | Optional z.ai API key |

## Building

### Requirements

- Unreal Engine 5.5 or later
- Visual Studio 2022 (Windows) or Xcode (Mac)
- C++14 support

### Build Steps

1. Place the plugin in your project's `Plugins` folder
2. Generate project files:
   ```bash
   # Right-click on .uproject file in Explorer
   # Or use the Unreal Build Tool
   ```
3. Open the generated solution in your IDE
4. Build the project

## Architecture

```
┌──────────────────────┐
│  Unreal Editor       │
│  ┌────────────────┐  │
│  │ UE AI Plugin   │  │
│  │  (C++ Module)  │  │
│  └────────┬───────┘  │
└───────────┼──────────┘
            │ HTTP
┌───────────▼──────────┐
│  Backend Server      │
│  (FastAPI + Claude)  │
│  localhost:8000      │
└──────────────────────┘
```

## Development

### Project Structure

```
ue-plugin/
├── UEAIPlugin.uplugin          # Plugin manifest
├── Source/
│   └── UEAIPlugin/
│       ├── UEAIPlugin.Build.cs # Build configuration
│       ├── Public/             # Public headers
│       │   ├── UEAIPlugin.h
│       │   ├── UEAIService.h
│       │   ├── UEAIEditorWidget.h
│       │   └── UEAIPluginSettings.h
│       └── Private/            # Private implementation
│           ├── UEAIPlugin.cpp
│           ├── UEAIService.cpp
│           ├── UEAIEditorWidget.cpp
│           └── UEAIPluginSettings.cpp
├── Resources/                   # Icons and assets
└── Content/                     # UE content
```

### Adding New Features

1. Add header to `Public/`
2. Add implementation to `Private/`
3. Update `UEAIPlugin.Build.cs` if new dependencies are needed
4. Rebuild the plugin

## Troubleshooting

### Plugin not appearing

1. Check that the plugin is in the `Plugins` folder
2. Verify the `UEAIPlugin.uplugin` file is valid
3. Enable the plugin in Edit → Plugins
4. Restart Unreal Editor

### Backend connection failed

1. Verify the backend server is running at the configured URL
2. Check the connection status in the plugin panel
3. Check firewall settings

### Compilation errors

1. Regenerate project files
2. Clean and rebuild
3. Check that all dependencies are listed in `.Build.cs`

## Contributing

This project follows TDD (Test Driven Development). See `TDD_POLICY.md` in the root directory.

## License

MIT License - See LICENSE file for details.

## Credits

- Developed for UE AI Plugin project
- Uses z.ai API for Claude integration
- Built with Unreal Engine 5.5
