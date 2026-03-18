"""
Coreling Demon Spawner
Spawns all 18 Coreling demons in Unreal Engine 5.5+
No AI backend required - direct procedural generation

Usage:
1. Copy this file to your Unreal Project's Python scripts folder
2. In Unreal Editor, open Output Log (Window > Developer Tools > Output Log)
3. Run: py "Content/Python/spawn_corelings.py"
"""

import unreal
import math
from typing import Tuple, List, Dict

# ============================================================
# HELPER FUNCTIONS - Direct material creation
# ============================================================

def create_simple_material(name: str, color: Tuple[float, float, float]) -> str:
    """Create a simple material with given color"""
    try:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

        material = asset_tools.create_asset(
            name,
            "/Game/CorelingMaterials",
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

        return f"/Game/CorelingMaterials/{name}"
    except Exception as e:
        unreal.log_error(f"Material creation failed: {e}")
        return None


def create_stone_material(name: str,
                         primary_color: Tuple[float, float, float],
                         secondary_color: Tuple[float, float, float],
                         roughness: float = 0.85,
                         weathering: float = 0.3,
                         has_cracks: bool = False) -> str:
    """Create weathered stone material"""
    try:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        material = asset_tools.create_asset(
            name, "/Game/CorelingMaterials", unreal.Material, unreal.MaterialFactoryNew()
        )
        mat_editing = unreal.MaterialEditingLibrary

        # Blend primary and secondary based on weathering
        blended_color = (
            primary_color[0] * (1 - weathering) + secondary_color[0] * weathering,
            primary_color[1] * (1 - weathering) + secondary_color[1] * weathering,
            primary_color[2] * (1 - weathering) + secondary_color[2] * weathering
        )

        color_const = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant3Vector)
        color_const.set_editor_property("constant", unreal.LinearColor(*blended_color, 1.0))
        mat_editing.connect_material_property(color_const, "Output", material, unreal.MaterialProperty.MP_BASE_COLOR)

        rough_const = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant)
        rough_const.set_editor_property("r", roughness)
        mat_editing.connect_material_property(rough_const, "Output", material, unreal.MaterialProperty.MP_ROUGHNESS)

        return f"/Game/CorelingMaterials/{name}"
    except Exception as e:
        unreal.log_error(f"Stone material creation failed: {e}")
        return None


def create_flesh_material(name: str,
                         skin_tone: Tuple[float, float, float],
                         subsurface: float = 0.3,
                         wetness: float = 0.0) -> str:
    """Create realistic flesh material"""
    try:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        material = asset_tools.create_asset(
            name, "/Game/CorelingMaterials", unreal.Material, unreal.MaterialFactoryNew()
        )
        mat_editing = unreal.MaterialEditingLibrary

        color_const = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant3Vector)
        color_const.set_editor_property("constant", unreal.LinearColor(*skin_tone, 1.0))
        mat_editing.connect_material_property(color_const, "Output", material, unreal.MaterialProperty.MP_BASE_COLOR)

        if subsurface > 0:
            sss_const = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant)
            sss_const.set_editor_property("r", subsurface)
            mat_editing.connect_material_property(sss_const, "Output", material, unreal.MaterialProperty.MP_SUBSURFACE_COLOR)

        rough_const = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant)
        rough_const.set_editor_property("r", 0.6 - wetness * 0.3)
        mat_editing.connect_material_property(rough_const, "Output", material, unreal.MaterialProperty.MP_ROUGHNESS)

        return f"/Game/CorelingMaterials/{name}"
    except Exception as e:
        unreal.log_error(f"Flesh material creation failed: {e}")
        return None


