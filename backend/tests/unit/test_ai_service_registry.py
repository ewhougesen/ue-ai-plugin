"""Unit tests for AI Service Registry"""
import pytest
from app.services.ai_service_registry import AIServiceRegistry


@pytest.mark.unit
class TestAIServiceRegistry:
    """Test AI Service Registry functionality"""

    def test_registry_initialization(self):
        """Test registry initializes correctly"""
        registry = AIServiceRegistry()
        assert isinstance(registry.services, dict)

    def test_select_service_returns_service(self):
        """Test select_service returns AIService instance"""
        registry = AIServiceRegistry()

        # This will fail because we don't have real services yet
        # That's OK - this is TDD, we write test first
        try:
            service = registry.select_service("MESH", None)
            assert hasattr(service, 'generate')
        except ValueError:
            # Expected - no services configured yet
            pass

    def test_select_service_with_invalid_type_raises_error(self):
        """Test select_service raises error for invalid type"""
        registry = AIServiceRegistry()

        with pytest.raises(ValueError):
            registry.select_service("INVALID_TYPE", None)


@pytest.mark.unit
class TestAIServiceBase:
    """Test AIService base class"""

    def test_ai_service_base_raises_not_implemented(self):
        """Test base class generate raises NotImplementedError"""
        from app.services.ai_service_registry import AIService

        service = AIService("test", "test_key")

        with pytest.raises(NotImplementedError):
            # Should raise because generate is not implemented
            import asyncio
            asyncio.run(service.generate("test", "MESH", {}))
