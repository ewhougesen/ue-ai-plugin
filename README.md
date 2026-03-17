# UE AI Plugin - Comprehensive Documentation

## Overview

The UE AI Plugin is a comprehensive AI-powered assistant for Unreal Engine 5. It understands natural language commands and can execute complex operations, generate assets, provide tutorials, and guide users through any Unreal Engine workflow.

**Current Version:** 0.1.0 (Alpha)
**Status:** Foundation Complete - Expansion in Progress

## What's Built Now

### ✅ Fully Functional

1. **Natural Language Understanding**
   - Process natural language requests
   - Extract intent and parameters
   - Handle 15+ action types
   - Smart property extraction

2. **Actor Creation** (12+ types)
   - Static Mesh Actors (cubes, spheres, etc.)
   - Lights (Point, Spot, Directional, Sky)
   - Cameras
   - Characters and Pawns
   - Atmospheric effects

3. **Material Generation**
   - Smart color extraction from text
   - Roughness, metallic, emissive detection
   - Full PBR material creation
   - Multiple material templates

4. **Texture Generation**
   - AI-powered texture generation (free service)
   - Custom resolution support
   - Automatic import and setup

5. **Lighting Setups**
   - Outdoor lighting (sun, sky, fog)
   - Indoor lighting (multiple points)
   - Cinematic lighting

6. **Post Processing**
   - Bloom
   - Depth of Field
   - Motion Blur
   - Color Grading

7. **AI Chat Assistant**
   - Comprehensive UE knowledge base
   - Tutorials and guidance
   - Troubleshooting help
   - Workflow instructions

8. **Actor Management**
   - Find and select actors
   - Move, rotate, scale
   - Delete actors

### 📚 Knowledge Base Coverage

The system includes comprehensive knowledge of:

- **Actors**: 12+ actor types with properties and creation
- **Components**: 10+ component types with usage
- **Materials**: Full material system with all nodes
- **Textures**: All types, formats, and settings
- **Meshes**: Static, skeletal, import/export
- **Animations**: All animation systems
- **Blueprints**: Complete blueprint reference
- **Levels**: Streaming, World Partition, instances
- **Lighting**: Lightmass, Lumen, Nanite
- **Physics**: Rigid bodies, constraints, collision
- **Niagara**: Complete particle system
- **UMG**: 18+ widget types
- **Input**: All input systems
- **Gameplay**: Full framework reference
- **Networking**: Replication, multi-player
- **Audio**: Complete audio system
- **AI**: Behavior trees, navigation, EQS
- **Rendering**: Advanced rendering techniques
- **Tools**: Editor scripting, automation

## How to Use

### Quick Start

1. **Restart Unreal Editor**
2. **Open Python Console** (Output Log → Python tab)
3. **Load the assistant:**
   ```python
   exec(open('/Volumes/SERENADA_2/_elliott/Unreal Projects/UEAI-Plugin-Test/Plugins/UEAIPlugin/Content/Python/ue_ai_assistant.py').read())
   ```

4. **Start commanding:**
   ```python
   ai.do("Create a red cube at position 100,0,0")
   ai.do("Make a shiny gold material")
   ai.do("Generate a brick wall texture")
   ai.do("Setup outdoor lighting")
   ```

### Example Commands

**Actor Creation:**
```python
ai.do("Create a sphere named Ball")
ai.do("Spawn a cylinder at 0,0,200")
ai.do("Add a point light at 100,100,100")
ai.do("Create a camera")
```

**Materials:**
```python
ai.do("Create a rough red plastic material")
ai.do("Make a shiny gold metal material")
ai.do("Create a blue glass material with transparency")
ai.do("Make a glowing red emissive material")
```

**Textures:**
```python
ai.do("Generate a wood texture")
ai.do("Create a brick wall texture 1024x1024")
ai.do("Generate a metal surface texture")
```

**Lighting:**
```python
ai.do("Setup outdoor lighting")
ai.do("Create cinematic lighting")
ai.do("Add a warm point light")
```

**Post Processing:**
```python
ai.do("Add bloom and depth of field")
ai.do("Enable motion blur")
```

