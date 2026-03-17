"""gRPC server implementation for UE AI Plugin"""
import asyncio
import structlog
from typing import AsyncIterator

from app.config import settings
from app.services.claude_service import ClaudeService
from app.services.asset_manager import AssetManager
from app.services.ai_service_registry import AIServiceRegistry


log = structlog.get_logger(__name__)


class UEAIGrpcServicer:
    """
    Main gRPC servicer for UE-AI communication

    Handles all gRPC calls from the Unreal Engine plugin
    """

    def __init__(
        self,
        claude_service: ClaudeService,
        asset_manager: AssetManager,
        ai_registry: AIServiceRegistry
    ):
        self.claude = claude_service
        self.asset_manager = asset_manager
        self.ai_registry = ai_registry
        self.active_sessions: dict[str, dict] = {}
        log.info("grpc_servicer_initialized")

    async def Connect(self, request, context):
        """Handle initial connection from UE plugin"""
        session_id = f"session_{request.machine_id}_{context.time()}"

        self.active_sessions[session_id] = {
            "ue_version": request.ue_version,
            "plugin_version": request.plugin_version,
            "machine_id": request.machine_id,
            "connected_at": context.time()
        }

        log.info("client_connected",
                 session_id=session_id,
                 ue_version=request.ue_version,
                 plugin_version=request.plugin_version)

        # Return response (will be proper proto message)
        return {
            "success": True,
            "session_id": session_id,
            "server_version": "0.1.0"
        }

    async def SendViewportFrame(self, request, context):
        """Analyze viewport frame and return scene understanding"""
        log.debug("received_viewport_frame",
                  width=request.width,
                  height=request.height,
                  object_count=len(request.objects))

        # For now, return basic analysis
        # Will be enhanced with vision models
        detected_objects = []
        for obj in request.objects:
            detected_objects.append({
                "name": obj.name,
                "type": obj.type,
                "confidence": 1.0,
                "bounds": {
                    "min": {"x": 0, "y": 0, "z": 0},
                    "max": {"x": 1, "y": 1, "z": 1}
                }
            })

        scene_description = f"Scene contains {len(detected_objects)} objects"

        return {
            "detected_objects": detected_objects,
            "scene_description": scene_description,
            "suggested_actions": ["analyze_scene", "create_asset", "modify_material"]
        }

    async def ProcessRequest(self, request, context):
        """Process natural language request with streaming response"""
        log.info("processing_request",
                 session_id=request.session_id,
                 user_input=request.user_input[:100])

        try:
            # Stream responses from Claude
            async for response in self.claude.process_request(
                user_input=request.user_input,
                context_frame=request.context_frame,
                context_data=request.context_data
            ):
                yield response

        except Exception as e:
            log.error("request_processing_failed",
                     session_id=request.session_id,
                     error=str(e))
            yield {
                "type": "ERROR",
                "content": f"Error processing request: {str(e)}"
            }

    async def ExecuteAction(self, request, context):
        """Execute action in Unreal Engine"""
        log.info("executing_action",
                 session_id=request.session_id,
                 action_type=request.action.type,
                 target=request.action.target)

        # This will be implemented to return action data for UE to execute
        return {
            "success": True,
            "message": f"Action {request.action.type} queued for execution",
            "result_data": {}
        }

    async def GenerateAsset(self, request, context):
        """Generate asset using AI services with progress updates"""
        log.info("generating_asset",
                 session_id=request.session_id,
                 asset_type=request.type,
                 prompt=request.prompt[:100])

        try:
            # Select best AI service for this request
            service = self.ai_registry.select_service(
                asset_type=request.type,
                preferred=request.preferred_service
            )

            # Stream generation progress
            async for progress in service.generate(
                prompt=request.prompt,
                asset_type=request.type,
                parameters=request.parameters
            ):
                yield progress

        except Exception as e:
            log.error("asset_generation_failed",
                     session_id=request.session_id,
                     error=str(e))
            yield {
                "progress": 0,
                "status": f"Error: {str(e)}",
                "warnings": [str(e)]
            }

    async def HealthCheck(self, request, context):
        """Health check via gRPC"""
        return {
            "healthy": True,
            "version": "0.1.0",
            "active_services": ["grpc", "claude", "asset_manager"]
        }