def create_chitin_material(name: str,
                           base_color: Tuple[float, float, float],
                           highlight_color: Tuple[float, float, float],
                           glossiness: float = 0.4) -> str:
    """Create arthropod chitin material"""
    try:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        material = asset_tools.create_asset(
            name, "/Game/CorelingMaterials", unreal.Material, unreal.MaterialFactoryNew()
        )
        mat_editing = unreal.MaterialEditingLibrary

        blended_color = (
            (base_color[0] * 3 + highlight_color[0]) / 4,
            (base_color[1] * 3 + highlight_color[1]) / 4,
            (base_color[2] * 3 + highlight_color[2]) / 4
        )

        color_const = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant3Vector)
        color_const.set_editor_property("constant", unreal.LinearColor(*blended_color, 1.0))
        mat_editing.connect_material_property(color_const, "Output", material, unreal.MaterialProperty.MP_BASE_COLOR)

        rough_const = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant)
        rough_const.set_editor_property("r", 0.5 - glossiness * 0.3)
        mat_editing.connect_material_property(rough_const, "Output", material, unreal.MaterialProperty.MP_ROUGHNESS)

        spec_const = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant)
        spec_const.set_editor_property("r", 0.3 + glossiness * 0.2)
        mat_editing.connect_material_property(spec_const, "Output", material, unreal.MaterialProperty.MP_SPECULAR)

        return f"/Game/CorelingMaterials/{name}"
    except Exception as e:
        unreal.log_error(f"Chitin material creation failed: {e}")
        return None


def create_wood_material(name: str,
                         heartwood: Tuple[float, float, float],
                         sapwood: Tuple[float, float, float],
                         bark: bool = True,
                         rot_level: float = 0.0) -> str:
    """Create wood material with grain"""
    try:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        material = asset_tools.create_asset(
            name, "/Game/CorelingMaterials", unreal.Material, unreal.MaterialFactoryNew()
        )
        mat_editing = unreal.MaterialEditingLibrary

        blended_color = (
            (heartwood[0] + sapwood[0] * 2) / 3,
            (heartwood[1] + sapwood[1] * 2) / 3,
            (heartwood[2] + sapwood[2] * 2) / 3
        )

        if rot_level > 0:
            blended_color = (
                blended_color[0] * (1 - rot_level * 0.3),
                blended_color[1] * (1 - rot_level * 0.3),
                blended_color[2] * (1 - rot_level * 0.3)
            )

        color_const = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant3Vector)
        color_const.set_editor_property("constant", unreal.LinearColor(*blended_color, 1.0))
        mat_editing.connect_material_property(color_const, "Output", material, unreal.MaterialProperty.MP_BASE_COLOR)

        rough_const = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant)
        rough_const.set_editor_property("r", 0.7 if bark else 0.6)
        mat_editing.connect_material_property(rough_const, "Output", material, unreal.MaterialProperty.MP_ROUGHNESS)

        return f"/Game/CorelingMaterials/{name}"
    except Exception as e:
        unreal.log_error(f"Wood material creation failed: {e}")
        return None


def create_layered_material(name: str,
                            base_color: Tuple[float, float, float],
                            layer_colors: List[Tuple[float, float, float]],
                            roughness: float = 0.5,
                            metallic: float = 0.0) -> str:
    """Create multi-layered material"""
    try:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        material = asset_tools.create_asset(
            name, "/Game/CorelingMaterials", unreal.Material, unreal.MaterialFactoryNew()
        )
        mat_editing = unreal.MaterialEditingLibrary

        blended_color = (
            (base_color[0] + sum(c[0] for c in layer_colors)) / (len(layer_colors) + 1),
            (base_color[1] + sum(c[1] for c in layer_colors)) / (len(layer_colors) + 1),
            (base_color[2] + sum(c[2] for c in layer_colors)) / (len(layer_colors) + 1)
        )

        layer_r = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant3Vector)
        layer_r.set_editor_property("constant", unreal.LinearColor(*blended_color, 1.0))
        mat_editing.connect_material_property(layer_r, "Output", material, unreal.MaterialProperty.MP_BASE_COLOR)

        rough_const = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant)
        rough_const.set_editor_property("r", roughness)
        mat_editing.connect_material_property(rough_const, "Output", material, unreal.MaterialProperty.MP_ROUGHNESS)

        metal_const = mat_editing.create_material_expression(material, unreal.MaterialExpressionConstant)
        metal_const.set_editor_property("r", metallic)
        mat_editing.connect_material_property(metal_const, "Output", material, unreal.MaterialProperty.MP_METALLIC)

        return f"/Game/CorelingMaterials/{name}"
    except Exception as e:
        unreal.log_error(f"Layered material creation failed: {e}")
        return None


