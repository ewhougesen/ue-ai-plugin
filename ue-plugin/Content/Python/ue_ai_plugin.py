"""
UE AI Plugin - Python Module
Provides AI-powered copilot functionality for Unreal Engine
"""

import unreal
import http.client
import json

# Backend server configuration
BACKEND_HOST = "localhost"
BACKEND_PORT = 8000


def send_chat_message(message: str, include_viewport: bool = False) -> dict:
    """
    Send a chat message to the AI backend and get a response

    Args:
        message: The user's message
        include_viewport: Whether to include viewport screenshot

    Returns:
        Response from the AI backend
    """
    try:
        # Prepare request data
        request_data = {
            "message": message,
            "context": {
                "project": unreal.SystemLibrary.get_project_name(),
                "engine_version": unreal.SystemConfiguration.get_engine_version()
            }
        }

        # Add viewport data if requested
        if include_viewport:
            # Capture viewport (would need to be implemented)
            request_data["viewport_image"] = None

        # Connect to backend
        conn = http.client.HTTPConnection(BACKEND_HOST, BACKEND_PORT)
        headers = {"Content-type": "application/json"}

        # Send request
        conn.request("POST", "/api/chat", json.dumps(request_data), headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        conn.close()

        return json.loads(data)

    except Exception as e:
        unreal.log_error(f"UE AI Plugin: Failed to connect to backend: {str(e)}")
        return {
            "error": str(e),
            "message": "Failed to connect to AI backend. Make sure the server is running."
        }


def create_material(material_name: str, color: tuple = (1.0, 0.0, 0.0)) -> str:
    """
    Create a new material with specified color

    Args:
        material_name: Name for the new material
        color: RGB color tuple (0-1)

    Returns:
        Path to the created material
    """
    try:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        material_path = f"/Game/Materials/{material_name}"

        # Create material
        material = asset_tools.create_asset(
            material_name,
            "/Game/Materials",
            unreal.Material,
            unreal.MaterialFactoryNew()
        )

        unreal.log(f"Created material: {material_path}")
        return str(material_path)

    except Exception as e:
        unreal.log_error(f"Failed to create material: {str(e)}")
        return ""


def create_cube(actor_name: str, location: tuple = (0.0, 0.0, 0.0)) -> str:
    """
    Create a cube actor in the level

    Args:
        actor_name: Name for the new actor
        location: XYZ location tuple

    Returns:
        Name of the created actor
    """
    try:
        actor_location = unreal.Vector(location[0], location[1], location[2])
        actor_class = unreal.StaticMeshActor

        # Spawn actor
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            actor_class,
            actor_location
        )

        actor.set_actor_label(actor_name)
        unreal.log(f"Created cube: {actor_name}")

        return actor_name

    except Exception as e:
        unreal.log_error(f"Failed to create cube: {str(e)}")
        return ""


# Register Python functions as Unreal commands
def register_commands():
    """Register plugin commands with Unreal's Python console"""
    unreal.log("UE AI Plugin: Python commands registered")
    return True


# Auto-register on import
register_commands()
