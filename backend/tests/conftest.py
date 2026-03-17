"""Pytest configuration and fixtures"""
import asyncio
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
import pytest

# Set test environment before importing app code
os.environ["ENVIRONMENT"] = "test"
os.environ["LOG_LEVEL"] = "warning"


@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_claude_api():
    """Mock Claude API client"""
    mock = AsyncMock()
    mock.messages.stream = AsyncMock()
    return mock


@pytest.fixture
def mock_settings():
    """Mock application settings"""
    from app.config import Settings

    return Settings(
        CLAUDE_API_KEY="test_key",
        GRPC_PORT=50051,
        HTTP_PORT=8000,
        ENVIRONMENT="test",
        LOG_LEVEL="warning",
        CACHE_DIR="/tmp/test_cache",
        LOG_DIR="/tmp/test_logs"
    )


@pytest.fixture
def sample_viewport_frame():
    """Sample viewport frame data"""
    return {
        "image_data": b"fake_image_data",
        "width": 1920,
        "height": 1080,
        "timestamp": 1234567890.0,
        "camera_name": "MainCamera",
        "objects": [
            {
                "name": "Cube",
                "type": "StaticMeshActor",
                "location": {"x": 0, "y": 0, "z": 0},
                "rotation": {"x": 0, "y": 0, "z": 0},
                "scale": {"x": 1, "y": 1, "z": 1}
            }
        ]
    }


@pytest.fixture
def sample_process_request():
    """Sample process request data"""
    return {
        "session_id": "test_session_123",
        "user_input": "Create a red sphere",
        "context_frame": None,
        "context_data": {"project": "TestProject"}
    }