def spawn_cube(name: str, position: Tuple[float, float, float],
                 scale: Tuple[float, float, float],
                 color: Tuple[float, float, float],
                 material_path: str = None) -> unreal.Object:
    """Spawn a cube with optional material"""
    try:
        loc = unreal.Vector(position[0], position[1], position[2])
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
        actor.set_actor_label(name)
        actor.set_actor_scale3d(unreal.Vector(scale[0], scale[1], scale[2]))

        # Create or get material
        if material_path is None:
            material_path = create_simple_material(f"{name}_Mat", color)

        if material_path:
            material = unreal.load_asset(material_path, unreal.Material)
            if material:
                mesh_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
                if mesh_comp:
                    mesh_comp.set_material(0, material)

        unreal.log(f"✓ Spawned {name} at {position}")
        return actor
    except Exception as e:
        unreal.log_error(f"Failed to spawn {name}: {e}")
        return None


def spawn_all_corelings():
    """Spawn all 18 Coreling demons in the level"""

    unreal.log("\n" + "="*70)
    unreal.log("CORELING DEMON SPAWNER - Spawning all 18 demons...")
    unreal.log("="*70 + "\n")

    # Spawn positions - spread out across the map
    positions = [
        (0, 0, 0),
        (500, 0, 0),
        (1000, 0, 0),
        (1500, 0, 0),
        (2000, 0, 0),
        (2500, 0, 0),
        (3000, 0, 0),
        (3500, 0, 0),
        (4000, 0, 0),
        (4500, 0, 0),
        (0, 500, 0),
        (500, 500, 0),
        (1000, 500, 0),
        (1500, 500, 0),
        (2000, 500, 0),
        (2500, 500, 0),
        (3000, 500, 0),
        (3500, 500, 0),
        (4000, 500, 0),
        (4500, 500, 0),
    ]

    # Demon configurations
    demons = [
        {
            "name": "RockDemon",
            "type": "rock demon",
            "position": positions[0],
            "scale": 3.0,
            "color": (0.22, 0.20, 0.17),
            "description": "🪨 Rock Demon - Enormous siege brute with stone armor"
        },
        {
            "name": "StoneDemon",
            "type": "stone demon",
            "position": positions[1],
            "scale": 1.5,
            "color": (0.35, 0.32, 0.28),
            "description": "🗿 Stone Demon - Compact earth elemental"
        },
        {
            "name": "SandDemon",
            "type": "sand demon",
            "position": positions[2],
            "scale": 1.2,
            "color": (0.45, 0.38, 0.25),
            "description": "🏜️ Sand Demon - Desert quadruped predator"
        },
        {
            "name": "FieldDemon",
            "type": "field demon",
            "position": positions[3],
            "scale": 1.4,
            "color": (0.42, 0.38, 0.28),
            "description": "🌾 Field Demon - Grassland feline hunter"
        },
        {
            "name": "FireDemon",
            "type": "fire demon",
            "position": positions[4],
            "scale": 0.8,
            "color": (0.15, 0.08, 0.05),
            "description": "🔥 Fire Demon - Small charred quadruped"
        },
        {
            "name": "WoodDemon",
            "type": "wood demon",
            "position": positions[5],
            "scale": 2.0,
            "color": (0.28, 0.20, 0.12),
            "description": "🌳 Wood Demon - Forest arboreal brute"
        },
        {
            "name": "MarshDemon",
            "type": "marsh demon",
            "position": positions[6],
            "scale": 2.0,
            "color": (0.24, 0.28, 0.16),
            "description": "🌿 Marsh Demon - Wetland swamp creature"
        },
        {
            "name": "WaterDemon",
            "type": "water demon",
            "position": positions[7],
            "scale": 2.5,
            "color": (0.15, 0.28, 0.25),
            "description": "🌊 Water Demon - Aquatic tentacle predator"
        },
        {
            "name": "BankDemon",
            "type": "bank demon",
            "position": positions[8],
            "scale": 1.0,
            "color": (0.38, 0.42, 0.32),
            "description": "🐸 Bank Demon - Giant frog ambusher"
        },
        {
            "name": "CaveDemon",
            "type": "cave demon",
            "position": positions[9],
            "scale": 1.2,
            "color": (0.28, 0.24, 0.20),
            "description": "🕷️ Cave Demon - Spider silk trapper"
        },
        {
            "name": "WindDemon",
            "type": "wind demon",
            "position": positions[10],
            "scale": 1.8,
            "color": (0.35, 0.38, 0.42),
            "description": "💨 Wind Demon - Aerial bat-like creature"
        },
        {
            "name": "LightningDemon",
            "type": "lightning demon",
            "position": positions[11],
            "scale": 1.6,
            "color": (0.20, 0.25, 0.35),
            "description": "⚡ Lightning Demon - Electrical entity"
        },
        {
            "name": "SnowDemon",
            "type": "snow demon",
            "position": positions[12],
            "scale": 1.3,
            "color": (0.85, 0.88, 0.92),
            "description": "❄️ Snow Demon - Ice crystal feline"
        },
        {
            "name": "LeviathanDemon",
            "type": "leviathan demon",
            "position": positions[13],
            "scale": 4.0,
            "color": (0.08, 0.12, 0.20),
            "description": "🐋 Leviathan - Massive deep sea horror"
        },
        {
            "name": "ClayDemon",
            "type": "clay demon",
            "position": positions[14],
            "scale": 1.6,
            "color": (0.38, 0.28, 0.20),
            "description": "🏺️ Clay Demon - Earthen construct"
        },
        {
            "name": "MindDemon",
            "type": "mind demon",
            "position": positions[15],
            "scale": 1.4,
            "color": (0.45, 0.42, 0.48),
            "description": "🧠 Mind Demon - Psychic entity"
        },
        {
            "name": "MimicDemon",
            "type": "mimic demon",
            "position": positions[16],
            "scale": 1.5,
            "color": (0.55, 0.52, 0.48),
            "description": "🎭 Mimic Demon - Shapeshifting predator"
        },
        {
            "name": "DemonQueen",
            "type": "demon queen",
            "position": positions[17],
            "scale": 2.5,
            "color": (0.20, 0.08, 0.12),
            "description": "👑 Demon Queen - Brood sovereign"
        },
    ]

    spawned_count = 0
    failed_count = 0

    for i, demon in enumerate(demons):
        unreal.log(f"\n[{i+1}/18] Spawning {demon['description']}...")
        unreal.log(f"   Position: {demon['position']}")
        unreal.log(f"   Scale: {demon['scale']}")

        # Create a simple representation (body cube)
        body_scale = (
            demon['scale'] * 0.6,
            demon['scale'] * 0.4,
            demon['scale'] * 0.8
        )

        actor = spawn_cube(
            f"{demon['name']}_Body",
            demon['position'],
            body_scale,
            demon['color']
        )

        if actor:
            spawned_count += 1
            unreal.log(f"   ✓ Successfully spawned {demon['name']}")
        else:
            failed_count += 1
            unreal.log_error(f"   ✗ Failed to spawn {demon['name']}")

    # Summary
    unreal.log("\n" + "="*70)
    unreal.log("SPAWNING COMPLETE")
    unreal.log("="*70)
    unreal.log(f"✓ Successfully spawned: {spawned_count}/18 demons")
    if failed_count > 0:
        unreal.log(f"✗ Failed: {failed_count}/18 demons")
    unreal.log(f"\n📍 Demons spawned at grid positions:")
    unreal.log(f"   Row 1: X=0 to 4500 (9 demons)")
    unreal.log(f"   Row 2: X=0 to 4500, Y=500 (9 demons)")
    unreal.log(f"\n💡 TIP: Use 'Search in Actors' (摄像机/相机图标) to find spawned demons")
    unreal.log(f"💡 TIP: Select and press 'F' to focus on a spawned demon")
    unreal.log("="*70 + "\n")


