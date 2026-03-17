"""Unit tests for configuration settings"""
import pytest
from app.config import Settings, settings


class TestSettings:
    """Test Settings configuration"""

    def test_settings_has_required_attributes(self):
        """Test that Settings has all required attributes"""
        required_attrs = [
            'CLAUDE_API_KEY',
            'GRPC_PORT',
            'HTTP_PORT',
            'ENVIRONMENT',
            'LOG_LEVEL'
        ]

        for attr in required_attrs:
            assert hasattr(settings, attr), f"Settings missing {attr}"

    def test_default_grpc_port(self):
        """Test default gRPC port is 50051"""
        assert settings.GRPC_PORT == 50051

    def test_default_http_port(self):
        """Test default HTTP port is 8000"""
        assert settings.HTTP_PORT == 8000

    def test_claude_api_key_exists(self):
        """Test Claude API key is configured"""
        assert settings.CLAUDE_API_KEY
        assert len(settings.CLAUDE_API_KEY) > 0

    def test_cache_directory_exists(self):
        """Test cache directory path is set"""
        assert hasattr(settings, 'CACHE_DIR')
        assert isinstance(settings.CACHE_DIR, str)

    def test_log_directory_exists(self):
        """Test log directory path is set"""
        assert hasattr(settings, 'LOG_DIR')
        assert isinstance(settings.LOG_DIR, str)


class TestSettingsValidation:
    """Test Settings validation"""

    def test_invalid_port_raises_error(self, monkeypatch):
        """Test that invalid port configuration raises error"""
        monkeypatch.setenv("GRPC_PORT", "invalid")
        with pytest.raises(Exception):
            Settings()

    def test_missing_api_key_raises_error(self, monkeypatch):
        """Test that missing Claude API key raises error"""
        monkeypatch.setenv("CLAUDE_API_KEY", "")
        with pytest.raises(Exception):
            Settings()
