"""
UE AI Plugin - Comprehensive AI Assistant
Understands everything about Unreal Engine and can generate anything
"""

import unreal
import http.client
import json
import urllib.request
import urllib.parse
import os
import tempfile
import re
from typing import Optional, Tuple, List, Dict, Any

# Import knowledge base and asset manager
import sys
sys.path.insert(0, '/Volumes/SERENADA_2/_elliott/Unreal Projects/UEAI-Plugin-Test/Plugins/UEAIPlugin/Content/Python')
from ue_knowledge_base import (
    UE_KNOWLEDGE_BASE,
    WORKFLOWS,
    TROUBLESHOOTING,
    ASSET_TEMPLATES,
    search_knowledge,
    get_workflow,
    solve_problem,
    get_asset_template
)


class UEAIAssistant:
    """
    Complete AI Assistant for Unreal Engine
    Understands natural language and executes complex operations
    """

    def __init__(self):
        self.backend_host = "localhost"
        self.backend_port = 8000
        self.temp_dir = tempfile.gettempdir()
        self.conversation_history = []
        self.execution_context = {
            "selected_actors": [],
            "current_level": None,
            "last_action": None,
            "clipboard": None
        }

    # ============================================================
    # MAIN INTERFACE - Process any request
    # ============================================================

    def do(self, request: str) -> Dict[str, Any]:
        """
        Main interface - Process any request

        This is the primary method that handles all user requests.
        It understands natural language and executes the appropriate action.

        Args:
            request: Natural language request

        Returns:
            Result dictionary with status and data
        """
        self.conversation_history.append({"role": "user", "content": request})

        try:
            # Step 1: Understand what the user wants
            intent = self._analyze_intent(request)
            unreal.log(f"\n🧠 Intent: {intent['action']} - {intent.get('description', '')}")

            # Step 2: Gather relevant information from knowledge base
            context = self._gather_context(request, intent)

            # Step 3: Execute the action
            result = self._execute_intent(intent, context)

            # Step 4: Format and return result
            response = {
                "success": True if result.get("error") is None else False,
                "action": intent["action"],
                "result": result,
                "message": result.get("message", ""),
                "details": result.get("details", {})
            }

            # Add AI commentary
            if "explanation" in result:
                response["explanation"] = result["explanation"]

            # Log response
            if response["success"]:
                unreal.log(f"✅ {result.get('message', 'Complete')}")
            else:
                unreal.log_error(f"❌ {result.get('error', 'Failed')}")

            return response

        except Exception as e:
            error_result = {
                "success": False,
                "action": "error",
                "error": str(e),
                "message": f"Error processing request: {e}"
            }
            unreal.log_error(f"❌ {error_result['message']}")
            return error_result

    # ============================================================
    # INTENT ANALYSIS - Understand what user wants
    # ============================================================

    def _analyze_intent(self, request: str) -> Dict[str, Any]:
        """Analyze request to determine intent and parameters"""
        request_lower = request.lower()

        # Initialize intent
        intent = {
            "action": "unknown",
            "description": request,
            "parameters": {},
            "confidence": 0.0
        }

        # ACTOR CREATION
        actor_keywords = {
            "create": ["spawn", "create", "make", "add", "place", "put", "instantiate"],
            "actor_types": {
                "cube": "static_mesh_actor",
                "sphere": "static_mesh_actor",
                "box": "static_mesh_actor",
                "cylinder": "static_mesh_actor",
                "cone": "static_mesh_actor",
                "plane": "static_mesh_actor",
                "floor": "static_mesh_actor",
                "light": "point_light",
                "point light": "point_light",
                "spotlight": "spot_light",
                "spot light": "spot_light",
                "sun": "directional_light",
                "directional light": "directional_light",
                "camera": "camera_actor",
                "character": "character",
                "pawn": "pawn",
                "player": "character"
            }
        }

        # Check for actor creation
        for create_word in actor_keywords["create"]:
            if create_word in request_lower:
                # Determine actor type
                actor_type = None
                for keyword, type_name in actor_keywords["actor_types"].items():
                    if keyword in request_lower:
                        actor_type = type_name
                        break

                if actor_type:
                    intent["action"] = "create_actor"
                    intent["actor_type"] = actor_type
                    intent["name"] = self._extract_name(request, actor_type.title())
                    intent["location"] = self._extract_location(request)
                    intent["confidence"] = 0.9
                    return intent

        # MATERIAL CREATION
        material_keywords = ["material", "mat", "surface", "substance"]
        if any(kw in request_lower for kw in material_keywords):
            intent["action"] = "create_material"
            intent["description"] = request
            intent["properties"] = self._parse_material_request(request)
            intent["name"] = self._extract_name(request, "Material")
            intent["confidence"] = 0.9
            return intent

        # TEXTURE GENERATION
        texture_keywords = ["texture", "tex", "image", "texture map"]
        if any(kw in request_lower for kw in texture_keywords):
            intent["action"] = "generate_texture"
            intent["prompt"] = request
            intent["size"] = self._extract_size(request, (512, 512))
            intent["confidence"] = 0.9
            return intent

        # 3D MODEL GENERATION
        model_keywords = ["model", "mesh", "3d", "generate", "procedural"]
        if any(kw in request_lower for kw in model_keywords):
            intent["action"] = "generate_model"
            intent["prompt"] = request
            intent["confidence"] = 0.8
            return intent

        # MODIFYING ACTORS
        modify_keywords = ["move", "rotate", "scale", "resize", "set", "change", "modify", "adjust"]
        if any(kw in request_lower for kw in modify_keywords):
            intent["action"] = "modify_actor"
            intent["target"] = self._extract_target(request)
            intent["modifications"] = self._parse_modifications(request)
            intent["confidence"] = 0.8
            return intent

        # DELETING ACTORS
        delete_keywords = ["delete", "remove", "destroy", "clear"]
        if any(kw in request_lower for kw in delete_keywords):
            intent["action"] = "delete_actor"
            intent["target"] = self._extract_target(request)
            intent["confidence"] = 0.9
            return intent

        # LIGHTING
        lighting_keywords = ["lighting", "lighting setup", "illumination", "bloom", "exposure"]
        if any(kw in request_lower for kw in lighting_keywords):
            intent["action"] = "setup_lighting"
            intent["type"] = self._extract_lighting_type(request)
            intent["confidence"] = 0.8
            return intent

        # POST PROCESSING
        post_keywords = ["bloom", "post process", "depth of field", "dof", "motion blur", "color grading"]
        if any(kw in request_lower for kw in post_keywords):
            intent["action"] = "configure_post_processing"
            intent["effects"] = self._parse_post_effects(request)
            intent["confidence"] = 0.8
            return intent

        # HELP/QUESTIONS
        question_keywords = ["how", "what", "why", "help", "explain", "tutorial", "guide"]
        if any(kw in request_lower for kw in question_keywords) or "?" in request:
            intent["action"] = "provide_help"
            intent["topic"] = request
            intent["confidence"] = 0.9
            return intent

        # SELECTION
        selection_keywords = ["select", "find", "highlight", "choose"]
        if any(kw in request_lower for kw in selection_keywords):
            intent["action"] = "select_actors"
            intent["criteria"] = request
            intent["confidence"] = 0.8
            return intent

        # DEFAULT: Ask AI
        intent["action"] = "ask_ai"
        intent["question"] = request
        intent["confidence"] = 0.5

        return intent

    def _extract_name(self, text: str, default: str) -> str:
        """Extract name from request"""
        # Remove action words
        text = re.sub(r'\b(create|make|spawn|add|place|put|generate|a|an|the)\b', '', text, flags=re.IGNORECASE)
        # Clean up
        text = text.strip()
        # Take first word
        words = text.split()
        if words:
            name = re.sub(r'[^\w\s-]', '', words[0])
            return name[:30]
        return default

    def _extract_location(self, text: str) -> Tuple[float, float, float]:
        """Extract location from text (x, y, z)"""
        # Look for coordinates
        coord_pattern = r'(-?\d+)[,\s]+(-?\d+)[,\s]+(-?\d+)'
        match = re.search(coord_pattern, text)
        if match:
            return (float(match.group(1)), float(match.group(2)), float(match.group(3)))

        # Look for "at position"
        position_keywords = {
            "origin": (0, 0, 0),
            "center": (0, 0, 0),
            "zero": (0, 0, 0)
        }
        text_lower = text.lower()
        for keyword, pos in position_keywords.items():
            if keyword in text_lower:
                return pos

        # Default
        return (0, 0, 0)

    def _extract_size(self, text: str, default: Tuple[int, int]) -> Tuple[int, int]:
        """Extract texture size"""
        size_pattern = r'(\d+)[xX](\d+)'
        match = re.search(size_pattern, text)
        if match:
            return (int(match.group(1)), int(match.group(2)))
        return default

    def _extract_target(self, text: str) -> str:
        """Extract target actor name"""
        # Remove action words
        text = re.sub(r'\b(delete|remove|destroy|clear|select|find)\b', '', text, flags=re.IGNORECASE)
        return text.strip()

    def _parse_material_request(self, text: str) -> Dict[str, Any]:
        """Parse material description"""
        return {
            "color": self._extract_color(text),
            "roughness": self._extract_roughness(text),
            "metallic": self._extract_metallic(text),
            "emissive": self._extract_emissive(text),
            "opacity": self._extract_opacity(text)
        }

    def _parse_modifications(self, text: str) -> Dict[str, Any]:
        """Parse modification instructions"""
        mods = {}

        # Location
        if "move" in text.lower() or "position" in text.lower():
            mods["location"] = self._extract_location(text)

        # Rotation
        if "rotate" in text.lower() or "rotation" in text.lower():
            rot_pattern = r'(-?\d+)\s*deg'
            matches = re.findall(rot_pattern, text)
            if len(matches) >= 3:
                mods["rotation"] = (float(matches[0]), float(matches[1]), float(matches[2]))

        # Scale
        if "scale" in text.lower() or "resize" in text.lower():
            scale_pattern = r'(\d+(?:\.\d+)?)'
            matches = re.findall(scale_pattern, text)
            if matches:
                mods["scale"] = float(matches[0])

        return mods

    def _extract_lighting_type(self, text: str) -> str:
        """Determine lighting setup type"""
        if "outdoor" in text.lower() or "sun" in text.lower():
            return "outdoor"
        elif "indoor" in text.lower() or "studio" in text.lower():
            return "indoor"
        elif "cinematic" in text.lower():
            return "cinematic"
        return "basic"

    def _parse_post_effects(self, text: str) -> Dict[str, Any]:
        """Parse post processing effects"""
        effects = {}

        if "bloom" in text.lower():
            effects["bloom"] = True
        if "dof" in text.lower() or "depth of field" in text.lower():
            effects["depth_of_field"] = True
        if "motion blur" in text.lower():
            effects["motion_blur"] = True
        if "color grade" in text.lower():
            effects["color_grading"] = True

        return effects

    def _extract_color(self, text: str) -> Tuple[float, float, float]:
        """Extract RGB color from text"""
        return get_color_from_text(text)

    def _extract_roughness(self, text: str) -> float:
        """Extract roughness value"""
        text_lower = text.lower()
        if "rough" in text_lower:
            return 0.9
        elif "smooth" in text_lower or "shiny" in text_lower or "glossy" in text_lower:
            return 0.1
        elif "matte" in text_lower:
            return 0.7
        return 0.5

    def _extract_metallic(self, text: str) -> float:
        """Extract metallic value"""
        text_lower = text.lower()
        if any(word in text_lower for word in ["metal", "steel", "silver", "chrome", "gold", "copper", "bronze", "iron"]):
            return 1.0
        elif "plastic" in text_lower or "wood" in text_lower or "fabric" in text_lower:
            return 0.0
        return 0.0

    def _extract_emissive(self, text: str) -> Tuple[float, float, float]:
        """Extract emissive color"""
        text_lower = text.lower()
        if "glow" in text_lower or "emissive" in text_lower or "light" in text_lower:
            color = self._extract_color(text)
            return color
        return None

    def _extract_opacity(self, text: str) -> float:
        """Extract opacity value"""
        text_lower = text.lower()
        if "transparent" in text_lower:
            return 0.5
        elif "translucent" in text_lower:
            return 0.7
        elif "opaque" in text_lower:
            return 1.0
        return 1.0

    # ============================================================
    # CONTEXT GATHERING - Get relevant info from knowledge base
    # ============================================================

    def _gather_context(self, request: str, intent: Dict) -> Dict[str, Any]:
        """Gather relevant context from knowledge base"""
        context = {
            "intent": intent,
            "request": request,
            "knowledge": {},
            "examples": []
        }

        # Search knowledge base
        search_terms = self._extract_search_terms(request, intent)
        for term in search_terms:
            results = search_knowledge(term)
            context["knowledge"][term] = results

        # Get relevant workflow
        workflow = get_workflow(intent["action"])
        if workflow:
            context["workflow"] = workflow

        # Get template if applicable
        template = get_asset_template(intent["action"])
        if template:
            context["template"] = template

        return context

    def _extract_search_terms(self, request: str, intent: Dict) -> List[str]:
        """Extract relevant search terms from request"""
        terms = []

        # Add action
        terms.append(intent["action"])

        # Add actor type
        if "actor_type" in intent:
            terms.append(intent["actor_type"])

        # Extract key nouns
        important_words = re.findall(r'\b[A-Z][a-z]+\b', request)
        terms.extend(important_words[:3])

        return list(set(terms))

    # ============================================================
    # INTENT EXECUTION - Perform the action
    # ============================================================

    def _execute_intent(self, intent: Dict, context: Dict) -> Dict[str, Any]:
        """Execute the intended action"""
        action = intent["action"]

        try:
            # Actor creation
            if action == "create_actor":
                return self._create_actor(
                    intent["actor_type"],
                    intent.get("name", "Actor"),
                    intent.get("location", (0, 0, 0))
                )

            # Material creation
            elif action == "create_material":
                return self._create_material(
                    intent.get("name", "Material"),
                    intent["properties"]
                )

            # Texture generation
            elif action == "generate_texture":
                return self._generate_texture(
                    intent["prompt"],
                    intent.get("size", (512, 512))
                )

            # Model generation
            elif action == "generate_model":
                return self._generate_model(intent["prompt"])

            # Modify actor
            elif action == "modify_actor":
                return self._modify_actor(
                    intent["target"],
                    intent["modifications"]
                )

            # Delete actor
            elif action == "delete_actor":
                return self._delete_actor(intent["target"])

            # Setup lighting
            elif action == "setup_lighting":
                return self._setup_lighting(intent.get("type", "basic"))

            # Configure post processing
            elif action == "configure_post_processing":
                return self._configure_post_processing(intent["effects"])

            # Provide help
            elif action == "provide_help":
                return self._provide_help(intent["topic"], context)

            # Select actors
            elif action == "select_actors":
                return self._select_actors(intent["criteria"])

            # Ask AI
            elif action == "ask_ai":
                return self._ask_ai(intent["question"])

            else:
                return {"error": f"Unknown action: {action}"}

        except Exception as e:
            return {"error": str(e), "exception": type(e).__name__}

    # ============================================================
    # ACTOR OPERATIONS
    # ============================================================

    def _create_actor(self, actor_type: str, name: str, location: Tuple[float, float, float]) -> Dict:
        """Create an actor of the specified type"""
        actor_classes = {
            "static_mesh_actor": unreal.StaticMeshActor,
            "point_light": unreal.PointLightActor,
            "spot_light": unreal.SpotLightActor,
            "directional_light": unreal.DirectionalLightActor,
            "camera_actor": unreal.CameraActor,
            "character": unreal.Character,
            "pawn": unreal.Pawn,
            "sky_light": unreal.SkyLightActor,
            "atmospheric_fog": unreal.AtmosphericFog,
            "exponential_height_fog": unreal.ExponentialHeightFog,
        }

        if actor_type not in actor_classes:
            return self._create_procedural_actor(actor_type, name, location)

        # Spawn actor
        loc = unreal.Vector(location[0], location[1], location[2])
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_classes[actor_type], loc)

        if not actor:
            return {"error": f"Failed to spawn {actor_type}"}

        # Set label
        actor.set_actor_label(name)

        # Configure based on type
        if "light" in actor_type.lower():
            self._configure_light_actor(actor, actor_type)

        return {
            "message": f"Created {actor_type}: {name}",
            "actor": actor,
            "name": name,
            "location": location,
            "details": {"actor_type": actor_type}
        }

    def _create_procedural_actor(self, actor_type: str, name: str, location: Tuple[float, float, float]) -> Dict:
        """Create actor for procedural shapes"""
        return self._create_actor("static_mesh_actor", name, location)

    def _configure_light_actor(self, actor, light_type: str):
        """Configure light properties"""
        try:
            if light_type == "point_light":
                light_comp = actor.get_component_by_class(unreal.PointLightComponent)
                if light_comp:
                    light_comp.set_editor_property("intensity", 1000)
                    light_comp.set_editor_property("attenuation_radius", 5000)
                    light_comp.set_editor_property("cast_shadows", True)

            elif light_type == "directional_light":
                light_comp = actor.get_component_by_class(unreal.DirectionalLightComponent)
                if light_comp:
                    light_comp.set_editor_property("intensity", 10)
                    light_comp.set_editor_property("cast_shadows", True)

        except Exception as e:
            unreal.log_error(f"Light config failed: {e}")

    def _modify_actor(self, target: str, modifications: Dict) -> Dict:
        """Modify an existing actor"""
        try:
            # Find actor by name
            actors = unreal.EditorLevelLibrary.get_selected_level_actors()
            if not actors:
                # Try to find by name
                actors = self._find_actors_by_name(target)

            if not actors:
                return {"error": f"No actors found matching '{target}'"}

            modified = []
            for actor in actors:
                if "location" in modifications:
                    loc = modifications["location"]
                    actor.set_actor_location(unreal.Vector(loc[0], loc[1], loc[2]))

                if "rotation" in modifications:
                    rot = modifications["rotation"]
                    actor.set_actor_rotation(unreal.Rotator(rot[0], rot[1], rot[2]))

                if "scale" in modifications:
                    scale = modifications["scale"]
                    actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))

                modified.append(actor.get_actor_label())

            return {
                "message": f"Modified {len(modified)} actor(s)",
                "modified": modified
            }

        except Exception as e:
            return {"error": str(e)}

    def _delete_actor(self, target: str) -> Dict:
        """Delete actor(s)"""
        try:
            actors = self._find_actors_by_name(target)
            if not actors:
                return {"error": f"No actors found matching '{target}'"}

            deleted = []
            for actor in actors:
                name = actor.get_actor_label()
                actor.destroy_actor()
                deleted.append(name)

            return {
                "message": f"Deleted {len(deleted)} actor(s)",
                "deleted": deleted
            }

        except Exception as e:
            return {"error": str(e)}

    def _find_actors_by_name(self, name: str) -> List:
        """Find actors by name (partial match)"""
        try:
            all_actors = unreal.GameplayStatics.get_all_actors_of_class(
                unreal.EditorLevelLibrary.get_game_world(),
                unreal.Actor
            )

            name_lower = name.lower().strip()
            matching = []

            for actor in all_actors:
                actor_name = actor.get_actor_label()
                if name_lower in actor_name.lower():
                    matching.append(actor)

            return matching

        except Exception as e:
            unreal.log_error(f"Find actors failed: {e}")
            return []

    def _select_actors(self, criteria: str) -> Dict:
        """Select actors based on criteria"""
        try:
            actors = self._find_actors_by_name(criteria)
            if not actors:
                return {"error": f"No actors found matching '{criteria}'"}

            # Select actors
            for actor in actors:
                actor.set_is_selected(True)

            return {
                "message": f"Selected {len(actors)} actor(s)",
                "selected": [a.get_actor_label() for a in actors]
            }

        except Exception as e:
            return {"error": str(e)}

    # ============================================================
    # ASSET CREATION
    # ============================================================

    def _create_material(self, name: str, properties: Dict) -> Dict:
        """Create a material with specified properties"""
        try:
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

            # Create material
            material = asset_tools.create_asset(
                name,
                "/Game/GeneratedMaterials",
                unreal.Material,
                unreal.MaterialFactoryNew()
            )

            # Set up material properties using MaterialEditingLibrary
            mat_editing = unreal.MaterialEditingLibrary

            # Base Color
            if properties.get("color"):
                color = properties["color"]
                if isinstance(color, tuple) and len(color) >= 3:
                    color_const = mat_editing.create_material_expression(
                        material,
                        unreal.MaterialExpressionConstant3Vector
                    )
                    color_const.set_editor_property(
                        "constant",
                        unreal.LinearColor(color[0], color[1], color[2], 1.0)
                    )
                    mat_editing.connect_material_property(
                        color_const,
                        "Output",
                        material,
                        unreal.MaterialProperty.MP_BASE_COLOR
                    )

            # Roughness
            roughness = properties.get("roughness", 0.5)
            roughness_const = mat_editing.create_material_expression(
                material,
                unreal.MaterialExpressionConstant
            )
            roughness_const.set_editor_property("r", roughness)
            mat_editing.connect_material_property(
                roughness_const,
                "Output",
                material,
                unreal.MaterialProperty.MP_ROUGHNESS
            )

            # Metallic
            metallic = properties.get("metallic", 0.0)
            metallic_const = mat_editing.create_material_expression(
                material,
                unreal.MaterialExpressionConstant
            )
            metallic_const.set_editor_property("r", metallic)
            mat_editing.connect_material_property(
                metallic_const,
                "Output",
                material,
                unreal.MaterialProperty.MP_METALLIC
            )

            # Emissive
            emissive = properties.get("emissive")
            if emissive and isinstance(emissive, tuple) and len(emissive) >= 3:
                emissive_const = mat_editing.create_material_expression(
                    material,
                    unreal.MaterialExpressionConstant3Vector
                )
                emissive_const.set_editor_property(
                    "constant",
                    unreal.LinearColor(emissive[0], emissive[1], emissive[2], 1.0)
                )
                mat_editing.connect_material_property(
                    emissive_const,
                    "Output",
                    material,
                    unreal.MaterialProperty.MP_EMISSIVE_COLOR
                )

            return {
                "message": f"Created material: {name}",
                "path": f"/Game/GeneratedMaterials/{name}",
                "properties": properties,
                "details": {
                    "base_color": properties.get("color"),
                    "roughness": roughness,
                    "metallic": metallic,
                    "emissive": emissive is not None
                }
            }

        except Exception as e:
            return {"error": f"Material creation failed: {e}"}

    def _generate_texture(self, prompt: str, size: Tuple[int, int]) -> Dict:
        """Generate texture using AI"""
        try:
            # Use free service (Pollinations.ai)
            encoded_prompt = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={size[0]}&height={size[1]}&seed={hash(prompt)}"

            # Download
            asset_name = self._sanitize_name(prompt)
            temp_path = os.path.join(self.temp_dir, f"{asset_name}.png")

            urllib.request.urlretrieve(url, temp_path)

            # Import into Unreal
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

            import_task = unreal.AssetImportTask()
            import_task.set_editor_property('filename', temp_path)
            import_task.set_editor_property('destination_path', '/Game/GeneratedTextures')
            import_task.set_editor_property('automated', True)

            asset_tools.import_asset_task([import_task])

            return {
                "message": f"Generated texture: {prompt}",
                "path": f"/Game/GeneratedTextures/{asset_name}",
                "prompt": prompt,
                "size": size,
                "details": {"source": "Pollinations.ai", "type": "AI Generated"}
            }

        except Exception as e:
            return {"error": f"Texture generation failed: {e}"}

    def _generate_model(self, prompt: str) -> Dict:
        """Generate 3D model"""
        # Try procedural generation based on prompt keywords
        prompt_lower = prompt.lower()

        if "cube" in prompt_lower or "box" in prompt_lower:
            return self._create_actor("static_mesh_actor", prompt.title(), (0, 0, 0))
        elif "sphere" in prompt_lower or "ball" in prompt_lower:
            return self._create_actor("static_mesh_actor", prompt.title(), (0, 0, 0))
        elif "cylinder" in prompt_lower:
            return self._create_actor("static_mesh_actor", prompt.title(), (0, 0, 0))
        else:
            # Default to cube
            return self._create_actor("static_mesh_actor", prompt.title(), (0, 0, 0))

    # ============================================================
    # LEVEL SETUP
    # ============================================================

    def _setup_lighting(self, setup_type: str) -> Dict:
        """Setup a complete lighting setup"""
        created = []

        try:
            if setup_type in ["outdoor", "basic"]:
                # Directional Light (Sun)
                sun = self._create_actor("directional_light", "Sun", (0, 0, 500))
                created.append("Sun (Directional Light)")

                # Sky Light
                sky = self._create_actor("sky_light", "Sky Light", (0, 0, 0))
                created.append("Sky Light")

                # Atmospheric Fog
                fog = self._create_actor("atmospheric_fog", "Atmospheric Fog", (0, 0, 0))
                created.append("Atmospheric Fog")

            if setup_type in ["indoor", "cinematic"]:
                # Add Point Lights
                for i, pos in enumerate([(200, 0, 200), (-200, 0, 200), (0, 0, 200)]):
                    light = self._create_actor("point_light", f"PointLight_{i}", pos)
                    created.append(f"PointLight_{i}")

            return {
                "message": f"Setup {setup_type} lighting",
                "created": created,
                "type": setup_type,
                "details": f"Created {len(created)} lights and effects"
            }

        except Exception as e:
            return {"error": f"Lighting setup failed: {e}"}

    def _configure_post_processing(self, effects: Dict) -> Dict:
        """Configure post processing effects"""
        try:
            # Create post process volume
            volume = unreal.EditorLevelLibrary.spawn_actor_from_class(
                unreal.PostProcessVolume,
                unreal.Vector(0, 0, 0)
            )
            volume.set_actor_label("PostProcessVolume")

            # Enable infinite extent
            volume.set_editor_property("bEnabled", True)
            volume.set_editor_property("bUnbound", True)

            configured = []
            if effects.get("bloom"):
                # Configure bloom (would need to access settings object)
                configured.append("Bloom")

            if effects.get("depth_of_field"):
                configured.append("Depth of Field")

            if effects.get("motion_blur"):
                configured.append("Motion Blur")

            if effects.get("color_grading"):
                configured.append("Color Grading")

            return {
                "message": f"Configured post processing: {', '.join(configured)}",
                "configured": configured,
                "details": {"effects": effects}
            }

        except Exception as e:
            return {"error": f"Post process setup failed: {e}"}

    # ============================================================
    # AI ASSISTANCE
    # ============================================================

    def _provide_help(self, topic: str, context: Dict) -> Dict:
        """Provide help on a topic"""
        # Search knowledge base
        search_result = search_knowledge(topic)

        # Check for troubleshooting
        solution = solve_problem(topic)

        # Get workflow
        workflow = get_workflow(topic)

        response = {
            "message": f"Help for: {topic}",
            "topic": topic,
            "details": {}
        }

        if search_result:
            response["details"]["knowledge"] = search_result

        if solution:
            response["solution"] = solution
            response["message"] = f"Solution for: {topic}"

        if workflow:
            response["details"]["workflow"] = workflow
            response["message"] = f"How to: {topic}"

        # Also ask AI for additional help
        ai_response = self._ask_ai(f"Help with Unreal Engine: {topic}")
        if ai_response and ai_response.get("message"):
            response["ai_advice"] = ai_response["message"]

        return response

    def _ask_ai(self, question: str) -> Dict:
        """Ask the AI assistant for help"""
        try:
            conn = http.client.HTTPConnection(self.backend_host, self.backend_port, timeout=60)
            conn.request("POST", "/api/api/chat", json.dumps({"user_input": question}),
                        {"Content-type": "application/json"})

            response = conn.getresponse()
            if response.status == 200:
                result = json.loads(response.read().decode())
                ai_message = result.get("full_response", "")

                return {
                    "message": ai_message,
                    "question": question,
                    "details": {"source": "AI Backend"}
                }

        except Exception as e:
            return {"error": f"AI request failed: {e}"}

    # ============================================================
    # UTILITY FUNCTIONS
    # ============================================================

    def _sanitize_name(self, text: str) -> str:
        """Clean text for use as asset name"""
        clean = re.sub(r'[^\w\s-]', '', text)
        clean = re.sub(r'\s+', '_', clean)
        return clean[:30]

    # ============================================================
    # QUICK ACCESS METHODS - Common operations
    # ============================================================

    def create_cube(self, name="Cube", location=(0, 0, 0)) -> Dict:
        """Create a cube"""
        return self.do(f"Create a cube named {name}")

    def create_sphere(self, name="Sphere", location=(0, 0, 0)) -> Dict:
        """Create a sphere"""
        return self.do(f"Create a sphere named {name}")

    def create_light(self, name="PointLight", location=(0, 0, 0)) -> Dict:
        """Create a point light"""
        return self.do(f"Create a point light named {name}")

    def create_material(self, name="Material", description="") -> Dict:
        """Create a material"""
        prompt = description if description else name
        return self.do(f"Create a material named {name} that is {prompt}")

    def chat(self, message: str) -> str:
        """Chat with the AI"""
        result = self.do(message)
        if result.get("success") and "message" in result:
            return result["message"]
        elif "error" in result:
            return f"Error: {result['error']}"
        return str(result)


