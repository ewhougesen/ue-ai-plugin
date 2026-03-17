"""
UE AI Plugin - Main Python Module
Provides AI-powered copilot functionality for Unreal Engine

Quick Start:
    import ue_ai_plugin
    ue_ai_plugin.ai_chat.send("Create a red cube")
    ue_ai_plugin.ai_chat.create_cube("MyCube")
"""

from .ue_ai_editor_panel import ai_chat

__version__ = "0.1.0"

# Export main interface
__all__ = ['ai_chat']

def get_version():
    """Get plugin version"""
    return __version__


def init():
    """Initialize the plugin (called automatically on import)"""
    import unreal
    unreal.log("")
    unreal.log("╔" + "═" * 48 + "╗")
    unreal.log("║     UE AI PLUGIN - Python Chat Interface        ║")
    unreal.log("╚" + "═" * 48 + "╝")
    unreal.log("")
    unreal.log("Backend: http://localhost:8000 (Docker)")
    unreal.log("")
    unreal.log("USAGE:")
    unreal.log("  ai_chat.send('your message')")
    unreal.log("  ai_chat.create_cube('Name', (x,y,z))")
    unreal.log("  ai_chat.create_material('Name', (r,g,b))")
    unreal.log("  ai_chat.history()")
    unreal.log("  ai_chat.clear()")
    unreal.log("")
    unreal.log("EXAMPLES:")
    unreal.log("  ai_chat.send('Create a cube at position 100,100,100')")
    unreal.log("  ai_chat.send('Make a blue material named Water')")
    unreal.log("  ai_chat.create_cube('TestCube', (0, 0, 100))")
    unreal.log("")
    unreal.log("╚" + "═" * 48 + "╝")
    unreal.log("")


# Auto-initialize on import
init()
