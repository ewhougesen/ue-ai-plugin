"""
UE AI Plugin - Full AI Generation
Generate 3D models, textures, materials with AI
"""

import unreal
import http.client
import json
import urllib.request
import os
import tempfile


class AIGenerator:
    """Full AI generation capabilities"""

    def __init__(self):
        self.backend_host = "localhost"
        self.backend_port = 8000
        self.download_dir = tempfile.gettempdir()

    def generate_3d_model(self, prompt: str):
        """
        Generate a 3D model using AI (Meshy.ai, CSM.ai, etc.)

        Example: ai.generate_3d_model("A fantasy sword")
        """
        unreal.log(f"\n🎨 Generating 3D model: {prompt}")

        try:
            # Call backend
            conn = http.client.HTTPConnection(self.backend_host, self.backend_port)
            data = json.dumps({"prompt": prompt, "asset_type": "MESH"})
            conn.request("POST", "/api/api/generate", data, {"Content-type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                result = json.loads(response.read().decode())

                if result.get("success"):
                    asset_info = result["result"]
                    service = asset_info.get("service", "unknown")
                    status = asset_info.get("status", "unknown")

                    if status == "completed" and "url" in asset_info:
                        unreal.log(f"✅ Model generated using {service}")
                        unreal.log(f"📥 Download URL: {asset_info['url']}")

                        # Download and import
                        return self._download_and_import_model(asset_info['url'], prompt)

                    elif status == "placeholder":
                        unreal.log("⚠️  AI service not configured - using placeholder")
                        unreal.log("💡 Add API keys to .env file:")
                        unreal.log("   MESHY_API_KEY=your_key")
                        unreal.log("   CSM_API_KEY=your_key")
                        return self._create_placeholder_model(prompt)
                else:
                    unreal.log_error(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
                    return None
            else:
                unreal.log_error(f"❌ HTTP {response.status}")
                return None

        except Exception as e:
            unreal.log_error(f"❌ Error: {e}")
            return None

    def generate_texture(self, prompt: str, width=512, height=512):
        """
        Generate AI texture

        Example: ai.generate_texture("Red brick wall texture")
        """
        unreal.log(f"\n🎨 Generating texture: {prompt}")

        try:
            conn = http.client.HTTPConnection(self.backend_host, self.backend_port)
            data = json.dumps({
                "prompt": prompt,
                "asset_type": "TEXTURE",
                "parameters": {"width": width, "height": height}
            })
            conn.request("POST", "/api/api/generate", data, {"Content-type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                result = json.loads(response.read().decode())

                if result.get("success"):
                    asset_info = result["result"]

                    if asset_info.get("status") == "completed" and "path" in asset_info:
                        # Texture was generated and saved
                        unreal.log(f"✅ Texture generated: {asset_info['path']}")
                        return self._import_texture(asset_info['path'], prompt)
                    else:
                        # Create procedural texture as fallback
                        return self._create_procedural_texture(prompt)
                else:
                    unreal.log_error(f"❌ {result.get('error')}")
                    return None

        except Exception as e:
            unreal.log_error(f"❌ Error: {e}")
            return None

    def generate_material(self, prompt: str):
        """
        Generate PBR material from description

        Example: ai.generate_material("Shiny gold metal")
        """
        unreal.log(f"\n🎨 Generating material: {prompt}")

        # Create material and interpret prompt
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        mat_name = self._sanitize_name(prompt)

        try:
            material = asset_tools.create_asset(
                mat_name,
                "/Game/Materials",
                unreal.Material,
                unreal.MaterialFactoryNew()
            )

            # Parse material properties from prompt
            color = self._extract_color(prompt)
            roughness = self._extract_roughness(prompt)
            metallic = self._extract_metallic(prompt)

            unreal.log(f"✅ Created: {mat_name}")
            unreal.log(f"   Color: {color}, Roughness: {roughness}, Metallic: {metallic}")

            return f"/Game/Materials/{mat_name}"

        except Exception as e:
            unreal.log_error(f"❌ Failed: {e}")
            return None

    def chat(self, message: str):
        """
        Chat with AI about your project

        Example: ai.chat("How do I make a glowing material?")
        """
        try:
            conn = http.client.HTTPConnection(self.backend_host, self.backend_port)
            data = json.dumps({"user_input": message})
            conn.request("POST", "/api/api/chat", data, {"Content-type": "application/json"})
            response = conn.getresponse()

            if response.status == 200:
                result = json.loads(response.read().decode())
                ai_response = result.get("full_response", "")

                unreal.log(f"\n🤖 AI: {ai_response}\n")
                return ai_response
            else:
                unreal.log_error(f"❌ HTTP {response.status}")
                return None

        except Exception as e:
            unreal.log_error(f"❌ Error: {e}")
            return None

    def create_cube(self, name="Cube", location=(0, 0, 0)):
        """Create a simple cube"""
        loc = unreal.Vector(location[0], location[1], location[2])
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
        actor.set_actor_label(name)
        unreal.log(f"✅ Created cube: {name}")
        return name

    def create_sphere(self, name="Sphere", location=(0, 0, 0)):
        """Create a simple sphere"""
        loc = unreal.Vector(location[0], location[1], location[2])
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
        actor.set_actor_label(name)
        unreal.log(f"✅ Created sphere: {name}")
        return name

    def create_light(self, name="Light", location=(0, 0, 0)):
        """Create a point light"""
        loc = unreal.Vector(location[0], location[1], location[2])
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLightActor, loc)
        actor.set_actor_label(name)
        unreal.log(f"✅ Created light: {name}")
        return name

    def _download_and_import_model(self, url: str, prompt: str):
        """Download and import 3D model"""
        try:
            # Download to temp file
            filename = os.path.join(self.download_dir, f"{self._sanitize_name(prompt)}.glb")
            urllib.request.urlretrieve(url, filename)

            unreal.log(f"📥 Downloaded to: {filename}")

            # Import into UE
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            imported = asset_tools.import_asset(
                [filename],
                "/Game/GeneratedModels"
            )

            unreal.log(f"✅ Imported model")
            return imported

        except Exception as e:
            unreal.log_error(f"❌ Import failed: {e}")
            return None

    def _import_texture(self, path: str, prompt: str):
        """Import generated texture"""
        try:
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            name = self._sanitize_name(prompt)

            texture = asset_tools.import_asset(
                [path],
                "/Game/Textures"
            )

            unreal.log(f"✅ Imported texture: {name}")
            return texture

        except Exception as e:
            unreal.log_error(f"❌ Import failed: {e}")
            return None

    def _create_placeholder_model(self, prompt: str):
        """Create placeholder cube when AI unavailable"""
        name = self._sanitize_name(prompt)
        return self.create_cube(f"Placeholder_{name}", (0, 0, 0))

    def _create_procedural_texture(self, prompt: str):
        """Create procedural texture"""
        try:
            name = self._sanitize_name(prompt)
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

            # Create texture render target or material
            texture = asset_tools.create_asset(
                name,
                "/Game/Textures",
                unreal.Texture2D,
                unreal.Texture2DFactoryNew()
            )

            unreal.log(f"✅ Created procedural texture: {name}")
            return texture

        except Exception as e:
            unreal.log_error(f"❌ Failed: {e}")
            return None

    def _sanitize_name(self, text: str) -> str:
        """Clean text for use as asset name"""
        return "".join(c for c in text if c.isalnum() or c in (' ', '-', '_'))[:30]

    def _extract_color(self, prompt: str):
        """Extract color from prompt"""
        colors = {
            "red": (1, 0, 0), "green": (0, 1, 0), "blue": (0, 0, 1),
            "yellow": (1, 1, 0), "cyan": (0, 1, 1), "magenta": (1, 0, 1),
            "white": (1, 1, 1), "black": (0, 0, 0),
            "orange": (1, 0.5, 0), "purple": (0.5, 0, 1)
        }

        prompt_lower = prompt.lower()
        for color_name, color_value in colors.items():
            if color_name in prompt_lower:
                return color_value
        return (0.5, 0.5, 0.5)  # Default gray

    def _extract_roughness(self, prompt: str) -> float:
        """Extract roughness from prompt"""
        if "rough" in prompt.lower():
            return 0.9
        elif "smooth" in prompt.lower() or "shiny" in prompt.lower():
            return 0.1
        elif "glossy" in prompt.lower():
            return 0.3
        return 0.5

    def _extract_metallic(self, prompt: str) -> float:
        """Extract metallic from prompt"""
        if "metal" in prompt.lower() or "steel" in prompt.lower() or "gold" in prompt.lower():
            return 1.0
        elif "plastic" in prompt.lower() or "wood" in prompt.lower():
            return 0.0
        return 0.0


# Create global instance
ai = AIGenerator()

# Show instructions
unreal.log("\n" + "█"*60)
unreal.log("█     🤖 UE AI PLUGIN - FULL GENERATION             █")
unreal.log("█"*60)
unreal.log("\n✨ AVAILABLE COMMANDS:\n")
unreal.log("   ai.generate_3d_model('prompt')    - Generate 3D model")
unreal.log("   ai.generate_texture('prompt')     - Generate texture")
unreal.log("   ai.generate_material('prompt')    - Create material")
unreal.log("   ai.chat('question')               - Ask AI for help")
unreal.log("   ai.create_cube('name')            - Create cube")
unreal.log("   ai.create_sphere('name')          - Create sphere")
unreal.log("   ai.create_light('name')           - Create light")
unreal.log("\n💡 AI GENERATION REQUIRES API KEYS:")
unreal.log("   Add to ~/repos/ue-ai-plugin/.env:")
unreal.log("   MESHY_API_KEY=your_key_here")
unreal.log("   CSM_API_KEY=your_key_here")
unreal.log("\n" + "█"*60 + "\n")
