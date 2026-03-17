"""AI Service Registry - manages multiple AI generation services"""
from typing import Optional, Dict, Type
import structlog

from app.config import settings


log = structlog.get_logger(__name__)


class AIServiceRegistry:
    """
    Registry and router for AI generation services

    Selects the best service for each request based on:
    - Asset type
    - User preference
    - Service availability
    - Quality requirements
    """

    def __init__(self):
        self.services: Dict[str, 'AIService'] = {}
        self._initialize_services()
        log.info("ai_service_registry_initialized",
                 service_count=len(self.services))

    def _initialize_services(self):
        """Initialize available AI services"""
        # Services will be initialized here
        # For now, placeholders
        available = []
        if settings.MESHY_API_KEY:
            available.append("meshy")
        if settings.CSM_API_KEY:
            available.append("csm")
        if settings.KAEDEM_API_KEY:
            available.append("kaedim")

        log.info("available_ai_services", services=available)

    def select_service(
        self,
        asset_type: str,
        preferred: Optional[str] = None
    ) -> 'AIService':
        """
        Select the best AI service for this request

        Selection logic:
        1. Use preferred service if specified and available
        2. Select based on asset type capabilities
        3. Fall back to default service
        """
        if preferred and preferred in self.services:
            log.info("using_preferred_service", service=preferred)
            return self.services[preferred]

        # Select based on asset type
        service_name = self._select_by_type(asset_type)

        if service_name and service_name in self.services:
            return self.services[service_name]

        # Fall back to default
        default = settings.DEFAULT_AI_SERVICE
        if default in self.services:
            return self.services[default]

        # No service available
        raise ValueError(f"No AI service available for asset type: {asset_type}")

    def _select_by_type(self, asset_type: str) -> Optional[str]:
        """Select best service based on asset type"""
        # Service selection logic based on capabilities
        selection_map = {
            "MESH": ["meshy", "kaedim", "csm"],
            "MATERIAL": ["meshy", "csm"],
            "TEXTURE": ["meshy", "csm"],
            "ANIMATION": ["kaedim"],
        }

        options = selection_map.get(asset_type.upper(), [])

        for service_name in options:
            if service_name in self.services:
                return service_name

        return None

    async def generate(
        self,
        prompt: str,
        asset_type: str,
        parameters: dict,
        preferred: Optional[str] = None
    ):
        """Generate asset using selected service"""
        service = self.select_service(asset_type, preferred)
        return await service.generate(prompt, asset_type, parameters)


class AIService:
    """Base class for AI service integrations"""

    def __init__(self, name: str, api_key: str):
        self.name = name
        self.api_key = api_key
        self.capabilities = []

    async def generate(self, prompt: str, asset_type: str, parameters: dict):
        """Generate asset - to be implemented by subclasses"""
        raise NotImplementedError
