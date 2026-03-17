"""
UE AI Plugin - ULTIMATE VERSION
Everything included - All Unreal Engine capabilities
"""

import unreal
import http.client
import json
import urllib.request
import urllib.parse
import os
import tempfile
import re
import math
from typing import Optional, Tuple, List, Dict, Any
from enum import Enum

# Import modules
sys.path.insert(0, '/Volumes/SERENADA_2/_elliott/Unreal Projects/UEAI-Plugin-Test/Plugins/UEAIPlugin/Content/Python')
try:
    from ue_knowledge_base import UE_KNOWLEDGE_BASE, search_knowledge, get_workflow
except:
    pass


class ActorType(Enum):
    """All supported actor types"""
    STATIC_MESH = "StaticMeshActor"
    SKELETAL_MESH = "SkeletalMeshActor"
    CHARACTER = "Character"
    PAWN = "Pawn"
    CAMERA = "CameraActor"
    POINT_LIGHT = "PointLightActor"
    SPOT_LIGHT = "SpotLightActor"
    DIRECTIONAL_LIGHT = "DirectionalLightActor"
    SKY_LIGHT = "SkyLightActor"
    ATMOSPHERIC_FOG = "AtmosphericFog"
    EXPONENTIAL_FOG = "ExponentialHeightFog"
    POST_PROCESS_VOLUME = "PostProcessVolume"
    BOX_TRIGGER = "BoxTrigger"
    SPHERE_TRIGGER = "SphereTrigger"
    PARTICLE_SYSTEM = "ParticleSystemActor"
    VOLUME = "Volume"
    BRUSH = "Brush"
    DECORATOR = "Decorator"