**Getting Help:**
```python
ai.do("How do I create a glowing material?")
ai.do("Explain blueprints")
ai.do("Help with lighting")
ai.do("Tutorial on animation blueprints")
```

**Modifying Actors:**
```python
ai.do("Select cube")
ai.do("Move the selected cube to 100,100,100")
ai.do("Rotate the sphere 45 degrees")
ai.do("Delete the selected actor")
```

### Direct Methods

```python
# Quick creation
ai.create_cube("MyCube", (0, 0, 100))
ai.create_sphere("MySphere")
ai.create_light("Light1", (100, 100, 100))

# Material with description
ai.create_material("Gold", "shiny gold metal")

# Chat
ai.chat("What's the difference between StaticMesh and SkeletalMesh?")
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     UNREAL ENGINE 5.5                        │
├─────────────────────────────────────────────────────────────┤
│  Python Plugin Layer                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │   AI Assistant (ue_ai_assistant.py)                   │  │
│  │   - Natural language understanding                     │  │
│  │   - Intent analysis                                   │  │
│  │   - Parameter extraction                               │  │
│  │   - Execution engine                                   │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                              │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │   Knowledge Base (ue_knowledge_base.py)              │  │
│  │   - Actors, Materials, Lighting, etc.                 │  │
│  │   - Workflows, Troubleshooting, Templates              │  │
│  └──────────────────────────────────────────────────────┘  │
│                 │                                              │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │   Asset Manager (ue_asset_system.py)                 │  │
│  │   - File download                                     │  │
│  │   - FBX/Texture import                                │  │
│  │   - Material creation                                  │  │
│  │   - Actor spawning                                    │  │
│  └──────────────┬───────────────────────────────────────┘  │
└─────────────────┼──────────────────────────────────────────┘
                  │
                  │ HTTP
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend Server (Docker: localhost:8000)                  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │   FastAPI                                            │  │
│  │   - Asset generation endpoints                        │  │
│  │   - AI Chat endpoint                                  │  │
│  └──────────────┬──────────────────────────────────────┘  │
│                 │                                              │
│  ┌──────────────▼──────────────────────────────────────┐  │
│  │   AI Services                                        │  │
│  │   - z.ai (Claude via glm-4.7)                       │  │
│  │   - Pollinations.ai (free textures)                 │  │
│  │   - Meshy.ai (3D models - API key required)          │  │
│  │   - CSM.ai (3D models - API key required)           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Roadmap

### Phase 1: Foundation ✅ (COMPLETE)
- Natural language understanding
- Basic actor/material/texture generation
- Knowledge base
- AI chat assistance

### Phase 2: Enhanced Generation (Current)
- Connect to production AI services
- Procedural generation improvements
- Viewport capture for scene understanding
- Asset library management

### Phase 3: Advanced Features
- Blueprint generation
- Animation setup
- Complex workflows

### Phase 4: Code Generation
- C++ code generation
- Python script generation
- Blueprint node generation
- Shader code generation

### Phase 5: Scene Understanding
- Viewport analysis
- Scene optimization suggestions
- Performance analysis

### Phase 6: Learning & Adaptation
- Learn from user patterns
- Suggest optimizations
- Remember project conventions

### Phase 7: Production AI Services
- Full Meshy.ai integration
- Full CSM.ai integration
- Kaedim integration
- Custom model training

## API Keys (Optional)

For enhanced features, add to `~/repos/ue-ai-plugin/.env`:

```bash
MESHY_API_KEY=your_key_from_meshy.ai
CSM_API_KEY=your_key_from_csm.ai
STABILITY_API_KEY=your_key_from_stability.ai
```

## Contributing

This is a long-term project. Contributions welcome in:
- Expanding the knowledge base
- Adding more intent types
- Improving natural language understanding
- Adding workflows
- Fixing bugs
- Documentation

## License

MIT License

## Credits

Built by ewhougesen with assistance from Claude (Anthropic)
Using z.ai API with glm-4.7 model

**Note:** This is an active project. The knowledge base and capabilities will continuously expand. The goal is to create an AI that truly understands everything about Unreal Engine and can generate anything through natural language.
