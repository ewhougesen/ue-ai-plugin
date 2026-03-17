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


class UEAIChatPanel(unreal.ToolMenuEntryScript):
    """
    Custom editor panel for AI chat
    """

    def __init__(self):
        self.chat_history = []
        self.is_processing = False

    def execute(self, context):
        """Called when menu item is clicked"""
        unreal.log("Opening UE AI Chat Panel...")
        self.show_chat_window()

    def show_chat_window(self):
        """Show the chat window"""
        try:
            # For now, show in Output Log with a prompt
            unreal.log("=" * 60)
            unreal.log("     UE AI CHAT PANEL")
            unreal.log("=" * 60)
            unreal.log("Backend connected: http://{}:{}".format(BACKEND_HOST, BACKEND_PORT))
            unreal.log("")
            unreal.log("USAGE:")
            unreal.log("  ai_chat.send('your message here')")
            unreal.log("  ai_chat.history()")
            unreal.log("  ai_chat.clear()")
            unreal.log("")
            unreal.log("EXAMPLES:")
            unreal.log("  ai_chat.send('Create a cube at 0,0,100')")
            unreal.log("  ai_chat.send('Make a red material')")
            unreal.log("=" * 60)

        except Exception as e:
            unreal.log_error(f"Error showing chat window: {str(e)}")


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
            # Prepare request
            request_data = {
                "message": message,
                "context": {
                    "project": unreal.SystemLibrary.get_project_name(),
                    "engine_version": unreal.SystemConfiguration.get_engine_version()
                }
            }

            # Connect to backend
            conn = http.client.HTTPConnection(BACKEND_HOST, BACKEND_PORT, timeout=10)
            headers = {"Content-type": "application/json"}

            conn.request("POST", "/api/chat", json.dumps(request_data), headers)
            response = conn.getresponse()

            if response.status == 200:
                data = response.read().decode("utf-8")
                result = json.loads(data)

                # Extract response
                if "response" in result:
                    ai_message = result["response"]
                elif "message" in result:
                    ai_message = result["message"]
                elif "choices" in result and len(result["choices"]) > 0:
                    ai_message = result["choices"][0].get("message", {}).get("content", str(result))
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
            error_msg = "Cannot connect to backend. Make sure Docker is running: docker-compose up"
            unreal.log_error(f"[AI Error]: {error_msg}")
            return error_msg
        except http.client.HTTPException as e:
            error_msg = f"HTTP Error: {str(e)}"
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
        import ue_ai_plugin
        result = ue_ai_plugin.create_cube(name, location)
        unreal.log(f"Created cube: {result}")
        return result

    def create_material(self, name="Material", color=(1, 0, 0)):
        """Create a material"""
        import ue_ai_plugin
        result = ue_ai_plugin.create_material(name, color)
        unreal.log(f"Created material: {result}")
        return result


def register_menu():
    """Register the AI Chat menu in Unreal Editor"""
    try:
        # Get the tool menus manager
        menus = unreal.ToolMenus.get()

        # Find or create the menu
        menu = menus.find_menu("LevelEditor.MainMenu.Window")
        if not menu:
            unreal.log_warning("Could not find Window menu")
            return

        # Add a new section for AI tools
        section = menu.add_section("AI_Tools", "AI Tools", unreal.ToolMenuInsertByName("WindowLayout", unreal.ToolMenuInsertType.AFTER))

        # Add menu entry for AI Chat
        entry = section.add_entry(
            unreal.ToolMenuEntry(
                name="UEAI_Chat",
                type=unreal.MultiBlockType.MENU_ENTRY,
                user_interface_action_type=unreal.UserInterfaceActionType.BUTTON,
                label="UE AI Chat",
                tool_tip="Open the UE AI Chat panel"
            )
        )

        # Set up the entry
        entry.set_string(unreal.ToolMenuEntry.STRING_PROPERTIES.URL, "http://localhost:8000")
        entry.set_icon(unreal.SlateIcon("EditorStyle", "Icons.Person"))

        unreal.log("UE AI Chat menu registered in Window menu")
        return True

    except Exception as e:
        unreal.log_error(f"Failed to register menu: {str(e)}")
        return False


# Create global instance
ai_chat = AIChatManager()

# Auto-register on import
def init():
    """Initialize the AI Chat panel"""
    unreal.log("=" * 50)
    unreal.log("UE AI CHAT PANEL LOADED")
    unreal.log("=" * 50)
    unreal.log("")
    unreal.log("QUICK START:")
    unreal.log("  ai_chat.send('Hello AI')")
    unreal.log("  ai_chat.create_cube()")
    unreal.log("  ai_chat.create_material()")
    unreal.log("")
    unreal.log("Type 'ai_chat' for available methods")
    unreal.log("=" * 50)

    # Try to register menu
    register_menu()

    return ai_chat


# Initialize
ai_chat = init()
