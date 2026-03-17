"""
UE AI Plugin - INFINITE CREATION ENGINE
Can create ANYTHING from natural language - dragons, spaceships, cities, etc.
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
import sys
from typing import Optional, Tuple, List, Dict, Any

sys.path.insert(0, '/Volumes/SERENADA_2/_elliott/Unreal Projects/UEAI-Plugin-Test/Plugins/UEAIPlugin/Content/Python')


class InfiniteCreationEngine:
    """
    INFINITE CREATION ENGINE
    Creates anything through procedural generation, composition, and AI
    """

    def __init__(self):
        self.backend_host = "localhost"
        self.backend_port = 8000
        self.temp_dir = tempfile.gettempdir()
        self.asset_library = {}
        self.creation_history = []

        # Initialize asset library
        self._initialize_asset_library()

    def _initialize_asset_library(self):
        """Initialize procedural asset templates"""
        self.asset_library = {
            # Creatures
            "dragon": {
                "components": ["body", "wings", "tail", "legs", "head"],
                "create": self._create_dragon,
                "materials": ["scales", "skin", "eyes"]
            },
            "wolf": {
                "components": ["body", "head", "legs", "tail"],
                "create": self._create_wolf,
                "materials": ["fur", "eyes"]
            },
            "eagle": {
                "components": ["body", "wings", "head", "tail", "legs"],
                "create": self._create_eagle,
                "materials": ["feathers", "beak"]
            },
            "fish": {
                "components": ["body", "tail", "fins", "head"],
                "create": self._create_fish,
                "materials": ["scales", "fins"]
            },
            "insect": {
                "components": ["body", "wings", "legs", "antennae"],
                "create": self._create_insect,
                "materials": ["shell", "wings"]
            },
            "unicorn": {
                "components": ["body", "head", "legs", "tail", "horn"],
                "create": self._create_unicorn,
                "materials": ["fur", "horn", "mane"]
            },
            "phoenix": {
                "components": ["body", "wings", "tail", "head"],
                "create": self._create_phoenix,
                "materials": ["flames", "feathers"]
            },
            "golem": {
                "components": ["body", "head", "arms", "legs"],
                "create": self._create_golem,
                "materials": ["stone", "crystals"]
            },
            # Corelings (The Painted Man / Demon Cycle series)
            "wind demon": {
                "components": ["body", "wings", "head", "tail", "claws"],
                "create": self._create_wind_demon,
                "materials": ["leather", "scales", "glowing_eyes"]
            },
            "fire demon": {
                "components": ["body", "head", "flames", "arms"],
                "create": self._create_fire_demon,
                "materials": ["flames", "charred_skin", "glowing_core"]
            },
            "water demon": {
                "components": ["body", "tentacles", "head", "tail"],
                "create": self._create_water_demon,
                "materials": ["slick_skin", "scales", "bioluminescence"]
            },
            "rock demon": {
                "components": ["body", "head", "arms", "armor"],
                "create": self._create_rock_demon,
                "materials": ["stone_armor", "rough_skin", "spikes"]
            },
            "wood demon": {
                "components": ["body", "head", "limbs", "vines"],
                "create": self._create_wood_demon,
                "materials": ["bark", "vines", "leaves"]
            },
            "mind demon": {
                "components": ["body", "head", "arms", "aura"],
                "create": self._create_mind_demon,
                "materials": ["pale_skin", "psychic_glow", "robe"]
            },
            "hashak": {
                "components": ["body", "head", "massive_arms", "armor"],
                "create": self._create_hashak,
                "materials": ["thick_armor", "spikes", "glowing_eyes"]
            },
            "clay demon": {
                "components": ["body", "head", "mud_arms", "elemental_form"],
                "create": self._create_clay_demon,
                "materials": ["clay", "mud", "earth"]
            },
            "sand demon": {
                "components": ["body", "head", "shifting_form", "sand"],
                "create": self._create_sand_demon,
                "materials": ["sand", "desert_camouflage", "dust"]
            },
            "ice demon": {
                "components": ["body", "head", "frost_aura", "ice_spikes"],
                "create": self._create_ice_demon,
                "materials": ["ice", "frost", "crystal"]
            },
            "forest demon": {
                "components": ["body", "head", "branches", "camouflage"],
                "create": self._create_forest_demon,
                "materials": ["bark", "moss", "vines"]
            },
            "coreling": {
                "components": ["body", "limbs", "magic_aura"],
                "create": self._create_coreling_generic,
                "materials": ["demon_skin", "magic"]
            },
            "spaceship": {
                "components": ["hull", "cockpit", "engines", "wings"],
                "create": self._create_spaceship,
                "materials": ["metal", "glass", "lights"]
            },
            "tree": {
                "components": ["trunk", "branches", "leaves"],
                "create": self._create_tree,
                "materials": ["bark", "leaves"]
            },
            # Vehicles
            "car": {
                "components": ["body", "cabin", "wheels"],
                "create": self._create_car,
                "materials": ["paint", "glass", "rubber"]
            },
            "motorcycle": {
                "components": ["body", "wheels", "handlebars"],
                "create": self._create_motorcycle,
                "materials": ["metal", "seat", "rubber"]
            },
            "boat": {
                "components": ["hull", "cabin", "propeller"],
                "create": self._create_boat,
                "materials": ["metal", "glass"]
            },
            "airplane": {
                "components": ["fuselage", "wings", "tail", "engines"],
                "create": self._create_airplane,
                "materials": ["metal", "glass"]
            },
            "helicopter": {
                "components": ["body", "rotor", "tail_rotor"],
                "create": self._create_helicopter,
                "materials": ["metal", "glass"]
            },
            "tank": {
                "components": ["body", "turret", "tracks", "barrel"],
                "create": self._create_tank,
                "materials": ["metal", "camouflage"]
            },
            # Architecture
            "castle": {
                "components": ["walls", "towers", "gate", "keep"],
                "create": self._create_castle,
                "materials": ["stone", "wood"]
            },
            "tower": {
                "components": ["base", "walls", "roof", "windows"],
                "create": self._create_tower,
                "materials": ["stone", "wood"]
            },
            "bridge": {
                "components": ["deck", "supports", "railings"],
                "create": self._create_bridge,
                "materials": ["stone", "wood", "metal"]
            },
            "fountain": {
                "components": ["base", "pool", "spout"],
                "create": self._create_fountain,
                "materials": ["stone", "water"]
            },
            "monument": {
                "components": ["base", "statue", "plaque"],
                "create": self._create_monument,
                "materials": ["stone", "metal", "marble"]
            },
            # Natural
            "mountain": {
                "components": ["peak", "slopes", "base"],
                "create": self._create_mountain,
                "materials": ["rock", "snow", "grass"]
            },
            "volcano": {
                "components": ["cone", "crater", "lava"],
                "create": self._create_volcano,
                "materials": ["rock", "lava", "ash"]
            },
            "river": {
                "components": ["bed", "water", "banks"],
                "create": self._create_river,
                "materials": ["water", "sand", "rocks"]
            },
            "cloud": {
                "components": ["puffs"],
                "create": self._create_cloud,
                "materials": ["vapor"]
            },
            "terrain": {
                "components": ["hills", "valleys", "plains"],
                "create": self._create_terrain,
                "materials": ["grass", "dirt", "rock"]
            },
            "building": {
                "components": ["walls", "roof", "door", "windows"],
                "create": self._create_building,
                "materials": ["concrete", "glass", "wood"]
            },
            "vehicle": {
                "components": ["body", "wheels", "windows"],
                "create": self._create_vehicle,
                "materials": ["metal", "glass", "paint"]
            },
            "character": {
                "components": ["body", "head", "limbs"],
                "create": self._create_character_advanced,
                "materials": ["skin", "clothes", "eyes"]
            },
            "weapon": {
                "components": ["blade", "handle", "guard"],
                "create": self._create_weapon,
                "materials": ["steel", "wood", "leather"]
            },
            "furniture": {
                "components": ["seat", "back", "legs"],
                "create": self._create_furniture,
                "materials": ["wood", "fabric", "metal"]
            }
        }

    def create(self, description: str) -> dict:
        """
        Main creation interface - creates anything from description

        Examples:
            create("a red dragon")
            create("a sci-fi spaceship")
            create("a medieval castle")
            create("a sports car")
            create("a fantasy character with sword")
            create("a dragon with red scales and gold eyes")
            create("a wooden chair")
        """
        unreal.log("\n" + "="*70)
        unreal.log(f"🎨 CREATING: {description}")
        unreal.log("="*70)

        # Parse the request
        parsed = self._parse_creation_request(description)

        # Create the asset
        try:
            result = self._create_from_parsed(parsed)
            unreal.log(f"✅ Created: {description}")
            return result
        except Exception as e:
            unreal.log_error(f"❌ Creation failed: {e}")
            return {"error": str(e)}

    def _parse_creation_request(self, description: str) -> dict:
        """Parse creation request into structured data"""
        desc_lower = description.lower()

        parsed = {
            "original": description,
            "type": None,
            "name": None,
            "properties": {},
            "components": [],
            "quantifiers": []
        }

        # Determine type
        types = [
            # Creatures
            "dragon", "wolf", "eagle", "fish", "insect", "unicorn", "phoenix", "golem",
            "creature", "monster", "animal", "beast",
            # Corelings (The Painted Man / Demon Cycle)
            "wind demon", "fire demon", "water demon", "rock demon", "wood demon",
            "mind demon", "hashak", "clay demon", "sand demon", "ice demon", "forest demon",
            "coreling", "demon",
            # Vehicles
            "spaceship", "starship", "car", "motorcycle", "boat", "airplane", "helicopter", "tank",
            "vehicle", "ship", "plane",
            # Buildings & Architecture
            "building", "castle", "tower", "bridge", "fountain", "monument",
            "house", "structure", "architecture",
            # Characters & Items
            "character", "person", "human",
            "weapon", "sword", "axe", "bow",
            "furniture", "chair", "table", "bed",
            # Nature
            "tree", "mountain", "volcano", "river", "lake", "ocean", "cloud", "sky", "terrain",
            "rock", "plant", "flower"
        ]

        detected_type = None
        for t in types:
            if t in desc_lower:
                detected_type = t
                break

        if not detected_type:
            # Default to procedural shape
            if "cube" in desc_lower or "box" in desc_lower:
                detected_type = "cube"
            elif "sphere" in desc_lower or "ball" in desc_lower:
                detected_type = "sphere"
            else:
                detected_type = "generic"

        parsed["type"] = detected_type

        # Extract properties
        parsed["properties"]["color"] = self._extract_color_advanced(description)
        parsed["properties"]["size"] = self._extract_size_advanced(description)
        parsed["properties"]["material"] = self._extract_material_properties(description)
        parsed["properties"]["style"] = self._extract_style(description)
        parsed["properties"]["position"] = self._extract_position(description)
        parsed["properties"]["quantity"] = self._extract_quantity_advanced(description)

        return parsed

    def _create_from_parsed(self, parsed: dict) -> dict:
        """Create asset from parsed description"""
        asset_type = parsed["type"]

        if asset_type in self.asset_library:
            # Use specialized creator
            creator_func = self.asset_library[asset_type]["create"]
            return creator_func(parsed)
        else:
            # Generic procedural creation
            return self._create_generic(parsed)

    # ============================================================
    # COMPLEX CREATION FUNCTIONS
    # ============================================================

    def _create_dragon(self, parsed: dict) -> dict:
        """Create a dragon from components"""
        name = parsed.get("name") or "Dragon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.0

        unreal.log("🐉 Creating dragon...")

        created_actors = []
        group_name = name

        # Main body (elongated cube)
        body_scale = (scale * 2, scale * 0.8, scale * 4)
        body_pos = (position[0], position[1], position[2] + scale * 2)
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            props.get("color", (0.8, 0.2, 0.1)))
        created_actors.append(body["actor"])

        # Neck
        neck_scale = (scale * 0.3, scale * 0.3, scale * 0.5)
        neck_pos = (position[0], position[1], position[2] + scale * 4)
        neck = self._create_composite_cube(
            f"{name}_Neck", neck_pos, neck_scale,
            props.get("color", (0.8, 0.2, 0.1)))
        created_actors.append(neck["actor"])

        # Head
        head_scale = (scale * 0.5, scale * 0.4, scale * 0.6)
        head_pos = (position[0], position[1] + scale * 0.3, position[2] + scale * 4.5)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            props.get("color", (0.8, 0.2, 0.1)))
        created_actors.append(head["actor"])

        # Eyes (if specified)
        if "eyes" in parsed["original"].lower() or "eye" in parsed["original"].lower():
            eye_color = self._extract_color_from_context(parsed["original"], "red")
            # Create small spheres for eyes
            eye_scale = (scale * 0.1, scale * 0.1, scale * 0.1)
            eye_pos_l = (head_pos[0] - scale * 0.15, head_pos[1], head_pos[2] + scale * 0.3)
            eye_pos_r = (head_pos[0] + scale * 0.15, head_pos[1], head_pos[2] + scale * 0.3)

            eye_l = self._create_composite_cube(
                f"{name}_Eye_L", eye_pos_l, eye_scale, eye_color
            )
            eye_r = self._create_composite_cube(
                f"{name}_Eye_R", eye_pos_r, eye_scale, eye_color
            )
            created_actors.append(eye_l["actor"])
            created_actors.append(eye_r["actor"])

        # Wings (spread out)
        wing_span = scale * 6
        wing_positions = [
            (position[0] - scale * 2, position[1], position[2] + scale * 2),
            (position[0] + scale * 2, position[1], position[2] + scale * 2)
        ]

        for i, wing_pos in enumerate(wing_positions):
            wing_scale = (scale * 3, scale * 0.1, scale * 2)
            wing = self._create_composite_cube(
                f"{name}_Wing_{i}", wing_pos, wing_scale,
                props.get("color", (0.6, 0.1, 0.05))
            )
            created_actors.append(wing["actor"])

        # Tail
        tail_segments = 5
        for i in range(tail_segments):
            tail_scale = (scale * (1 - i * 0.15), scale * 0.3, scale * 0.3)
            tail_pos = (
                position[0],
                position[1] - scale * 0.3 * i,
                position[2] + scale * 2 - scale * 0.3 * i
            )
            tail = self._create_composite_cube(
                f"{name}_Tail_{i}", tail_pos, tail_scale,
                props.get("color", (0.8, 0.2, 0.1))
            )
            created_actors.append(tail["actor"])

        # Legs (4 legs)
        leg_positions = [
            (position[0] - scale * 0.5, position[1] - scale * 0.5, position[2]),
            (position[0] + scale * 0.5, position[1] - scale * 0.5, position[2]),
            (position[0] - scale * 0.5, position[1] + scale * 0.5, position[2]),
            (position[0] + scale * 0.5, position[1] + scale * 0.5, position[2]),
        ]

        for i, leg_pos in enumerate(leg_positions):
            leg_scale = (scale * 0.3, scale * 0.3, scale * 1.5)
            leg = self._create_composite_cube(
                f"{name}_Leg_{i}", leg_pos, leg_scale,
                props.get("color", (0.8, 0.2, 0.1))
            )
            created_actors.append(leg["actor"])

        # Create dragon material
        self._create_dragon_material(props)

        unreal.log(f"🐉 Dragon created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Dragon)",
            "name": name,
            "type": "dragon",
            "actors": created_actors,
            "components": len(created_actors)
        }

    def _create_spaceship(self, parsed: dict) -> dict:
        """Create a spaceship"""
        name = parsed.get("name") or "Spaceship"
        props = parsed["properties"]
        position = props["position"]
        style = props["style"] or "sci-fi"
        scale = props["size"] or 1.0

        unreal.log("🚀 Creating spaceship...")

        created_actors = []

        # Main hull
        hull_scale = (scale * 3, scale * 1, scale * 6)
        hull_pos = position
        hull = self._create_composite_cube(
            f"{name}_Hull", hull_pos, hull_scale,
            self._get_spaceship_color(style)
        )
        created_actors.append(hull["actor"])

        # Cockpit
        cockpit_scale = (scale * 1.2, scale * 0.8, scale * 1)
        cockpit_pos = (position[0], position[1] + scale * 0.5, position[2] + scale * 2)
        cockpit = self._create_composite_cube(
            f"{name}_Cockpit", cockpit_pos, cockpit_scale,
            (0.2, 0.3, 0.4)
        )
        created_actors.append(cockpit["actor"])

        # Engines (3 engines)
        for i in range(3):
            engine_scale = (scale * 0.4, scale * 0.4, scale * 0.6)
            engine_pos = (
                position[0] + (i - 1) * scale * 1.5,
                position[1] - scale * 0.6,
                position[2] - scale * 1.5
            )
            engine = self._create_composite_cube(
                f"{name}_Engine_{i}", engine_pos, engine_scale,
                (0.3, 0.3, 0.3)
            )
            created_actors.append(engine["actor"])

        # Wings
        wing_span = scale * 8
        for side in [-1, 1]:
            wing_scale = (scale * 4, scale * 0.1, scale * 1.5)
            wing_pos = (position[0] + side * scale * 2, position[1], position[2] + scale * 0.5)
            wing = self._create_composite_cube(
                f"{name}_Wing_{'R' if side > 0 else 'L'}", wing_pos, wing_scale,
                self._get_spaceship_color(style)
            )
            created_actors.append(wing["actor"])

        unreal.log(f"🚀 Spaceship created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Spaceship)",
            "name": name,
            "type": "spaceship",
            "actors": created_actors
        }

    def _create_tree(self, parsed: dict) -> dict:
        """Create a tree"""
        name = parsed.get("name") or "Tree"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.0

        unreal.log("🌳 Creating tree...")

        created_actors = []

        # Trunk
        trunk_scale = (scale * 0.3, scale * 0.3, scale * 4)
        trunk_pos = position
        trunk = self._create_composite_cube(
            f"{name}_Trunk", trunk_pos, trunk_scale,
            self._get_tree_bark_color()
        )
        created_actors.append(trunk["actor"])

        # Branches
        num_branches = 5
        for i in range(num_branches):
            angle = (2 * math.pi * i) / num_branches
            branch_length = scale * 2
            branch_pos = (
                position[0] + branch_length * 0.7 * math.cos(angle),
                position[1] + branch_length * 0.7 * math.sin(angle),
                position[2] + scale * 3
            )
            branch_scale = (scale * 0.1, scale * 0.1, branch_length)
            branch = self._create_composite_cube(
                f"{name}_Branch_{i}", branch_pos, branch_scale,
                self._get_tree_bark_color()
            )
            created_actors.append(branch["actor"])

            # Leaves (simple cubes for now)
            num_leaves = 3
            for j in range(num_leaves):
                leaf_angle = angle + (j - 1) * 0.5
                leaf_pos = (
                    branch_pos[0] + branch_scale[0] * math.cos(leaf_angle),
                    branch_pos[1] + branch_scale[1] * math.sin(leaf_angle),
                    branch_pos[2] + branch_scale[2] * 0.5
                )
                leaf = self._create_composite_cube(
                    f"{name}_Leaf_{i}_{j}", leaf_pos,
                    (scale * 0.3, scale * 0.3, scale * 0.3),
                    self._get_leaf_color()
                )
                created_actors.append(leaf["actor"])

        unreal.log(f"🌳 Tree created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Tree)",
            "name": name,
            "type": "tree",
            "actors": created_actors
        }

    def _create_building(self, parsed: dict) -> dict:
        """Create a building"""
        name = parsed.get("name") or "Building"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.0

        unreal.log("🏠 Creating building...")

        created_actors = []

        # Floor
        floor_scale = (scale * 4, scale * 4, scale * 0.2)
        floor_pos = position
        floor = self._create_composite_cube(
            f"{name}_Floor", floor_pos, floor_scale,
            (0.5, 0.5, 0.5)
        )
        created_actors.append(floor["actor"])

        # Walls (4 walls)
        wall_configs = [
            ("BackWall", (0, -scale * 2, scale * 2), (scale * 4, scale * 0.3, scale * 4)),
            ("FrontWall", (0, scale * 2, scale * 2), (scale * 4, scale * 0.3, scale * 4)),
            ("LeftWall", (-scale * 2, 0, scale * 2), (scale * 0.3, scale * 4, scale * 4)),
            ("RightWall", (scale * 2, 0, scale * 2), (scale * 0.3, scale * 4, scale * 4))
        ]

        for wall_name, wall_pos, wall_scale in wall_configs:
            wall = self._create_composite_cube(
                f"{name}_{wall_name}", wall_pos, wall_scale,
                (0.8, 0.8, 0.75)
            )
            created_actors.append(wall["actor"])

        # Roof
        roof_scale = (scale * 4.2, scale * 4.2, scale * 0.3)
        roof_pos = (position[0], position[1], position[2] + scale * 4)
        roof = self._create_composite_cube(
            f"{name}_Roof", roof_pos, roof_scale,
            (0.6, 0.4, 0.3)
        )
        created_actors.append(roof["actor"])

        # Door
        door_scale = (scale * 0.8, scale * 1.5, scale * 0.2)
        door_pos = (position[0], position[1] + scale * 2 - scale * 0.75, scale * 2)
        door = self._create_composite_cube(
            f"{name}_Door", door_pos, door_scale,
            (0.4, 0.25, 0.15)
        )
        created_actors.append(door["actor"])

        # Windows
        for side in [-1, 1]:
            window_scale = (scale * 0.8, scale * 0.6, scale * 0.2)
            window_pos = (position[0] + side * scale * 1.2, position[1], scale * 3)
            window = self._create_composite_cube(
                f"{name}_Window_{'R' if side > 0 else 'L'}", window_pos, window_scale,
                (0.3, 0.5, 0.7)  # Glass-like
            )
            created_actors.append(window["actor"])

        unreal.log(f"🏠 Building created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Building)",
            "name": name,
            "type": "building",
            "actors": created_actors
        }

    def _create_character_advanced(self, parsed: dict) -> dict:
        """Create a character"""
        name = parsed.get("name") or "Character"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.0

        unreal.log("👤 Creating character...")

        created_actors = []

        # Body
        body_scale = (scale * 0.6, scale * 0.3, scale * 1.7)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            props.get("color", (0.8, 0.6, 0.5))
        )
        created_actors.append(body["actor"])

        # Head
        head_scale = (scale * 0.3, scale * 0.3, scale * 0.35)
        head_pos = (position[0], position[1], position[2] + scale * 1.8)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            props.get("color", (0.9, 0.7, 0.6))
        )
        created_actors.append(head["actor"])

        # Eyes
        eye_color = self._extract_color_from_context(parsed["original"], "blue")
        eye_scale = (scale * 0.05, scale * 0.05, scale * 0.05)
        eye_pos_l = (head_pos[0] - scale * 0.1, head_pos[1], head_pos[2] + scale * 0.18)
        eye_pos_r = (head_pos[0] + scale * 0.1, head_pos[1], head_pos[2] + scale * 0.18)

        eye_l = self._create_composite_cube(
            f"{name}_Eye_L", eye_pos_l, eye_scale, eye_color
        )
        eye_r = self._create_composite_cube(
            f"{name}_Eye_R", eye_pos_r, eye_scale, eye_color
        )
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Arms
        arm_scale = (scale * 0.15, scale * 0.15, scale * 0.7)
        arm_pos_l = (position[0] - scale * 0.45, position[1], position[2] + scale * 1.3)
        arm_pos_r = (position[0] + scale * 0.45, position[1], position[2] + scale * 1.3)

        arm_l = self._create_composite_cube(
            f"{name}_Arm_L", arm_pos_l, arm_scale,
            props.get("color", (0.8, 0.6, 0.5))
        )
        arm_r = self._create_composite_cube(
            f"{name}_Arm_R", arm_pos_r, arm_scale,
            props.get("color", (0.8, 0.6, 0.5))
        )
        created_actors.append(arm_l["actor"])
        created_actors.append(arm_r["actor"])

        # Hands
        hand_scale = (scale * 0.12, scale * 0.1, scale * 0.12)
        hand_pos_l = (arm_pos_l[0], arm_pos_l[1], arm_pos_l[2] + scale * 0.7)
        hand_pos_r = (arm_pos_r[0], arm_pos_r[1], arm_pos_r[2] + scale * 0.7)

        hand_l = self._create_composite_cube(
            f"{name}_Hand_L", hand_pos_l, hand_scale,
            props.get("color", (0.9, 0.7, 0.6))
        )
        hand_r = self._create_composite_cube(
            f"{name}_Hand_R", hand_pos_r, hand_scale,
            props.get("color", (0.9, 0.7, 0.6))
        )
        created_actors.append(hand_l["actor"])
        created_actors.append(hand_r["actor"])

        # Legs
        leg_scale = (scale * 0.15, scale * 0.15, scale * 0.8)
        leg_pos_l = (position[0] - scale * 0.15, position[1], position[2])
        leg_pos_r = (position[0] + scale * 0.15, position[1], position[2])

        leg_l = self._create_composite_cube(
            f"{name}_Leg_L", leg_pos_l, leg_scale,
            props.get("color", (0.8, 0.6, 0.5))
        )
        leg_r = self._create_composite_cube(
            f"{name}_Leg_R", leg_pos_r, leg_scale,
            props.get("color", (0.8, 0.6, 0.5))
        )
        created_actors.append(leg_l["actor"])
        created_actors.append(leg_r["actor"])

        unreal.log(f"👤 Character created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Character)",
            "name": name,
            "type": "character",
            "actors": created_actors
        }

    def _create_weapon(self, parsed: dict) -> dict:
        """Create a weapon"""
        name = parsed.get("name") or "Weapon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.0

        unreal.log("⚔️ Creating weapon...")

        created_actors = []

        # Handle
        handle_scale = (scale * 0.15, scale * 0.15, scale * 0.8)
        handle_pos = (position[0], position[1], position[2] + scale * 0.4)
        handle = self._create_composite_cube(
            f"{name}_Handle", handle_pos, handle_scale,
            (0.4, 0.3, 0.2)  # Wood/leather
        )
        created_actors.append(handle["actor"])

        # Guard
        guard_scale = (scale * 0.1, scale * 0.3, scale * 0.6)
        guard_pos = (position[0], position[1], position[2] + scale * 1.2)
        guard = self._create_composite_cube(
            f"{name}_Guard", guard_pos, guard_scale,
            (0.7, 0.6, 0.5)  # Steel/metal
        )
        created_actors.append(guard["actor"])

        # Blade
        blade_scale = (scale * 0.08, scale * 1.5, scale * 0.1)
        blade_pos = (position[0], position[1], position[2] + scale * 2)
        blade = self._create_composite_cube(
            f"{name}_Blade", blade_pos, blade_scale,
            (0.9, 0.9, 0.7)  # Sharp metal
        )
        created_actors.append(blade["actor"])

        unreal.log(f"⚔️ Weapon created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Weapon)",
            "name": name,
            "type": "weapon",
            "actors": created_actors
        }

    def _create_vehicle(self, parsed: dict) -> dict:
        """Create a vehicle"""
        name = parsed.get("name") or "Vehicle"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.0

        unreal.log("🚗 Creating vehicle...")

        created_actors = []

        # Body
        body_scale = (scale * 2, scale * 1, scale * 4)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            props.get("color", (0.2, 0.4, 0.8))  # Blue
        )
        created_actors.append(body["actor"])

        # Cabin
        cabin_scale = (scale * 1.5, scale * 1.2, scale * 1)
        cabin_pos = (position[0], position[1] + scale * 0.4, position[2] + scale * 1)
        cabin = self._create_composite_cube(
            f"{name}_Cabin", cabin_pos, cabin_scale,
            (0.3, 0.5, 0.7)  # Glass
        )
        created_actors.append(cabin["actor"])

        # Wheels (4 wheels)
        wheel_scale = (scale * 0.6, scale * 0.6, scale * 0.6)
        wheel_positions = [
            (position[0] + scale * 1.2, position[1] - scale * 0.8, position[2]),
            (position[0] + scale * 1.2, position[1] + scale * 0.8, position[2]),
            (position[0] - scale * 1.2, position[1] - scale * 0.8, position[2]),
            (position[0] - scale * 1.2, position[1] + scale * 0.8, position[2])
        ]

        for i, wheel_pos in enumerate(wheel_positions):
            wheel = self._create_composite_cube(
                f"{name}_Wheel_{i}", wheel_pos, wheel_scale,
                (0.1, 0.1, 0.1)  # Black rubber
            )
            created_actors.append(wheel["actor"])

        unreal.log(f"🚗 Vehicle created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Vehicle)",
            "name": name,
            "type": "vehicle",
            "actors": created_actors
        }

    def _create_wolf(self, parsed: dict) -> dict:
        """Create a wolf"""
        name = parsed.get("name") or "Wolf"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 0.8

        unreal.log("🐺 Creating wolf...")

        created_actors = []

        # Body
        body_scale = (scale * 0.4, scale * 0.3, scale * 0.8)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            props.get("color", (0.5, 0.4, 0.3))
        )
        created_actors.append(body["actor"])

        # Head
        head_scale = (scale * 0.2, scale * 0.2, scale * 0.25)
        head_pos = (position[0], position[1], position[2] + scale * 0.5)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            props.get("color", (0.5, 0.4, 0.3))
        )
        created_actors.append(head["actor"])

        # Snout
        snout_scale = (scale * 0.08, scale * 0.25, scale * 0.1)
        snout_pos = (position[0], position[1] + scale * 0.2, position[2] + scale * 0.5)
        snout = self._create_composite_cube(
            f"{name}_Snout", snout_pos, snout_scale,
            props.get("color", (0.5, 0.4, 0.3))
        )
        created_actors.append(snout["actor"])

        # Ears (pointed)
        ear_scale = (scale * 0.06, scale * 0.06, scale * 0.12)
        ear_pos_l = (head_pos[0] - scale * 0.08, head_pos[1], head_pos[2] + scale * 0.15)
        ear_pos_r = (head_pos[0] + scale * 0.08, head_pos[1], head_pos[2] + scale * 0.15)
        ear_l = self._create_composite_cube(f"{name}_Ear_L", ear_pos_l, ear_scale, props.get("color", (0.5, 0.4, 0.3)))
        ear_r = self._create_composite_cube(f"{name}_Ear_R", ear_pos_r, ear_scale, props.get("color", (0.5, 0.4, 0.3)))
        created_actors.append(ear_l["actor"])
        created_actors.append(ear_r["actor"])

        # Legs (4 legs)
        leg_scale = (scale * 0.08, scale * 0.08, scale * 0.4)
        leg_positions = [
            (position[0] - scale * 0.15, position[1] - scale * 0.15, position[2] - scale * 0.2),
            (position[0] + scale * 0.15, position[1] - scale * 0.15, position[2] - scale * 0.2),
            (position[0] - scale * 0.15, position[1] + scale * 0.15, position[2] - scale * 0.2),
            (position[0] + scale * 0.15, position[1] + scale * 0.15, position[2] - scale * 0.2),
        ]
        for i, leg_pos in enumerate(leg_positions):
            leg = self._create_composite_cube(
                f"{name}_Leg_{i}", leg_pos, leg_scale,
                props.get("color", (0.5, 0.4, 0.3))
            )
            created_actors.append(leg["actor"])

        # Tail
        tail_scale = (scale * 0.08, scale * 0.3, scale * 0.08)
        tail_pos = (position[0], position[1] - scale * 0.25, position[2])
        tail = self._create_composite_cube(
            f"{name}_Tail", tail_pos, tail_scale,
            props.get("color", (0.4, 0.3, 0.2))
        )
        created_actors.append(tail["actor"])

        unreal.log(f"🐺 Wolf created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Wolf)",
            "name": name,
            "type": "wolf",
            "actors": created_actors
        }

    def _create_eagle(self, parsed: dict) -> dict:
        """Create an eagle"""
        name = parsed.get("name") or "Eagle"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.0

        unreal.log("🦅 Creating eagle...")

        created_actors = []

        # Body
        body_scale = (scale * 0.3, scale * 0.2, scale * 0.5)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            props.get("color", (0.4, 0.3, 0.2))
        )
        created_actors.append(body["actor"])

        # Head
        head_scale = (scale * 0.15, scale * 0.15, scale * 0.15)
        head_pos = (position[0], position[1], position[2] + scale * 0.35)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (1, 1, 1)  # White eagle head
        )
        created_actors.append(head["actor"])

        # Beak
        beak_scale = (scale * 0.03, scale * 0.1, scale * 0.05)
        beak_pos = (position[0], position[1] + scale * 0.12, position[2] + scale * 0.35)
        beak = self._create_composite_cube(
            f"{name}_Beak", beak_pos, beak_scale,
            (1, 0.84, 0)  # Gold/yellow beak
        )
        created_actors.append(beak["actor"])

        # Wings (large, spread out)
        wing_span = scale * 4
        for side in [-1, 1]:
            wing_scale = (scale * 2, scale * 0.05, scale * 0.6)
            wing_pos = (position[0] + side * scale, position[1], position[2] + scale * 0.1)
            wing = self._create_composite_cube(
                f"{name}_Wing_{'R' if side > 0 else 'L'}", wing_pos, wing_scale,
                props.get("color", (0.3, 0.3, 0.4))
            )
            created_actors.append(wing["actor"])

        # Tail
        tail_scale = (scale * 0.2, scale * 0.3, scale * 0.05)
        tail_pos = (position[0], position[1] - scale * 0.2, position[2] - scale * 0.1)
        tail = self._create_composite_cube(
            f"{name}_Tail", tail_pos, tail_scale,
            (0.2, 0.2, 0.3)
        )
        created_actors.append(tail["actor"])

        unreal.log(f"🦅 Eagle created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Eagle)",
            "name": name,
            "type": "eagle",
            "actors": created_actors
        }

    def _create_fish(self, parsed: dict) -> dict:
        """Create a fish"""
        name = parsed.get("name") or "Fish"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 0.5

        unreal.log("🐟 Creating fish...")

        created_actors = []

        # Body (streamlined)
        body_scale = (scale * 0.2, scale * 0.15, scale * 0.5)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            props.get("color", (0.3, 0.5, 0.7))
        )
        created_actors.append(body["actor"])

        # Head
        head_scale = (scale * 0.12, scale * 0.12, scale * 0.12)
        head_pos = (position[0], position[1], position[2] + scale * 0.3)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            props.get("color", (0.3, 0.5, 0.7))
        )
        created_actors.append(head["actor"])

        # Tail
        tail_scale = (scale * 0.15, scale * 0.02, scale * 0.15)
        tail_pos = (position[0], position[1] - scale * 0.15, position[2] - scale * 0.2)
        tail = self._create_composite_cube(
            f"{name}_Tail", tail_pos, tail_scale,
            props.get("color", (0.3, 0.5, 0.7))
        )
        created_actors.append(tail["actor"])

        # Fins
        fin_scale = (scale * 0.08, scale * 0.02, scale * 0.12)
        fin_positions = [
            (position[0] + scale * 0.1, position[1], position[2]),
            (position[0] - scale * 0.1, position[1], position[2]),
        ]
        for i, fin_pos in enumerate(fin_positions):
            fin = self._create_composite_cube(
                f"{name}_Fin_{i}", fin_pos, fin_scale,
                (0.2, 0.4, 0.6)
            )
            created_actors.append(fin["actor"])

        unreal.log(f"🐟 Fish created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Fish)",
            "name": name,
            "type": "fish",
            "actors": created_actors
        }

    def _create_insect(self, parsed: dict) -> dict:
        """Create an insect"""
        name = parsed.get("name") or "Insect"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 0.2

        unreal.log("🪲 Creating insect...")

        created_actors = []

        # Body segments
        for i in range(3):
            segment_scale = (scale * 0.08, scale * 0.08, scale * 0.1)
            segment_pos = (position[0], position[1] + scale * i * 0.1, position[2])
            segment = self._create_composite_cube(
                f"{name}_Body_{i}", segment_pos, segment_scale,
                props.get("color", (0.2, 0.2, 0.2))
            )
            created_actors.append(segment["actor"])

        # Wings (4 wings, 2 pairs)
        wing_scale = (scale * 0.15, scale * 0.01, scale * 0.1)
        for i in range(4):
            wing_pos = (
                position[0] + ((-1) ** i) * scale * 0.1,
                position[1] + scale * 0.1,
                position[2] + ((-1) ** (i // 2)) * scale * 0.05
            )
            wing = self._create_composite_cube(
                f"{name}_Wing_{i}", wing_pos, wing_scale,
                (0.9, 0.9, 0.9, 0.5)  # Semi-transparent
            )
            created_actors.append(wing["actor"])

        # Legs (6 legs)
        leg_scale = (scale * 0.01, scale * 0.1, scale * 0.01)
        for i in range(6):
            leg_pos = (
                position[0] + ((-1) ** i) * scale * 0.05,
                position[1] + (i // 2) * scale * 0.1,
                position[2] - scale * 0.05
            )
            leg = self._create_composite_cube(
                f"{name}_Leg_{i}", leg_pos, leg_scale,
                (0.2, 0.2, 0.2)
            )
            created_actors.append(leg["actor"])

        unreal.log(f"🪲 Insect created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Insect)",
            "name": name,
            "type": "insect",
            "actors": created_actors
        }

    def _create_unicorn(self, parsed: dict) -> dict:
        """Create a unicorn"""
        name = parsed.get("name") or "Unicorn"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.5

        unreal.log("🦄 Creating unicorn...")

        created_actors = []

        # Body (similar to horse)
        body_scale = (scale * 0.6, scale * 0.3, scale * 1.2)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            props.get("color", (1, 1, 1))  # White unicorn
        )
        created_actors.append(body["actor"])

        # Head
        head_scale = (scale * 0.2, scale * 0.2, scale * 0.3)
        head_pos = (position[0], position[1], position[2] + scale * 0.75)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            props.get("color", (1, 1, 1))
        )
        created_actors.append(head["actor"])

        # Horn (spiraled)
        horn_scale = (scale * 0.04, scale * 0.04, scale * 0.4)
        horn_pos = (position[0], position[1], position[2] + scale * 1.1)
        horn = self._create_composite_cube(
            f"{name}_Horn", horn_pos, horn_scale,
            (1, 0.84, 0.5)  # Golden horn
        )
        created_actors.append(horn["actor"])

        # Mane
        for i in range(5):
            mane_scale = (scale * 0.02, scale * 0.15, scale * 0.2)
            mane_pos = (position[0] - scale * 0.05, position[1] - scale * 0.1 + i * scale * 0.05, position[2] + scale * 0.8)
            mane = self._create_composite_cube(
                f"{name}_Mane_{i}", mane_pos, mane_scale,
                props.get("color", (0.9, 0.7, 0.9))  # Pinkish mane
            )
            created_actors.append(mane["actor"])

        # Legs (4 legs)
        leg_scale = (scale * 0.1, scale * 0.1, scale * 0.8)
        leg_positions = [
            (position[0] - scale * 0.25, position[1] - scale * 0.15, position[2] - scale * 0.4),
            (position[0] + scale * 0.25, position[1] - scale * 0.15, position[2] - scale * 0.4),
            (position[0] - scale * 0.25, position[1] + scale * 0.15, position[2] - scale * 0.4),
            (position[0] + scale * 0.25, position[1] + scale * 0.15, position[2] - scale * 0.4),
        ]
        for i, leg_pos in enumerate(leg_positions):
            leg = self._create_composite_cube(
                f"{name}_Leg_{i}", leg_pos, leg_scale,
                props.get("color", (1, 1, 1))
            )
            created_actors.append(leg["actor"])

        # Tail
        tail_scale = (scale * 0.05, scale * 0.3, scale * 0.05)
        tail_pos = (position[0], position[1] - scale * 0.25, position[2] + scale * 0.2)
        tail = self._create_composite_cube(
            f"{name}_Tail", tail_pos, tail_scale,
            props.get("color", (0.9, 0.7, 0.9))
        )
        created_actors.append(tail["actor"])

        unreal.log(f"🦄 Unicorn created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Unicorn)",
            "name": name,
            "type": "unicorn",
            "actors": created_actors
        }

    def _create_phoenix(self, parsed: dict) -> dict:
        """Create a phoenix"""
        name = parsed.get("name") or "Phoenix"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("🔥 Creating phoenix...")

        created_actors = []

        # Body
        body_scale = (scale * 0.4, scale * 0.3, scale * 0.7)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (1, 0.3, 0)  # Fiery orange-red
        )
        created_actors.append(body["actor"])

        # Head
        head_scale = (scale * 0.2, scale * 0.15, scale * 0.2)
        head_pos = (position[0], position[1], position[2] + scale * 0.45)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (1, 0.4, 0.1)
        )
        created_actors.append(head["actor"])

        # Wings (large, flaming)
        for side in [-1, 1]:
            wing_scale = (scale * 2.5, scale * 0.05, scale * 1)
            wing_pos = (position[0] + side * scale * 0.8, position[1], position[2] + scale * 0.2)
            wing = self._create_composite_cube(
                f"{name}_Wing_{'R' if side > 0 else 'L'}", wing_pos, wing_scale,
                (1, 0.5, 0)  # Orange flames
            )
            created_actors.append(wing["actor"])

        # Tail (fiery plumes)
        for i in range(5):
            tail_scale = (scale * 0.1, scale * 0.3, scale * 0.05)
            tail_pos = (
                position[0] + (i - 2) * scale * 0.1,
                position[1] - scale * 0.4,
                position[2] - scale * 0.2
            )
            tail = self._create_composite_cube(
                f"{name}_Tail_{i}", tail_pos, tail_scale,
                (1, 0.3 - i * 0.05, 0)  # Gradient from orange to red
            )
            created_actors.append(tail["actor"])

        # Flame particles (simulated with small cubes)
        for i in range(10):
            flame_scale = (scale * 0.05, scale * 0.05, scale * 0.05)
            flame_pos = (
                position[0] + (i % 3 - 1) * scale * 0.3,
                position[1] + (i // 3 - 1) * scale * 0.3,
                position[2] + scale * 0.5 + (i % 2) * scale * 0.2
            )
            flame = self._create_composite_cube(
                f"{name}_Flame_{i}", flame_pos, flame_scale,
                (1, 1, 0)  # Yellow flames
            )
            created_actors.append(flame["actor"])

        unreal.log(f"🔥 Phoenix created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Phoenix)",
            "name": name,
            "type": "phoenix",
            "actors": created_actors
        }

    def _create_golem(self, parsed: dict) -> dict:
        """Create a golem"""
        name = parsed.get("name") or "Golem"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 3.0

        unreal.log("🗿 Creating golem...")

        created_actors = []

        # Body (large, blocky)
        body_scale = (scale * 1.5, scale * 1.2, scale * 2.5)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.4, 0.35, 0.3)  # Stone color
        )
        created_actors.append(body["actor"])

        # Head (blocky)
        head_scale = (scale * 0.8, scale * 0.7, scale * 0.8)
        head_pos = (position[0], position[1], position[2] + scale * 1.8)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (0.4, 0.35, 0.3)
        )
        created_actors.append(head["actor"])

        # Eyes (glowing crystals)
        eye_scale = (scale * 0.15, scale * 0.1, scale * 0.15)
        eye_pos_l = (head_pos[0] - scale * 0.2, head_pos[1], head_pos[2] + scale * 0.2)
        eye_pos_r = (head_pos[0] + scale * 0.2, head_pos[1], head_pos[2] + scale * 0.2)
        eye_l = self._create_composite_cube(
            f"{name}_Eye_L", eye_pos_l, eye_scale,
            (0.2, 0.8, 1)  # Glowing blue
        )
        eye_r = self._create_composite_cube(
            f"{name}_Eye_R", eye_pos_r, eye_scale,
            (0.2, 0.8, 1)
        )
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Arms (massive)
        arm_scale = (scale * 0.5, scale * 0.5, scale * 1.5)
        arm_pos_l = (position[0] - scale * 1.2, position[1], position[2] + scale * 0.5)
        arm_pos_r = (position[0] + scale * 1.2, position[1], position[2] + scale * 0.5)
        arm_l = self._create_composite_cube(
            f"{name}_Arm_L", arm_pos_l, arm_scale,
            (0.4, 0.35, 0.3)
        )
        arm_r = self._create_composite_cube(
            f"{name}_Arm_R", arm_pos_r, arm_scale,
            (0.4, 0.35, 0.3)
        )
        created_actors.append(arm_l["actor"])
        created_actors.append(arm_r["actor"])

        # Hands (large, blocky)
        hand_scale = (scale * 0.6, scale * 0.4, scale * 0.4)
        hand_pos_l = (arm_pos_l[0], arm_pos_l[1], arm_pos_l[2] - scale * 0.9)
        hand_pos_r = (arm_pos_r[0], arm_pos_r[1], arm_pos_r[2] - scale * 0.9)
        hand_l = self._create_composite_cube(
            f"{name}_Hand_L", hand_pos_l, hand_scale,
            (0.4, 0.35, 0.3)
        )
        hand_r = self._create_composite_cube(
            f"{name}_Hand_R", hand_pos_r, hand_scale,
            (0.4, 0.35, 0.3)
        )
        created_actors.append(hand_l["actor"])
        created_actors.append(hand_r["actor"])

        # Legs (short, thick)
        leg_scale = (scale * 0.5, scale * 0.5, scale * 1)
        leg_pos_l = (position[0] - scale * 0.4, position[1], position[2] - scale * 1.7)
        leg_pos_r = (position[0] + scale * 0.4, position[1], position[2] - scale * 1.7)
        leg_l = self._create_composite_cube(
            f"{name}_Leg_L", leg_pos_l, leg_scale,
            (0.4, 0.35, 0.3)
        )
        leg_r = self._create_composite_cube(
            f"{name}_Leg_R", leg_pos_r, leg_scale,
            (0.4, 0.35, 0.3)
        )
        created_actors.append(leg_l["actor"])
        created_actors.append(leg_r["actor"])

        unreal.log(f"🗿 Golem created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Golem)",
            "name": name,
            "type": "golem",
            "actors": created_actors
        }

    # ============================================================
    # CORELING CREATION (The Painted Man / Demon Cycle)
    # ============================================================

    def _create_wind_demon(self, parsed: dict) -> dict:
        """Create a Wind Demon - flying, bat-like with leather wings"""
        name = parsed.get("name") or "WindDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.5

        unreal.log("💨 Creating Wind Demon...")

        created_actors = []

        # Body (lean, humanoid)
        body_scale = (scale * 0.4, scale * 0.3, scale * 1.2)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.3, 0.25, 0.2)  # Dark brown/gray skin
        )
        created_actors.append(body["actor"])

        # Head (bestial, bat-like)
        head_scale = (scale * 0.25, scale * 0.3, scale * 0.3)
        head_pos = (position[0], position[1], position[2] + scale * 0.75)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (0.3, 0.25, 0.2)
        )
        created_actors.append(head["actor"])

        # Glowing eyes (red)
        eye_scale = (scale * 0.05, scale * 0.05, scale * 0.05)
        eye_pos_l = (head_pos[0] - scale * 0.08, head_pos[1], head_pos[2] + scale * 0.12)
        eye_pos_r = (head_pos[0] + scale * 0.08, head_pos[1], head_pos[2] + scale * 0.12)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (1, 0.2, 0))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (1, 0.2, 0))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Wings (large, leather-like)
        for side in [-1, 1]:
            wing_scale = (scale * 2.5, scale * 0.05, scale * 1.2)
            wing_pos = (position[0] + side * scale * 0.8, position[1], position[2] + scale * 0.3)
            wing = self._create_composite_cube(
                f"{name}_Wing_{'L' if side < 0 else 'R'}", wing_pos, wing_scale,
                (0.25, 0.2, 0.15)  # Dark leather
            )
            created_actors.append(wing["actor"])

        # Claws (on hands and feet)
        for side in [-1, 1]:
            claw_scale = (scale * 0.08, scale * 0.15, scale * 0.08)
            claw_pos_l = (position[0] + side * scale * 0.5, position[1] - scale * 0.2, position[2] + scale * 0.5)
            claw_pos_f = (position[0] + side * scale * 0.5, position[1] - scale * 0.2, position[2])
            claw_l = self._create_composite_cube(f"{name}_Claw_Hand_{'L' if side < 0 else 'R'}", claw_pos_l, claw_scale, (0.2, 0.15, 0.1))
            claw_f = self._create_composite_cube(f"{name}_Claw_Foot_{'L' if side < 0 else 'R'}", claw_pos_f, claw_scale, (0.2, 0.15, 0.1))
            created_actors.append(claw_l["actor"])
            created_actors.append(claw_f["actor"])

        # Tail (long, thin)
        tail_scale = (scale * 0.08, scale * 0.4, scale * 0.08)
        tail_pos = (position[0], position[1] - scale * 0.3, position[2] - scale * 0.3)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, (0.3, 0.25, 0.2))
        created_actors.append(tail["actor"])

        unreal.log(f"💨 Wind Demon created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Wind Demon)",
            "name": name,
            "type": "wind demon",
            "actors": created_actors
        }

    def _create_fire_demon(self, parsed: dict) -> dict:
        """Create a Fire Demon - humanoid, engulfed in flames"""
        name = parsed.get("name") or "FireDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("🔥 Creating Fire Demon...")

        created_actors = []

        # Body (charred, dark skin)
        body_scale = (scale * 0.6, scale * 0.4, scale * 1.5)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.15, 0.1, 0.08)  # Charred black/brown
        )
        created_actors.append(body["actor"])

        # Head
        head_scale = (scale * 0.3, scale * 0.3, scale * 0.35)
        head_pos = (position[0], position[1], position[2] + scale * 0.95)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (0.15, 0.1, 0.08)
        )
        created_actors.append(head["actor"])

        # Glowing eyes (intense orange)
        eye_scale = (scale * 0.08, scale * 0.05, scale * 0.08)
        eye_pos_l = (head_pos[0] - scale * 0.1, head_pos[1], head_pos[2] + scale * 0.15)
        eye_pos_r = (head_pos[0] + scale * 0.1, head_pos[1], head_pos[2] + scale * 0.15)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (1, 0.5, 0))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (1, 0.5, 0))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Arms
        arm_scale = (scale * 0.2, scale * 0.2, scale * 0.8)
        arm_pos_l = (position[0] - scale * 0.5, position[1], position[2] + scale * 0.5)
        arm_pos_r = (position[0] + scale * 0.5, position[1], position[2] + scale * 0.5)
        arm_l = self._create_composite_cube(f"{name}_Arm_L", arm_pos_l, arm_scale, (0.15, 0.1, 0.08))
        arm_r = self._create_composite_cube(f"{name}_Arm_R", arm_pos_r, arm_scale, (0.15, 0.1, 0.08))
        created_actors.append(arm_l["actor"])
        created_actors.append(arm_r["actor"])

        # Flames surrounding the body (multiple layers)
        for i in range(12):
            flame_scale = (scale * 0.15, scale * 0.15, scale * 0.3)
            angle = (2 * math.pi * i) / 12
            flame_pos = (
                position[0] + scale * 0.6 * math.cos(angle),
                position[1] + scale * 0.6 * math.sin(angle),
                position[2] + scale * 0.5 + (i % 3) * scale * 0.3
            )
            flame = self._create_composite_cube(
                f"{name}_Flame_{i}", flame_pos, flame_scale,
                (1, 0.3 - (i % 3) * 0.05, 0)  # Orange to yellow gradient
            )
            created_actors.append(flame["actor"])

        # Core glow (chest)
        core_scale = (scale * 0.2, scale * 0.1, scale * 0.2)
        core_pos = (position[0], position[1] + scale * 0.25, position[2] + scale * 0.5)
        core = self._create_composite_cube(f"{name}_Core", core_pos, core_scale, (1, 0.8, 0))
        created_actors.append(core["actor"])

        unreal.log(f"🔥 Fire Demon created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Fire Demon)",
            "name": name,
            "type": "fire demon",
            "actors": created_actors
        }

    def _create_water_demon(self, parsed: dict) -> dict:
        """Create a Water Demon - aquatic with tentacles"""
        name = parsed.get("name") or "WaterDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.5

        unreal.log("🌊 Creating Water Demon...")

        created_actors = []

        # Body (streamlined, aquatic)
        body_scale = (scale * 0.8, scale * 0.6, scale * 1.5)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.1, 0.3, 0.4)  # Blue-green aquatic color
        )
        created_actors.append(body["actor"])

        # Head (fish-like)
        head_scale = (scale * 0.4, scale * 0.35, scale * 0.4)
        head_pos = (position[0], position[1], position[2] + scale * 0.95)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (0.1, 0.3, 0.4)
        )
        created_actors.append(head["actor"])

        # Bioluminescent eyes
        eye_scale = (scale * 0.1, scale * 0.08, scale * 0.1)
        eye_pos_l = (head_pos[0] - scale * 0.15, head_pos[1], head_pos[2] + scale * 0.15)
        eye_pos_r = (head_pos[0] + scale * 0.15, head_pos[1], head_pos[2] + scale * 0.15)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (0.5, 1, 0.8))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (0.5, 1, 0.8))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Tentacles (8 tentacles)
        for i in range(8):
            angle = (2 * math.pi * i) / 8
            for j in range(3):  # 3 segments per tentacle
                tentacle_scale = (scale * 0.08, scale * 0.15, scale * 0.08)
                tentacle_pos = (
                    position[0] + (scale * 0.5 + j * scale * 0.2) * math.cos(angle),
                    position[1] + (scale * 0.5 + j * scale * 0.2) * math.sin(angle),
                    position[2] - scale * 0.5 - j * scale * 0.2
                )
                tentacle = self._create_composite_cube(
                    f"{name}_Tentacle_{i}_{j}", tentacle_pos, tentacle_scale,
                    (0.1, 0.3, 0.4)
                )
                created_actors.append(tentacle["actor"])

        # Tail (aquatic)
        tail_scale = (scale * 0.3, scale * 0.8, scale * 0.2)
        tail_pos = (position[0], position[1] - scale * 0.5, position[2] - scale * 0.8)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, (0.1, 0.3, 0.4))
        created_actors.append(tail["actor"])

        # Scales (decorative)
        for i in range(6):
            scale_scale = (scale * 0.1, scale * 0.02, scale * 0.1)
            scale_pos = (
                body_pos[0] + ((i % 2) - 0.5) * scale * 0.4,
                body_pos[1] + scale * 0.31,
                body_pos[2] + (i // 2) * scale * 0.3
            )
            sc = self._create_composite_cube(
                f"{name}_Scale_{i}", scale_pos, scale_scale,
                (0.15, 0.35, 0.45)  # Lighter scale color
            )
            created_actors.append(sc["actor"])

        unreal.log(f"🌊 Water Demon created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Water Demon)",
            "name": name,
            "type": "water demon",
            "actors": created_actors
        }

    def _create_rock_demon(self, parsed: dict) -> dict:
        """Create a Rock Demon - heavily armored, stone-like"""
        name = parsed.get("name") or "RockDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 3.0

        unreal.log("🪨 Creating Rock Demon...")

        created_actors = []

        # Body (massive, bulky)
        body_scale = (scale * 1.2, scale * 1, scale * 2)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.3, 0.28, 0.25)  # Gray-brown stone
        )
        created_actors.append(body["actor"])

        # Stone armor plates
        for i in range(8):
            plate_scale = (scale * 0.4, scale * 0.15, scale * 0.5)
            angle = (2 * math.pi * i) / 8
            plate_pos = (
                position[0] + scale * 0.65 * math.cos(angle),
                position[1] + scale * 0.65 * math.sin(angle),
                position[2] + scale * 0.5 + (i % 2) * scale * 0.5
            )
            plate = self._create_composite_cube(
                f"{name}_Armor_{i}", plate_pos, plate_scale,
                (0.35, 0.32, 0.3)  # Lighter stone armor
            )
            created_actors.append(plate["actor"])

        # Head (helmet-like)
        head_scale = (scale * 0.7, scale * 0.7, scale * 0.7)
        head_pos = (position[0], position[1], position[2] + scale * 1.4)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (0.3, 0.28, 0.25)
        )
        created_actors.append(head["actor"])

        # Glowing eyes from within armor
        eye_scale = (scale * 0.12, scale * 0.1, scale * 0.12)
        eye_pos_l = (head_pos[0] - scale * 0.2, head_pos[1] - scale * 0.3, head_pos[2] + scale * 0.2)
        eye_pos_r = (head_pos[0] + scale * 0.2, head_pos[1] - scale * 0.3, head_pos[2] + scale * 0.2)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (0.8, 0.2, 0.1))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (0.8, 0.2, 0.1))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Massive arms
        arm_scale = (scale * 0.5, scale * 0.5, scale * 1.2)
        arm_pos_l = (position[0] - scale * 0.9, position[1], position[2] + scale * 0.3)
        arm_pos_r = (position[0] + scale * 0.9, position[1], position[2] + scale * 0.3)
        arm_l = self._create_composite_cube(f"{name}_Arm_L", arm_pos_l, arm_scale, (0.3, 0.28, 0.25))
        arm_r = self._create_composite_cube(f"{name}_Arm_R", arm_pos_r, arm_scale, (0.3, 0.28, 0.25))
        created_actors.append(arm_l["actor"])
        created_actors.append(arm_r["actor"])

        # Spikes on armor
        for i in range(4):
            spike_scale = (scale * 0.1, scale * 0.3, scale * 0.1)
            spike_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.5,
                position[1] + scale * 0.55,
                position[2] + scale * 0.8 + (i // 2) * scale * 0.3
            )
            spike = self._create_composite_cube(
                f"{name}_Spike_{i}", spike_pos, spike_scale,
                (0.25, 0.23, 0.2)
            )
            created_actors.append(spike["actor"])

        # Legs (thick, pillar-like)
        leg_scale = (scale * 0.4, scale * 0.4, scale * 0.8)
        leg_pos_l = (position[0] - scale * 0.4, position[1], position[2] - scale * 1)
        leg_pos_r = (position[0] + scale * 0.4, position[1], position[2] - scale * 1)
        leg_l = self._create_composite_cube(f"{name}_Leg_L", leg_pos_l, leg_scale, (0.3, 0.28, 0.25))
        leg_r = self._create_composite_cube(f"{name}_Leg_R", leg_pos_r, leg_scale, (0.3, 0.28, 0.25))
        created_actors.append(leg_l["actor"])
        created_actors.append(leg_r["actor"])

        unreal.log(f"🪨 Rock Demon created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Rock Demon)",
            "name": name,
            "type": "rock demon",
            "actors": created_actors
        }

    def _create_wood_demon(self, parsed: dict) -> dict:
        """Create a Wood Demon - bark-like camouflage, vine features"""
        name = parsed.get("name") or "WoodDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("🌲 Creating Wood Demon...")

        created_actors = []

        # Body (bark-like texture)
        body_scale = (scale * 0.6, scale * 0.5, scale * 1.8)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.25, 0.2, 0.12)  # Dark brown bark
        )
        created_actors.append(body["actor"])

        # Head (twisted, root-like)
        head_scale = (scale * 0.35, scale * 0.35, scale * 0.4)
        head_pos = (position[0], position[1], position[2] + scale * 1.1)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (0.28, 0.22, 0.15)
        )
        created_actors.append(head["actor"])

        # Glowing green eyes
        eye_scale = (scale * 0.08, scale * 0.06, scale * 0.08)
        eye_pos_l = (head_pos[0] - scale * 0.12, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.15)
        eye_pos_r = (head_pos[0] + scale * 0.12, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.15)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (0.3, 0.8, 0.2))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (0.3, 0.8, 0.2))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Vine-like appendages (arms)
        for side in [-1, 1]:
            for i in range(3):  # 3 segments per vine arm
                vine_scale = (scale * 0.08, scale * 0.25, scale * 0.08)
                vine_pos = (
                    position[0] + side * (scale * 0.4 + i * scale * 0.15),
                    position[1],
                    position[2] + scale * 0.8 - i * scale * 0.2
                )
                vine = self._create_composite_cube(
                    f"{name}_VineArm_{'L' if side < 0 else 'R'}_{i}", vine_pos, vine_scale,
                    (0.3, 0.35, 0.15)  # Greenish-brown vines
                )
                created_actors.append(vine["actor"])

        # Root-like legs
        for i in range(4):
            root_scale = (scale * 0.15, scale * 0.15, scale * 0.6)
            angle = (2 * math.pi * i) / 4
            root_pos = (
                position[0] + scale * 0.3 * math.cos(angle),
                position[1] + scale * 0.3 * math.sin(angle),
                position[2] - scale * 0.7
            )
            root = self._create_composite_cube(
                f"{name}_Root_{i}", root_pos, root_scale,
                (0.25, 0.2, 0.12)
            )
            created_actors.append(root["actor"])

        # Leaves/camouflage
        for i in range(8):
            leaf_scale = (scale * 0.15, scale * 0.02, scale * 0.12)
            leaf_pos = (
                position[0] + (i % 3 - 1) * scale * 0.4,
                position[1] + ((i // 3) % 3 - 1) * scale * 0.4,
                position[2] + scale * 0.5 + (i % 2) * scale * 0.5
            )
            leaf = self._create_composite_cube(
                f"{name}_Leaf_{i}", leaf_pos, leaf_scale,
                (0.2, 0.6, 0.15)  # Green leaves
            )
            created_actors.append(leaf["actor"])

        # Bark plates (armor)
        for i in range(6):
            plate_scale = (scale * 0.25, scale * 0.08, scale * 0.35)
            plate_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.35,
                position[1] + scale * 0.27,
                position[2] + (i // 2) * scale * 0.4
            )
            plate = self._create_composite_cube(
                f"{name}_BarkPlate_{i}", plate_pos, plate_scale,
                (0.3, 0.25, 0.18)
            )
            created_actors.append(plate["actor"])

        unreal.log(f"🌲 Wood Demon created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Wood Demon)",
            "name": name,
            "type": "wood demon",
            "actors": created_actors
        }

    def _create_mind_demon(self, parsed: dict) -> dict:
        """Create a Mind Demon - small, intelligent, psychic glow"""
        name = parsed.get("name") or "MindDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.2

        unreal.log("🧠 Creating Mind Demon...")

        created_actors = []

        # Body (slender, humanoid but smaller)
        body_scale = (scale * 0.35, scale * 0.2, scale * 0.9)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.85, 0.82, 0.78)  # Pale, almost white skin
        )
        created_actors.append(body["actor"])

        # Head (large, elongated)
        head_scale = (scale * 0.25, scale * 0.25, scale * 0.3)
        head_pos = (position[0], position[1], position[2] + scale * 0.6)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (0.85, 0.82, 0.78)
        )
        created_actors.append(head["actor"])

        # Large, glowing purple eyes (psychic)
        eye_scale = (scale * 0.08, scale * 0.06, scale * 0.08)
        eye_pos_l = (head_pos[0] - scale * 0.08, head_pos[1] - scale * 0.12, head_pos[2] + scale * 0.1)
        eye_pos_r = (head_pos[0] + scale * 0.08, head_pos[1] - scale * 0.12, head_pos[2] + scale * 0.1)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (0.6, 0.2, 0.8))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (0.6, 0.2, 0.8))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Psychic aura (glowing rings around head)
        for i in range(3):
            aura_scale = (scale * (0.4 + i * 0.15), scale * 0.02, scale * (0.4 + i * 0.15))
            aura_pos = (position[0], position[1], position[2] + scale * 0.75 + i * scale * 0.05)
            aura = self._create_composite_cube(
                f"{name}_Aura_{i}", aura_pos, aura_scale,
                (0.7, 0.3, 0.9, 0.5)  # Purple glow, semi-transparent
            )
            created_actors.append(aura["actor"])

        # Robe/cloak
        robe_scale = (scale * 0.5, scale * 0.08, scale * 1)
        robe_pos = (position[0], position[1], position[2] + scale * 0.3)
        robe = self._create_composite_cube(
            f"{name}_Robe", robe_pos, robe_scale,
            (0.3, 0.25, 0.2)  # Dark robe
        )
        created_actors.append(robe["actor"])

        # Arms (slender)
        arm_scale = (scale * 0.08, scale * 0.08, scale * 0.5)
        arm_pos_l = (position[0] - scale * 0.25, position[1], position[2] + scale * 0.4)
        arm_pos_r = (position[0] + scale * 0.25, position[1], position[2] + scale * 0.4)
        arm_l = self._create_composite_cube(f"{name}_Arm_L", arm_pos_l, arm_scale, (0.85, 0.82, 0.78))
        arm_r = self._create_composite_cube(f"{name}_Arm_R", arm_pos_r, arm_scale, (0.85, 0.82, 0.78))
        created_actors.append(arm_l["actor"])
        created_actors.append(arm_r["actor"])

        # Psychic tendrils (floating)
        for i in range(6):
            tendril_scale = (scale * 0.03, scale * 0.2, scale * 0.03)
            angle = (2 * math.pi * i) / 6
            tendril_pos = (
                position[0] + scale * 0.5 * math.cos(angle),
                position[1] + scale * 0.5 * math.sin(angle),
                position[2] + scale * 0.5
            )
            tendril = self._create_composite_cube(
                f"{name}_Tendril_{i}", tendril_pos, tendril_scale,
                (0.8, 0.4, 1)  # Lavender psychic energy
            )
            created_actors.append(tendril["actor"])

        unreal.log(f"🧠 Mind Demon created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Mind Demon)",
            "name": name,
            "type": "mind demon",
            "actors": created_actors
        }

    def _create_hashak(self, parsed: dict) -> dict:
        """Create a Hashak - the most powerful, giant demon"""
        name = parsed.get("name") or "Hashak"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 5.0

        unreal.log("👹 Creating Hashak...")

        created_actors = []

        # Body (massive, terrifying)
        body_scale = (scale * 2, scale * 1.8, scale * 3.5)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.15, 0.12, 0.1)  # Dark, charred appearance
        )
        created_actors.append(body["actor"])

        # Thick armor plates
        for i in range(12):
            plate_scale = (scale * 0.8, scale * 0.2, scale * 1)
            angle = (2 * math.pi * i) / 12
            plate_pos = (
                position[0] + scale * 1.1 * math.cos(angle),
                position[1] + scale * 1.1 * math.sin(angle),
                position[2] + scale * 1 + (i % 3) * scale * 0.7
            )
            plate = self._create_composite_cube(
                f"{name}_Armor_{i}", plate_pos, plate_scale,
                (0.18, 0.15, 0.12)  # Dark armor
            )
            created_actors.append(plate["actor"])

        # Massive head
        head_scale = (scale * 1.2, scale * 1, scale * 1.2)
        head_pos = (position[0], position[1], position[2] + scale * 2.5)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (0.15, 0.12, 0.1)
        )
        created_actors.append(head["actor"])

        # Multiple glowing eyes (horrific)
        for row in range(3):
            for col in range(3):
                eye_scale = (scale * 0.15, scale * 0.1, scale * 0.15)
                eye_pos = (
                    head_pos[0] + (col - 1) * scale * 0.3,
                    head_pos[1] - scale * 0.55,
                    head_pos[2] + scale * 0.3 + row * scale * 0.25
                )
                eye = self._create_composite_cube(
                    f"{name}_Eye_{row}_{col}", eye_pos, eye_scale,
                    (1, 0.1, 0)  # Burning red
                )
                created_actors.append(eye["actor"])

        # Massive, spiked arms
        arm_scale = (scale * 0.8, scale * 0.8, scale * 2)
        arm_pos_l = (position[0] - scale * 1.5, position[1], position[2] + scale * 0.8)
        arm_pos_r = (position[0] + scale * 1.5, position[1], position[2] + scale * 0.8)
        arm_l = self._create_composite_cube(f"{name}_Arm_L", arm_pos_l, arm_scale, (0.15, 0.12, 0.1))
        arm_r = self._create_composite_cube(f"{name}_Arm_R", arm_pos_r, arm_scale, (0.15, 0.12, 0.1))
        created_actors.append(arm_l["actor"])
        created_actors.append(arm_r["actor"])

        # Hands (massive, clawed)
        hand_scale = (scale * 1, scale * 0.4, scale * 0.8)
        hand_pos_l = (arm_pos_l[0], arm_pos_l[1], arm_pos_l[2] - scale * 1.2)
        hand_pos_r = (arm_pos_r[0], arm_pos_r[1], arm_pos_r[2] - scale * 1.2)
        hand_l = self._create_composite_cube(f"{name}_Hand_L", hand_pos_l, hand_scale, (0.15, 0.12, 0.1))
        hand_r = self._create_composite_cube(f"{name}_Hand_R", hand_pos_r, hand_scale, (0.15, 0.12, 0.1))
        created_actors.append(hand_l["actor"])
        created_actors.append(hand_r["actor"])

        # Claws
        for i in range(5):
            claw_scale = (scale * 0.2, scale * 0.3, scale * 0.2)
            claw_pos_l = (hand_pos_l[0] + (i - 2) * scale * 0.2, hand_pos_l[1] - scale * 0.3, hand_pos_l[2])
            claw_pos_r = (hand_pos_r[0] + (i - 2) * scale * 0.2, hand_pos_r[1] - scale * 0.3, hand_pos_r[2])
            claw_l = self._create_composite_cube(f"{name}_Claw_L_{i}", claw_pos_l, claw_scale, (0.12, 0.1, 0.08))
            claw_r = self._create_composite_cube(f"{name}_Claw_R_{i}", claw_pos_r, claw_scale, (0.12, 0.1, 0.08))
            created_actors.append(claw_l["actor"])
            created_actors.append(claw_r["actor"])

        # Massive spikes
        for i in range(8):
            spike_scale = (scale * 0.15, scale * 0.8, scale * 0.15)
            angle = (2 * math.pi * i) / 8
            spike_pos = (
                position[0] + scale * 0.9 * math.cos(angle),
                position[1] + scale * 0.9 * math.sin(angle),
                position[2] + scale * 2
            )
            spike = self._create_composite_cube(
                f"{name}_Spike_{i}", spike_pos, spike_scale,
                (0.12, 0.1, 0.08)
            )
            created_actors.append(spike["actor"])

        # Pillar-like legs
        leg_scale = (scale * 0.8, scale * 0.8, scale * 1.5)
        leg_pos_l = (position[0] - scale * 0.7, position[1], position[2] - scale * 2)
        leg_pos_r = (position[0] + scale * 0.7, position[1], position[2] - scale * 2)
        leg_l = self._create_composite_cube(f"{name}_Leg_L", leg_pos_l, leg_scale, (0.15, 0.12, 0.1))
        leg_r = self._create_composite_cube(f"{name}_Leg_R", leg_pos_r, leg_scale, (0.15, 0.12, 0.1))
        created_actors.append(leg_l["actor"])
        created_actors.append(leg_r["actor"])

        unreal.log(f"👹 Hashak created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Hashak)",
            "name": name,
            "type": "hashak",
            "actors": created_actors
        }

    def _create_clay_demon(self, parsed: dict) -> dict:
        """Create a Clay Demon - earth elemental with mud form"""
        name = parsed.get("name") or "ClayDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("🏺 Creating Clay Demon...")

        created_actors = []

        # Body (amorphous, clay-like)
        body_scale = (scale * 0.8, scale * 0.7, scale * 1.5)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.45, 0.35, 0.25)  # Brown clay color
        )
        created_actors.append(body["actor"])

        # Head (molded clay)
        head_scale = (scale * 0.4, scale * 0.4, scale * 0.4)
        head_pos = (position[0], position[1], position[2] + scale * 1)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (0.45, 0.35, 0.25)
        )
        created_actors.append(head["actor"])

        # Earth-tone eyes
        eye_scale = (scale * 0.08, scale * 0.08, scale * 0.08)
        eye_pos_l = (head_pos[0] - scale * 0.12, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.15)
        eye_pos_r = (head_pos[0] + scale * 0.12, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.15)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (0.6, 0.4, 0.2))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (0.6, 0.4, 0.2))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Mud arms (shifting, malleable)
        for side in [-1, 1]:
            for i in range(4):  # 4 segments per arm
                arm_scale = (scale * 0.15 - i * scale * 0.02, scale * 0.2, scale * 0.15 - i * scale * 0.02)
                arm_pos = (
                    position[0] + side * (scale * 0.5 + i * scale * 0.15),
                    position[1],
                    position[2] + scale * 0.8 - i * scale * 0.15
                )
                arm = self._create_composite_cube(
                    f"{name}_Arm_{'L' if side < 0 else 'R'}_{i}", arm_pos, arm_scale,
                    (0.5, 0.4, 0.3)
                )
                created_actors.append(arm["actor"])

        # Earth elemental aura (dust and debris)
        for i in range(6):
            debris_scale = (scale * 0.1, scale * 0.1, scale * 0.1)
            angle = (2 * math.pi * i) / 6
            debris_pos = (
                position[0] + scale * 0.7 * math.cos(angle),
                position[1] + scale * 0.7 * math.sin(angle),
                position[2] + scale * 0.5
            )
            debris = self._create_composite_cube(
                f"{name}_Dust_{i}", debris_pos, debris_scale,
                (0.5, 0.42, 0.35)
            )
            created_actors.append(debris["actor"])

        # Cracked, drying mud texture on body
        for i in range(8):
            crack_scale = (scale * 0.02, scale * 0.2, scale * 0.02)
            crack_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.4,
                position[1] + scale * 0.36,
                position[2] + (i // 2) * scale * 0.4
            )
            crack = self._create_composite_cube(
                f"{name}_Crack_{i}", crack_pos, crack_scale,
                (0.35, 0.25, 0.15)  # Darker cracked areas
            )
            created_actors.append(crack["actor"])

        unreal.log(f"🏺 Clay Demon created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Clay Demon)",
            "name": name,
            "type": "clay demon",
            "actors": created_actors
        }

    def _create_sand_demon(self, parsed: dict) -> dict:
        """Create a Sand Demon - desert demon with shifting form"""
        name = parsed.get("name") or "SandDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.8

        unreal.log("🏜️ Creating Sand Demon...")

        created_actors = []

        # Body (shifting sand form)
        body_scale = (scale * 0.6, scale * 0.5, scale * 1.3)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.76, 0.7, 0.5)  # Sandy yellow-tan color
        )
        created_actors.append(body["actor"])

        # Head (sand-formed)
        head_scale = (scale * 0.35, scale * 0.35, scale * 0.35)
        head_pos = (position[0], position[1], position[2] + scale * 0.85)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (0.76, 0.7, 0.5)
        )
        created_actors.append(head["actor"])

        # Golden eyes (desert predator)
        eye_scale = (scale * 0.08, scale * 0.08, scale * 0.08)
        eye_pos_l = (head_pos[0] - scale * 0.1, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.12)
        eye_pos_r = (head_pos[0] + scale * 0.1, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.12)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (1, 0.84, 0))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (1, 0.84, 0))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Shifting sand arms (constantly changing form)
        for side in [-1, 1]:
            for i in range(3):  # 3 segments per arm
                arm_scale = (scale * 0.12, scale * 0.18, scale * 0.12)
                arm_pos = (
                    position[0] + side * (scale * 0.45 + i * scale * 0.12),
                    position[1],
                    position[2] + scale * 0.7 - i * scale * 0.12
                )
                arm = self._create_composite_cube(
                    f"{name}_Arm_{'L' if side < 0 else 'R'}_{i}", arm_pos, arm_scale,
                    (0.8, 0.72, 0.52)
                )
                created_actors.append(arm["actor"])

        # Sand cloud aura (dust swirling)
        for i in range(10):
            dust_scale = (scale * 0.08, scale * 0.08, scale * 0.08)
            angle = (2 * math.pi * i) / 10
            dust_pos = (
                position[0] + scale * 0.6 * math.cos(angle),
                position[1] + scale * 0.6 * math.sin(angle),
                position[2] + scale * 0.4 + (i % 3) * scale * 0.2
            )
            dust = self._create_composite_cube(
                f"{name}_Dust_{i}", dust_pos, dust_scale,
                (0.85, 0.78, 0.6)  # Lighter sand dust
            )
            created_actors.append(dust["actor"])

        # Desert camouflage markings
        for i in range(5):
            stripe_scale = (scale * 0.15, scale * 0.03, scale * 0.2)
            stripe_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.35,
                position[1] + scale * 0.27,
                position[2] + (i // 2) * scale * 0.35
            )
            stripe = self._create_composite_cube(
                f"{name}_Camouflage_{i}", stripe_pos, stripe_scale,
                (0.7, 0.65, 0.45)  # Darker sand stripes
            )
            created_actors.append(stripe["actor"])

        unreal.log(f"🏜️ Sand Demon created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Sand Demon)",
            "name": name,
            "type": "sand demon",
            "actors": created_actors
        }

    def _create_ice_demon(self, parsed: dict) -> dict:
        """Create an Ice Demon - frozen demon with frost aura"""
        name = parsed.get("name") or "IceDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.2

        unreal.log("❄️ Creating Ice Demon...")

        created_actors = []

        # Body (crystalline ice)
        body_scale = (scale * 0.6, scale * 0.5, scale * 1.4)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.85, 0.92, 1)  # Icy blue-white
        )
        created_actors.append(body["actor"])

        # Head (ice crystal)
        head_scale = (scale * 0.35, scale * 0.35, scale * 0.4)
        head_pos = (position[0], position[1], position[2] + scale * 0.95)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (0.88, 0.94, 1)
        )
        created_actors.append(head["actor"])

        # Glowing blue eyes
        eye_scale = (scale * 0.08, scale * 0.08, scale * 0.08)
        eye_pos_l = (head_pos[0] - scale * 0.1, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.15)
        eye_pos_r = (head_pos[0] + scale * 0.1, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.15)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (0.4, 0.7, 1))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (0.4, 0.7, 1))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Ice spike armor covering body
        for i in range(12):
            spike_scale = (scale * 0.08, scale * 0.25, scale * 0.08)
            angle = (2 * math.pi * i) / 12
            spike_pos = (
                position[0] + scale * 0.5 * math.cos(angle),
                position[1] + scale * 0.5 * math.sin(angle),
                position[2] + scale * 0.5 + (i % 3) * scale * 0.3
            )
            spike = self._create_composite_cube(
                f"{name}_IceSpike_{i}", spike_pos, spike_scale,
                (0.9, 0.96, 1)  # Sharp ice spikes
            )
            created_actors.append(spike["actor"])

        # Frosty arms (icicle-like fingers)
        for side in [-1, 1]:
            for i in range(3):  # 3 segments per arm
                arm_scale = (scale * 0.1, scale * 0.22, scale * 0.1)
                arm_pos = (
                    position[0] + side * (scale * 0.4 + i * scale * 0.12),
                    position[1],
                    position[2] + scale * 0.75 - i * scale * 0.15
                )
                arm = self._create_composite_cube(
                    f"{name}_Arm_{'L' if side < 0 else 'R'}_{i}", arm_pos, arm_scale,
                    (0.85, 0.92, 1)
                )
                created_actors.append(arm["actor"])

        # Frost aura (cold mist)
        for i in range(8):
            frost_scale = (scale * 0.15, scale * 0.02, scale * 0.15)
            angle = (2 * math.pi * i) / 8
            frost_pos = (
                position[0] + scale * 0.7 * math.cos(angle),
                position[1] + scale * 0.7 * math.sin(angle),
                position[2] + scale * 0.5 + (i % 2) * scale * 0.1
            )
            frost = self._create_composite_cube(
                f"{name}_Frost_{i}", frost_pos, frost_scale,
                (0.92, 0.96, 1, 0.5)  # Semi-transparent frost
            )
            created_actors.append(frost["actor"])

        # Ice crystals floating around
        for i in range(6):
            crystal_scale = (scale * 0.06, scale * 0.12, scale * 0.06)
            angle = (2 * math.pi * i) / 6
            crystal_pos = (
                position[0] + scale * 0.6 * math.cos(angle),
                position[1] + scale * 0.6 * math.sin(angle),
                position[2] + scale * 0.3
            )
            crystal = self._create_composite_cube(
                f"{name}_Crystal_{i}", crystal_pos, crystal_scale,
                (0.95, 0.98, 1)
            )
            created_actors.append(crystal["actor"])

        unreal.log(f"❄️ Ice Demon created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Ice Demon)",
            "name": name,
            "type": "ice demon",
            "actors": created_actors
        }

    def _create_forest_demon(self, parsed: dict) -> dict:
        """Create a Forest Demon - distinct from Wood Demon, more primal"""
        name = parsed.get("name") or "ForestDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.5

        unreal.log("🌲 Creating Forest Demon...")

        created_actors = []

        # Body (ancient forest energy)
        body_scale = (scale * 0.7, scale * 0.6, scale * 1.6)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.15, 0.25, 0.12)  # Deep forest green
        )
        created_actors.append(body["actor"])

        # Head (antler-like features)
        head_scale = (scale * 0.4, scale * 0.4, scale * 0.45)
        head_pos = (position[0], position[1], position[2] + scale * 1.05)
        head = self._create_composite_cube(
            f"{name}_Head", head_pos, head_scale,
            (0.18, 0.28, 0.15)
        )
        created_actors.append(head["actor"])

        # Antlers (branch-like)
        for side in [-1, 1]:
            for i in range(3):  # 3 antler branches per side
                antler_scale = (scale * 0.06, scale * 0.25, scale * 0.06)
                antler_pos = (
                    head_pos[0] + side * scale * 0.15 + (i - 1) * scale * 0.08,
                    head_pos[1],
                    head_pos[2] + scale * 0.3 + i * scale * 0.1
                )
                antler = self._create_composite_cube(
                    f"{name}_Antler_{'L' if side < 0 else 'R'}_{i}", antler_pos, antler_scale,
                    (0.2, 0.3, 0.18)
                )
                created_actors.append(antler["actor"])

        # Emerald green eyes
        eye_scale = (scale * 0.1, scale * 0.08, scale * 0.1)
        eye_pos_l = (head_pos[0] - scale * 0.12, head_pos[1] - scale * 0.2, head_pos[2] + scale * 0.18)
        eye_pos_r = (head_pos[0] + scale * 0.12, head_pos[1] - scale * 0.2, head_pos[2] + scale * 0.18)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (0.2, 0.8, 0.4))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (0.2, 0.8, 0.4))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Branch-like arms
        for side in [-1, 1]:
            for i in range(4):  # 4 segments per branch arm
                branch_scale = (scale * 0.08, scale * 0.2, scale * 0.08)
                branch_pos = (
                    position[0] + side * (scale * 0.45 + i * scale * 0.1),
                    position[1],
                    position[2] + scale * 0.8 - i * scale * 0.12
                )
                branch = self._create_composite_cube(
                    f"{name}_BranchArm_{'L' if side < 0 else 'R'}_{i}", branch_pos, branch_scale,
                    (0.18, 0.3, 0.16)
                )
                created_actors.append(branch["actor"])

        # Root legs (spreading into ground)
        for i in range(6):
            root_scale = (scale * 0.12, scale * 0.12, scale * 0.5)
            angle = (2 * math.pi * i) / 6
            root_pos = (
                position[0] + scale * 0.35 * math.cos(angle),
                position[1] + scale * 0.35 * math.sin(angle),
                position[2] - scale * 0.6
            )
            root = self._create_composite_cube(
                f"{name}_Root_{i}", root_pos, root_scale,
                (0.15, 0.25, 0.12)
            )
            created_actors.append(root["actor"])

        # Moss covering
        for i in range(10):
            moss_scale = (scale * 0.12, scale * 0.04, scale * 0.12)
            moss_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.3,
                position[1] + scale * 0.32,
                position[2] + (i // 3) * scale * 0.4
            )
            moss = self._create_composite_cube(
                f"{name}_Moss_{i}", moss_pos, moss_scale,
                (0.25, 0.4, 0.2)  # Vibrant green moss
            )
            created_actors.append(moss["actor"])

        # Leaves and ferns growing on body
        for i in range(8):
            leaf_scale = (scale * 0.1, scale * 0.02, scale * 0.08)
            leaf_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.4,
                position[1] + ((i // 2) % 2 - 0.5) * scale * 0.45,
                position[2] + scale * 0.6 + (i // 4) * scale * 0.3
            )
            leaf = self._create_composite_cube(
                f"{name}_Leaf_{i}", leaf_pos, leaf_scale,
                (0.2, 0.6, 0.25)  # Bright green leaves
            )
            created_actors.append(leaf["actor"])

        unreal.log(f"🌲 Forest Demon created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Forest Demon)",
            "name": name,
            "type": "forest demon",
            "actors": created_actors
        }

    def _create_coreling_generic(self, parsed: dict) -> dict:
        """Create a generic Coreling"""
        name = parsed.get("name") or "Coreling"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.5

        unreal.log("👿 Creating Coreling...")

        created_actors = []

        # Body
        body_scale = (scale * 0.5, scale * 0.4, scale * 1)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            (0.2, 0.15, 0.12)  # Dark demon skin
        )
        created_actors.append(body["actor"])

        # Head
        head_scale = (scale * 0.3, scale * 0.3, scale * 0.3)
        head_pos = (position[0], position[1], position[2] + scale * 0.65)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, (0.2, 0.15, 0.12))
        created_actors.append(head["actor"])

        # Glowing eyes
        eye_scale = (scale * 0.06, scale * 0.06, scale * 0.06)
        eye_pos_l = (head_pos[0] - scale * 0.1, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.1)
        eye_pos_r = (head_pos[0] + scale * 0.1, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.1)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (1, 0.2, 0))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (1, 0.2, 0))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Magic aura
        for i in range(4):
            aura_scale = (scale * 0.4, scale * 0.02, scale * 0.4)
            aura_pos = (position[0], position[1], position[2] + scale * 0.5 + i * scale * 0.15)
            aura = self._create_composite_cube(
                f"{name}_Aura_{i}", aura_pos, aura_scale,
                (0.8, 0.2, 0)  # Red magic glow
            )
            created_actors.append(aura["actor"])

        unreal.log(f"👿 Coreling created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Coreling)",
            "name": name,
            "type": "coreling",
            "actors": created_actors
        }

    def _create_furniture(self, parsed: dict) -> dict:
        """Create furniture"""
        name = parsed.get("name") or "Furniture"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.0

        unreal.log("🛋️ Creating furniture...")

        created_actors = []

        # Seat
        seat_scale = (scale * 1.2, scale * 0.4, scale * 0.3)
        seat_pos = (position[0], position[1], position[2] + scale * 0.3)
        seat = self._create_composite_cube(
            f"{name}_Seat", seat_pos, seat_scale,
            props.get("color", (0.6, 0.4, 0.2))  # Wood/fabric
        )
        created_actors.append(seat["actor"])

        # Back
        back_scale = (scale * 1.2, scale * 0.4, scale * 0.3)
        back_pos = (position[0], position[1] - scale * 0.35, position[2] + scale * 0.6)
        back = self._create_composite_cube(
            f"{name}_Back", back_pos, back_scale,
            props.get("color", (0.6, 0.4, 0.2))
        )
        created_actors.append(back["actor"])

        # Legs (4 legs)
        leg_scale = (scale * 0.1, scale * 0.1, scale * 0.3)
        leg_positions = [
            (position[0] - scale * 0.5, position[1] - scale * 0.5, position[2]),
            (position[0] + scale * 0.5, position[1] - scale * 0.5, position[2]),
            (position[0] - scale * 0.5, position[1] + scale * 0.5, position[2]),
            (position[0] + scale * 0.5, position[1] + scale * 0.5, position[2])
        ]

        for i, leg_pos in enumerate(leg_positions):
            leg = self._create_composite_cube(
                f"{name}_Leg_{i}", leg_pos, leg_scale,
                (0.4, 0.3, 0.2)  # Dark wood
            )
            created_actors.append(leg["actor"])

        unreal.log(f"🛋️ Furniture created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Furniture)",
            "name": name,
            "type": "furniture",
            "actors": created_actors
        }

    def _create_generic(self, parsed: dict) -> dict:
        """Create generic object"""
        unreal.log(f"Creating: {parsed['type']}")

        # Default to cube
        name = parsed.get("name") or parsed["type"].title()
        position = parsed["properties"]["position"]

        cube = self._create_cube(name, position, parsed["properties"]["color"])

        return {
            "message": f"Created {name}",
            "name": name,
            "actors": [cube["actor"]] if "actor" in cube else []
        }

    # ============================================================
    # VEHICLE CREATION
    # ============================================================

    def _create_car(self, parsed: dict) -> dict:
        """Create a car"""
        name = parsed.get("name") or "Car"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.0

        unreal.log("🚗 Creating car...")

        created_actors = []

        # Body
        body_scale = (scale * 2, scale * 1, scale * 4)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            props.get("color", (0.2, 0.4, 0.8))
        )
        created_actors.append(body["actor"])

        # Cabin
        cabin_scale = (scale * 1.5, scale * 1.2, scale * 1)
        cabin_pos = (position[0], position[1] + scale * 0.4, position[2] + scale * 1)
        cabin = self._create_composite_cube(
            f"{name}_Cabin", cabin_pos, cabin_scale,
            (0.3, 0.5, 0.7)  # Glass
        )
        created_actors.append(cabin["actor"])

        # Wheels (4 wheels)
        wheel_scale = (scale * 0.6, scale * 0.6, scale * 0.6)
        wheel_positions = [
            (position[0] + scale * 1.2, position[1] - scale * 0.8, position[2]),
            (position[0] + scale * 1.2, position[1] + scale * 0.8, position[2]),
            (position[0] - scale * 1.2, position[1] - scale * 0.8, position[2]),
            (position[0] - scale * 1.2, position[1] + scale * 0.8, position[2])
        ]

        for i, wheel_pos in enumerate(wheel_positions):
            wheel = self._create_composite_cube(
                f"{name}_Wheel_{i}", wheel_pos, wheel_scale,
                (0.1, 0.1, 0.1)  # Black rubber
            )
            created_actors.append(wheel["actor"])

        # Headlights
        for side in [-1, 1]:
            light_scale = (scale * 0.2, scale * 0.1, scale * 0.1)
            light_pos = (position[0] + side * scale * 0.6, position[1] - scale * 0.5, position[2] + scale * 0.3)
            light = self._create_composite_cube(
                f"{name}_Headlight_{'L' if side < 0 else 'R'}", light_pos, light_scale,
                (1, 1, 0.8)  # Bright white-yellow
            )
            created_actors.append(light["actor"])

        unreal.log(f"🚗 Car created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Car)",
            "name": name,
            "type": "car",
            "actors": created_actors
        }

    def _create_motorcycle(self, parsed: dict) -> dict:
        """Create a motorcycle"""
        name = parsed.get("name") or "Motorcycle"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 0.8

        unreal.log("🏍️ Creating motorcycle...")

        created_actors = []

        # Body/frame
        body_scale = (scale * 0.3, scale * 0.4, scale * 1.5)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            props.get("color", (0.8, 0.1, 0.1))  # Red
        )
        created_actors.append(body["actor"])

        # Seat
        seat_scale = (scale * 0.25, scale * 0.3, scale * 0.4)
        seat_pos = (position[0], position[1], position[2] + scale * 0.3)
        seat = self._create_composite_cube(
            f"{name}_Seat", seat_pos, seat_scale,
            (0.2, 0.2, 0.2)  # Black seat
        )
        created_actors.append(seat["actor"])

        # Handlebars
        handlebar_scale = (scale * 0.03, scale * 0.6, scale * 0.03)
        handlebar_pos = (position[0], position[1], position[2] + scale * 0.8)
        handlebar = self._create_composite_cube(
            f"{name}_Handlebar", handlebar_pos, handlebar_scale,
            (0.7, 0.7, 0.7)  # Chrome
        )
        created_actors.append(handlebar["actor"])

        # Wheels (2 wheels)
        wheel_scale = (scale * 0.5, scale * 0.5, scale * 0.5)
        wheel_pos_front = (position[0], position[1], position[2] + scale * 0.8)
        wheel_pos_back = (position[0], position[1], position[2] - scale * 0.8)
        wheel_front = self._create_composite_cube(
            f"{name}_Wheel_Front", wheel_pos_front, wheel_scale,
            (0.1, 0.1, 0.1)
        )
        wheel_back = self._create_composite_cube(
            f"{name}_Wheel_Back", wheel_pos_back, wheel_scale,
            (0.1, 0.1, 0.1)
        )
        created_actors.append(wheel_front["actor"])
        created_actors.append(wheel_back["actor"])

        # Engine
        engine_scale = (scale * 0.3, scale * 0.25, scale * 0.4)
        engine_pos = (position[0], position[1] - scale * 0.3, position[2])
        engine = self._create_composite_cube(
            f"{name}_Engine", engine_pos, engine_scale,
            (0.5, 0.5, 0.5)  # Metallic
        )
        created_actors.append(engine["actor"])

        unreal.log(f"🏍️ Motorcycle created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Motorcycle)",
            "name": name,
            "type": "motorcycle",
            "actors": created_actors
        }

    def _create_boat(self, parsed: dict) -> dict:
        """Create a boat"""
        name = parsed.get("name") or "Boat"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("⛵ Creating boat...")

        created_actors = []

        # Hull
        hull_scale = (scale * 1.5, scale * 0.6, scale * 5)
        hull_pos = position
        hull = self._create_composite_cube(
            f"{name}_Hull", hull_pos, hull_scale,
            props.get("color", (0.9, 0.9, 0.9))  # White hull
        )
        created_actors.append(hull["actor"])

        # Cabin
        cabin_scale = (scale * 1, scale * 0.8, scale * 1.5)
        cabin_pos = (position[0], position[1] + scale * 0.4, position[2] + scale * 0.5)
        cabin = self._create_composite_cube(
            f"{name}_Cabin", cabin_pos, cabin_scale,
            (0.85, 0.85, 0.85)
        )
        created_actors.append(cabin["actor"])

        # Windshield
        windshield_scale = (scale * 0.8, scale * 0.05, scale * 0.6)
        windshield_pos = (position[0], position[1] + scale * 0.7, position[2] + scale * 0.7)
        windshield = self._create_composite_cube(
            f"{name}_Windshield", windshield_pos, windshield_scale,
            (0.3, 0.5, 0.7)  # Glass
        )
        created_actors.append(windshield["actor"])

        # Propeller
        propeller_scale = (scale * 0.3, scale * 0.05, scale * 0.3)
        propeller_pos = (position[0], position[1] - scale * 0.5, position[2] - scale * 2.3)
        propeller = self._create_composite_cube(
            f"{name}_Propeller", propeller_pos, propeller_scale,
            (0.7, 0.7, 0.7)  # Metal
        )
        created_actors.append(propeller["actor"])

        unreal.log(f"⛵ Boat created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Boat)",
            "name": name,
            "type": "boat",
            "actors": created_actors
        }

    def _create_airplane(self, parsed: dict) -> dict:
        """Create an airplane"""
        name = parsed.get("name") or "Airplane"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 5.0

        unreal.log("✈️ Creating airplane...")

        created_actors = []

        # Fuselage
        fuselage_scale = (scale * 0.8, scale * 0.8, scale * 6)
        fuselage_pos = position
        fuselage = self._create_composite_cube(
            f"{name}_Fuselage", fuselage_pos, fuselage_scale,
            props.get("color", (0.9, 0.9, 0.9))  # White
        )
        created_actors.append(fuselage["actor"])

        # Wings (main wings)
        for side in [-1, 1]:
            wing_scale = (scale * 4, scale * 0.1, scale * 1)
            wing_pos = (position[0] + side * scale * 2.5, position[1], position[2] + scale * 0.3)
            wing = self._create_composite_cube(
                f"{name}_Wing_{'L' if side < 0 else 'R'}", wing_pos, wing_scale,
                props.get("color", (0.9, 0.9, 0.9))
            )
            created_actors.append(wing["actor"])

        # Tail (horizontal stabilizer)
        tail_h_scale = (scale * 1.5, scale * 0.05, scale * 0.5)
        tail_h_pos = (position[0], position[1], position[2] - scale * 2.5)
        tail_h = self._create_composite_cube(
            f"{name}_Tail_Horizontal", tail_h_pos, tail_h_scale,
            props.get("color", (0.9, 0.9, 0.9))
        )
        created_actors.append(tail_h["actor"])

        # Tail (vertical stabilizer)
        tail_v_scale = (scale * 0.05, scale * 0.8, scale * 0.8)
        tail_v_pos = (position[0], position[1], position[2] - scale * 2.5)
        tail_v = self._create_composite_cube(
            f"{name}_Tail_Vertical", tail_v_pos, tail_v_scale,
            props.get("color", (0.9, 0.9, 0.9))
        )
        created_actors.append(tail_v["actor"])

        # Engines (2 engines under wings)
        for side in [-1, 1]:
            engine_scale = (scale * 0.4, scale * 0.4, scale * 1)
            engine_pos = (position[0] + side * scale * 1.8, position[1] - scale * 0.4, position[2] + scale * 0.2)
            engine = self._create_composite_cube(
                f"{name}_Engine_{'L' if side < 0 else 'R'}", engine_pos, engine_scale,
                (0.5, 0.5, 0.5)  # Dark engine
            )
            created_actors.append(engine["actor"])

        # Cockpit windows
        cockpit_scale = (scale * 0.6, scale * 0.05, scale * 0.5)
        cockpit_pos = (position[0], position[1] + scale * 0.38, position[2] + scale * 2)
        cockpit = self._create_composite_cube(
            f"{name}_Cockpit", cockpit_pos, cockpit_scale,
            (0.2, 0.4, 0.6)  # Dark glass
        )
        created_actors.append(cockpit["actor"])

        unreal.log(f"✈️ Airplane created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Airplane)",
            "name": name,
            "type": "airplane",
            "actors": created_actors
        }

    def _create_helicopter(self, parsed: dict) -> dict:
        """Create a helicopter"""
        name = parsed.get("name") or "Helicopter"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("🚁 Creating helicopter...")

        created_actors = []

        # Body/fuselage
        body_scale = (scale * 1, scale * 1, scale * 3)
        body_pos = position
        body = self._create_composite_cube(
            f"{name}_Body", body_pos, body_scale,
            props.get("color", (0.3, 0.5, 0.7))  # Blue
        )
        created_actors.append(body["actor"])

        # Cockpit
        cockpit_scale = (scale * 0.8, scale * 0.05, scale * 0.8)
        cockpit_pos = (position[0], position[1] + scale * 0.5, position[2] + scale * 0.8)
        cockpit = self._create_composite_cube(
            f"{name}_Cockpit", cockpit_pos, cockpit_scale,
            (0.2, 0.4, 0.6)  # Glass
        )
        created_actors.append(cockpit["actor"])

        # Main rotor
        rotor_scale = (scale * 6, scale * 0.05, scale * 0.3)
        rotor_pos = (position[0], position[1], position[2] + scale * 1.5)
        rotor = self._create_composite_cube(
            f"{name}_Rotor_Main", rotor_pos, rotor_scale,
            (0.3, 0.3, 0.3)  # Dark rotor
        )
        created_actors.append(rotor["actor"])

        # Tail boom
        tail_boom_scale = (scale * 0.3, scale * 0.3, scale * 2)
        tail_boom_pos = (position[0], position[1], position[2] - scale * 2)
        tail_boom = self._create_composite_cube(
            f"{name}_TailBoom", tail_boom_pos, tail_boom_scale,
            props.get("color", (0.3, 0.5, 0.7))
        )
        created_actors.append(tail_boom["actor"])

        # Tail rotor
        tail_rotor_scale = (scale * 0.05, scale * 1.2, scale * 0.2)
        tail_rotor_pos = (position[0], position[1], position[2] - scale * 2.8)
        tail_rotor = self._create_composite_cube(
            f"{name}_Rotor_Tail", tail_rotor_pos, tail_rotor_scale,
            (0.3, 0.3, 0.3)
        )
        created_actors.append(tail_rotor["actor"])

        # Landing skids
        for side in [-1, 1]:
            skid_scale = (scale * 0.05, scale * 2, scale * 0.05)
            skid_pos = (position[0] + side * scale * 0.5, position[1], position[2] - scale * 0.8)
            skid = self._create_composite_cube(
                f"{name}_Skid_{'L' if side < 0 else 'R'}", skid_pos, skid_scale,
                (0.2, 0.2, 0.2)  # Black
            )
            created_actors.append(skid["actor"])

        unreal.log(f"🚁 Helicopter created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Helicopter)",
            "name": name,
            "type": "helicopter",
            "actors": created_actors
        }

    def _create_tank(self, parsed: dict) -> dict:
        """Create a tank"""
        name = parsed.get("name") or "Tank"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("🎖️ Creating tank...")

        created_actors = []

        # Hull/body
        hull_scale = (scale * 2, scale * 1.5, scale * 4)
        hull_pos = position
        hull = self._create_composite_cube(
            f"{name}_Hull", hull_pos, hull_scale,
            props.get("color", (0.4, 0.5, 0.35))  # Military green
        )
        created_actors.append(hull["actor"])

        # Tracks (left and right)
        for side in [-1, 1]:
            track_scale = (scale * 0.5, scale * 1.2, scale * 4.2)
            track_pos = (position[0] + side * scale * 1.3, position[1], position[2])
            track = self._create_composite_cube(
                f"{name}_Track_{'L' if side < 0 else 'R'}", track_pos, track_scale,
                (0.15, 0.15, 0.15)  # Dark tracks
            )
            created_actors.append(track["actor"])

        # Turret
        turret_scale = (scale * 1.5, scale * 1, scale * 1.5)
        turret_pos = (position[0], position[1], position[2] + scale * 1.3)
        turret = self._create_composite_cube(
            f"{name}_Turret", turret_pos, turret_scale,
            (0.35, 0.45, 0.3)  # Slightly darker green
        )
        created_actors.append(turret["actor"])

        # Cannon barrel
        barrel_scale = (scale * 0.2, scale * 0.2, scale * 3)
        barrel_pos = (position[0], position[1] + scale * 0.6, position[2] + scale * 1.3)
        barrel = self._create_composite_cube(
            f"{name}_Barrel", barrel_pos, barrel_scale,
            (0.2, 0.2, 0.2)  # Dark barrel
        )
        created_actors.append(barrel["actor"])

        # Commander's cupola
        cupola_scale = (scale * 0.4, scale * 0.3, scale * 0.4)
        cupola_pos = (position[0], position[1] - scale * 0.3, position[2] + scale * 2.1)
        cupola = self._create_composite_cube(
            f"{name}_Cupola", cupola_pos, cupola_scale,
            (0.35, 0.45, 0.3)
        )
        created_actors.append(cupola["actor"])

        unreal.log(f"🎖️ Tank created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Tank)",
            "name": name,
            "type": "tank",
            "actors": created_actors
        }

    # ============================================================
    # ARCHITECTURAL CREATION
    # ============================================================

    def _create_castle(self, parsed: dict) -> dict:
        """Create a castle"""
        name = parsed.get("name") or "Castle"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 3.0

        unreal.log("🏰 Creating castle...")

        created_actors = []

        # Main keep (central tower)
        keep_scale = (scale * 3, scale * 3, scale * 8)
        keep_pos = position
        keep = self._create_composite_cube(
            f"{name}_Keep", keep_pos, keep_scale,
            (0.5, 0.45, 0.4)  # Stone
        )
        created_actors.append(keep["actor"])

        # Corner towers (4 towers)
        for i in range(4):
            angle = (2 * math.pi * i) / 4
            tower_scale = (scale * 2, scale * 2, scale * 6)
            tower_pos = (
                position[0] + scale * 4 * math.cos(angle),
                position[1] + scale * 4 * math.sin(angle),
                position[2]
            )
            tower = self._create_composite_cube(
                f"{name}_Tower_{i}", tower_pos, tower_scale,
                (0.5, 0.45, 0.4)
            )
            created_actors.append(tower["actor"])

            # Tower roof (conical - simplified as cube)
            roof_scale = (scale * 2.2, scale * 2.2, scale * 1)
            roof_pos = (tower_pos[0], tower_pos[1], tower_pos[2] + scale * 3)
            roof = self._create_composite_cube(
                f"{name}_TowerRoof_{i}", roof_pos, roof_scale,
                (0.4, 0.2, 0.15)  # Dark red roof
            )
            created_actors.append(roof["actor"])

        # Walls (connecting towers)
        wall_configs = [
            ("North", (0, scale * 4, scale * 2), (scale * 8, scale * 1, scale * 4)),
            ("East", (scale * 4, 0, scale * 2), (scale * 1, scale * 8, scale * 4)),
            ("South", (0, -scale * 4, scale * 2), (scale * 8, scale * 1, scale * 4)),
            ("West", (-scale * 4, 0, scale * 2), (scale * 1, scale * 8, scale * 4))
        ]

        for wall_name, wall_pos, wall_scale in wall_configs:
            wall = self._create_composite_cube(
                f"{name}_Wall_{wall_name}",
                (position[0] + wall_pos[0], position[1] + wall_pos[1], position[2] + wall_pos[2]),
                wall_scale,
                (0.5, 0.45, 0.4)
            )
            created_actors.append(wall["actor"])

        # Gate
        gate_scale = (scale * 2, scale * 0.5, scale * 3)
        gate_pos = (position[0], position[1] + scale * 4, position[2] + scale * 1.5)
        gate = self._create_composite_cube(
            f"{name}_Gate", gate_pos, gate_scale,
            (0.3, 0.2, 0.1)  # Wood
        )
        created_actors.append(gate["actor"])

        # Main keep roof
        keep_roof_scale = (scale * 3.5, scale * 3.5, scale * 1)
        keep_roof_pos = (position[0], position[1], position[2] + scale * 4.5)
        keep_roof = self._create_composite_cube(
            f"{name}_KeepRoof", keep_roof_pos, keep_roof_scale,
            (0.4, 0.2, 0.15)
        )
        created_actors.append(keep_roof["actor"])

        unreal.log(f"🏰 Castle created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Castle)",
            "name": name,
            "type": "castle",
            "actors": created_actors
        }

    def _create_tower(self, parsed: dict) -> dict:
        """Create a tower"""
        name = parsed.get("name") or "Tower"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("🗼 Creating tower...")

        created_actors = []

        # Main tower structure
        tower_scale = (scale * 2, scale * 2, scale * 8)
        tower_pos = position
        tower = self._create_composite_cube(
            f"{name}_Main", tower_pos, tower_scale,
            (0.5, 0.45, 0.4)  # Stone
        )
        created_actors.append(tower["actor"])

        # Roof
        roof_scale = (scale * 2.2, scale * 2.2, scale * 1.5)
        roof_pos = (position[0], position[1], position[2] + scale * 4.7)
        roof = self._create_composite_cube(
            f"{name}_Roof", roof_pos, roof_scale,
            (0.4, 0.2, 0.15)  # Dark red roof
        )
        created_actors.append(roof["actor"])

        # Windows (multiple levels)
        for level in range(3):
            for side in [-1, 1]:
                window_scale = (scale * 0.3, scale * 0.1, scale * 0.5)
                window_pos = (
                    position[0] + side * scale * 1.05,
                    position[1],
                    position[2] + scale * (1 + level * 2)
                )
                window = self._create_composite_cube(
                    f"{name}_Window_{level}_{'L' if side < 0 else 'R'}",
                    window_pos, window_scale,
                    (0.2, 0.3, 0.4)  # Dark window
                )
                created_actors.append(window["actor"])

        # Door
        door_scale = (scale * 0.8, scale * 0.2, scale * 2)
        door_pos = (position[0], position[1] + scale * 1.1, position[2] + scale * 1)
        door = self._create_composite_cube(
            f"{name}_Door", door_pos, door_scale,
            (0.3, 0.2, 0.1)  # Wood
        )
        created_actors.append(door["actor"])

        unreal.log(f"🗼 Tower created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Tower)",
            "name": name,
            "type": "tower",
            "actors": created_actors
        }

    def _create_bridge(self, parsed: dict) -> dict:
        """Create a bridge"""
        name = parsed.get("name") or "Bridge"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 5.0

        unreal.log("🌉 Creating bridge...")

        created_actors = []

        # Bridge deck
        deck_scale = (scale * 3, scale * 0.5, scale * 15)
        deck_pos = position
        deck = self._create_composite_cube(
            f"{name}_Deck", deck_pos, deck_scale,
            (0.4, 0.35, 0.3)  # Wood/stone
        )
        created_actors.append(deck["actor"])

        # Supports (pillars)
        for i in range(4):
            support_scale = (scale * 0.8, scale * 3, scale * 0.8)
            support_pos = (
                position[0],
                position[1],
                position[2] - scale * 2.5 + i * scale * 1.7
            )
            support = self._create_composite_cube(
                f"{name}_Support_{i}", support_pos, support_scale,
                (0.5, 0.45, 0.4)  # Stone
            )
            created_actors.append(support["actor"])

        # Railings
        for side in [-1, 1]:
            railing_scale = (scale * 0.1, scale * 0.8, scale * 15)
            railing_pos = (position[0] + side * scale * 1.5, position[1], position[2] + scale * 0.6)
            railing = self._create_composite_cube(
                f"{name}_Railing_{'L' if side < 0 else 'R'}", railing_pos, railing_scale,
                (0.3, 0.25, 0.2)  # Wood/metal
            )
            created_actors.append(railing["actor"])

        unreal.log(f"🌉 Bridge created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Bridge)",
            "name": name,
            "type": "bridge",
            "actors": created_actors
        }

    def _create_fountain(self, parsed: dict) -> dict:
        """Create a fountain"""
        name = parsed.get("name") or "Fountain"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.5

        unreal.log("⛲ Creating fountain...")

        created_actors = []

        # Base pool
        pool_scale = (scale * 4, scale * 0.5, scale * 4)
        pool_pos = position
        pool = self._create_composite_cube(
            f"{name}_Pool", pool_pos, pool_scale,
            (0.5, 0.45, 0.4)  # Stone
        )
        created_actors.append(pool["actor"])

        # Water
        water_scale = (scale * 3.5, scale * 0.1, scale * 3.5)
        water_pos = (position[0], position[1], position[2] + scale * 0.3)
        water = self._create_composite_cube(
            f"{name}_Water", water_pos, water_scale,
            (0.2, 0.5, 0.7)  # Blue water
        )
        created_actors.append(water["actor"])

        # Central pedestal
        pedestal_scale = (scale * 0.5, scale * 1.5, scale * 0.5)
        pedestal_pos = (position[0], position[1], position[2] + scale * 0.5)
        pedestal = self._create_composite_cube(
            f"{name}_Pedestal", pedestal_pos, pedestal_scale,
            (0.5, 0.45, 0.4)
        )
        created_actors.append(pedestal["actor"])

        # Spout (top)
        spout_scale = (scale * 0.3, scale * 0.4, scale * 0.3)
        spout_pos = (position[0], position[1], position[2] + scale * 1.7)
        spout = self._create_composite_cube(
            f"{name}_Spout", spout_pos, spout_scale,
            (0.5, 0.45, 0.4)
        )
        created_actors.append(spout["actor"])

        # Water spray effect (small cubes)
        for i in range(8):
            angle = (2 * math.pi * i) / 8
            spray_scale = (scale * 0.1, scale * 0.3, scale * 0.1)
            spray_pos = (
                position[0] + scale * 0.4 * math.cos(angle),
                position[1] + scale * 0.4 * math.sin(angle),
                position[2] + scale * 1.9
            )
            spray = self._create_composite_cube(
                f"{name}_Spray_{i}", spray_pos, spray_scale,
                (0.6, 0.7, 0.9)  # Light blue water spray
            )
            created_actors.append(spray["actor"])

        unreal.log(f"⛲ Fountain created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Fountain)",
            "name": name,
            "type": "fountain",
            "actors": created_actors
        }

    def _create_monument(self, parsed: dict) -> dict:
        """Create a monument"""
        name = parsed.get("name") or "Monument"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("🗿 Creating monument...")

        created_actors = []

        # Base platform
        base_scale = (scale * 4, scale * 0.5, scale * 4)
        base_pos = position
        base = self._create_composite_cube(
            f"{name}_Base", base_pos, base_scale,
            (0.5, 0.45, 0.4)  # Stone
        )
        created_actors.append(base["actor"])

        # Statue base
        statue_base_scale = (scale * 2, scale * 1, scale * 2)
        statue_base_pos = (position[0], position[1], position[2] + scale * 0.75)
        statue_base = self._create_composite_cube(
            f"{name}_StatueBase", statue_base_pos, statue_base_scale,
            (0.45, 0.4, 0.35)  # Marble
        )
        created_actors.append(statue_base["actor"])

        # Statue (simplified human form)
        # Body
        body_scale = (scale * 0.8, scale * 0.5, scale * 1.5)
        body_pos = (position[0], position[1], position[2] + scale * 2)
        body = self._create_composite_cube(
            f"{name}_Statue_Body", body_pos, body_scale,
            (0.95, 0.95, 0.9)  # White marble
        )
        created_actors.append(body["actor"])

        # Head
        head_scale = (scale * 0.3, scale * 0.3, scale * 0.35)
        head_pos = (position[0], position[1], position[2] + scale * 3)
        head = self._create_composite_cube(
            f"{name}_Statue_Head", head_pos, head_scale,
            (0.95, 0.95, 0.9)
        )
        created_actors.append(head["actor"])

        # Plaque
        plaque_scale = (scale * 1, scale * 0.1, scale * 0.8)
        plaque_pos = (position[0], position[1] + scale * 2.1, position[2] + scale * 1)
        plaque = self._create_composite_cube(
            f"{name}_Plaque", plaque_pos, plaque_scale,
            (0.7, 0.65, 0.3)  # Bronze
        )
        created_actors.append(plaque["actor"])

        unreal.log(f"🗿 Monument created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Monument)",
            "name": name,
            "type": "monument",
            "actors": created_actors
        }

    # ============================================================
    # NATURE CREATION
    # ============================================================

    def _create_mountain(self, parsed: dict) -> dict:
        """Create a mountain"""
        name = parsed.get("name") or "Mountain"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 10.0

        unreal.log("🏔️ Creating mountain...")

        created_actors = []

        # Main peak (large pyramid)
        peak_scale = (scale * 8, scale * 6, scale * 10)
        peak_pos = position
        peak = self._create_composite_cube(
            f"{name}_Peak", peak_pos, peak_scale,
            (0.4, 0.35, 0.3)  # Rock color
        )
        created_actors.append(peak["actor"])

        # Snow cap
        snow_scale = (scale * 3, scale * 1.5, scale * 3)
        snow_pos = (position[0], position[1], position[2] + scale * 4)
        snow = self._create_composite_cube(
            f"{name}_SnowCap", snow_pos, snow_scale,
            (1, 1, 1)  # Snow white
        )
        created_actors.append(snow["actor"])

        # Side slopes
        for i in range(4):
            angle = (2 * math.pi * i) / 4
            slope_scale = (scale * 5, scale * 3, scale * 6)
            slope_pos = (
                position[0] + scale * 5 * math.cos(angle),
                position[1] + scale * 5 * math.sin(angle),
                position[2] - scale * 2
            )
            slope = self._create_composite_cube(
                f"{name}_Slope_{i}", slope_pos, slope_scale,
                (0.35, 0.4, 0.25)  # Grass/moss
            )
            created_actors.append(slope["actor"])

        unreal.log(f"🏔️ Mountain created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Mountain)",
            "name": name,
            "type": "mountain",
            "actors": created_actors
        }

    def _create_volcano(self, parsed: dict) -> dict:
        """Create a volcano"""
        name = parsed.get("name") or "Volcano"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 8.0

        unreal.log("🌋 Creating volcano...")

        created_actors = []

        # Main cone
        cone_scale = (scale * 10, scale * 5, scale * 10)
        cone_pos = position
        cone = self._create_composite_cube(
            f"{name}_Cone", cone_pos, cone_scale,
            (0.25, 0.2, 0.15)  # Dark volcanic rock
        )
        created_actors.append(cone["actor"])

        # Crater
        crater_scale = (scale * 2, scale * 0.5, scale * 2)
        crater_pos = (position[0], position[1], position[2] + scale * 2.5)
        crater = self._create_composite_cube(
            f"{name}_Crater", crater_pos, crater_scale,
            (0.1, 0.05, 0.05)  # Dark crater
        )
        created_actors.append(crater["actor"])

        # Lava (glowing)
        lava_scale = (scale * 1.5, scale * 0.3, scale * 1.5)
        lava_pos = (position[0], position[1], position[2] + scale * 2.7)
        lava = self._create_composite_cube(
            f"{name}_Lava", lava_pos, lava_scale,
            (1, 0.3, 0)  # Bright orange lava
        )
        created_actors.append(lava["actor"])

        # Lava glow particles
        for i in range(6):
            glow_scale = (scale * 0.3, scale * 0.1, scale * 0.3)
            glow_pos = (
                position[0] + (i % 2 - 0.5) * scale * 0.5,
                position[1] + ((i // 2) % 2 - 0.5) * scale * 0.5,
                position[2] + scale * 2.9 + (i % 3) * scale * 0.2
            )
            glow = self._create_composite_cube(
                f"{name}_Glow_{i}", glow_pos, glow_scale,
                (1, 0.5, 0)  # Orange glow
            )
            created_actors.append(glow["actor"])

        unreal.log(f"🌋 Volcano created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Volcano)",
            "name": name,
            "type": "volcano",
            "actors": created_actors
        }

    def _create_river(self, parsed: dict) -> dict:
        """Create a river"""
        name = parsed.get("name") or "River"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 5.0

        unreal.log("🌊 Creating river...")

        created_actors = []

        # River bed (multiple segments)
        num_segments = 10
        for i in range(num_segments):
            # Slight curve
            offset_x = math.sin(i * 0.5) * scale * 0.5

            segment_scale = (scale * 1.5, scale * 0.2, scale * 2)
            segment_pos = (
                position[0] + offset_x,
                position[1],
                position[2] + i * scale * 1.5
            )
            segment = self._create_composite_cube(
                f"{name}_Segment_{i}", segment_pos, segment_scale,
                (0.6, 0.5, 0.3)  # Sand/dirt
            )
            created_actors.append(segment["actor"])

            # Water on top
            water_scale = (scale * 1.4, scale * 0.05, scale * 1.8)
            water_pos = (segment_pos[0], segment_pos[1], segment_pos[2] + scale * 0.12)
            water = self._create_composite_cube(
                f"{name}_Water_{i}", water_pos, water_scale,
                (0.2, 0.5, 0.7)  # Blue water
            )
            created_actors.append(water["actor"])

        # River banks
        for side in [-1, 1]:
            bank_scale = (scale * 0.8, scale * 0.3, scale * 15)
            bank_pos = (position[0] + side * scale * 1.2, position[1], position[2] + scale * 6)
            bank = self._create_composite_cube(
                f"{name}_Bank_{'L' if side < 0 else 'R'}", bank_pos, bank_scale,
                (0.3, 0.5, 0.2)  # Grass
            )
            created_actors.append(bank["actor"])

        unreal.log(f"🌊 River created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (River)",
            "name": name,
            "type": "river",
            "actors": created_actors
        }

    def _create_cloud(self, parsed: dict) -> dict:
        """Create a cloud"""
        name = parsed.get("name") or "Cloud"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("☁️ Creating cloud...")

        created_actors = []

        # Main puffs (rounded cubes)
        puff_positions = [
            (0, 0, 0),
            (1, 0.3, 0.2),
            (-1, 0.2, -0.1),
            (0.5, -0.2, 0.3),
            (-0.5, -0.1, -0.2),
            (0, 0.4, 0),
            (0.7, 0, -0.2),
        ]

        for i, puff_offset in enumerate(puff_positions):
            puff_scale = (scale * 0.8, scale * 0.5, scale * 0.7)
            puff_pos = (
                position[0] + puff_offset[0] * scale * 0.6,
                position[1] + puff_offset[1] * scale * 0.6,
                position[2] + puff_offset[2] * scale * 0.6
            )
            puff = self._create_composite_cube(
                f"{name}_Puff_{i}", puff_pos, puff_scale,
                (1, 1, 1, 0.8)  # White, slightly transparent
            )
            created_actors.append(puff["actor"])

        unreal.log(f"☁️ Cloud created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Cloud)",
            "name": name,
            "type": "cloud",
            "actors": created_actors
        }

    def _create_terrain(self, parsed: dict) -> dict:
        """Create terrain (hills and valleys)"""
        name = parsed.get("name") or "Terrain"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 5.0

        unreal.log("🏔️ Creating terrain...")

        created_actors = []

        # Create varied terrain with multiple heights
        terrain_grid = [
            [0.2, 0.5, 0.3, 0.6, 0.2],
            [0.4, 0.8, 1.2, 0.9, 0.5],
            [0.3, 1.0, 1.5, 1.1, 0.4],
            [0.5, 0.7, 0.9, 0.6, 0.3],
            [0.2, 0.4, 0.3, 0.5, 0.2],
        ]

        for x in range(5):
            for y in range(5):
                height = terrain_grid[x][y]
                block_scale = (scale * 1.1, scale * height, scale * 1.1)
                block_pos = (
                    position[0] + (x - 2) * scale * 1.2,
                    position[1] + (y - 2) * scale * 1.2,
                    position[2] + scale * height * 0.5
                )

                # Vary material based on height
                if height > 1.0:
                    color = (0.5, 0.45, 0.4)  # Rock
                elif height > 0.6:
                    color = (0.3, 0.5, 0.2)  # Grass
                else:
                    color = (0.4, 0.5, 0.3)  # Light grass

                block = self._create_composite_cube(
                    f"{name}_Block_{x}_{y}", block_pos, block_scale,
                    color
                )
                created_actors.append(block["actor"])

        unreal.log(f"🏔️ Terrain created with {len(created_actors)} components")

        return {
            "message": f"Created {name} (Terrain)",
            "name": name,
            "type": "terrain",
            "actors": created_actors
        }

    # ============================================================
    # MATERIAL CREATION
    # ============================================================

    def _create_dragon_material(self, props: dict):
        """Create dragon material with scales"""
        try:
            base_color = props.get("color", (0.7, 0.15, 0.05))

            # Main scales material
            scales_mat = self._create_advanced_material(
                "DragonScales",
                base_color,
                roughness=0.7,
                metallic=0.0,
                normal_intensity=0.5
            )

            # Belly/underbelly (lighter)
            belly_mat = self._create_advanced_material(
                "DragonBelly",
                (base_color[0] * 0.8, base_color[1] * 0.8, base_color[2] * 0.7),
                roughness=0.9,
                metallic=0.0
            )

            unreal.log("🐉 Dragon materials created")

        except Exception as e:
            unreal.log_error(f"Dragon material creation failed: {e}")

    def _create_spaceship_material(self, style: str):
        """Create spaceship materials"""
        try:
            if "sci-fi" in style.lower():
                # Metallic, glowing
                hull_mat = self._create_advanced_material(
                    "SpaceshipHull",
                    (0.3, 0.4, 0.5),
                    roughness=0.3,
                    metallic=0.9,
                    emissive=(0.1, 0.2, 0.3)
                )
            else:
                # Realistic
                hull_mat = self._create_advanced_material(
                    "SpaceshipHull",
                    (0.5, 0.5, 0.6),
                    roughness=0.4,
                    metallic=0.7
                )

        except Exception as e:
            unreal.log_error(f"Spaceship material creation failed: {e}")

    def _create_advanced_material(self, name: str, base_color: Tuple[float, float, float],
                              roughness: float = 0.5, metallic: float = 0.0,
                              normal_intensity: float = 0.5,
                              emissive: Optional[Tuple[float, float, float]] = None) -> str:
        """Create advanced material with all properties"""
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
            color_const.set_editor_property("constant", unreal.LinearColor(
                base_color[0], base_color[1], base_color[2], 1.0
            ))
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

            # Normal (for detail)
            if normal_intensity > 0:
                normal_const = mat_editing.create_material_expression(
                    material, unreal.MaterialExpressionConstant3Vector
                )
                normal_const.set_editor_property("constant", unreal.LinearColor(
                    normal_intensity, normal_intensity, normal_intensity, 1.0
                ))
                mat_editing.connect_material_property(
                    normal_const, "Output", material, unreal.MaterialProperty.MP_NORMAL
                )

            # Emissive (if specified)
            if emissive:
                emissive_const = mat_editing.create_material_expression(
                    material, unreal.MaterialExpressionConstant3Vector
                )
                emissive_const.set_editor_property("constant", unreal.LinearColor(
                    emissive[0], emissive[1], emissive[2], 1.0
                ))
                mat_editing.connect_material_property(
                    emissive_const, "Output", material, unreal.MaterialProperty.MP_EMISSIVE_COLOR
                )

            unreal.log(f"Created advanced material: {name}")

            return f"/Game/GeneratedMaterials/{name}"

        except Exception as e:
            unreal.log_error(f"Material creation failed: {e}")
            return None

    # ============================================================
    # COMPOSITE CREATION HELPERS
    # ============================================================

    def _create_composite_cube(self, name: str, position: Tuple[float, float, float],
                               scale: Tuple[float, float, float],
                               color: Tuple[float, float, float]) -> dict:
        """Create a cube as part of composite object"""
        try:
            loc = unreal.Vector(position[0], position[1], position[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
            actor.set_actor_label(name)
            actor.set_actor_scale3d(unreal.Vector(scale[0], scale[1], scale[2]))

            # Create material
            mat_name = f"{name}_Mat_{hash(color)}"
            if mat_name not in self.asset_library.get("materials", {}):
                mat_path = self._create_simple_material_for_name(mat_name, color)
                if "materials" not in self.asset_library:
                    self.asset_library["materials"] = {}
                self.asset_library["materials"][mat_name] = mat_path

            # Assign material
            if mat_name in self.asset_library["materials"]:
                mat_path = self.asset_library["materials"][mat_name]
                material = unreal.load_asset(mat_path, unreal.Material)
                if material:
                    mesh_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
                    if mesh_comp:
                        mesh_comp.set_material(0, material)

            return {"name": name, "actor": actor}
        except Exception as e:
            return {"error": str(e)}

    def _create_simple_material_for_name(self, mat_name: str, color: Tuple[float, float, float]) -> str:
        """Create a simple material with given name and color"""
        try:
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

            material = asset_tools.create_asset(
                mat_name,
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
            rough_const.set_editor_property("r", 0.5)
            mat_editing.connect_material_property(
                rough_const, "Output", material, unreal.MaterialProperty.MP_ROUGHNESS
            )

            return f"/Game/GeneratedMaterials/{mat_name}"

        except Exception as e:
            unreal.log_error(f"Material creation failed: {e}")
            return None

    # ============================================================
    # COLOR EXTRACTION
    # ============================================================

    def _extract_color_advanced(self, description: str) -> Tuple[float, float, float]:
        """Extract color with context awareness"""
        desc_lower = description.lower()

        # Named colors
        colors = {
            "red": (1, 0, 0), "crimson": (0.86, 0.08, 0.24),
            "dark red": (0.7, 0.1, 0.1),
            "bright red": (1, 0.2, 0.2),
            "green": (0, 1, 0), "emerald": (0.18, 0.55, 0.34),
            "dark green": (0.1, 0.5, 0.1),
            "lime": (0.2, 1, 0), "forest": (0.13, 0.55, 0.13),
            "blue": (0, 0, 1), "navy": (0, 0, 0.5), "azure": (0, 0.5, 1),
            "sky blue": (0.53, 0.81, 0.92), "cyan": (0, 1, 1),
            "teal": (0, 0.5, 0.5), "turquoise": (0.04, 0.74, 0.83),
            "yellow": (1, 1, 0), "gold": (1, 0.84, 0), "amber": (1, 0.75, 0),
            "orange": (1, 0.5, 0), "rust": (0.7, 0.3, 0.1),
            "purple": (0.5, 0, 1), "violet": (0.5, 0, 1),
            "magenta": (1, 0, 1), "pink": (1, 0.5, 0.5),
            "brown": (0.6, 0.4, 0.2), "tan": (0.82, 0.71, 0.55),
            "beige": (0.96, 0.96, 0.86), "cream": (1, 1, 0.84),
            "white": (1, 1, 1), "ivory": (1, 1, 0.94),
            "gray": (0.5, 0.5, 0.5), "grey": (0.5, 0.5, 0.5),
            "black": (0, 0, 0), "charcoal": (0.2, 0.2, 0.2),
            "silver": (0.75, 0.75, 0.75), "chrome": (0.8, 0.8, 0.8),
            "iron": (0.7, 0.7, 0.7), "steel": (0.7, 0.7, 0.7),
            "copper": (0.72, 0.45, 0.2), "bronze": (0.72, 0.45, 0.2)
        }

        for color_name, color_value in colors.items():
            if color_name in desc_lower:
                return color_value

        return (0.5, 0.5, 0.5)  # Default gray

    def _extract_color_from_context(self, text: str, default_color: str) -> Tuple[float, float, float]:
        """Extract color based on context around the word"""
        # Look for color mentioned near the target word
        words = text.split()

        # Find the word that might be the color
        for i, word in enumerate(words):
            if word.lower() in ["red", "green", "blue", "yellow", "orange", "purple", "pink", "cyan", "white", "black", "gray", "brown", "gold", "silver"]:
                # Check surrounding words for more context
                context_words = words[max(0, i-2):i+3]
                context = " ".join(context_words)

                # Check for modifiers
                if "dark" in context.lower():
                    if "red" in context.lower():
                        return (0.5, 0.1, 0.1)
                    elif "blue" in context.lower():
                        return (0.1, 0.1, 0.3)
                    elif "green" in context.lower():
                        return (0.1, 0.3, 0.1)
                elif "bright" in context.lower():
                    if "red" in context.lower():
                        return (1, 0.3, 0.3)
                    elif "blue" in context.lower():
                        return (0.3, 0.5, 1)
                    elif "green" in context.lower():
                        return (0.3, 1, 0.3)
                elif "light" in context.lower():
                    if "red" in context.lower():
                        return (1, 0.5, 0.5)
                    elif "blue" in context.lower():
                        return (0.5, 0.7, 1)

        # Default color for the context
        if default_color == "red":
            return (1, 0, 0)
        elif default_color == "green":
            return (0, 1, 0)
        elif default_color == "blue":
            return (0, 0, 1)
        elif default_color == "yellow":
            return (1, 1, 0)
        elif default_color == "orange":
            return (1, 0.5, 0)
        elif default_color == "purple":
            return (0.5, 0, 1)
        elif default_color == "white":
            return (1, 1, 1)
        elif default_color == "black":
            return (0, 0, 0)
        elif default_color == "gold":
            return (1, 0.84, 0)
        elif default_color == "silver":
            return (0.75, 0.75, 0.75)

        # Fallback colors by type
        if "dragon" in text.lower():
            return (0.7, 0.15, 0.05)  # Greenish-brown
        elif "spaceship" in text.lower():
            return (0.3, 0.4, 0.5)  # Metallic blue-gray
        elif "character" in text.lower():
            return (0.8, 0.6, 0.5)  # Skin tone

        return (0.5, 0.5, 0.5)

    # ============================================================
    # PROPERTY EXTRACTION
    # ============================================================

    def _extract_size_advanced(self, text: str) -> float:
        """Extract size with context"""
        desc_lower = text.lower()

        # Explicit size
        size_patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:times|bigger|larger|size)',
            r'(\d+(?:\.\d+)?)\s*x',
            r'scale\s*(\d+(?:\.\d+)?)'
        ]

        for pattern in size_patterns:
            match = re.search(pattern, desc_lower)
            if match:
                try:
                    return float(match.group(1))
                except:
                    pass

        # Size words
        size_words = {
            "tiny": 0.1, "small": 0.3, "normal": 1.0,
            "large": 2.0, "huge": 5.0, "massive": 10.0,
            "giant": 20.0, "colossal": 50.0
        }

        for word, size in size_words.items():
            if word in desc_lower:
                return size

        # Context-based
        if "character" in desc_lower:
            return 1.8  # Human scale
        elif "building" in desc_lower:
            return 5.0  # Building scale
        elif "vehicle" in desc_lower:
            return 3.0  # Vehicle scale
        elif "spaceship" in desc_lower:
            return 10.0  # Spaceship scale
        elif "dragon" in desc_lower:
            return 8.0  # Dragon scale

        return 1.0  # Default

    def _extract_material_properties(self, description: str) -> dict:
        """Extract material properties from description"""
        props = {}

        desc_lower = description.lower()

        # Color
        props["color"] = self._extract_color_advanced(description)

        # Roughness
        if "rough" in desc_lower:
            props["roughness"] = 0.9
        elif "smooth" in desc_lower or "polished" in desc_lower:
            props["roughness"] = 0.1
        elif "matte" in desc_lower:
            props["roughness"] = 0.7
        else:
            props["roughness"] = 0.5

        # Metallic
        metals = ["metal", "steel", "iron", "chrome", "gold", "silver", "copper", "bronze"]
        non_metals = ["wood", "plastic", "fabric", "rubber", "organic", "stone", "ceramic", "glass"]

        if any(m in desc_lower for m in metals):
            props["metallic"] = 1.0
        elif any(nm in desc_lower for nm in non_metals):
            props["metallic"] = 0.0
        else:
            props["metallic"] = 0.0

        # Special materials
        if "glass" in desc_lower or "transparent" in desc_lower:
            props["opacity"] = 0.5
        if "glowing" in desc_lower or "emissive" in desc_lower:
            props["emissive"] = self._extract_color_advanced(description)

        return props

    def _extract_style(self, description: str) -> str:
        """Extract style from description"""
        desc_lower = description.lower()

        if "sci-fi" in desc_lower or "futuristic" in desc_lower:
            return "sci-fi"
        elif "medieval" in desc_lower or "fantasy" in desc_lower:
            return "medieval"
        elif "modern" in desc_lower or "contemporary" in desc_lower:
            return "modern"
        elif "ancient" in desc_lower or "old" in desc_lower:
            return "ancient"
        else:
            return "generic"

    def _extract_position(self, description: str) -> Tuple[float, float, float]:
        """Extract position from description"""
        return (0, 0, 0)  # Default origin

    def _extract_quantity_advanced(self, description: str) -> Optional[int]:
        """Extract quantity"""
        return self._extract_quantity(description)

    def _extract_quantity(self, text: str) -> Optional[int]:
        """Extract quantity from text"""
        number_words = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "dozen": 12
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

    # ============================================================
    # SPECIALIZED GETTERS
    # ============================================================

    def _get_spaceship_color(self, style: str) -> Tuple[float, float, float]:
        """Get spaceship color based on style"""
        if "sci-fi" in style.lower():
            return (0.2, 0.4, 0.6)  # Cool blue-gray
        else:
            return (0.5, 0.5, 0.5)  # Generic gray

    def _get_tree_bark_color(self) -> Tuple[float, float, float]:
        """Get tree bark color"""
        return (0.4, 0.25, 0.1)  # Brown

    def _get_leaf_color(self) -> Tuple[float, float, float]:
        """Get leaf color based on season/context"""
        return (0.2, 0.6, 0.2)  # Green

    def _get_dragon_material(self, props: dict) -> str:
        """Get dragon material name"""
        color = props.get("color", (0.7, 0.15, 0.05))
        return f"Dragon_{int(color[0]*255)}_{int(color[1]*255)}_{int(color[2]*255)}"


# Create global instance
creation_engine = InfiniteCreationEngine()

# ============================================================
# MAIN API
# ============================================================

def create(description: str) -> dict:
    """
    Main creation function - creates anything from description

    This is the primary function for infinite creation.

    Examples:
        create("a red dragon with gold eyes")
        create("a sci-fi spaceship")
        create("a medieval castle")
        create("a sports car")
        create("a fantasy warrior with sword")
        create("a dragon with glowing eyes")
        create("a wooden table with 4 chairs")
        create("a sci-fi city")
        create("a character with red hair")
        create("a diamond sword")
        create("a glass cup")
        create("a golden throne")
    """
    return creation_engine.create(description)


# Display banner
unreal.log("\n" + "█"*70)
unreal.log("█                                                          █")
unreal.log("█     🎨 INFINITE CREATION ENGINE - CREATE ANYTHING              █")
unreal.log("█                                                          █")
unreal.log("█"*70)
unreal.log("\n🌟� JUST DESCRIBE WHAT YOU WANT:\n")

examples = [
    'create("a red dragon with golden eyes")',
    'create("a sci-fi spaceship")',
    'create("a medieval castle")',
    'create("a sports car")',
    'create("a fantasy character with sword")',
    'create("a wooden table with 4 chairs")',
    'create("a glowing sword")',
    'create("a dragon with blue scales")',
    'create("a futuristic city")',
    'create("a character with red hair")'
]

for i, example in enumerate(examples, 1):
    unreal.log(f"   {i}. {example}")

unreal.log(f"\n📚 CREATION TYPES:\n")
creation_types = [
    "🐉 Creatures: dragon, wolf, eagle, fish, insect, unicorn, phoenix, golem",
    "👹 Corelings (The Painted Man): wind demon, fire demon, water demon, rock demon, wood demon, mind demon, hashak",
    "🚀 Vehicles: spaceship, car, motorcycle, boat, airplane, helicopter, tank",
    "🏠 Architecture: building, castle, tower, bridge, fountain, monument",
    "🌳 Nature: tree, mountain, volcano, river, cloud, terrain",
    "👤 Characters: character, person, human",
    "⚔️ Items: weapon, sword, furniture, chair, table"
]
for ct in creation_types:
    unreal.log(f"   {ct}")

unreal.log(f"\n💡 MORE EXAMPLES:\n")
examples_list = [
    "create(\"a wind demon soaring through the sky\")",
    "create(\"a fire demon engulfed in flames\")",
    "create(\"a water demon rising from the depths\")",
    "create(\"a rock demon with stone armor\")",
    "create(\"a wood demon camouflaged in the forest\")",
    "create(\"a mind demon with psychic aura\")",
    "create(\"a hashak - the most powerful demon\")",
    "create(\"an army of corelings attacking\")",
    "create(\"5 dragons in a circle\")",
    "create(\"a pack of wolves howling at the moon\")",
    "create(\"a majestic eagle with golden feathers\")",
    "create(\"a school of colorful fish\")",
    "create(\"a magical unicorn with rainbow mane\")",
    "create(\"a phoenix rising from flames\")",
    "create(\"a stone golem guardian\")",
    "create(\"a fleet of sci-fi spaceships\")",
    "create(\"a sports car racing down the road\")",
    "create(\"a motorcycle speeding\")",
    "create(\"a sailboat on the ocean\")",
    "create(\"a passenger jet flying\")",
    "create(\"a helicopter rescue mission\")",
    "create(\"a tank battalion\")",
    "create(\"a medieval castle on a hill\")",
    "create(\"a tall stone tower\")",
    "create(\"an ancient bridge over a river\")",
    "create(\"a beautiful fountain in a plaza\")",
    "create(\"a monument to heroes\")",
    "create(\"a majestic mountain range\")",
    "create(\"an erupting volcano\")",
    "create(\"a winding river through a valley\")",
    "create(\"fluffy clouds in the sky\")",
    "create(\"rolling hills and valleys\")",
    "create(\"a dragon with purple scales and green eyes\")",
    "create(\"a golden throne with jewels\")",
    "create(\"a sci-fi city with lights\")",
    "create(\"a medieval knight with armor and sword\")",
]
for i, ex in enumerate(examples_list[:15], 1):
    unreal.log(f"   {i}. {ex}")
unreal.log("   ...and many more! Type anything and it will be created.")

unreal.log("\n" + "="*70 + "\n")
