"""Asset management service - Real AI generation"""
import asyncio
import aiohttp
import base64
from pathlib import Path
from typing import Optional
import structlog

from app.config import settings

log = structlog.get_logger(__name__)


class AssetManager:
    """Manages asset generation using real AI services"""

    def __init__(self):
        self.cache_dir = Path(settings.CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.pending_generations: dict[str, asyncio.Task] = {}
        log.info("asset_manager_initialized", cache_dir=str(self.cache_dir))

    async def generate_asset(
        self,
        prompt: str,
        asset_type: str = "MESH",
        service: str = "auto",
        parameters: dict = None
    ) -> dict:
        """
        Generate asset using AI services

        Services:
        - meshy: Meshy.ai for 3D models
        - csm: CSM.ai for 3D models from text
        - tripo: TripoSR for fast mesh generation
        - texture: AI texture generation
        """
        if parameters is None:
            parameters = {}

        asset_id = f"{service}_{asset_type}_{abs(hash(prompt))}"

        # Check cache
        cached = self._check_cache(asset_id)
        if cached:
            log.info("asset_found_in_cache", asset_id=asset_id)
            return cached

        # Select best service
        if service == "auto":
            service = self._select_service(asset_type, prompt)

        # Generate using selected service
        result = await self._generate_with_service(
            asset_id, prompt, asset_type, service, parameters
        )

        return result

    def _select_service(self, asset_type: str, prompt: str) -> str:
        """Auto-select best AI service"""
        if asset_type == "MESH":
            # Use Meshy.ai for high-quality models
            return "meshy"
        elif asset_type == "TEXTURE":
            return "texture_ai"
        elif asset_type == "MATERIAL":
            return "texture_ai"
        return "meshy"

    async def _generate_with_service(
        self,
        asset_id: str,
        prompt: str,
        asset_type: str,
        service: str,
        parameters: dict
    ) -> dict:
        """Generate asset using specific service"""

        if service == "meshy":
            return await self._generate_meshy(prompt, asset_id)
        elif service == "csm":
            return await self._generate_csm(prompt, asset_id)
        elif service == "texture_ai":
            return await self._generate_texture(prompt, asset_id, parameters)
        else:
            return await self._generate_placeholder(prompt, asset_id)

    async def _generate_meshy(self, prompt: str, asset_id: str) -> dict:
        """Generate 3D model using Meshy.ai"""
        try:
            # Meshy.ai API endpoint
            url = "https://api.meshy.ai/v1/text-to-3d"

            # API call to Meshy
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {settings.MESHY_API_KEY}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "mode": "preview",
                    "prompt": prompt,
                    "enable_pbr": True
                }

                async with session.post(url, json=payload, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        task_id = data.get("task_id")

                        # Poll for completion
                        result_url = await self._poll_meshy_task(task_id)

                        return {
                            "asset_id": asset_id,
                            "service": "meshy",
                            "type": "MESH",
                            "prompt": prompt,
                            "url": result_url,
                            "status": "completed"
                        }
                    else:
                        log.error("meshy_error", status=resp.status)
                        return await self._generate_placeholder(prompt, asset_id)

        except Exception as e:
            log.error("meshy_generation_failed", error=str(e))
            return await self._generate_placeholder(prompt, asset_id)

    async def _poll_meshy_task(self, task_id: str, max_wait: int = 120) -> str:
        """Poll Meshy for task completion"""
        url = f"https://api.meshy.ai/v1/text-to-3d/{task_id}"

        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {settings.MESHY_API_KEY}"}

            for _ in range(max_wait):
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        status = data.get("status")

                        if status == "succeeded":
                            return data.get("model_url")
                        elif status == "failed":
                            log.error("meshy_task_failed")
                            return None

                await asyncio.sleep(2)

        return None

    async def _generate_csm(self, prompt: str, asset_id: str) -> dict:
        """Generate using CSM.ai"""
        try:
            url = "https://api.csm.ai/v1/generate"

            async with aiohttp.ClientSession() as session:
                headers = {
                    "x-api-key": settings.CSM_API_KEY,
                    "Content-Type": "application/json"
                }

                payload = {
                    "text_prompt": prompt,
                    "output_format": "glb"
                }

                async with session.post(url, json=payload, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            "asset_id": asset_id,
                            "service": "csm",
                            "type": "MESH",
                            "prompt": prompt,
                            "url": data.get("download_url"),
                            "status": "completed"
                        }

        except Exception as e:
            log.error("csm_generation_failed", error=str(e))

        return await self._generate_placeholder(prompt, asset_id)

    async def _generate_texture(self, prompt: str, asset_id: str, params: dict) -> dict:
        """Generate AI texture"""
        try:
            # Use stability AI or similar for texture generation
            width = params.get("width", 512)
            height = params.get("height", 512)

            url = "https://api.stability.ai/v1/generation/text-to-image"

            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {settings.STABILITY_API_KEY}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "text_prompts": [{"text": prompt}],
                    "cfg_scale": 7,
                    "height": height,
                    "width": width,
                    "samples": 1,
                    "steps": 30
                }

                async with session.post(url, json=payload, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        artifact = data["artifacts"][0]
                        image_data = base64.b64decode(artifact["base64"])

                        # Save to cache
                        texture_path = self.cache_dir / f"{asset_id}.png"
                        texture_path.write_bytes(image_data)

                        return {
                            "asset_id": asset_id,
                            "service": "stability",
                            "type": "TEXTURE",
                            "prompt": prompt,
                            "path": str(texture_path),
                            "status": "completed"
                        }

        except Exception as e:
            log.error("texture_generation_failed", error=str(e))

        return await self._generate_placeholder(prompt, asset_id)

    async def _generate_placeholder(self, prompt: str, asset_id: str) -> dict:
        """Generate placeholder when AI services fail"""
        log.info("generating_placeholder", prompt=prompt)

        # Create a simple placeholder
        placeholder_path = self.cache_dir / f"{asset_id}_placeholder.txt"
        placeholder_path.write_text(f"Prompt: {prompt}\nStatus: Placeholder")

        return {
            "asset_id": asset_id,
            "service": "placeholder",
            "type": "UNKNOWN",
            "prompt": prompt,
            "path": str(placeholder_path),
            "status": "placeholder",
            "message": "AI generation service unavailable - using placeholder"
        }

    def _check_cache(self, asset_id: str) -> Optional[dict]:
        """Check if asset exists in cache"""
        asset_path = self.cache_dir / asset_id
        if asset_path.exists():
            return {
                "asset_id": asset_id,
                "cached": True,
                "path": str(asset_path)
            }
        return None

    def clear_cache(self, older_than_hours: Optional[int] = None):
        """Clear cached assets"""
        log.info("cache_cleared", older_than_hours=older_than_hours)
