"""Integration tests for gRPC Server"""
import pytest
from app.grpc_server import UEAIGrpcServicer
from app.services.claude_service import ClaudeService
from app.services.asset_manager import AssetManager
from app.services.ai_service_registry import AIServiceRegistry


@pytest.mark.integration
@pytest.mark.grpc
class TestGRPCServicer:
    """Test gRPC servicer integration"""

    def test_servicer_initialization(self):
        """Test servicer initializes with all services"""
        with pytest.MonkeyPatch.context() as m:
            # Mock the services
            m.setenv("CLAUDE_API_KEY", "test_key")

            servicer = UEAIGrpcServicer(
                claude_service=ClaudeService(),
                asset_manager=AssetManager(),
                ai_registry=AIServiceRegistry()
            )

            assert servicer.claude is not None
            assert servicer.asset_manager is not None
            assert servicer.ai_registry is not None
            assert servicer.active_sessions == {}

    @pytest.mark.asyncio
    async def test_connect_creates_session(self):
        """Test Connect creates a new session"""
        with pytest.MonkeyPatch.context() as m:
            m.setenv("CLAUDE_API_KEY", "test_key")

            servicer = UEAIGrpcServicer(
                claude_service=ClaudeService(),
                asset_manager=AssetManager(),
                ai_registry=AIServiceRegistry()
            )

            # Mock request
            request = MagicMock()
            request.ue_version = "5.5"
            request.plugin_version = "0.1.0"
            request.machine_id = "test_machine"

            # Mock context
            context = MagicMock()
            context.time = MagicMock(return_value=123456)

            response = await servicer.Connect(request, context)

            assert response["success"] is True
            assert "session_id" in response
            assert response["session_id"] in servicer.active_sessions

    @pytest.mark.asyncio
    async def test_send_viewport_frame_returns_analysis(self):
        """Test SendViewportFrame returns frame analysis"""
        with pytest.MonkeyPatch.context() as m:
            m.setenv("CLAUDE_API_KEY", "test_key")

            servicer = UEAIGrpcServicer(
                claude_service=ClaudeService(),
                asset_manager=AssetManager(),
                ai_registry=AIServiceRegistry()
            )

            # Mock request
            request = MagicMock()
            request.width = 1920
            request.height = 1080
            request.timestamp = 1234567890.0
            request.camera_name = "MainCamera"
            request.objects = []

            response = await servicer.SendViewportFrame(request, MagicMock())

            assert "scene_description" in response
            assert "suggested_actions" in response
