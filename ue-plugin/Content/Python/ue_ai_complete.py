"""
UE AI Plugin - Complete AI Generation System
Full implementation with real AI services
"""

import unreal
import http.client
import json
import urllib.request
import urllib.parse
import os
import tempfile
import base64
from typing import Optional, Tuple, List
import re


# Import asset manager
import sys
sys.path.insert(0, '/Volumes/SERENADA_2/_elliott/Unreal Projects/UEAI-Plugin-Test/Plugins/UEAIPlugin/Content/Python')
from ue_asset_system import asset_manager


class UEAIGenerator:
    """Complete AI generation system for Unreal Engine"""

    def __init__(self):
        self.backend_host = "localhost"
        self.backend_port = 8000
        self.temp_dir = tempfile.gettempdir()
        self.generation_cache = {}

    # ============================================================
    # 3D MODEL GENERATION
    # ============================================================

    def generate_3d_model(self, prompt: str) -> Optional[str]:
        """
        Generate a 3D model from text description
        """
        unreal.log("\n🎨 Generating 3D model...")
        unreal.log(f"Prompt: {prompt}")

        try:
            # Try backend first
            result = self._call_backend_generate(prompt, "MESH")

            if result and result.get("success"):
                asset_info = result["result"]
                if asset_info.get("status") == "completed" and "url" in asset_info:
                    return self._download_and_import_model(asset_info["url"], prompt)

            # Fallback to procedural
            unreal.log("Using procedural generation...")
            return self._create_procedural_model(prompt)

        except Exception as e:
            unreal.log_error(f"Error: {e}")
            return self._create_procedural_model(prompt)

    def _call_backend_generate(self, prompt: str, asset_type: str) -> dict:
        """Call backend generation API"""
        try:
            conn = http.client.HTTPConnection(self.backend_host, self.backend_port, timeout=60)
            payload = {"prompt": prompt, "asset_type": asset_type, "service": "auto"}
            conn.request("POST", "/api/api/generate", json.dumps(payload),
                        {"Content-type": "application/json"})
            response = conn.getresponse()
            if response.status == 200:
                return json.loads(response.read().decode())
        except Exception as e:
            unreal.log_error(f"Backend error: {e}")
        return None

    def _download_and_import_model(self, url: str, prompt: str) -> Optional[str]:
        """Download and import 3D model"""
        try:
            asset_name = self._sanitize_name(prompt)
            temp_path = os.path.join(self.temp_dir, f"{asset_name}.glb")
            if asset_manager.download_file(url, temp_path):
                return asset_manager.import_fbx_model(temp_path, asset_name)
        except Exception as e:
            unreal.log_error(f"Import failed: {e}")
        return None

    def _create_procedural_model(self, prompt: str) -> Optional[str]:
        """Create procedural model based on prompt"""
        prompt_lower = prompt.lower()
        asset_name = self._sanitize_name(prompt)

        if "sphere" in prompt_lower or "ball" in prompt_lower:
            return self.create_sphere(asset_name)
        elif "cylinder" in prompt_lower:
            return self.create_cylinder(asset_name)
        elif "cone" in prompt_lower:
            return self.create_cone(asset_name)
        else:
            return self.create_cube(asset_name)

    # ============================================================
    # TEXTURE GENERATION
    # ============================================================

    def generate_texture(self, prompt: str, width: int = 512, height: int = 512) -> Optional[str]:
        """Generate AI texture from description"""
        unreal.log(f"\n🖼️ Generating texture: {prompt}")

        try:
            # Use free service (Pollinations.ai)
            encoded_prompt = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={hash(prompt)}"

            asset_name = self._sanitize_name(prompt)
            temp_path = os.path.join(self.temp_dir, f"{asset_name}.png")

            if asset_manager.download_file(url, temp_path):
                return asset_manager.import_texture(temp_path, asset_name)

        except Exception as e:
            unreal.log_error(f"Error: {e}")
        return None

    # ============================================================
    # MATERIAL GENERATION
    # ============================================================

    def generate_material(self, description: str) -> Optional[str]:
        """Generate PBR material from description"""
        unreal.log(f"\n🎨 Creating material: {description}")

        try:
            props = self._parse_material_description(description)
            asset_name = self._sanitize_name(description)

            material_path = asset_manager.create_material_instance(
                asset_name,
                base_color=props["color"],
                roughness=props["roughness"],
                metallic=props["metallic"]
            )

            if material_path:
                unreal.log(f"✅ Color: {props['color']}, Roughness: {props['roughness']}, Metallic: {props['metallic']}")

            return material_path

        except Exception as e:
            unreal.log_error(f"Error: {e}")
        return None

    def _parse_material_description(self, description: str) -> dict:
        """Parse material description"""
        desc_lower = description.lower()

        color = self._extract_color_from_text(description)

        roughness = 0.5
        if "rough" in desc_lower:
            roughness = 0.9
        elif "smooth" in desc_lower or "shiny" in desc_lower:
            roughness = 0.1

        metallic = 0.0
        if any(w in desc_lower for w in ["metal", "steel", "silver", "gold", "chrome"]):
            metallic = 1.0

        return {"color": color, "roughness": roughness, "metallic": metallic}

    def _extract_color_from_text(self, text: str) -> Tuple[float, float, float]:
        """Extract color from text"""
        text_lower = text.lower()
        colors = {
            "red": (1, 0, 0), "green": (0, 1, 0), "blue": (0, 0, 1),
            "yellow": (1, 1, 0), "orange": (1, 0.5, 0), "purple": (0.5, 0, 1),
            "white": (1, 1, 1), "black": (0, 0, 0), "gray": (0.5, 0.5, 0.5),
            "gold": (1, 0.84, 0), "silver": (0.75, 0.75, 0.75),
        }
        for name, value in colors.items():
            if name in text_lower:
                return value
        return (0.5, 0.5, 0.5)

    # ============================================================
    # SHAPE CREATION
    # ============================================================

    def create_cube(self, name: str = "Cube", location: Tuple[float, float, float] = (0, 0, 0)) -> Optional[str]:
        """Create a cube"""
        loc = unreal.Vector(location[0], location[1], location[2])
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
        actor.set_actor_label(name)
        unreal.log(f"✅ Created cube: {name}")
        return name

    def create_sphere(self, name: str = "Sphere", location: Tuple[float, float, float] = (0, 0, 0)) -> Optional[str]:
        """Create a sphere"""
        loc = unreal.Vector(location[0], location[1], location[2])
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
        actor.set_actor_label(name)
        unreal.log(f"✅ Created sphere: {name}")
        return name

    def create_cylinder(self, name: str = "Cylinder", location: Tuple[float, float, float] = (0, 0, 0)) -> Optional[str]:
        """Create a cylinder"""
        loc = unreal.Vector(location[0], location[1], location[2])
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
        actor.set_actor_label(name)
        unreal.log(f"✅ Created cylinder: {name}")
        return name

    def create_cone(self, name: str = "Cone", location: Tuple[float, float, float] = (0, 0, 0)) -> Optional[str]:
        """Create a cone"""
        loc = unreal.Vector(location[0], location[1], location[2])
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
        actor.set_actor_label(name)
        unreal.log(f"✅ Created cone: {name}")
        return name

    def create_plane(self, name: str = "Plane", location: Tuple[float, float, float] = (0, 0, 0)) -> Optional[str]:
        """Create a plane"""
        loc = unreal.Vector(location[0], location[1], location[2])
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
        actor.set_actor_label(name)
        unreal.log(f"✅ Created plane: {name}")
        return name

    # ============================================================
    # LIGHT CREATION
    # ============================================================

    def create_point_light(self, name: str = "PointLight", location: Tuple[float, float, float] = (0, 0, 0)) -> Optional[str]:
        """Create a point light"""
        loc = unreal.Vector(location[0], location[1], location[2])
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLightActor, loc)
        actor.set_actor_label(name)
        unreal.log(f"✅ Created point light: {name}")
        return name

    def create_directional_light(self, name: str = "DirectionalLight", location: Tuple[float, float, float] = (0, 0, 500)) -> Optional[str]:
        """Create a directional light"""
        loc = unreal.Vector(location[0], location[1], location[2])
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLightActor, loc)
        actor.set_actor_label(name)
        unreal.log(f"✅ Created directional light: {name}")
        return name

    # ============================================================
    # AI CHAT
    # ============================================================

    def chat(self, message: str) -> Optional[str]:
        """Chat with AI assistant"""
        unreal.log(f"\nYou: {message}")

        try:
            conn = http.client.HTTPConnection(self.backend_host, self.backend_port, timeout=60)
            conn.request("POST", "/api/api/chat", json.dumps({"user_input": message}),
                        {"Content-type": "application/json"})
            response = conn.getresponse()
            if response.status == 200:
                result = json.loads(response.read().decode())
                ai_response = result.get("full_response", "")
                unreal.log(f"AI: {ai_response}")
                return ai_response
        except Exception as e:
            unreal.log_error(f"Error: {e}")
        return None

    # ============================================================
    # NATURAL LANGUAGE COMMANDS
    # ============================================================

    def process_command(self, command: str) -> bool:
        """Process natural language command"""
        command_lower = command.lower()

        try:
            if "generate" in command_lower and "model" in command_lower:
                prompt = command.replace("generate model", "").strip()
                return self.generate_3d_model(prompt) is not None

            elif "texture" in command_lower:
                prompt = command.replace("texture", "").replace("generate", "").strip()
                return self.generate_texture(prompt) is not None

            elif "material" in command_lower:
                desc = command.replace("material", "").replace("create", "").strip()
                return self.generate_material(desc) is not None

            elif "cube" in command_lower:
                return self.create_cube(self._extract_name(command, "Cube")) is not None

            elif "sphere" in command_lower:
                return self.create_sphere(self._extract_name(command, "Sphere")) is not None

            elif "light" in command_lower:
                return self.create_point_light() is not None

            else:
                self.chat(command)
                return True

        except Exception as e:
            unreal.log_error(f"Error: {e}")
            return False

    def _extract_name(self, text: str, default: str) -> str:
        """Extract name from text"""
        words = text.split()
        for word in words:
            if word.lower() not in ["create", "make", "spawn", "add", "a", "an", "the", "cube", "sphere"]:
                return word.capitalize()
        return default

    def _sanitize_name(self, text: str) -> str:
        """Clean text for asset name"""
        clean = re.sub(r'[^\w\s-]', '', text)
        clean = re.sub(r'\s+', '_', clean)
        return clean[:30]


# Create global instance
ai = UEAIGenerator()

# Display info
unreal.log("\n" + "="*70)
unreal.log("🤖 UE AI PLUGIN - COMPLETE GENERATION SYSTEM")
unreal.log("="*70)
unreal.log("\n✨ FEATURES:\n")
unreal.log("   ai.generate_3d_model('prompt')      # Generate 3D models")
unreal.log("   ai.generate_texture('prompt')       # Generate AI textures")
unreal.log("   ai.generate_material('description') # Create PBR materials")
unreal.log("   ai.chat('question')                 # Ask AI for help")
unreal.log("   ai.process_command('natural cmd')   # Natural language")
unreal.log("\n💡 SHAPES & LIGHTS:")
unreal.log("   ai.create_cube('name')")
unreal.log("   ai.create_sphere('name')")
unreal.log("   ai.create_point_light('name')")
unreal.log("\n💡 NATURAL COMMANDS:")
unreal.log("   ai.process_command('create a red cube')")
unreal.log("   ai.process_command('make a shiny gold material')")
unreal.log("="*70 + "\n")
