"""Claude AI service integration"""
import asyncio
from typing import AsyncIterator, Optional
from anthropic import AsyncAnthropic
import structlog

from app.config import settings


log = structlog.get_logger(__name__)


class ClaudeService:
    """Service for interacting with Claude API"""

    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.CLAUDE_API_KEY)
        self.conversation_history: dict[str, list[dict]] = {}
        log.info("claude_service_initialized")

    async def process_request(
        self,
        user_input: str,
        context_frame: Optional[dict] = None,
        context_data: Optional[dict] = None
    ) -> AsyncIterator[dict]:
        """
        Process user request through Claude with streaming response

        Yields response chunks as they arrive
        """
        # Build system message
        system_message = self._build_system_message(context_frame)

        # Build user message with context
        user_message = self._build_user_message(user_input, context_frame, context_data)

        # Get conversation history for this session
        session_id = context_data.get("session_id", "default") if context_data else "default"
        messages = self.conversation_history.get(session_id, [])

        # Add current message
        messages.append({"role": "user", "content": user_message})

        try:
            # Stream response from Claude
            async with self.client.messages.stream(
                model=settings.CLAUDE_MODEL,
                max_tokens=settings.CLAUDE_MAX_TOKENS,
                system=system_message,
                messages=messages
            ) as stream:

                # Send thinking status
                yield {
                    "type": "THINKING",
                    "content": "",
                    "progress": 0
                }

                # Accumulate response
                full_response = ""
                async for text in stream.text_stream:
                    full_response += text
                    yield {
                        "type": "THINKING",
                        "content": text,
                        "progress": -1  # Indeterminate progress
                    }

                # Save to conversation history
                messages.append({"role": "assistant", "content": full_response})
                self.conversation_history[session_id] = messages

                # Send complete status
                yield {
                    "type": "COMPLETE",
                    "content": full_response,
                    "progress": 100
                }

        except Exception as e:
            log.error("claude_api_error", error=str(e))
            raise

    def _build_system_message(self, context_frame: Optional[dict]) -> str:
        """Build system message for Claude"""
        base_message = """You are an AI assistant integrated with Unreal Engine 5.
You help users create and edit 3D assets, materials, and animations through natural language.

Available capabilities:
- Generate 3D meshes (primitive shapes, AI-generated models)
- Create and modify materials (procedural, AI-generated textures)
- Edit existing objects in the scene
- Provide real-time feedback on viewport content

When the user makes requests:
1. Understand their intent clearly
2. Ask clarifying questions if needed
3. Provide specific, actionable responses
4. Use appropriate AI services for generation tasks

Respond concisely and focus on being helpful."""

        if context_frame:
            base_message += f"\n\nCurrent viewport contains {len(context_frame.get('objects', []))} objects."

        return base_message

    def _build_user_message(
        self,
        user_input: str,
        context_frame: Optional[dict],
        context_data: Optional[dict]
    ) -> str:
        """Build user message with context"""
        message = user_input

        if context_frame and context_frame.get("objects"):
            objects = context_frame["objects"]
            message += f"\n\nScene objects ({len(objects)}):"
            for obj in objects[:10]:  # Limit to first 10
                message += f"\n- {obj.get('name', 'Unknown')} ({obj.get('type', 'Object')})"

        if context_data:
            relevant_data = {k: v for k, v in context_data.items()
                           if k not in ["session_id", "timestamp"]}
            if relevant_data:
                message += f"\n\nContext: {relevant_data}"

        return message

    def clear_history(self, session_id: str = "default"):
        """Clear conversation history for a session"""
        if session_id in self.conversation_history:
            del self.conversation_history[session_id]
            log.info("conversation_cleared", session_id=session_id)
