"""
UE AI Plugin - Chat UI
Provides a chat interface for interacting with the AI backend
"""

import unreal
import http.client
import json

# Backend configuration
BACKEND_HOST = "localhost"
BACKEND_PORT = 8000

# Global chat history
chat_history = []


class AIChatWindow:
    """Simple chat window for AI interaction"""

    def __init__(self):
        self.window_name = "UE AI Chat"
        self.is_visible = False

    def show(self):
        """Show the chat window using Slate"""
        unreal.log("=== UE AI Chat ===")
        unreal.log("Backend: http://{}:{}".format(BACKEND_HOST, BACKEND_PORT))
        unreal.log("Type 'help' for commands")
        unreal.log("=================")

    def send_message(self, message: str) -> str:
        """Send message to AI backend and get response"""
        if not message or message.strip() == "":
            return ""

        # Add to history
        chat_history.append({"role": "user", "content": message})

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
            conn = http.client.HTTPConnection(BACKEND_HOST, BACKEND_PORT)
            headers = {"Content-type": "application/json"}

            conn.request("POST", "/api/chat", json.dumps(request_data), headers)
            response = conn.getresponse()
            data = response.read().decode("utf-8")
            conn.close()

            result = json.loads(data)

            # Extract response
            if "response" in result:
                ai_message = result["response"]
            elif "message" in result:
                ai_message = result["message"]
            else:
                ai_message = str(result)

            chat_history.append({"role": "assistant", "content": ai_message})
            return ai_message

        except Exception as e:
            error_msg = "Error: Failed to connect to backend. Make sure Docker is running."
            unreal.log_error(f"UE AI: {error_msg} - {str(e)}")
            chat_history.append({"role": "assistant", "content": error_msg})
            return error_msg

    def get_history(self) -> list:
        """Get chat history"""
        return chat_history

    def clear_history(self):
        """Clear chat history"""
        chat_history.clear()


# Global instance
_chat_window = None


def get_chat_window() -> AIChatWindow:
    """Get or create the chat window instance"""
    global _chat_window
    if _chat_window is None:
        _chat_window = AIChatWindow()
    return _chat_window


def open_chat():
    """Open the AI chat window"""
    window = get_chat_window()
    window.show()
    unreal.log("AI Chat window ready. Use send_ai_message() to chat.")


def send_ai_message(message: str) -> str:
    """
    Send a message to the AI and get a response

    Args:
        message: Your message to the AI

    Returns:
        AI's response
    """
    window = get_chat_window()
    response = window.send_message(message)

    unreal.log(f"You: {message}")
    unreal.log(f"AI: {response}")

    return response


def get_chat_history() -> list:
    """Get the current chat history"""
    return get_chat_window().get_history()


def clear_chat_history():
    """Clear the chat history"""
    get_chat_window().clear_history()
    unreal.log("Chat history cleared")


def create_test_material():
    """Create a test material to verify Python access"""
    import ue_ai_plugin
    mat_path = ue_ai_plugin.create_material("TestMaterial", (1.0, 0.5, 0.0))
    unreal.log(f"Created test material: {mat_path}")
    return mat_path


def create_test_cube():
    """Create a test cube to verify Python access"""
    import ue_ai_plugin
    cube_name = ue_ai_plugin.create_cube("TestCube", (100, 100, 100))
    unreal.log(f"Created test cube: {cube_name}")
    return cube_name


# Auto-initialize
unreal.log("UE AI Chat module loaded. Functions available:")
unreal.log("  - open_chat()")
unreal.log("  - send_ai_message('your message')")
unreal.log("  - create_test_material()")
unreal.log("  - create_test_cube()")