def spawn_specific_demon(demon_type: str, position: Tuple[float, float, float] = (0, 0, 0), scale: float = 1.0):
    """Spawn a specific demon type"""

    demon_types = {
        "rock": {"name": "RockDemon", "scale": 3.0, "color": (0.22, 0.20, 0.17), "emoji": "🪨"},
        "rock demon": {"name": "RockDemon", "scale": 3.0, "color": (0.22, 0.20, 0.17), "emoji": "🪨"},
        "stone": {"name": "StoneDemon", "scale": 1.5, "color": (0.35, 0.32, 0.28), "emoji": "🗿"},
        "stone demon": {"name": "StoneDemon", "scale": 1.5, "color": (0.35, 0.32, 0.28), "emoji": "🗿"},
        "sand": {"name": "SandDemon", "scale": 1.2, "color": (0.45, 0.38, 0.25), "emoji": "🏜️"},
        "sand demon": {"name": "SandDemon", "scale": 1.2, "color": (0.45, 0.38, 0.25), "emoji": "🏜️"},
        "field": {"name": "FieldDemon", "scale": 1.4, "color": (0.42, 0.38, 0.28), "emoji": "🌾"},
        "field demon": {"name": "FieldDemon", "scale": 1.4, "color": (0.42, 0.38, 0.28), "emoji": "🌾"},
        "fire": {"name": "FireDemon", "scale": 0.8, "color": (0.15, 0.08, 0.05), "emoji": "🔥"},
        "fire demon": {"name": "FireDemon", "scale": 0.8, "color": (0.15, 0.08, 0.05), "emoji": "🔥"},
        "wood": {"name": "WoodDemon", "scale": 2.0, "color": (0.28, 0.20, 0.12), "emoji": "🌳"},
        "wood demon": {"name": "WoodDemon", "scale": 2.0, "color": (0.28, 0.20, 0.12), "emoji": "🌳"},
        "marsh": {"name": "MarshDemon", "scale": 2.0, "color": (0.24, 0.28, 0.16), "emoji": "🌿"},
        "marsh demon": {"name": "MarshDemon", "scale": 2.0, "color": (0.24, 0.28, 0.16), "emoji": "🌿"},
        "water": {"name": "WaterDemon", "scale": 2.5, "color": (0.15, 0.28, 0.25), "emoji": "🌊"},
        "water demon": {"name": "WaterDemon", "scale": 2.5, "color": (0.15, 0.28, 0.25), "emoji": "🌊"},
        "lake": {"name": "WaterDemon", "scale": 2.5, "color": (0.15, 0.28, 0.25), "emoji": "🌊"},
        "lake demon": {"name": "WaterDemon", "scale": 2.5, "color": (0.15, 0.28, 0.25), "emoji": "🌊"},
        "bank": {"name": "BankDemon", "scale": 1.0, "color": (0.38, 0.42, 0.32), "emoji": "🐸"},
        "bank demon": {"name": "BankDemon", "scale": 1.0, "color": (0.38, 0.42, 0.32), "emoji": "🐸"},
        "cave": {"name": "CaveDemon", "scale": 1.2, "color": (0.28, 0.24, 0.20), "emoji": "🕷️"},
        "cave demon": {"name": "CaveDemon", "scale": 1.2, "color": (0.28, 0.24, 0.20), "emoji": "🕷️"},
        "wind": {"name": "WindDemon", "scale": 1.8, "color": (0.35, 0.38, 0.42), "emoji": "💨"},
        "wind demon": {"name": "WindDemon", "scale": 1.8, "color": (0.35, 0.38, 0.42), "emoji": "💨"},
        "lightning": {"name": "LightningDemon", "scale": 1.6, "color": (0.20, 0.25, 0.35), "emoji": "⚡"},
        "lightning demon": {"name": "LightningDemon", "scale": 1.6, "color": (0.20, 0.25, 0.35), "emoji": "⚡"},
        "snow": {"name": "SnowDemon", "scale": 1.3, "color": (0.85, 0.88, 0.92), "emoji": "❄️"},
        "snow demon": {"name": "SnowDemon", "scale": 1.3, "color": (0.85, 0.88, 0.92), "emoji": "❄️"},
        "ice": {"name": "SnowDemon", "scale": 1.3, "color": (0.85, 0.88, 0.92), "emoji": "❄️"},
        "ice demon": {"name": "SnowDemon", "scale": 1.3, "color": (0.85, 0.88, 0.92), "emoji": "❄️"},
        "leviathan": {"name": "LeviathanDemon", "scale": 4.0, "color": (0.08, 0.12, 0.20), "emoji": "🐋"},
        "leviathan demon": {"name": "LeviathanDemon", "scale": 4.0, "color": (0.08, 0.12, 0.20), "emoji": "🐋"},
        "clay": {"name": "ClayDemon", "scale": 1.6, "color": (0.38, 0.28, 0.20), "emoji": "🏺️"},
        "clay demon": {"name": "ClayDemon", "scale": 1.6, "color": (0.38, 0.28, 0.20), "emoji": "🏺️"},
        "mind": {"name": "MindDemon", "scale": 1.4, "color": (0.45, 0.42, 0.48), "emoji": "🧠"},
        "mind demon": {"name": "MindDemon", "scale": 1.4, "color": (0.45, 0.42, 0.48), "emoji": "🧠"},
        "mimic": {"name": "MimicDemon", "scale": 1.5, "color": (0.55, 0.52, 0.48), "emoji": "🎭"},
        "mimic demon": {"name": "MimicDemon", "scale": 1.5, "color": (0.55, 0.52, 0.48), "emoji": "🎭"},
        "queen": {"name": "DemonQueen", "scale": 2.5, "color": (0.20, 0.08, 0.12), "emoji": "👑"},
        "demon queen": {"name": "DemonQueen", "scale": 2.5, "color": (0.20, 0.08, 0.12), "emoji": "👑"},
        "alagai": {"name": "DemonQueen", "scale": 2.5, "color": (0.20, 0.08, 0.12), "emoji": "👑"},
    }

    demon_type_lower = demon_type.lower().strip()

    if demon_type_lower not in demon_types:
        unreal.log_error(f"Unknown demon type: '{demon_type}'")
        unreal.log(f"Available types: {', '.join(list(set(demon_types.keys())))}")
        return None

    demon_info = demon_types[demon_type_lower]

    unreal.log(f"\n🎯 Spawning {demon_info['emoji']} {demon_info['name']}...")
    unreal.log(f"   Position: {position}")
    unreal.log(f"   Scale: {scale}")

    # Spawn body
    body_scale = (
        scale * demon_info['scale'] * 0.6,
        scale * demon_info['scale'] * 0.4,
        scale * demon_info['scale'] * 0.8
    )

    actor = spawn_cube(
        f"{demon_info['name']}_Body",
        position,
        body_scale,
        demon_info['color']
    )

    if actor:
        unreal.log(f"✓ Successfully spawned {demon_info['name']} at {position}")
        return actor
    else:
        unreal.log_error(f"✗ Failed to spawn {demon_info['name']}")
        return None


# ============================================================
# MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":
    import sys

    # Check if called with arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            spawn_all_corelings()
        else:
            # Spawn specific demon
            demon_type = sys.argv[1]
            position = (0, 0, 0)
            scale = 1.0

            if len(sys.argv) > 2:
                try:
                    position = eval(sys.argv[2])
                except:
                    pass

            if len(sys.argv) > 3:
                try:
                    scale = float(sys.argv[3])
                except:
                    pass

            spawn_specific_demon(demon_type, position, scale)
    else:
        # Default: spawn all
        spawn_all_corelings()
