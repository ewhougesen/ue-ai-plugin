"""
Configuration settings for UE AI Plugin Backend
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # API Keys
    CLAUDE_API_KEY: str
    MESHY_API_KEY: Optional[str] = None
    CSM_API_KEY: Optional[str] = None
    KAEDEM_API_KEY: Optional[str] = None
    TRIPOSR_API_KEY: Optional[str] = None

    # Server
    GRPC_PORT: int = 50051
    HTTP_PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "debug"

    # Paths
    CACHE_DIR: str = "./cache"
    LOG_DIR: str = "./logs"

    # AI Service Settings
    DEFAULT_AI_SERVICE: str = "meshy"  # Default to use
    ASSET_TIMEOUT_SECONDS: int = 300  # 5 minutes

    # Claude Settings
    CLAUDE_MODEL: str = "claude-3-5-sonnet-20241022"
    CLAUDE_MAX_TOKENS: int = 4096

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