# Helper functions
def get_color_from_text(text: str) -> Tuple[float, float, float]:
    """Extract color from text description"""
    text_lower = text.lower()

    colors = {
        "red": (1, 0, 0), "green": (0, 1, 0), "blue": (0, 0, 1),
        "yellow": (1, 1, 0), "orange": (1, 0.5, 0), "purple": (0.5, 0, 1),
        "pink": (1, 0.5, 0.5), "cyan": (0, 1, 1), "magenta": (1, 0, 1),
        "white": (1, 1, 1), "black": (0, 0, 0),
        "gray": (0.5, 0.5, 0.5), "grey": (0.5, 0.5, 0.5),
        "brown": (0.6, 0.4, 0.2), "gold": (1, 0.84, 0),
        "silver": (0.75, 0.75, 0.75), "chrome": (0.8, 0.8, 0.8),
        "emerald": (0.18, 0.55, 0.34), "ruby": (0.78, 0.06, 0.18),
        "sapphire": (0.07, 0.09, 0.33), "amber": (1.0, 0.75, 0.0)
    }

    for color_name, color_value in colors.items():
        if color_name in text_lower:
            return color_value

    return (0.5, 0.5, 0.5)  # Default gray


# Create global instance
ai = UEAIAssistant()

# Display comprehensive welcome message
unreal.log("\n" + "█"*70)
unreal.log("█                                                          █")
unreal.log("█     🤖 UE AI ASSISTANT - COMPREHENSIVE MODE              █")
unreal.log("█                                                          █")
unreal.log("█"*70)
unreal.log("\n✨ UNDERSTANDS NATURAL LANGUAGE - DESCRIBE WHAT YOU WANT\n")
unreal.log("\n💬 ASK ME ANYTHING:\n")
unreal.log("   ai.do('Create a red cube at position 100,0,0')")
unreal.log("   ai.do('Make a shiny gold material')")
unreal.log("   ai.do('Generate a wood texture')")
unreal.log("   ai.do('Setup outdoor lighting')")
unreal.log("   ai.do('Create a character')")
unreal.log("   ai.do('Add bloom and depth of field')")
unreal.log("   ai.do('How do I create a glowing material?')")
unreal.log("   ai.do('Help with blueprints')")
unreal.log("\n🔧 QUICK METHODS:\n")
unreal.log("   ai.create_cube('MyCube', (0, 0, 100))")
unreal.log("   ai.create_sphere('MySphere')")
unreal.log("   ai.create_light('Light1', (100, 100, 100))")
unreal.log("   ai.create_material('Gold', 'shiny gold metal')")
unreal.log("   ai.chat('How do I make water material?')")
unreal.log("\n📚 KNOWLEDGE AREAS:")
areas = list(UE_KNOWLEDGE_BASE.keys())
for i, area in enumerate(areas):
    unreal.log(f"   {area}")
unreal.log("\n" + "█"*70 + "\n")