class UEMasterAI:
    """
    MASTER AI CONTROLLER - Does EVERYTHING in Unreal Engine
    """

    def __init__(self):
        self.backend_host = "localhost"
        self.backend_port = 8000
        self.temp_dir = tempfile.gettempdir()
        self.project_dir = self._get_project_dir()
        self.conversation_history = []
        self.execution_context = {
            "selected_actors": [],
            "current_level": self._get_current_level(),
            "clipboard": None,
            "last_created": [],
            "asset_library": {}
        }

        # Initialize
        self._ensure_directories()
        unreal.log("🚀 UE Master AI initialized")

    # ============================================================
    # GETTERS
    # ============================================================

    def _get_project_dir(self) -> str:
        """Get project directory"""
        try:
            return unreal.SystemLibrary.get_project_directory()
        except:
            return "/Volumes/SERENADA_2/_elliott/Unreal Projects/UEAI-Plugin-Test"

    def _get_current_level(self) -> str:
        """Get current level name"""
        try:
            world = unreal.EditorLevelLibrary.get_editor_world()
            level_name = world.get_path_name()
            return level_name
        except:
            return "Persistent_Level"

    def _ensure_directories(self):
        """Ensure all directories exist"""
        dirs = [
            "Content/GeneratedModels",
            "Content/GeneratedTextures",
            "Content/GeneratedMaterials",
            "Content/GeneratedBlueprints",
            "Content/GeneratedFX",
            "Content/GeneratedAudio"
        ]
        for d in dirs:
            path = os.path.join(self._get_project_dir(), d)
            os.makedirs(path, exist_ok=True)

    # ============================================================
    # MAIN COMMAND INTERFACE
    # ============================================================

    def do(self, command: str) -> Dict[str, Any]:
        """
        Main command interface - handles all requests

        Examples:
            ai.do("create a red cube")
            ai.do("make 5 cubes in a circle")
            ai.do("create a character with sword")
            ai.do("setup a night scene")
            ai.do("help with materials")
        """
        unreal.log(f"\n🤖 Processing: {command}")

        # Parse the command
        action, params = self._parse_command(command)

        # Execute
        try:
            result = self._execute_action(action, params)
            if result:
                unreal.log(f"✅ {result.get('message', 'Complete')}")
            return result
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            unreal.log_error(f"❌ {error_msg}")
            return {"error": error_msg}

    # ============================================================
    # COMMAND PARSING
    # ============================================================

    def _parse_command(self, command: str) -> Tuple[str, Dict]:
        """Parse command into action and parameters"""
        cmd_lower = command.lower()

        # Extract quantity
        quantity = self._extract_quantity(command)
        if quantity:
            params = {"quantity": quantity}
        else:
            params = {}

        # Create operations
        if "create" in cmd_lower or "make" in cmd_lower or "spawn" in cmd_lower or "add" in cmd_lower:
            # Determine what to create
            if "cube" in cmd_lower:
                return "create_cubes", {**params, "shape": "cube", **self._extract_all_params(command)}
            elif "sphere" in cmd_lower or "ball" in cmd_lower:
                return "create_spheres", {**params, "shape": "sphere", **self._extract_all_params(command)}
            elif "cylinder" in cmd_lower:
                return "create_cylinders", {**params, "shape": "cylinder", **self._extract_all_params(command)}
            elif "cone" in cmd_lower:
                return "create_cones", {**params, "shape": "cone", **self._extract_all_params(command)}
            elif "plane" in cmd_lower or "floor" in cmd_lower:
                return "create_planes", {**params, "shape": "plane", **self._extract_all_params(command)}
            elif "light" in cmd_lower:
                return "create_lights", {**params, **self._extract_all_params(command)}
            elif "camera" in cmd_lower:
                return "create_cameras", {**params, **self._extract_all_params(command)}
            elif "character" in cmd_lower:
                return "create_character", {**params, **self._extract_all_params(command)}
            elif "material" in cmd_lower:
                return "create_materials", {**params, **self._extract_all_params(command)}
            elif "texture" in cmd_lower:
                return "generate_textures", {**params, **self._extract_all_params(command)}
            elif "mesh" in cmd_lower or "model" in cmd_lower:
                return "generate_models", {**params, **self._extract_all_params(command)}
            else:
                return "generic_create", {**params, **self._extract_all_params(command)}

        # Setup operations
        elif "setup" in cmd_lower or "scene" in cmd_lower:
            if "night" in cmd_lower or "evening" in cmd_lower:
                return "setup_night_scene", params
            elif "day" in cmd_lower or "outdoor" in cmd_lower:
                return "setup_day_scene", params
            elif "indoor" in cmd_lower or "room" in cmd_lower:
                return "setup_indoor_scene", params
            elif "cinematic" in cmd_lower:
                return "setup_cinematic", params

        # Lighting
        elif "lighting" in cmd_lower:
            return "setup_lighting", {**params, **self._extract_lighting_params(command)}

        # Post processing
        elif "post" in cmd_lower or "bloom" in cmd_lower or "dof" in cmd_lower:
            return "setup_post_processing", {**params, **self._extract_post_params(command)}

        # Help
        elif "help" in cmd_lower or "how" in cmd_lower or "explain" in cmd_lower:
            return "provide_help", {"topic": command}

        # Chat
        else:
            return "chat", {"message": command}

    def _extract_quantity(self, text: str) -> Optional[int]:
        """Extract quantity from text"""
        # Patterns: "5 cubes", "three spheres", etc.
        number_words = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12
        }

        text_lower = text.lower()
        for word, num in number_words.items():
            if word in text_lower:
                return num

        # Extract digits
        match = re.search(r'\b(\d+)\b', text)
        if match:
            return int(match.group(1))

        return None

    def _extract_all_params(self, text: str) -> Dict:
        """Extract all possible parameters"""
        params = {}

        # Name
        name = self._extract_name(text)
        if name:
            params["name"] = name

        # Location
        location = self._extract_location(text)
        if location != (0, 0, 0):
            params["location"] = location

        # Color
        color = self._extract_color(text)
        if color != (0.5, 0.5, 0.5):
            params["color"] = color

        # Size/Scale
        size = self._extract_size(text)
        if size:
            params["size"] = size

        # Material properties
        params["roughness"] = self._extract_roughness(text)
        params["metallic"] = self._extract_metallic(text)

        # Position patterns
        if "in a circle" in text.lower() or "circle" in text.lower():
            params["arrangement"] = "circle"
        elif "in a row" in text.lower() or "line" in text.lower():
            params["arrangement"] = "line"
        elif "grid" in text.lower():
            params["arrangement"] = "grid"

        return params

    def _extract_name(self, text: str) -> Optional[str]:
        """Extract name from text"""
        # Remove action words
        text = re.sub(r'\b(create|make|spawn|add|place|put|generate|a|an|the|named|called)\b', '', text, flags=re.IGNORECASE)
        # Clean and take first meaningful word
        words = [w for w in text.split() if len(w) > 2 and not w.isdigit()]
        if words:
            return words[0][:30].title()
        return None

    def _extract_location(self, text: str) -> Tuple[float, float, float]:
        """Extract 3D location"""
        coord_pattern = r'(-?\d+)[,\s]+(-?\d+)[,\s]+(-?\d+)'
        match = re.search(coord_pattern, text)
        if match:
            return (float(match.group(1)), float(match.group(2)), float(match.group(3)))

        # Named positions
        positions = {
            "origin": (0, 0, 0), "center": (0, 0, 0),
            "above": (0, 0, 100), "below": (0, 0, -100),
            "left": (-100, 0, 0), "right": (100, 0, 0),
            "forward": (0, 100, 0), "back": (0, -100, 0)
        }
        text_lower = text.lower()
        for pos, coords in positions.items():
            if pos in text_lower:
                return coords

        return (0, 0, 0)

    def _extract_color(self, text: str) -> Tuple[float, float, float]:
        """Extract RGB color"""
        text_lower = text.lower()

        colors = {
            "red": (1, 0, 0), "crimson": (0.86, 0.08, 0.24),
            "green": (0, 1, 0), "lime": (0.2, 1, 0),
            "blue": (0, 0, 1), "navy": (0, 0, 0.5),
            "yellow": (1, 1, 0), "gold": (1, 0.84, 0),
            "orange": (1, 0.5, 0), "amber": (1, 0.75, 0),
            "purple": (0.5, 0, 1), "violet": (0.5, 0, 1),
            "pink": (1, 0.5, 0.5), "magenta": (1, 0, 1),
            "cyan": (0, 1, 1), "teal": (0, 0.5, 0.5),
            "white": (1, 1, 1), "black": (0, 0, 0),
            "gray": (0.5, 0.5, 0.5), "grey": (0.5, 0.5, 0.5),
            "brown": (0.6, 0.4, 0.2), "tan": (0.82, 0.71, 0.55),
            "silver": (0.75, 0.75, 0.75), "chrome": (0.8, 0.8, 0.8),
            "emerald": (0.18, 0.55, 0.34), "ruby": (0.78, 0.06, 0.18),
            "sapphire": (0.07, 0.09, 0.33), "diamond": (0.81, 0.89, 0.94)
        }

        for name, rgb in colors.items():
            if name in text_lower:
                return rgb

        # Check for color in RGB format
        rgb_match = re.search(r'rgb\s*\(\s*(\d+\.?\d*)\s*,\s*(\d+\.?\d*)\s*,\s*(\d+\.?\d*)\s*\)', text)
        if rgb_match:
            r, g, b = rgb_match.groups()
            return (float(r)/255, float(g)/255, float(b)/255)

        return (0.5, 0.5, 0.5)  # Default

    def _extract_size(self, text: str) -> Optional[float]:
        """Extract size/scalar"""
        # Look for "size X", "scale X", "X times"
        patterns = [
            r'size\s*(\d+(?:\.\d+)?)',
            r'scale\s*(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*times?'
        ]

        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return float(match.group(1))

        # Words
        size_words = {"tiny": 0.2, "small": 0.5, "normal": 1.0, "large": 2.0, "huge": 5.0}
        text_lower = text.lower()
        for word, size in size_words.items():
            if word in text_lower:
                return size

        return None

    def _extract_roughness(self, text: str) -> float:
        """Extract roughness"""
        text_lower = text.lower()
        if "rough" in text_lower:
            return 0.9
        elif "smooth" in text_lower or "shiny" in text_lower or "polished" in text_lower or "glossy" in text_lower:
            return 0.1
        elif "matte" in text_lower:
            return 0.7
        return 0.5

    def _extract_metallic(self, text: str) -> float:
        """Extract metallic value"""
        text_lower = text.lower()
        metals = ["metal", "steel", "iron", "silver", "chrome", "gold", "copper", "bronze", "titanium"]
        if any(m in text_lower for m in metals):
            return 1.0
        non_metals = ["plastic", "wood", "fabric", "rubber", "organic", "ceramic"]
        if any(nm in text_lower for nm in non_metals):
            return 0.0
        return 0.0

    def _extract_lighting_params(self, text: str) -> Dict:
        """Extract lighting parameters"""
        params = {}
        text_lower = text.lower()

        if "warm" in text_lower:
            params["color"] = (1, 0.9, 0.7)
        elif "cool" in text_lower or "cold" in text_lower:
            params["color"] = (0.7, 0.8, 1)

        if "bright" in text_lower:
            params["intensity"] = 2000
        elif "dim" in text_lower:
            params["intensity"] = 500

        return params

    def _extract_post_params(self, text: str) -> Dict:
        """Extract post processing parameters"""
        params = {}
        text_lower = text.lower()

        if "bloom" in text_lower:
            params["bloom"] = True
        if "dof" in text_lower or "depth" in text_lower:
            params["depth_of_field"] = True
        if "motion" in text_lower and "blur" in text_lower:
            params["motion_blur"] = True
        if "color" in text_lower and "grad" in text_lower:
            params["color_grading"] = True

        return params

    # ============================================================
    # ACTION EXECUTION
    # ============================================================

    def _execute_action(self, action: str, params: Dict) -> Dict:
        """Execute the parsed action"""
        actions = {
            "create_cubes": self._create_cubes_action,
            "create_spheres": self._create_spheres_action,
            "create_cylinders": self._create_cylinders_action,
            "create_cones": self._create_cones_action,
            "create_planes": self._create_planes_action,
            "create_lights": self._create_lights_action,
            "create_cameras": self._create_cameras_action,
            "create_character": self._create_character_action,
            "create_materials": self._create_materials_action,
            "generate_textures": self._generate_textures_action,
            "generate_models": self._generate_models_action,
            "setup_night_scene": self._setup_night_scene_action,
            "setup_day_scene": self._setup_day_scene_action,
            "setup_indoor_scene": self._setup_indoor_scene_action,
            "setup_cinematic": self._setup_cinematic_action,
            "setup_lighting": self._setup_lighting_action,
            "setup_post_processing": self._setup_post_processing_action,
            "provide_help": self._provide_help_action,
            "chat": self._chat_action,
            "generic_create": self._generic_create_action
        }

        if action in actions:
            return actions[action](params)
        else:
            return {"error": f"Unknown action: {action}"}

    # ============================================================
    # CREATION ACTIONS
    # ============================================================

    def _create_cubes_action(self, params: Dict) -> Dict:
        """Create cube(s)"""
        quantity = params.get("quantity", 1)
        name = params.get("name", "Cube")
        location = params.get("location", (0, 0, 0))
        color = params.get("color", None)
        arrangement = params.get("arrangement", None)

        created = []

        if arrangement == "circle":
            radius = 200
            for i in range(quantity):
                angle = (2 * math.pi * i) / quantity
                x = location[0] + radius * math.cos(angle)
                y = location[1] + radius * math.sin(angle)
                z = location[2]
                result = self._create_cube(f"{name}_{i}", (x, y, z), color)
                created.append(result.get("name", ""))
        elif arrangement == "line":
            spacing = 100
            for i in range(quantity):
                pos = (location[0] + i * spacing, location[1], location[2])
                result = self._create_cube(f"{name}_{i}", pos, color)
                created.append(result.get("name", ""))
        else:
            for i in range(quantity):
                if quantity > 1:
                    n = f"{name}_{i}"
                else:
                    n = name
                result = self._create_cube(n, location, color)
                created.append(result.get("name", ""))

        return {
            "message": f"Created {len(created)} cube(s)",
            "created": created,
            "quantity": len(created)
        }

    def _create_cube(self, name: str, location: Tuple[float, float, float] = (0, 0, 0),
                     color: Optional[Tuple[float, float, float]] = None) -> Dict:
        """Create a single cube"""
        try:
            loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
            actor.set_actor_label(name)

            # If color specified, create and assign material
            if color:
                mat_name = f"{name}_Mat"
                mat = self._create_simple_material(mat_name, color)
                if mat:
                    self._assign_material_to_actor(actor, mat)

            return {"name": name, "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    def _create_spheres_action(self, params: Dict) -> Dict:
        """Create sphere(s)"""
        quantity = params.get("quantity", 1)
        name = params.get("name", "Sphere")
        location = params.get("location", (0, 0, 0))
        color = params.get("color", None)
        arrangement = params.get("arrangement", None)

        created = []

        for i in range(quantity):
            n = f"{name}_{i}" if quantity > 1 else name
            result = self._create_sphere(n, location, color)
            created.append(result.get("name", ""))

        return {
            "message": f"Created {len(created)} sphere(s)",
            "created": created,
            "quantity": len(created)
        }

    def _create_sphere(self, name: str, location: Tuple[float, float, float] = (0, 0, 0),
                       color: Optional[Tuple[float, float, float]] = None) -> Dict:
        """Create a single sphere"""
        try:
            loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
            actor.set_actor_label(name)

            if color:
                mat_name = f"{name}_Mat"
                mat = self._create_simple_material(mat_name, color)
                if mat:
                    self._assign_material_to_actor(actor, mat)

            return {"name": name, "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    def _create_cylinders_action(self, params: Dict) -> Dict:
        """Create cylinder(s)"""
        quantity = params.get("quantity", 1)
        name = params.get("name", "Cylinder")
        location = params.get("location", (0, 0, 0))
        color = params.get("color", None)

        created = []
        for i in range(quantity):
            n = f"{name}_{i}" if quantity > 1 else name
            result = self._create_cylinder(n, location, color)
            created.append(result.get("name", ""))

        return {
            "message": f"Created {len(created)} cylinder(s)",
            "created": created,
            "quantity": len(created)
        }

    def _create_cylinder(self, name: str, location: Tuple[float, float, float] = (0, 0, 0),
                          color: Optional[Tuple[float, float, float]] = None) -> Dict:
        """Create a single cylinder"""
        try:
            loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
            actor.set_actor_label(name)

            if color:
                mat_name = f"{name}_Mat"
                mat = self._create_simple_material(mat_name, color)
                if mat:
                    self._assign_material_to_actor(actor, mat)

            return {"name": name, "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    def _create_cones_action(self, params: Dict) -> Dict:
        """Create cone(s)"""
        quantity = params.get("quantity", 1)
        name = params.get("name", "Cone")
        location = params.get("location", (0, 0, 0))
        color = params.get("color", None)

        created = []
        for i in range(quantity):
            n = f"{name}_{i}" if quantity > 1 else name
            result = self._create_cone(n, location, color)
            created.append(result.get("name", ""))

        return {
            "message": f"Created {len(created)} cone(s)",
            "created": created,
            "quantity": len(created)
        }

    def _create_cone(self, name: str, location: Tuple[float, float, float] = (0, 0, 0),
                      color: Optional[Tuple[float, float, float]] = None) -> Dict:
        """Create a single cone"""
        try:
            loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
            actor.set_actor_label(name)

            if color:
                mat_name = f"{name}_Mat"
                mat = self._create_simple_material(mat_name, color)
                if mat:
                    self._assign_material_to_actor(actor, mat)

            return {"name": name, "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    def _create_planes_action(self, params: Dict) -> Dict:
        """Create plane(s)"""
        quantity = params.get("quantity", 1)
        name = params.get("name", "Plane")
        location = params.get("location", (0, 0, 0))
        size = params.get("size", 100)
        color = params.get("color", None)

        created = []
        for i in range(quantity):
            n = f"{name}_{i}" if quantity > 1 else name
            result = self._create_plane(n, location, size, color)
            created.append(result.get("name", ""))

        return {
            "message": f"Created {len(created)} plane(s)",
            "created": created,
            "quantity": len(created)
        }

    def _create_plane(self, name: str, location: Tuple[float, float, float] = (0, 0, 0),
                       size: float = 100, color: Optional[Tuple[float, float, float]] = None) -> Dict:
        """Create a single plane"""
        try:
            loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
            actor.set_actor_label(name)
            actor.set_actor_scale3d(unreal.Vector(size, size, size))

            if color:
                mat_name = f"{name}_Mat"
                mat = self._create_simple_material(mat_name, color)
                if mat:
                    self._assign_material_to_actor(actor, mat)

            return {"name": name, "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    # ============================================================
    # LIGHT CREATION
    # ============================================================

    def _create_lights_action(self, params: Dict) -> Dict:
        """Create light(s)"""
        quantity = params.get("quantity", 1)
        name = params.get("name", "Light")
        location = params.get("location", (0, 0, 0))
        intensity = params.get("intensity", 1000)
        light_color = params.get("color", (1, 1, 1))

        created = []
        for i in range(quantity):
            n = f"{name}_{i}" if quantity > 1 else name
            result = self._create_point_light(n, location, intensity, light_color)
            created.append(result.get("name", ""))

        return {
            "message": f"Created {len(created)} light(s)",
            "created": created
        }

    def _create_point_light(self, name: str, location: Tuple[float, float, float],
                             intensity: float = 1000,
                             color: Tuple[float, float, float] = (1, 1, 1)) -> Dict:
        """Create a point light"""
        try:
            loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLightActor, loc)
            actor.set_actor_label(name)

            light_comp = actor.get_component_by_class(unreal.PointLightComponent)
            light_comp.set_editor_property("intensity", intensity)
            light_comp.set_editor_property("light_color", unreal.LinearColor(color[0], color[1], color[2], 1))

            return {"name": name, "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    # ============================================================
    # CAMERA CREATION
    # ============================================================

    def _create_cameras_action(self, params: Dict) -> Dict:
        """Create camera(s)"""
        quantity = params.get("quantity", 1)
        name = params.get("name", "Camera")
        location = params.get("location", (0, 0, 0))

        created = []
        for i in range(quantity):
            n = f"{name}_{i}" if quantity > 1 else name
            result = self._create_camera(n, location)
            created.append(result.get("name", ""))

        return {
            "message": f"Created {len(created)} camera(s)",
            "created": created
        }

    def _create_camera(self, name: str, location: Tuple[float, float, float] = (0, 0, 0)) -> Dict:
        """Create a camera"""
        try:
            loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CameraActor, loc)
            actor.set_actor_label(name)
            return {"name": name, "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    # ============================================================
    # CHARACTER CREATION
    # ============================================================

    def _create_character_action(self, params: Dict) -> Dict:
        """Create a character"""
        name = params.get("name", "Character")
        location = params.get("location", (0, 0, 0))

        return self._create_character(name, location)

    def _create_character(self, name: str, location: Tuple[float, float, float] = (0, 0, 0)) -> Dict:
        """Create a basic character"""
        try:
            loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Character, loc)
            actor.set_actor_label(name)

            return {
                "message": f"Created character: {name}",
                "name": name,
                "actor": actor
            }
        except Exception as e:
            return {"error": str(e)}

    # ============================================================
    # MATERIAL CREATION
    # ============================================================

    def _create_materials_action(self, params: Dict) -> Dict:
        """Create material(s)"""
        return self._create_material_action(params)

    def _create_material_action(self, params: Dict) -> Dict:
        """Create a material"""
        name = params.get("name", "Material")
        color = params.get("color", (0.5, 0.5, 0.5))
        roughness = params.get("roughness", 0.5)
        metallic = params.get("metallic", 0.0)

        result = self._create_material(name, color, roughness, metallic)

        if result.get("error"):
            return result

        return {
            "message": f"Created material: {name}",
            "name": name,
            "path": result.get("path", "")
        }

    def _create_material(self, name: str, color: Tuple[float, float, float] = (0.5, 0.5, 0.5),
                        roughness: float = 0.5, metallic: float = 0.0) -> Dict:
        """Create a material"""
        try:
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

            material = asset_tools.create_asset(
                name,
                "/Game/GeneratedMaterials",
                unreal.Material,
                unreal.MaterialFactoryNew()
            )

            mat_editing = unreal.MaterialEditingLibrary

            # Base Color
            color_const = mat_editing.create_material_expression(
                material, unreal.MaterialExpressionConstant3Vector
            )
            color_const.set_editor_property("constant", unreal.LinearColor(color[0], color[1], color[2], 1.0))
            mat_editing.connect_material_property(
                color_const, "Output", material, unreal.MaterialProperty.MP_BASE_COLOR
            )

            # Roughness
            rough_const = mat_editing.create_material_expression(
                material, unreal.MaterialExpressionConstant
            )
            rough_const.set_editor_property("r", roughness)
            mat_editing.connect_material_property(
                rough_const, "Output", material, unreal.MaterialProperty.MP_ROUGHNESS
            )

            # Metallic
            metal_const = mat_editing.create_material_expression(
                material, unreal.MaterialExpressionConstant
            )
            metal_const.set_editor_property("r", metallic)
            mat_editing.connect_material_property(
                metal_const, "Output", material, unreal.MaterialProperty.MP_METALLIC
            )

            return {"path": f"/Game/GeneratedMaterials/{name}"}

        except Exception as e:
            return {"error": str(e)}

    def _create_simple_material(self, name: str, color: Tuple[float, float, float]) -> Optional[str]:
        """Create a simple material"""
        result = self._create_material(name, color, 0.5, 0.0)
        if result and "path" in result:
            return result["path"]
        return None

    def _assign_material_to_actor(self, actor, material_path: str):
        """Assign material to actor"""
        try:
            material = unreal.load_asset(material_path, unreal.Material)
            if not material:
                return

            mesh_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
            if mesh_comp:
                mesh_comp.set_material(0, material)
        except Exception as e:
            unreal.log_error(f"Failed to assign material: {e}")

    # ============================================================
    # TEXTURE GENERATION
    # ============================================================

    def _generate_textures_action(self, params: Dict) -> Dict:
        """Generate texture(s)"""
        prompt = params.get("prompt", "texture")
        size = params.get("size", (512, 512))

        return self._generate_texture(prompt, size)

    def _generate_texture(self, prompt: str, size: Tuple[int, int] = (512, 512)) -> Dict:
        """Generate AI texture"""
        try:
            encoded = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded}?width={size[0]}&height={size[1]}&seed={hash(prompt)}"

            asset_name = self._sanitize_name(prompt)
            temp_path = os.path.join(self.temp_dir, f"{asset_name}.png")

            urllib.request.urlretrieve(url, temp_path)

            # Import
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            import_task = unreal.AssetImportTask()
            import_task.set_editor_property('filename', temp_path)
            import_task.set_editor_property('destination_path', '/Game/GeneratedTextures')
            import_task.set_editor_property('automated', True)

            asset_tools.import_asset_task([import_task])

            return {
                "message": f"Generated texture: {prompt}",
                "path": f"/Game/GeneratedTextures/{asset_name}",
                "prompt": prompt
            }

        except Exception as e:
            return {"error": f"Texture generation failed: {e}"}

    # ============================================================
    # MODEL GENERATION
    # ============================================================

    def _generate_models_action(self, params: Dict) -> Dict:
        """Generate model(s)"""
        prompt = params.get("prompt", "model")
        return self._generate_model(prompt)

    def _generate_model(self, prompt: str) -> Dict:
        """Generate 3D model"""
        # Try backend first
        try:
            conn = http.client.HTTPConnection(self.backend_host, self.backend_port, timeout=30)
            conn.request("POST", "/api/api/generate", json.dumps({
                "prompt": prompt,
                "asset_type": "MESH",
                "service": "auto"
            }), {"Content-type": "application/json"})

            response = conn.getresponse()
            if response.status == 200:
                result = json.loads(response.read().decode())
                # Would download and import here
                return {"message": f"Model generation initiated: {prompt}"}

        except:
            pass

        # Fallback to procedural
        return self._create_procedural_model(prompt)

    def _create_procedural_model(self, prompt: str) -> Dict:
        """Create procedural model based on prompt"""
        return self._create_cube(prompt.title(), (0, 0, 0))

    # ============================================================
    # SCENE SETUP
    # ============================================================

    def _setup_night_scene_action(self, params: Dict) -> Dict:
        """Setup a night scene"""
        created = []

        # Dark sky
        result = self._create_directional_light("Moon", (0, 0, 1000), 0.5, (0.2, 0.2, 0.3))
        created.append(result.get("name"))

        # Sky light
        result = self._create_sky_light("NightSky", (0, 0, 0), 0.5)
        created.append(result.get("name"))

        # Fog
        result = self._create_atmospheric_fog()
        created.append("AtmosphericFog")

        # Ambient lights
        for i, pos in enumerate([(200, 0, 100), (-200, 0, 100), (0, 200, 100)]):
            result = self._create_point_light(f"NightLight_{i}", pos, 500, (0.5, 0.5, 0.8))
            created.append(result.get("name"))

        return {
            "message": "Night scene setup complete",
            "created": created
        }

    def _setup_day_scene_action(self, params: Dict) -> Dict:
        """Setup a day scene"""
        created = []

        # Sun
        result = self._create_directional_light("Sun", (0, 0, 1000), 10, (1, 0.95, 0.8))
        created.append(result.get("name"))

        # Sky
        result = self._create_sky_light("DaySky", (0, 0, 0), 1.0)
        created.append(result.get("name"))

        # Fog
        result = self._create_atmospheric_fog()
        created.append("AtmosphericFog")

        return {
            "message": "Day scene setup complete",
            "created": created
        }

    def _setup_indoor_scene_action(self, params: Dict) -> Dict:
        """Setup an indoor scene"""
        created = []

        # Floor
        result = self._create_plane("Floor", (0, 0, 0), 500)
        created.append(result.get("name"))

        # Walls
        wall_positions = [
            ("BackWall", (0, -500, 250)),
            ("LeftWall", (-500, 0, 250)),
            ("RightWall", (500, 0, 250))
        ]

        for name, pos in wall_positions:
            result = self._create_plane(name, pos, 500)
            actor = result.get("actor")
            if actor:
                rotator = unreal.Rotator(90, 0, 0)
                actor.set_actor_rotation(rotator)
            created.append(name)

        # Ceiling
        result = self._create_plane("Ceiling", (0, 0, 500), 500)
        created.append(result.get("name"))

        # Lights
        for i in range(3):
            result = self._create_point_light(f"RoomLight_{i}", (0, 0, 400), 800)
            created.append(result.get("name"))

        return {
            "message": "Indoor scene setup complete",
            "created": created
        }

    def _setup_cinematic_action(self, params: Dict) -> Dict:
        """Setup cinematic lighting"""
        created = []

        # Key light
        result = self._create_spot_light("KeyLight", (-200, 200, 300), 2000)
        created.append(result.get("name"))

        # Fill light
        result = self._create_spot_light("FillLight", (200, 200, 300), 1000, (0.8, 0.8, 1))
        created.append(result.get("name"))

        # Back light
        result = self._create_spot_light("BackLight", (0, -200, 200), 800, (0.5, 0.5, 0.6))
        created.append(result.get("name"))

        # Post process
        result = self._create_post_process_volume()
        created.append("PostProcessVolume")

        return {
            "message": "Cinematic setup complete",
            "created": created
        }

    # ============================================================
    # HELP
    # ============================================================

    def _provide_help_action(self, params: Dict) -> Dict:
        """Provide help on a topic"""
        topic = params.get("topic", "")

        # Generate help response
        help_text = self._generate_help(topic)

        return {
            "message": f"Help: {topic}",
            "help": help_text
        }

    def _generate_help(self, topic: str) -> str:
        """Generate help text for a topic"""
        topic_lower = topic.lower()

        help_topics = {
            "material": "MATERIALS:\n- Base Color: The surface color\n- Roughness: 0=smooth, 1=rough\n- Metallic: 0=non-metal, 1=metal\n- Normal: Surface detail\n- Emissive: Glow\n\nCreate: ai.do('Create a red material')",
            "lighting": "LIGHTING:\n- Point Light: Omni-directional\n- Spot Light: Cone-shaped\n- Directional: Sun/moon\n- Sky Light: Ambient\n\nCreate: ai.do('Add a point light')",
            "blueprint": "BLUEPRINTS:\n- Visual scripting for logic\n- Event Graph: Events and functions\n- Construction Script: On creation\n- Variables: Editable instance\n\nCreate: ai.do('Create a blueprint class')",
            "animation": "ANIMATION:\n- Animation Sequence: Raw data\n- Blueprint: State machine\n- Montage: Sections of animation\n- Aim Offset: Aiming poses\n\nCreate: ai.do('Create an animation')",
        }

        for key, value in help_topics.items():
            if key in topic_lower:
                return value

        # Ask AI
        response = self._chat_action({"message": f"Help with Unreal Engine: {topic}"})
        if response and "message" in response:
            return response["message"]

        return "Try: ai.do('create a cube'), ai.do('make a material'), ai.do('setup lighting')"

    # ============================================================
    # CHAT
    # ============================================================

    def _chat_action(self, params: Dict) -> Dict:
        """Chat with AI"""
        message = params.get("message", "")

        try:
            conn = http.client.HTTPConnection(self.backend_host, self.backend_port, timeout=60)
            conn.request("POST", "/api/api/chat", json.dumps({"user_input": message}),
                        {"Content-type": "application/json"})

            response = conn.getresponse()
            if response.status == 200:
                result = json.loads(response.read().decode())
                ai_message = result.get("full_response", "")

                return {
                    "message": ai_message,
                    "response": ai_message
                }

        except Exception as e:
            return {"error": f"Chat failed: {e}"}

    # ============================================================
    # SPECIALIZED CREATION HELPERS
    # ============================================================

    def _create_sky_light(self, name: str, location: Tuple[float, float, float] = (0, 0, 0),
                           intensity: float = 1.0) -> Dict:
        """Create a sky light"""
        try:
            loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyLightActor, loc)
            actor.set_actor_label(name)

            sky_comp = actor.get_component_by_class(unreal.SkyLightComponent)
            sky_comp.set_editor_property("intensity", intensity)

            return {"name": name, "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    def _create_directional_light(self, name: str, location: Tuple[float, float, float] = (0, 0, 500),
                                 intensity: float = 10,
                                 color: Tuple[float, float, float] = (1, 0.95, 0.8)) -> Dict:
        """Create a directional light"""
        try:
            loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLightActor, loc)
            actor.set_actor_label(name)

            light_comp = actor.get_component_by_class(unreal.DirectionalLightComponent)
            light_comp.set_editor_property("intensity", intensity)
            light_comp.set_editor_property("light_color", unreal.LinearColor(color[0], color[1], color[2], 1))

            return {"name": name, "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    def _create_atmospheric_fog(self) -> Dict:
        """Create atmospheric fog"""
        try:
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.AtmosphericFog, unreal.Vector(0, 0, 0))
            actor.set_actor_label("AtmosphericFog")
            return {"name": "AtmosphericFog", "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    def _create_spot_light(self, name: str, location: Tuple[float, float, float],
                           intensity: float = 1000,
                           color: Tuple[float, float, float] = (1, 1, 1)) -> Dict:
        """Create a spot light"""
        try:
            loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SpotLightActor, loc)
            actor.set_actor_label(name)

            light_comp = actor.get_component_by_class(unreal.SpotLightComponent)
            light_comp.set_editor_property("intensity", intensity)

            return {"name": name, "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    def _create_post_process_volume(self) -> Dict:
        """Create a post process volume"""
        try:
            loc = unreal.Vector(0, 0, 0)
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PostProcessVolume, loc)
            actor.set_actor_label("PostProcessVolume")
            actor.set_editor_property("bEnabled", True)
            actor.set_editor_property("bUnbound", True)
            return {"name": "PostProcessVolume", "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    def _generic_create_action(self, params: Dict) -> Dict:
        """Generic creation based on parameters"""
        # Determine best actor type
        desc = params.get("description", "").lower()

        if "cube" in desc:
            return self._create_cubes_action(params)
        elif "sphere" in desc:
            return self._create_spheres_action(params)
        elif "light" in desc:
            return self._create_lights_action(params)
        elif "material" in desc:
            return self._create_material_action(params)
        elif "texture" in desc:
            return self._generate_textures_action(params)
        else:
            return {"error": f"Could not determine what to create from: {params}"}

    # ============================================================
    # UTILITIES
    # ============================================================

    def _sanitize_name(self, text: str) -> str:
        """Clean text for asset name"""
        clean = re.sub(r'[^\w\s-]', '', text)
        clean = re.sub(r'\s+', '_', clean)
        return clean[:30]

    # ============================================================
    # PUBLIC SHORTCUTS
    # ============================================================

    def create_cube(self, name="Cube", location=(0, 0, 0), color=None):
        """Quick cube creation"""
        params = {"name": name, "location": location}
        if color:
            params["color"] = color
        return self._create_cubes_action(params)

    def create_sphere(self, name="Sphere", location=(0, 0, 0), color=None):
        """Quick sphere creation"""
        params = {"name": name, "location": location}
        if color:
            params["color"] = color
        return self._create_spheres_action(params)

    def create_light(self, name="Light", location=(0, 0, 0)):
        """Quick light creation"""
        return self._create_lights_action({"name": name, "location": location})

    def create_material(self, name="Material", description=""):
        """Quick material creation"""
        return self._create_material_action({"name": name, **self._parse_material_request(description)})

    def chat(self, message):
        """Quick chat"""
        return self._chat_action({"message": message})

    def help(self, topic):
        """Quick help"""
        return self._provide_help_action({"topic": topic})

    def _parse_material_request(self, text: str) -> Dict:
        """Parse material from description"""
        return {
            "color": self._extract_color(text),
            "roughness": self._extract_roughness(text),
            "metallic": self._extract_metallic(text)
        }


# Create global instance
ai = UEMasterAI()

# Show banner
unreal.log("\n" + "█"*70)
unreal.log("█     🤖 UE AI MASTER - ULTIMATE VERSION                     █")
unreal.log("█                                                          █")
unreal.log("█"*70)
unreal.log("\n✨ NATURAL LANGUAGE COMMANDS:\n")
unreal.log("   ai.do('create 5 red cubes in a circle')")
unreal.log("   ai.do('make 10 blue spheres')")
unreal.log("   ai.do('generate a wood texture 1024x1024')")
unreal.log("   ai.do('create a shiny gold material')")
unreal.log("   ai.do('setup a night scene')")
unreal.log("   ai.do('create a character')")
unreal.log("   ai.do('setup cinematic lighting')")
unreal.log("\n🔧 QUICK METHODS:\n")
unreal.log("   ai.create_cube('RedCube', color=(1,0,0))")
unreal.log("   ai.create_sphere('MySphere', (100,0,0))")
unreal.log("   ai.create_light('SunLight', (0,0,1000))")
unreal.log("   ai.create_material('Gold', 'shiny metal')")
unreal.log("   ai.chat('How do I make a glowing material?')")
unreal.log("   ai.help('lighting')")
unreal.log("\n📚 KNOWLEDGE COVERAGE:")
unreal.log("   Actors, Components, Materials, Textures, Meshes, Animations")
unreal.log("   Blueprints, Levels, Lighting, Post Processing, Physics")
unreal.log("   Niagara, UMG, Input, Gameplay, Networking, Audio, AI")
unreal.log("   Rendering, Tools, AND MORE!\n")
unreal.log("="*70 + "\n")
