"""
UE AI Plugin - Backend Server
Main entry point for the gRPC server
"""
import asyncio
import logging
from pathlib import Path

import structlog
from fastapi import FastAPI
from grpc import aio
from uvicorn import run

from app.config import settings
from app.grpc_server import UEAIGrpcServicer
from app.health import health_check_router
from app.services.claude_service import ClaudeService
from app.services.asset_manager import AssetManager
from app.services.ai_service_registry import AIServiceRegistry

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

log = structlog.get_logger(__name__)


# Initialize FastAPI for health checks
app = FastAPI(title="UE AI Plugin Backend", version="0.1.0")
app.include_router(health_check_router)


async def serve():
    """Start the gRPC server"""
    log.info("starting_ue_ai_backend",
             version="0.1.0",
             grpc_port=settings.GRPC_PORT,
             http_port=settings.HTTP_PORT)

    # Initialize services
    claude_service = ClaudeService()
    asset_manager = AssetManager()
    ai_registry = AIServiceRegistry()

    # Create gRPC server
    server = aio.server()
    servicer = UEAIGrpcServicer(
        claude_service=claude_service,
        asset_manager=asset_manager,
        ai_registry=ai_registry
    )

    # Register servicer (will be done after proto compilation)
    # ue_ai_pb2_grpc.add_UEAIPluginServicer_to_server(servicer, server)

    server.add_insecure_port(f'[::]:{settings.GRPC_PORT}')
    await server.start()

    log.info("grpc_server_started", port=settings.GRPC_PORT)

    # Keep server running
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        log.info("shutting_down_server")
        await server.stop(0)


if __name__ == '__main__':
    # Run HTTP server in background, gRPC in foreground
    import threading

    def run_http():
        run(app, host="0.0.0.0", port=settings.HTTP_PORT, log_level="info")

    http_thread = threading.Thread(target=run_http, daemon=True)
    http_thread.start()

    asyncio.run(serve())
