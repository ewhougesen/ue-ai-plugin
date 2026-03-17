"""
UE AI Plugin - Editor Panel
Creates a custom tab in Unreal Editor for chatting with the AI
"""

import unreal
import http.client
import json
import threading

# Backend configuration
BACKEND_HOST = "localhost"
BACKEND_PORT = 8000


class AIChatManager:
    """Manages AI chat functionality"""

    def __init__(self):
        self.history = []

    def send(self, message: str) -> str:
        """
        Send a message to the AI

        Args:
            message: Your message to the AI

        Returns:
            AI's response
        """
        if not message or message.strip() == "":
            return "Please enter a message."

        unreal.log(f"[You]: {message}")

        try:
            # Prepare request - use correct API format
            request_data = {
                "user_input": message,
                "context_data": {
                    "project": unreal.SystemLibrary.get_project_name(),
                    "engine_version": "5.5"
                }
            }

            # Connect to backend - correct endpoint
            conn = http.client.HTTPConnection(BACKEND_HOST, BACKEND_PORT, timeout=10)
            headers = {"Content-type": "application/json"}

            conn.request("POST", "/api/api/chat", json.dumps(request_data), headers)
            response = conn.getresponse()

            if response.status == 200:
                data = response.read().decode("utf-8")
                result = json.loads(data)

                # Extract response from the correct format
                if result.get("success") and "full_response" in result:
                    ai_message = result["full_response"]
                elif "responses" in result and len(result["responses"]) > 0:
                    ai_message = result["responses"][-1].get("content", str(result))
                else:
                    ai_message = str(result)

                self.history.append({"role": "user", "content": message})
                self.history.append({"role": "assistant", "content": ai_message})

                unreal.log(f"[AI]: {ai_message}")
                return ai_message
            else:
                error_msg = f"HTTP {response.status}: {response.reason}"
                unreal.log_error(f"[AI Error]: {error_msg}")
                return f"Error: {error_msg}"

        except ConnectionRefusedError:
            error_msg = "Cannot connect to backend. Make sure Docker is running."
            unreal.log_error(f"[AI Error]: {error_msg}")
            return error_msg
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            unreal.log_error(f"[AI Error]: {error_msg}")
            return error_msg

    def history(self):
        """Show chat history"""
        unreal.log("=" * 40)
        unreal.log("CHAT HISTORY:")
        unreal.log("=" * 40)
        for i, msg in enumerate(self.history):
            role = msg["role"].upper()
            content = msg["content"]
            if role == "USER":
                unreal.log(f"{i}. [You]: {content}")
            else:
                unreal.log(f"{i}. [AI]: {content}")
        unreal.log("=" * 40)
        return self.history

    def clear(self):
        """Clear chat history"""
        self.history.clear()
        unreal.log("Chat history cleared.")

    def create_cube(self, name="Cube", location=(0, 0, 0)):
        """Create a cube in the scene"""
        try:
            actor_loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                unreal.StaticMeshActor,
                actor_loc
            )
            actor.set_actor_label(name)
            unreal.log(f"✅ Created cube: {name} at {location}")
            return name
        except Exception as e:
            unreal.log_error(f"Failed to create cube: {e}")
            return ""

    def create_material(self, name="Material", color=(1, 0, 0)):
        """Create a material"""
        try:
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            material = asset_tools.create_asset(
                name,
                "/Game/Materials",
                unreal.Material,
                unreal.MaterialFactoryNew()
            )
            unreal.log(f"✅ Created material: {name}")
            return f"/Game/Materials/{name}"
        except Exception as e:
            unreal.log_error(f"Failed to create material: {e}")
            return ""


# Create global instance
ai_chat = AIChatManager()

# Initialize
unreal.log("=" * 50)
unreal.log("UE AI CHAT LOADED")
unreal.log("=" * 50)
unreal.log("Type: ai_chat.send('your message')")
unreal.log("=" * 50)
