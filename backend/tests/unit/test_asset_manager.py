"""Unit tests for Asset Manager"""
import pytest
from pathlib import Path
from app.services.asset_manager import AssetManager


@pytest.mark.unit
class TestAssetManager:
    """Test Asset Manager initialization and basic functionality"""

    def test_asset_manager_initialization(self):
        """Test Asset Manager initializes correctly"""
        manager = AssetManager()
        assert manager.cache_dir.exists()
        assert manager.pending_generations == {}

    def test_cache_directory_created(self, tmp_path):
        """Test cache directory is created on init"""
        import tempfile
        from app.config import settings

        with tempfile.TemporaryDirectory() as tmp:
            settings.CACHE_DIR = tmp
            manager = AssetManager()
            assert Path(tmp).exists()


@pytest.mark.unit
class TestAssetGeneration:
    """Test asset generation functionality"""

    @pytest.mark.asyncio
    async def test_generate_asset_returns_dict(self):
        """Test generate_asset returns dict with asset_id"""
        manager = AssetManager()

        result = await manager.generate_asset(
            prompt="test cube",
            asset_type="MESH",
            service="test",
            parameters={}
        )

        assert isinstance(result, dict)
        assert "asset_id" in result

    @pytest.mark.asyncio
    async def test_generate_asset_creates_unique_id(self):
        """Test each generation gets unique asset_id"""
        manager = AssetManager()

        result1 = await manager.generate_asset("test", "MESH", "service", {})
        result2 = await manager.generate_asset("test2", "MESH", "service", {})

        assert result1["asset_id"] != result2["asset_id"]


@pytest.mark.unit
class TestAssetCaching:
    """Test asset caching functionality"""

    def test_check_cache_returns_none_for_missing(self):
        """Test cache check returns None for non-existent asset"""
        manager = AssetManager()
        result = manager._check_cache("nonexistent_id")
        assert result is None

    def test_check_cache_returns_data_for_cached(self, tmp_path):
        """Test cache check returns data for cached asset"""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            from app.config import settings
            settings.CACHE_DIR = tmp

            manager = AssetManager()

            # Create fake cached file
            cache_path = Path(tmp) / "test_asset_id"
            cache_path.touch()

            result = manager._check_cache("test_asset_id")
            assert result is not None
            assert result["cached"] is True
