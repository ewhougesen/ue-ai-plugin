"""
Configuration settings for UE AI Plugin Backend
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # z.ai API Configuration
    ANTHROPIC_AUTH_TOKEN: str
    ANTHROPIC_BASE_URL: str = "https://api.z.ai/api/anthropic"
    API_TIMEOUT_MS: int = 180000

    # Claude Code Settings
    CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: str = "1"
    CLAUDE_CODE_DISABLE_TELEMETRY: str = "1"
    CLAUDE_CODE_STRICT_MODEL_ROUTING: str = "1"

    # Model Routing
    ANTHROPIC_DEFAULT_OPUS_MODEL: str = "glm-5"
    ANTHROPIC_DEFAULT_SONNET_MODEL: str = "glm-4.7"
    ANTHROPIC_DEFAULT_HAIKU_MODEL: str = "glm-4.5-air"
    ANTHROPIC_MAX_RETRIES: int = 2
    ANTHROPIC_STREAMING: str = "1"

    # AI Service Keys (Meshy, CSM, Kaedim, etc.)
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
    DEFAULT_AI_SERVICE: str = "meshy"
    ASSET_TIMEOUT_SECONDS: int = 300  # 5 minutes

    # Claude Settings (mapped to z.ai models)
    CLAUDE_MODEL: str = None  # Will use ANTHROPIC_DEFAULT_SONNET_MODEL
    CLAUDE_MAX_TOKENS: int = 4096

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_claude_model(self) -> str:
        """Get the appropriate Claude model for z.ai"""
        if self.CLAUDE_MODEL:
            return self.CLAUDE_MODEL
        return self.ANTHROPIC_DEFAULT_SONNET_MODEL


# Global settings instance
settings = Settings()
