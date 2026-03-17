"""Unit tests for Claude Service"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.claude_service import ClaudeService


@pytest.mark.unit
class TestClaudeService:
    """Test Claude service initialization and basic functionality"""

    def test_service_initialization(self, mock_settings):
        """Test Claude service initializes correctly"""
        with patch('app.services.claude_service.AsyncAnthropic'):
            service = ClaudeService()
            assert service.conversation_history == {}
            assert service.client is not None

    def test_conversation_history_storage(self, mock_settings):
        """Test conversation history is stored per session"""
        with patch('app.services.claude_service.AsyncAnthropic'):
            service = ClaudeService()

            # Initially empty
            assert service.conversation_history == {}

            # After storing data
            service.conversation_history["session_1"] = [
                {"role": "user", "content": "Hello"}
            ]
            assert "session_1" in service.conversation_history

    def test_clear_history_removes_session(self, mock_settings):
        """Test clearing history removes session data"""
        with patch('app.services.claude_service.AsyncAnthropic'):
            service = ClaudeService()
            service.conversation_history["session_1"] = [{"role": "user", "content": "test"}]

            service.clear_history("session_1")

            assert "session_1" not in service.conversation_history


@pytest.mark.unit
class TestClaudeServiceProcessRequest:
    """Test Claude service request processing"""

    @pytest.mark.asyncio
    async def test_process_request_returns_iterator(self, mock_settings):
        """Test that process_request returns async iterator"""
        with patch('app.services.claude_service.AsyncAnthropic') as mock_anthropic:
            # Mock the stream response
            mock_stream = AsyncMock()
            mock_stream.text_stream = AsyncMock(return_value="test response")
            mock_anthropic.return_value.messages.stream.return_value.__aenter__ = AsyncMock(return_value=mock_stream)
            mock_anthropic.return_value.messages.stream.return_value.__aexit__ = AsyncMock()

            service = ClaudeService()
            response = service.process_request(
                user_input="test",
                context_frame=None,
                context_data=None
            )

            # Should return async iterator
            assert hasattr(response, '__aiter__')

    @pytest.mark.asyncio
    async def test_process_request_yields_thinking_status(self, mock_settings):
        """Test that process_request yields THINKING status first"""
        with patch('app.services.claude_service.AsyncAnthropic') as mock_anthropic:
            mock_stream = AsyncMock()
            mock_stream.text_stream = AsyncMock(return_value="response")
            mock_anthropic.return_value.messages.stream.return_value.__aenter__ = AsyncMock(return_value=mock_stream)
            mock_anthropic.return_value.messages.stream.return_value.__aexit__ = AsyncMock()

            service = ClaudeService()
            responses = []
            async for r in service.process_request("test", None, None):
                responses.append(r)
                break  # Just check first response

            assert responses[0]["type"] == "THINKING"


@pytest.mark.unit
class TestClaudeServiceMessageBuilding:
    """Test message building for Claude API"""

    def test_build_system_message_includes_context(self, mock_settings):
        """Test system message includes viewport context"""
        with patch('app.services.claude_service.AsyncAnthropic'):
            service = ClaudeService()

            context_frame = {"objects": [{"name": "Cube"}]}
            message = service._build_system_message(context_frame)

            assert "Unreal Engine" in message
            assert "1 objects" in message

    def test_build_user_message_includes_scene_info(self, mock_settings):
        """Test user message includes scene object information"""
        with patch('app.services.claude_service.AsyncAnthropic'):
            service = ClaudeService()

            context_frame = {
                "objects": [
                    {"name": "Cube", "type": "StaticMeshActor"},
                    {"name": "Sphere", "type": "StaticMeshActor"}
                ]
            }
            message = service._build_user_message("Create a box", context_frame, None)

            assert "Create a box" in message
            assert "Cube" in message
            assert "Sphere" in message
