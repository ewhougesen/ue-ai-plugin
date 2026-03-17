"""Health check endpoints"""
from fastapi import APIRouter
from pydantic import BaseModel

health_check_router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response"""
    healthy: bool = True
    version: str = "0.1.0"
    services: list[str] = ["http_api", "claude", "asset_manager"]


@health_check_router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse()


@health_check_router.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "UE AI Plugin Backend",
        "version": "0.1.0",
        "status": "running"
    }
