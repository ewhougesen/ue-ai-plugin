"""API routes for UE AI Plugin"""
from fastapi import APIRouter
import structlog

from app.services.claude_service import ClaudeService
from app.services.asset_manager import AssetManager
from app.config import settings

log = structlog.get_logger(__name__)

api_router = APIRouter()

# Services will be initialized at app startup
claude_service: ClaudeService = None
asset_manager: AssetManager = None


def set_services(claude: ClaudeService, asset: AssetManager):
    """Set service instances"""
    global claude_service, asset_manager
    claude_service = claude
    asset_manager = asset


@api_router.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "UE AI Plugin API",
        "version": "0.1.0",
        "status": "running"
    }


@api_router.post("/api/chat")
async def chat(request: dict):
    """Process chat request through Claude"""
    if not claude_service:
        return {"error": "Service not initialized"}

    user_input = request.get("user_input", "")
    context_data = request.get("context_data", {})

    if not user_input:
        return {"error": "user_input is required"}

    log.info("chat_request", user_input=user_input[:100])

    try:
        # Collect streaming responses
        responses = []
        async for response in claude_service.process_request(
            user_input=user_input,
            context_frame=None,
            context_data=context_data
        ):
            responses.append(response)

        # Return full response
        return {
            "success": True,
            "responses": responses,
            "full_response": responses[-1].get("content", "") if responses else ""
        }
    except Exception as e:
        log.error("chat_error", error=str(e))
        return {"error": str(e)}


@api_router.post("/api/generate")
async def generate_asset(request: dict):
    """Generate asset using AI services (Meshy, CSM, Stability AI, etc.)"""
    if not asset_manager:
        return {"error": "Service not initialized"}

    prompt = request.get("prompt", "")
    asset_type = request.get("asset_type", "MESH")
    service = request.get("service", "auto")
    parameters = request.get("parameters", {})

    if not prompt:
        return {"error": "prompt is required"}

    log.info("asset_generation_request",
             asset_type=asset_type,
             service=service,
             prompt=prompt[:100])

    try:
        result = await asset_manager.generate_asset(
            prompt=prompt,
            asset_type=asset_type,
            service=service,
            parameters=parameters
        )

        if "error" in result:
            return {"error": result["error"]}

        return {
            "success": True,
            "result": result,
            "message": f"Generated {asset_type} using {result.get('service', service)}"
        }
    except Exception as e:
        log.error("asset_generation_error", error=str(e))
        return {"error": str(e)}
