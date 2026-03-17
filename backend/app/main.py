"""
UE AI Plugin - Backend Server (HTTP API MVP)
Main entry point for FastAPI server
"""
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog
from uvicorn import run

from app.config import settings
from app.health import health_check_router
from app import api  # Changed from app.api.routes
from app.services.claude_service import ClaudeService
from app.services.asset_manager import AssetManager

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

log = structlog.get_logger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="UE AI Plugin Backend",
    version="0.1.0",
    description="AI-powered copilot for Unreal Engine 5"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_check_router)
app.include_router(api.api_router, prefix="/api")

# Initialize services
claude_service = ClaudeService()
asset_manager = AssetManager()

# Set services in API module
api.set_services(claude_service, asset_manager)

# Startup event
@app.on_event("startup")
async def startup_event():
    log.info("ue_ai_backend_started",
             version="0.1.0",
             environment=settings.ENVIRONMENT,
             base_url=settings.ANTHROPIC_BASE_URL,
             model=settings.get_claude_model())


@app.on_event("shutdown")
async def shutdown_event():
    log.info("ue_ai_backend_shutting_down")


if __name__ == '__main__':
    run(
        app,
        host="0.0.0.0",
        port=settings.HTTP_PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
