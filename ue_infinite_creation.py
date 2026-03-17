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
            # ============================================================
            # CORELINGS (The Painted Man / Demon Cycle) - HOLLYWOOD READY
            # 18 Canon Demon Types - Strict VFX Sheet Adherence
            # ============================================================

            # 1) ROCK DEMON - High Confidence
            "rock demon": {
                "components": ["enormous_body", "massive_shoulders", "thick_neck", "barrel_torso", "huge_forearms", "weighty_club_tail", "horned_mineral_armor"],
                "create": self._create_rock_demon_hollywood,
                "materials": ["basalt", "granite", "slate", "iron_rich_stone", "low_sheen", "dusty_edges"],
                "scale_class": "giant_terrestrial",
                "locomotion": "slow_unstoppable_siege_beast",
                "lock_level": "high_confidence"
            },

            # 2) STONE DEMON - Soft Lock
            "stone demon": {
                "components": ["compact_dense_body", "reduced_mass", "finer_armor_breakup", "quicker_reflexes"],
                "create": self._create_stone_demon_hollywood,
                "materials": ["dense_stone", "closer_grained_rock", "darker_compact_mineral"],
                "scale_class": "smaller_cousin_to_rock",
                "locomotion": "compact_quicker_maneuverable",
                "lock_level": "soft_lock"
            },

            # 3) SAND DEMON - High Confidence
            "sand demon": {
                "components": ["lean_desert_body", "long_limb_predator", "quadruped_gait", "upright_fight_mode", "flexible_spine_pelvis", "long_snout", "black_lidless_eyes", "curved_talons", "flexible_spiked_tail"],
                "create": self._create_sand_demon_hollywood,
                "materials": ["ochre", "dusty_yellow", "pale_sandstone", "dry_bone", "scorched_tan", "sand_camouflage_scales"],
                "scale_class": "human_height_near_human_scale",
                "locomotion": "quadruped_gallop_upright_slash",
                "lock_level": "high_confidence"
            },

            # 4) FIELD DEMON - Moderate Confidence
            "field demon": {
                "components": ["sleek_plains_runner", "feline_massing", "deep_chest", "elastic_torso", "long_hind_drive", "quadruped_form"],
                "create": self._create_field_demon_hollywood,
                "materials": ["dry_grassland_palettes", "tawny_demon_hide", "muted_gold_brown", "darker_structure_accents"],
                "scale_class": "larger_than_nightwolf_medium_large_pursuit",
                "locomotion": "quadruped_feline_plains_runner",
                "lock_level": "moderate_confidence"
            },

            # 5) FIRE/FLAME DEMON - High Confidence Form, Soft on Measurements
            "fire demon": {
                "components": ["smallest_common_breed", "low_fast_vicious", "compact_body", "dangerous_head_throat_weapon", "quadruped_agile", "demonfire_spitting_mechanism"],
                "create": self._create_fire_demon_hollywood,
                "materials": ["charcoal_hide", "ember_mouth", "glowing_eyes", "scorched_black_red_orange_internals", "cracked_cinder_accents"],
                "scale_class": "small_cat_sized",
                "locomotion": "quadrupedal_agile_darting",
                "lock_level": "high_confidence_form_soft_measurements"
            },
            "flame demon": {
                "components": ["smallest_common_breed", "low_fast_vicious", "compact_body", "dangerous_head_throat_weapon", "quadruped_agile", "demonfire_spitting_mechanism"],
                "create": self._create_fire_demon_hollywood,
                "materials": ["charcoal_hide", "ember_mouth", "glowing_eyes", "scorched_black_red_orange_internals", "cracked_cinder_accents"],
                "scale_class": "small_cat_sized",
                "locomotion": "quadrupedal_agile_darting",
                "lock_level": "high_confidence_form_soft_measurements"
            },

            # 6) WOOD DEMON - High Confidence
            "wood demon": {
                "components": ["arboreal_ambush_brute", "trunk_branch_massing", "broad_upper_body", "barklike_armor", "layered_wood_plates", "knots_ridges", "thorned_growth", "predatory_reveal"],
                "create": self._create_wood_demon_hollywood,
                "materials": ["bark_browns", "deadwood_gray", "dark_moss undertones", "sap_black_seams", "forest_camouflage"],
                "scale_class": "large_lesser_eight_feet_heavy",
                "locomotion": "climbing_dropping_swinging_forest_interstitial",
                "lock_level": "high_confidence"
            },

            # 7) MARSH DEMON - Moderate Confidence
            "marsh demon": {
                "components": ["wetland_adapted_wood_derivative", "swollen_amphibious", "blotched_green_brown_camouflage", "mud_coated_armor", "slime_residue", "reed_peat_texture", "spit_capable_mouth"],
                "create": self._create_marsh_demon_hollywood,
                "materials": ["swamp_green", "peat_brown", "algae_stain", "black_mud_gloss", "rotten_timber_undertones"],
                "scale_class": "large_lesser_boggy_read",
                "locomotion": "amphibious_trees_mud_shallow_water",
                "lock_level": "moderate_confidence"
            },

            # 8) WATER/LAKE DEMON - High Confidence
            "water demon": {
                "components": ["long_hydrodynamic_body", "tentacular_strike_profile", "scaled_primary_body", "tentacles_with_webbed_claws", "drowning_machine"],
                "create": self._create_water_demon_hollywood,
                "materials": ["black_water", "eel_dark_green", "drowned_bronze", "lake_silt_gray", "slick_wet_highlights"],
                "scale_class": "large_aquatic_predator",
                "locomotion": "rapid_submerged_propulsion_brief_surfacing",
                "lock_level": "high_confidence"
            },
            "lake demon": {
                "components": ["long_hydrodynamic_body", "tentacular_strike_profile", "scaled_primary_body", "tentacles_with_webbed_claws", "drowning_machine"],
                "create": self._create_water_demon_hollywood,
                "materials": ["black_water", "eel_dark_green", "drowned_bronze", "lake_silt_gray", "slick_wet_highlights"],
                "scale_class": "large_aquatic_predator",
                "locomotion": "rapid_submerged_propulsion_brief_surfacing",
                "lock_level": "high_confidence"
            },

            # 9) BANK DEMON - Moderate to High Confidence
            "bank demon": {
                "components": ["giant_frog_like_ambusher", "grotesquely_oversized_mouth", "primary_tongue_weapon", "explosive_hind_launch", "swallow_human_whole_aperture"],
                "create": self._create_bank_demon_hollywood,
                "materials": ["mud_green", "cold_olive", "river_black_mottling", "slick_wet_grays"],
                "scale_class": "swallow_human_whole",
                "locomotion": "squat_lurching_stillness_explosive_launch",
                "lock_level": "moderate_to_high"
            },

            # 10) CAVE DEMON - High Confidence
            "cave demon": {
                "components": ["low_fast_segmented_arachnid", "night_tunnel_horror", "eight_segmented_legs", "magic_dead_silk", "trap_based_hunter", "silk_producing_anatomy"],
                "create": self._create_cave_demon_hollywood,
                "materials": ["cave_black", "mineral_brown", "fungal_gray", "low_specular_chitin", "dusted_tunnel_residue"],
                "scale_class": "enclosed_space_terror",
                "locomotion": "rapid_multi_leg_scuttle_wall_ceiling_use",
                "lock_level": "high_confidence"
            },

            # 11) WIND DEMON - High Confidence
            "wind demon": {
                "components": ["huge_wingspan", "lean_central_body", "long_wing_finger_geometry", "vulnerable_thin_membranes", "graceful_flight", "awkward_ground", "runway_takeoff"],
                "create": self._create_wind_demon_hollywood,
                "materials": ["storm_black", "moon_silver_edges", "thin_membrane_translucency", "cold_sky_tones"],
                "scale_class": "largest_by_wingspan",
                "locomotion": "true_flyer_graceful_air_clumsy_ground",
                "lock_level": "high_confidence"
            },

            # 12) LIGHTNING DEMON - Soft Lock
            "lightning demon": {
                "components": ["wind_demon_chassis", "storm_associated_read", "electrical_phenomena", "aerial_harassment"],
                "create": self._create_lightning_demon_hollywood,
                "materials": ["dark_storm_blue_black", "charged_highlights", "ozone_white_flashes"],
                "scale_class": "aerial_class_family",
                "locomotion": "flying_wind_adjacent_storm_pass",
                "lock_level": "soft_lock"
            },

            # 13) SNOW DEMON - High Confidence (Replaces Ice Demon)
            "snow demon": {
                "components": ["large_cat_like_mountain_predator", "thick_white_fur", "visible_horns_spikes", "feline_massing", "powerful_quiet_ambush", "freezing_spit_mechanism"],
                "create": self._create_snow_demon_hollywood,
                "materials": ["dirty_white", "ice_gray", "pale_bone", "frost_blue_undertones", "storm_shadow_cools", "cold_weather_fur"],
                "scale_class": "large_apex_lesser_demon",
                "locomotion": "feline_mountain_avalanche_like",
                "lock_level": "high_confidence"
            },

            # 14) LEVIATHAN DEMON - Moderate Confidence
            "leviathan": {
                "components": ["gigantic_toothed_fish_demon", "not_whale_not_serpent", "ship_killing_mythic_size", "massive_predatory_head", "ship_killing_dentition", "deep_water_power"],
                "create": self._create_leviathan_demon_hollywood,
                "materials": ["abyss_black_blue", "drowned_iron", "oil_dark_wet_speculars", "deep_sea_green_shadowing"],
                "scale_class": "largest_demon_class_overall",
                "locomotion": "deep_water_power_devastating_momentum",
                "lock_level": "moderate_confidence"
            },
            "leviathan demon": {
                "components": ["gigantic_toothed_fish_demon", "not_whale_not_serpent", "ship_killing_mythic_size", "massive_predatory_head", "ship_killing_dentition", "deep_water_power"],
                "create": self._create_leviathan_demon_hollywood,
                "materials": ["abyss_black_blue", "drowned_iron", "oil_dark_wet_speculars", "deep_sea_green_shadowing"],
                "scale_class": "largest_demon_class_overall",
                "locomotion": "deep_water_power_devastating_momentum",
                "lock_level": "moderate_confidence"
            },

            # 15) CLAY DEMON - Soft Lock
            "clay demon": {
                "components": ["front_loaded_battering_form", "cranial_mass", "thick_neck", "shoulder_power", "reinforced_ram_skull", "head_is_weapon", "compact_front_loaded_torso"],
                "create": self._create_clay_demon_hollywood,
                "materials": ["packed_clay_red_brown", "sun_dried_ochre", "earthen_matte_finish", "cracked_compression_surfaces"],
                "scale_class": "medium_heavy_lesser_demon",
                "locomotion": "straightforward_breaching_oriented",
                "lock_level": "soft_lock"
            },

            # 16) MIND DEMON - Moderate Confidence
            "mind demon": {
                "components": ["physically_restrained_hierarchic", "unsettling_intelligence", "invasive_perception", "economical_self_possessed", "psychic_authority", "refined_body"],
                "create": self._create_mind_demon_hollywood,
                "materials": ["pallid_demon_tones", "dark_courtly_neutrals", "restrained_sheen", "subtle_alien_patterning"],
                "scale_class": "slighter_than_great_bruces",
                "locomotion": "economical_controlled_invasive",
                "lock_level": "moderate_confidence"
            },

            # 17) MIMIC DEMON - High Confidence Function, Soft Form
            "mimic demon": {
                "components": ["metamorphic_weapons_platform", "adaptive_anatomy", "transitional_surfaces", "mutable_tissue_armor", "selective_hardening", "tentacular_offense", "rock_demon_defense"],
                "create": self._create_mimic_demon_hollywood,
                "materials": ["neutral_mutable_base", "chameleon_adaptive", "transitional_tissue"],
                "scale_class": "variable_by_definition",
                "locomotion": "adaptive_with_borrowed_forms",
                "lock_level": "high_confidence_function_soft_form"
            },

            # 18) DEMON QUEEN / ALAGAI'TING KA - Moderate Confidence
            "demon queen": {
                "components": ["brood_sovereign", "huge_reproductive_central_mass", "psychic_dominance", "venomous_armored_tail", "ancient_armored_body", "core_bound"],
                "create": self._create_demon_queen_hollywood,
                "materials": ["subterranean_black_red", "deep_chitinous_bronze", "venom_dark_sheen", "egg_chamber_pallor"],
                "scale_class": "queen_class_core_bound",
                "locomotion": "limited_brood_stationary",
                "lock_level": "moderate_confidence"
            },
            "alagai": {
                "components": ["brood_sovereign", "huge_reproductive_central_mass", "psychic_dominance", "venomous_armored_tail", "ancient_armored_body", "core_bound"],
                "create": self._create_demon_queen_hollywood,
                "materials": ["subterranean_black_red", "deep_chitinous_bronze", "venom_dark_sheen", "egg_chamber_pallor"],
                "scale_class": "queen_class_core_bound",
                "locomotion": "limited_brood_stationary",
                "lock_level": "moderate_confidence"
            },

            # Generic Coreling for non-specific requests
            "coreling": {
                "components": ["body", "limbs", "magic_aura"],
                "create": self._create_generic_coreling_hollywood,
                "materials": ["demon_skin", "magic", "coreling_base"]
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
            # Corelings (The Painted Man / Demon Cycle) - All 18 Canon Types
            "rock demon", "stone demon", "sand demon", "field demon",
            "fire demon", "flame demon", "wood demon", "marsh demon",
            "water demon", "lake demon", "bank demon", "cave demon",
            "wind demon", "lightning demon", "snow demon", "leviathan",
            "clay demon", "mind demon", "mimic demon", "demon queen", "alagai",
            "forest demon", "ice demon", "coreling", "demon",
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
    # CORELING CREATION (The Painted Man / Demon Cycle) - HOLLYWOOD READY
    # 18 Canon Demon Types - Strict VFX Sheet Adherence
    # ============================================================

    def _create_rock_demon_hollywood(self, parsed: dict) -> dict:
        """
        ROCK DEMON (High Confidence)
        - Enormous upright siege brute
        - Massive shoulders, barrel torso, thick neck
        - Weighty club tail with crushing force
        - Horned mineral armor plates
        - Slow unstoppable locomotion
        - Materials: basalt, granite, slate, iron-rich stone, low sheen, dusty edges
        - Scale: Giant terrestrial (8-12 feet tall)
        """
        name = parsed.get("name") or "RockDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 3.0

        unreal.log("🪨 Creating ROCK DEMON (Hollywood Ready)...")

        created_actors = []
        base_color = (0.25, 0.22, 0.18)  # Basalt dark gray
        accent_color = (0.35, 0.32, 0.28)  # Granite lighter
        horn_color = (0.15, 0.12, 0.10)  # Iron-rich dark stone

        # ENORMOUS BODY - Upright siege posture
        body_scale = (scale * 1.2, scale * 0.9, scale * 2.0)
        body_pos = (position[0], position[1], position[2] + scale * 1.0)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, base_color)
        created_actors.append(body["actor"])

        # MASSIVE SHOULDERS - Boulders of muscle and stone
        for side in [-1, 1]:
            shoulder_scale = (scale * 0.7, scale * 0.6, scale * 0.8)
            shoulder_pos = (position[0] + side * scale * 0.9, position[1], position[2] + scale * 1.7)
            shoulder = self._create_composite_cube(
                f"{name}_Shoulder_{'L' if side < 0 else 'R'}", shoulder_pos, shoulder_scale, accent_color
            )
            created_actors.append(shoulder["actor"])

        # THICK NECK - Column of solid rock
        neck_scale = (scale * 0.5, scale * 0.5, scale * 0.4)
        neck_pos = (position[0], position[1], position[2] + scale * 2.1)
        neck = self._create_composite_cube(f"{name}_Neck", neck_pos, neck_scale, base_color)
        created_actors.append(neck["actor"])

        # BARREL TORSO ARMOR - Overlapping stone plates
        for i in range(6):
            plate_scale = (scale * 1.3, scale * 0.15, scale * 0.4)
            plate_pos = (
                position[0],
                position[1] + scale * 0.95,
                position[2] + scale * 0.8 + i * scale * 0.25
            )
            plate = self._create_composite_cube(
                f"{name}_ArmorPlate_{i}", plate_pos, plate_scale, accent_color
            )
            created_actors.append(plate["actor"])

        # HEAD - Blocky, horned cranium
        head_scale = (scale * 0.6, scale * 0.7, scale * 0.5)
        head_pos = (position[0], position[1], position[2] + scale * 2.5)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, base_color)
        created_actors.append(head["actor"])

        # HORNS - Multiple mineral crowns
        for i in range(4):
            horn_scale = (scale * 0.12, scale * 0.12, scale * 0.4)
            angle = (math.pi * i) / 4
            horn_pos = (
                head_pos[0] + scale * 0.35 * math.cos(angle),
                head_pos[1] + scale * 0.35 * math.sin(angle),
                head_pos[2] + scale * 0.2
            )
            horn = self._create_composite_cube(
                f"{name}_Horn_{i}", horn_pos, horn_scale, horn_color
            )
            created_actors.append(horn["actor"])

        # GLOWING EYES - Deep in stone sockets
        eye_scale = (scale * 0.1, scale * 0.1, scale * 0.1)
        eye_pos_l = (head_pos[0] - scale * 0.2, head_pos[1] - scale * 0.35, head_pos[2])
        eye_pos_r = (head_pos[0] + scale * 0.2, head_pos[1] - scale * 0.35, head_pos[2])
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (1, 0.3, 0.1))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (1, 0.3, 0.1))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # HUGE FOREARMS - Crushing strength
        for side in [-1, 1]:
            forearm_scale = (scale * 0.4, scale * 0.5, scale * 1.0)
            forearm_pos = (position[0] + side * scale * 1.3, position[1], position[2] + scale * 1.3)
            forearm = self._create_composite_cube(
                f"{name}_Forearm_{'L' if side < 0 else 'R'}", forearm_pos, forearm_scale, base_color
            )
            created_actors.append(forearm["actor"])

        # MASSIVE HANDS - Battering ram fists
        for side in [-1, 1]:
            hand_scale = (scale * 0.5, scale * 0.4, scale * 0.4)
            hand_pos = (position[0] + side * scale * 1.3, position[1] - scale * 0.5, position[2] + scale * 0.6)
            hand = self._create_composite_cube(
                f"{name}_Hand_{'L' if side < 0 else 'R'}", hand_pos, hand_scale, accent_color
            )
            created_actors.append(hand["actor"])

        # THICK LEGS - Pillar supports
        for side in [-1, 1]:
            leg_scale = (scale * 0.5, scale * 0.6, scale * 1.2)
            leg_pos = (position[0] + side * scale * 0.5, position[1], position[2])
            leg = self._create_composite_cube(
                f"{name}_Leg_{'L' if side < 0 else 'R'}", leg_pos, leg_scale, base_color
            )
            created_actors.append(leg["actor"])

        # WEIGHTY CLUB TAIL - Crushing siege weapon
        tail_base_scale = (scale * 0.5, scale * 0.5, scale * 1.0)
        tail_base_pos = (position[0], position[1] + scale * 1.0, position[2] - scale * 0.5)
        tail_base = self._create_composite_cube(f"{name}_Tail_Base", tail_base_pos, tail_base_scale, base_color)
        created_actors.append(tail_base["actor"])

        # Tail club - massive stone mace
        club_scale = (scale * 0.8, scale * 0.8, scale * 0.8)
        club_pos = (position[0], position[1] + scale * 1.5, position[2] - scale * 1.3)
        club = self._create_composite_cube(f"{name}_Tail_Club", club_pos, club_scale, accent_color)
        created_actors.append(club["actor"])

        # Spikes on tail club
        for i in range(6):
            spike_scale = (scale * 0.15, scale * 0.15, scale * 0.3)
            angle = (2 * math.pi * i) / 6
            spike_pos = (
                club_pos[0] + scale * 0.5 * math.cos(angle),
                club_pos[1] + scale * 0.5 * math.sin(angle),
                club_pos[2]
            )
            spike = self._create_composite_cube(
                f"{name}_ClubSpike_{i}", spike_pos, spike_scale, horn_color
            )
            created_actors.append(spike["actor"])

        unreal.log(f"🪨 ROCK DEMON created with {len(created_actors)} components (Hollywood Ready)")
        return {
            "message": f"Created {name} (Rock Demon - Hollywood Ready)",
            "name": name,
            "type": "rock demon",
            "actors": created_actors
        }

    def _create_stone_demon_hollywood(self, parsed: dict) -> dict:
        """
        STONE DEMON (Soft Lock - Rock Demon's Smaller Cousin)
        - Compact, quicker version of Rock Demon
        - Smaller but still heavily armored
        - Faster locomotion than Rock Demon
        - Same mineral aesthetics but streamlined
        - Materials: limestone, sandstone, weathered stone
        - Scale: Large terrestrial (5-7 feet tall)
        """
        name = parsed.get("name") or "StoneDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.8

        unreal.log("🗿 Creating STONE DEMON (Hollywood Ready)...")

        created_actors = []
        base_color = (0.45, 0.42, 0.38)  # Limestone light gray
        armor_color = (0.55, 0.52, 0.48)  # Sandstone accent
        dark_color = (0.30, 0.28, 0.25)  # Weathered stone

        # COMPACT BODY - Streamlined siege posture
        body_scale = (scale * 0.8, scale * 0.6, scale * 1.4)
        body_pos = (position[0], position[1], position[2] + scale * 0.7)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, base_color)
        created_actors.append(body["actor"])

        # Compact shoulders
        for side in [-1, 1]:
            shoulder_scale = (scale * 0.4, scale * 0.35, scale * 0.5)
            shoulder_pos = (position[0] + side * scale * 0.55, position[1], position[2] + scale * 1.1)
            shoulder = self._create_composite_cube(
                f"{name}_Shoulder_{'L' if side < 0 else 'R'}", shoulder_pos, shoulder_scale, armor_color
            )
            created_actors.append(shoulder["actor"])

        # Streamlined neck
        neck_scale = (scale * 0.3, scale * 0.3, scale * 0.25)
        neck_pos = (position[0], position[1], position[2] + scale * 1.5)
        neck = self._create_composite_cube(f"{name}_Neck", neck_pos, neck_scale, base_color)
        created_actors.append(neck["actor"])

        # Overlapping armor plates (fewer than Rock Demon)
        for i in range(4):
            plate_scale = (scale * 0.9, scale * 0.1, scale * 0.3)
            plate_pos = (
                position[0],
                position[1] + scale * 0.65,
                position[2] + scale * 0.5 + i * scale * 0.22
            )
            plate = self._create_composite_cube(
                f"{name}_ArmorPlate_{i}", plate_pos, plate_scale, armor_color
            )
            created_actors.append(plate["actor"])

        # Head - Smaller but still horned
        head_scale = (scale * 0.4, scale * 0.45, scale * 0.35)
        head_pos = (position[0], position[1], position[2] + scale * 1.8)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, base_color)
        created_actors.append(head["actor"])

        # Smaller horns (2 main horns)
        for side in [-1, 1]:
            horn_scale = (scale * 0.1, scale * 0.1, scale * 0.3)
            horn_pos = (head_pos[0] + side * scale * 0.2, head_pos[1], head_pos[2] + scale * 0.15)
            horn = self._create_composite_cube(
                f"{name}_Horn_{'L' if side < 0 else 'R'}", horn_pos, horn_scale, dark_color
            )
            created_actors.append(horn["actor"])

        # Glowing eyes
        eye_scale = (scale * 0.07, scale * 0.07, scale * 0.07)
        eye_pos_l = (head_pos[0] - scale * 0.12, head_pos[1] - scale * 0.25, head_pos[2])
        eye_pos_r = (head_pos[0] + scale * 0.12, head_pos[1] - scale * 0.25, head_pos[2])
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (1, 0.3, 0.1))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (1, 0.3, 0.1))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Streamlined forearms
        for side in [-1, 1]:
            forearm_scale = (scale * 0.25, scale * 0.3, scale * 0.7)
            forearm_pos = (position[0] + side * scale * 0.75, position[1], position[2] + scale * 0.9)
            forearm = self._create_composite_cube(
                f"{name}_Forearm_{'L' if side < 0 else 'R'}", forearm_pos, forearm_scale, base_color
            )
            created_actors.append(forearm["actor"])

        # Compact hands
        for side in [-1, 1]:
            hand_scale = (scale * 0.3, scale * 0.25, scale * 0.25)
            hand_pos = (position[0] + side * scale * 0.75, position[1] - scale * 0.35, position[2] + scale * 0.4)
            hand = self._create_composite_cube(
                f"{name}_Hand_{'L' if side < 0 else 'R'}", hand_pos, hand_scale, armor_color
            )
            created_actors.append(hand["actor"])

        # Quick legs
        for side in [-1, 1]:
            leg_scale = (scale * 0.3, scale * 0.35, scale * 0.8)
            leg_pos = (position[0] + side * scale * 0.3, position[1], position[2])
            leg = self._create_composite_cube(
                f"{name}_Leg_{'L' if side < 0 else 'R'}", leg_pos, leg_scale, base_color
            )
            created_actors.append(leg["actor"])

        # Smaller tail club
        tail_scale = (scale * 0.3, scale * 0.3, scale * 0.6)
        tail_pos = (position[0], position[1] + scale * 0.6, position[2] - scale * 0.3)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, base_color)
        created_actors.append(tail["actor"])

        # Mini club
        club_scale = (scale * 0.4, scale * 0.4, scale * 0.4)
        club_pos = (position[0], position[1] + scale * 0.85, position[2] - scale * 0.8)
        club = self._create_composite_cube(f"{name}_Tail_Club", club_pos, club_scale, armor_color)
        created_actors.append(club["actor"])

        unreal.log(f"🗿 STONE DEMON created with {len(created_actors)} components (Hollywood Ready)")
        return {
            "message": f"Created {name} (Stone Demon - Hollywood Ready)",
            "name": name,
            "type": "stone demon",
            "actors": created_actors
        }

    def _create_fire_demon_hollywood(self, parsed: dict) -> dict:
        """
        FIRE DEMON (High Confidence Form, Soft Measurements)
        - SMALLEST demon - quadrupedal
        - Low profile, agile
        - Charred obsidian skin with magma cracks
        - Internal glow showing through cracks
        - Materials: charred obsidian, magma cracks, internal glow
        - Scale: Small quadrupedal (2-3 feet long)
        - Locomotion: Quick, darting movement
        """
        name = parsed.get("name") or "FireDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 0.8

        unreal.log("🔥 Creating FIRE DEMON (Hollywood Ready - Smallest, Quadrupedal)...")

        created_actors = []
        obsidian_color = (0.08, 0.05, 0.04)  # Charred obsidian
        magma_color = (1, 0.4, 0.05)  # Magma orange
        glow_color = (1, 0.9, 0.3)  # Internal yellow-white glow

        # LOW PROFILE BODY - Quadrupedal stance
        body_scale = (scale * 0.5, scale * 0.35, scale * 0.9)
        body_pos = (position[0], position[1], position[2] + scale * 0.4)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, obsidian_color)
        created_actors.append(body["actor"])

        # Magma cracks in body (glowing lines)
        for i in range(8):
            crack_scale = (scale * 0.15, scale * 0.02, scale * 0.3)
            crack_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.3,
                position[1] + scale * 0.36,
                position[2] + scale * 0.3 + (i // 2) * scale * 0.15
            )
            crack = self._create_composite_cube(
                f"{name}_MagmaCrack_{i}", crack_pos, crack_scale, magma_color
            )
            created_actors.append(crack["actor"])

        # Head - Angular, reptilian
        head_scale = (scale * 0.25, scale * 0.35, scale * 0.2)
        head_pos = (position[0], position[1] - scale * 0.15, position[2] + scale * 0.5)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, obsidian_color)
        created_actors.append(head["actor"])

        # Snout
        snout_scale = (scale * 0.15, scale * 0.2, scale * 0.12)
        snout_pos = (position[0], position[1] - scale * 0.45, position[2] + scale * 0.45)
        snout = self._create_composite_cube(f"{name}_Snout", snout_pos, snout_scale, obsidian_color)
        created_actors.append(snout["actor"])

        # Glowing eyes - Intense orange
        eye_scale = (scale * 0.05, scale * 0.05, scale * 0.05)
        eye_pos_l = (head_pos[0] - scale * 0.08, head_pos[1] - scale * 0.35, head_pos[2])
        eye_pos_r = (head_pos[0] + scale * 0.08, head_pos[1] - scale * 0.35, head_pos[2])
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, magma_color)
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, magma_color)
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Horns - Small obsidian spikes
        for side in [-1, 1]:
            horn_scale = (scale * 0.04, scale * 0.04, scale * 0.12)
            horn_pos = (head_pos[0] + side * scale * 0.1, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.12)
            horn = self._create_composite_cube(
                f"{name}_Horn_{'L' if side < 0 else 'R'}", horn_pos, horn_scale, obsidian_color
            )
            created_actors.append(horn["actor"])

        # Quadrupedal legs - 4 agile legs
        leg_positions = [
            (-1, -1),  # Front left
            (1, -1),   # Front right
            (-1, 1),   # Back left
            (1, 1)     # Back right
        ]

        for i, (side_x, side_y) in enumerate(leg_positions):
            leg_scale = (scale * 0.08, scale * 0.08, scale * 0.35)
            leg_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.2,
                position[2] + scale * 0.25
            )
            leg = self._create_composite_cube(
                f"{name}_Leg_{i}", leg_pos, leg_scale, obsidian_color
            )
            created_actors.append(leg["actor"])

            # Magma crack on each leg
            crack_scale = (scale * 0.02, scale * 0.02, scale * 0.2)
            crack_pos = (
                leg_pos[0],
                leg_pos[1] + scale * 0.08,
                leg_pos[2]
            )
            crack = self._create_composite_cube(
                f"{name}_LegCrack_{i}", crack_pos, crack_scale, magma_color
            )
            created_actors.append(crack["actor"])

        # Tail - Thin, tapered
        tail_scale = (scale * 0.06, scale * 0.25, scale * 0.06)
        tail_pos = (position[0], position[1] + scale * 0.5, position[2] + scale * 0.35)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, obsidian_color)
        created_actors.append(tail["actor"])

        # Flame tuft at tail end
        flame_scale = (scale * 0.1, scale * 0.08, scale * 0.1)
        flame_pos = (position[0], position[1] + scale * 0.65, position[2] + scale * 0.35)
        flame = self._create_composite_cube(f"{name}_TailFlame", flame_pos, flame_scale, magma_color)
        created_actors.append(flame["actor"])

        # Spine ridge - Magma glow
        for i in range(5):
            spine_scale = (scale * 0.06, scale * 0.06, scale * 0.08)
            spine_pos = (
                position[0],
                position[1] - scale * 0.15 + i * scale * 0.2,
                position[2] + scale * 0.75
            )
            spine = self._create_composite_cube(
                f"{name}_SpineRidge_{i}", spine_pos, spine_scale, magma_color
            )
            created_actors.append(spine["actor"])

        unreal.log(f"🔥 FIRE DEMON created with {len(created_actors)} components (Hollywood Ready - Smallest)")
        return {
            "message": f"Created {name} (Fire Demon - Hollywood Ready - Smallest Quadrupedal)",
            "name": name,
            "type": "fire demon",
            "actors": created_actors
        }

    def _create_water_demon_hollywood(self, parsed: dict) -> dict:
        """
        WATER/LAKE DEMON (High Confidence)
        - Tentacled drowning machine
        - Massive aquatic predator
        - Multiple tentacles with gripping suckers
        - Amphibious - can drag victims underwater
        - Materials: slick scales, bioluminescent markings, sucker pads
        - Scale: Large aquatic (8-15 feet long with tentacles)
        - Locomotion: Swimming, tentacled dragging
        """
        name = parsed.get("name") or "WaterDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.5

        unreal.log("🌊 Creating WATER/LAKE DEMON (Hollywood Ready - Tentacled Drowning Machine)...")

        created_actors = []
        body_color = (0.08, 0.35, 0.42)  # Deep aquatic blue-green
        scale_color = (0.12, 0.42, 0.5)  # Lighter scales
        bio_color = (0.3, 0.8, 0.7)  # Bioluminescent green
        sucker_color = (0.2, 0.5, 0.55)  # Sucker pads

        # MASSIVE BODY - Streamlined aquatic form
        body_scale = (scale * 0.9, scale * 0.7, scale * 1.8)
        body_pos = (position[0], position[1], position[2] + scale * 0.9)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, body_color)
        created_actors.append(body["actor"])

        # Scale patterns on body
        for i in range(12):
            scale_piece_scale = (scale * 0.2, scale * 0.03, scale * 0.15)
            scale_piece_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.3,
                position[1] + scale * 0.72,
                position[2] + scale * 0.4 + (i // 3) * scale * 0.35
            )
            scale_piece = self._create_composite_cube(
                f"{name}_Scale_{i}", scale_piece_pos, scale_piece_scale, scale_color
            )
            created_actors.append(scale_piece["actor"])

        # Bioluminescent stripes
        for i in range(6):
            bio_scale = (scale * 0.08, scale * 0.02, scale * 0.4)
            bio_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.4,
                position[1] + scale * 0.72,
                position[2] + scale * 0.5 + (i // 2) * scale * 0.4
            )
            bio = self._create_composite_cube(
                f"{name}_BioStripe_{i}", bio_pos, bio_scale, bio_color
            )
            created_actors.append(bio["actor"])

        # Head - Aquatic predator
        head_scale = (scale * 0.5, scale * 0.6, scale * 0.4)
        head_pos = (position[0], position[1] - scale * 0.35, position[2] + scale * 1.0)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, body_color)
        created_actors.append(head["actor"])

        # Jaw line
        jaw_scale = (scale * 0.4, scale * 0.15, scale * 0.15)
        jaw_pos = (position[0], position[1] - scale * 0.7, position[2] + scale * 0.85)
        jaw = self._create_composite_cube(f"{name}_Jaw", jaw_pos, jaw_scale, body_color)
        created_actors.append(jaw["actor"])

        # Glowing eyes - Bioluminescent
        eye_scale = (scale * 0.12, scale * 0.1, scale * 0.12)
        eye_pos_l = (head_pos[0] - scale * 0.18, head_pos[1] - scale * 0.55, head_pos[2] + scale * 0.05)
        eye_pos_r = (head_pos[0] + scale * 0.18, head_pos[1] - scale * 0.55, head_pos[2] + scale * 0.05)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, bio_color)
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, bio_color)
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # MASSIVE TENTACLES - 8 main tentacles
        for i in range(8):
            angle = (2 * math.pi * i) / 8
            # Base of tentacle
            tentacle_base_scale = (scale * 0.25, scale * 0.25, scale * 0.3)
            tentacle_base_pos = (
                position[0] + scale * 0.5 * math.cos(angle),
                position[1] + scale * 0.5 * math.sin(angle),
                position[2] + scale * 0.7
            )
            tentacle_base = self._create_composite_cube(
                f"{name}_Tentacle{i}_Base", tentacle_base_pos, tentacle_base_scale, body_color
            )
            created_actors.append(tentacle_base["actor"])

            # Tentacle segments (4 segments per tentacle)
            for j in range(4):
                segment_scale = (scale * (0.22 - j * 0.03), scale * 0.2, scale * 0.25)
                segment_pos = (
                    position[0] + (scale * 0.6 + j * scale * 0.35) * math.cos(angle),
                    position[1] + (scale * 0.6 + j * scale * 0.35) * math.sin(angle),
                    position[2] + scale * 0.7 - j * scale * 0.15
                )
                segment = self._create_composite_cube(
                    f"{name}_Tentacle{i}_Segment{j}", segment_pos, segment_scale, body_color
                )
                created_actors.append(segment["actor"])

                # Sucker pads on each segment
                for k in range(3):
                    sucker_angle = (2 * math.pi * k) / 3
                    sucker_scale = (scale * 0.06, scale * 0.02, scale * 0.06)
                    sucker_pos = (
                        segment_pos[0] + scale * 0.15 * math.cos(sucker_angle),
                        segment_pos[1] + scale * 0.15 * math.sin(sucker_angle),
                        segment_pos[2]
                    )
                    sucker = self._create_composite_cube(
                        f"{name}_Tentacle{i}_Sucker{j}_{k}", sucker_pos, sucker_scale, sucker_color
                    )
                    created_actors.append(sucker["actor"])

        # Tail - Powerful aquatic propulsion
        tail_scale = (scale * 0.3, scale * 0.9, scale * 0.15)
        tail_pos = (position[0], position[1] + scale * 1.0, position[2] + scale * 0.6)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, body_color)
        created_actors.append(tail["actor"])

        # Tail fin
        fin_scale = (scale * 0.6, scale * 0.05, scale * 0.3)
        fin_pos = (position[0], position[1] + scale * 1.4, position[2] + scale * 0.55)
        fin = self._create_composite_cube(f"{name}_TailFin", fin_pos, fin_scale, scale_color)
        created_actors.append(fin["actor"])

        unreal.log(f"🌊 WATER/LAKE DEMON created with {len(created_actors)} components (Hollywood Ready - Tentacled)")
        return {
            "message": f"Created {name} (Water/Lake Demon - Hollywood Ready - Tentacled Drowning Machine)",
            "name": name,
            "type": "water demon",
            "actors": created_actors
        }

    def _create_wood_demon_hollywood(self, parsed: dict) -> dict:
        """
        WOOD DEMON (High Confidence)
        - Arboreal bark armor
        - Vine-wrapped features
        - Tree-like camouflage
        - Root-based locomotion
        - Materials: rough bark, twisted vines, moss patches, leaf camouflage
        - Scale: Large terrestrial (7-10 feet tall)
        - Locomotion: Root-dragging forest stalker
        """
        name = parsed.get("name") or "WoodDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.2

        unreal.log("🌲 Creating WOOD DEMON (Hollywood Ready - Arboreal Bark Armor)...")

        created_actors = []
        bark_color = (0.28, 0.22, 0.15)  # Dark brown bark
        vine_color = (0.35, 0.4, 0.18)  # Greenish vines
        moss_color = (0.25, 0.35, 0.2)  # Moss green
        leaf_color = (0.18, 0.5, 0.12)  # Forest green

        # TALL BODY - Tree-like trunk
        body_scale = (scale * 0.7, scale * 0.6, scale * 2.0)
        body_pos = (position[0], position[1], position[2] + scale * 1.0)
        body = self._create_composite_cube(f"{name}_Trunk", body_pos, body_scale, bark_color)
        created_actors.append(body["actor"])

        # Bark armor plates - overlapping protection
        for i in range(10):
            plate_scale = (scale * 0.75, scale * 0.1, scale * 0.35)
            plate_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.05,
                position[1] + scale * 0.62,
                position[2] + scale * 0.3 + i * scale * 0.18
            )
            plate = self._create_composite_cube(
                f"{name}_BarkPlate_{i}", plate_pos, plate_scale, bark_color
            )
            created_actors.append(plate["actor"])

        # Moss patches on bark
        for i in range(8):
            moss_scale = (scale * 0.15, scale * 0.03, scale * 0.2)
            moss_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.4,
                position[1] + scale * 0.63,
                position[2] + scale * 0.5 + (i // 2) * scale * 0.35
            )
            moss = self._create_composite_cube(
                f"{name}_Moss_{i}", moss_pos, moss_scale, moss_color
            )
            created_actors.append(moss["actor"])

        # Head - Knotted wood cranium
        head_scale = (scale * 0.4, scale * 0.45, scale * 0.35)
        head_pos = (position[0], position[1], position[2] + scale * 2.2)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, bark_color)
        created_actors.append(head["actor"])

        # Root horns - Twisted wood crown
        for i in range(4):
            horn_scale = (scale * 0.08, scale * 0.08, scale * 0.3)
            angle = (math.pi * i) / 3
            horn_pos = (
                head_pos[0] + scale * 0.25 * math.cos(angle),
                head_pos[1] + scale * 0.25 * math.sin(angle),
                head_pos[2] + scale * 0.2
            )
            horn = self._create_composite_cube(
                f"{name}_RootHorn_{i}", horn_pos, horn_scale, bark_color
            )
            created_actors.append(horn["actor"])

        # Glowing green eyes
        eye_scale = (scale * 0.08, scale * 0.06, scale * 0.08)
        eye_pos_l = (head_pos[0] - scale * 0.12, head_pos[1] - scale * 0.25, head_pos[2])
        eye_pos_r = (head_pos[0] + scale * 0.12, head_pos[1] - scale * 0.25, head_pos[2])
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (0.4, 0.9, 0.3))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (0.4, 0.9, 0.3))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Vine-wrapped arms - Branch-like limbs
        for side in [-1, 1]:
            # Main branch arm
            for i in range(4):
                vine_scale = (scale * 0.12, scale * 0.25, scale * 0.1)
                vine_pos = (
                    position[0] + side * (scale * 0.45 + i * scale * 0.1),
                    position[1],
                    position[2] + scale * 1.5 - i * scale * 0.2
                )
                vine = self._create_composite_cube(
                    f"{name}_VineArm_{'L' if side < 0 else 'R'}_{i}", vine_pos, vine_scale, vine_color
                )
                created_actors.append(vine["actor"])

            # Twig fingers
            for j in range(3):
                twig_scale = (scale * 0.04, scale * 0.12, scale * 0.04)
                twig_pos = (
                    position[0] + side * scale * 0.8,
                    position[1] + (j - 1) * scale * 0.08,
                    position[2] + scale * 0.8
                )
                twig = self._create_composite_cube(
                    f"{name}_Twig_{'L' if side < 0 else 'R'}_{j}", twig_pos, twig_scale, vine_color
                )
                created_actors.append(twig["actor"])

        # Root-like legs - Spreading root base
        for i in range(5):
            root_scale = (scale * 0.18, scale * 0.18, scale * 0.8)
            angle = (2 * math.pi * i) / 5
            root_pos = (
                position[0] + scale * 0.35 * math.cos(angle),
                position[1] + scale * 0.35 * math.sin(angle),
                position[2] - scale * 0.3
            )
            root = self._create_composite_cube(
                f"{name}_RootLeg_{i}", root_pos, root_scale, bark_color
            )
            created_actors.append(root["actor"])

        # Leaf camouflage - Scattered foliage
        for i in range(12):
            leaf_scale = (scale * 0.12, scale * 0.02, scale * 0.1)
            leaf_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.35,
                position[1] + ((i // 4) % 3 - 1) * scale * 0.4,
                position[2] + scale * 1.0 + (i // 12) * scale * 0.5
            )
            leaf = self._create_composite_cube(
                f"{name}_Leaf_{i}", leaf_pos, leaf_scale, leaf_color
            )
            created_actors.append(leaf["actor"])

        # Vine wraps around body
        for i in range(6):
            vine_wrap_scale = (scale * 0.06, scale * 0.72, scale * 0.06)
            vine_wrap_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.4,
                position[1],
                position[2] + scale * 0.5 + i * scale * 0.25
            )
            vine_wrap = self._create_composite_cube(
                f"{name}_VineWrap_{i}", vine_wrap_pos, vine_wrap_scale, vine_color
            )
            created_actors.append(vine_wrap["actor"])

        unreal.log(f"🌲 WOOD DEMON created with {len(created_actors)} components (Hollywood Ready - Arboreal)")
        return {
            "message": f"Created {name} (Wood Demon - Hollywood Ready - Arboreal Bark Armor)",
            "name": name,
            "type": "wood demon",
            "actors": created_actors
        }

    def _create_mind_demon_hollywood(self, parsed: dict) -> dict:
        """
        MIND DEMON (Moderate Confidence)
        - Psychic intelligence manifested
        - Small, slender humanoid form
        - Powerful psychic abilities
        - Mental manipulation and control
        - Materials: pale ethereal skin, purple psychic glow, lavender energy tendrils
        - Scale: Small humanoid (4-5 feet tall)
        - Locomotion: Floating/hovering psychic form
        """
        name = parsed.get("name") or "MindDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.0

        unreal.log("🧠 Creating MIND DEMON (Hollywood Ready - Psychic Intelligence)...")

        created_actors = []
        skin_color = (0.88, 0.85, 0.82)  # Pale ethereal skin
        purple_glow = (0.7, 0.35, 0.9)  # Psychic purple
        lavender_color = (0.8, 0.5, 0.95)  # Lavender energy
        eye_color = (0.85, 0.4, 1)  # Glowing purple eyes

        # SLENDER BODY - Frail but powerful
        body_scale = (scale * 0.3, scale * 0.18, scale * 0.8)
        body_pos = (position[0], position[1], position[2] + scale * 0.4)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, skin_color)
        created_actors.append(body["actor"])

        # LARGE CRANIUM - Enlarged head for psychic brain
        head_scale = (scale * 0.22, scale * 0.22, scale * 0.28)
        head_pos = (position[0], position[1], position[2] + scale * 0.85)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, skin_color)
        created_actors.append(head["actor"])

        # Brain veins - Psychic energy pathways
        for i in range(6):
            vein_scale = (scale * 0.02, scale * 0.15, scale * 0.02)
            vein_pos = (
                head_pos[0] + ((i % 2) - 0.5) * scale * 0.1,
                head_pos[1] + scale * 0.22,
                head_pos[2] - scale * 0.05 + (i // 2) * scale * 0.12
            )
            vein = self._create_composite_cube(
                f"{name}_PsychicVein_{i}", vein_pos, vein_scale, purple_glow
            )
            created_actors.append(vein["actor"])

        # Glowing purple eyes - Psychic power
        eye_scale = (scale * 0.06, scale * 0.05, scale * 0.06)
        eye_pos_l = (head_pos[0] - scale * 0.06, head_pos[1] - scale * 0.11, head_pos[2] + scale * 0.08)
        eye_pos_r = (head_pos[0] + scale * 0.06, head_pos[1] - scale * 0.11, head_pos[2] + scale * 0.08)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, eye_color)
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, eye_color)
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # PSYCHIC AURA - Multiple glowing rings
        for i in range(4):
            aura_scale = (scale * (0.35 + i * 0.12), scale * 0.02, scale * (0.35 + i * 0.12))
            aura_pos = (position[0], position[1], position[2] + scale * 0.85 + i * scale * 0.04)
            aura = self._create_composite_cube(
                f"{name}_PsychicAura_{i}", aura_pos, aura_scale, purple_glow
            )
            created_actors.append(aura["actor"])

        # Slender arms
        for side in [-1, 1]:
            arm_scale = (scale * 0.06, scale * 0.06, scale * 0.4)
            arm_pos = (position[0] + side * scale * 0.2, position[1], position[2] + scale * 0.35)
            arm = self._create_composite_cube(
                f"{name}_Arm_{'L' if side < 0 else 'R'}", arm_pos, arm_scale, skin_color
            )
            created_actors.append(arm["actor"])

        # Psychic hands - glowing fingertips
        for side in [-1, 1]:
            for i in range(3):
                finger_scale = (scale * 0.025, scale * 0.08, scale * 0.025)
                finger_pos = (
                    position[0] + side * scale * 0.2 + (i - 1) * scale * 0.025,
                    position[1] - scale * 0.12,
                    position[2] + scale * 0.2
                )
                finger = self._create_composite_cube(
                    f"{name}_PsychicFinger_{'L' if side < 0 else 'R'}_{i}", finger_pos, finger_scale, lavender_color
                )
                created_actors.append(finger["actor"])

        # PSYCHIC TENDRILS - Floating energy arms
        for i in range(8):
            tendril_scale = (scale * 0.04, scale * 0.25, scale * 0.04)
            angle = (2 * math.pi * i) / 8
            tendril_pos = (
                position[0] + scale * 0.5 * math.cos(angle),
                position[1] + scale * 0.5 * math.sin(angle),
                position[2] + scale * 0.5
            )
            tendril = self._create_composite_cube(
                f"{name}_PsychicTendril_{i}", tendril_pos, tendril_scale, lavender_color
            )
            created_actors.append(tendril["actor"])

        # Floating particles - Psychic energy
        for i in range(12):
            particle_scale = (scale * 0.04, scale * 0.04, scale * 0.04)
            angle = (2 * math.pi * i) / 12
            particle_pos = (
                position[0] + scale * 0.6 * math.cos(angle),
                position[1] + scale * 0.6 * math.sin(angle),
                position[2] + scale * 0.3 + (i % 4) * scale * 0.15
            )
            particle = self._create_composite_cube(
                f"{name}_PsychicParticle_{i}", particle_pos, particle_scale, purple_glow
            )
            created_actors.append(particle["actor"])

        # Hover effect - No visible legs, just psychic energy
        hover_scale = (scale * 0.35, scale * 0.05, scale * 0.35)
        hover_pos = (position[0], position[1], position[2])
        hover = self._create_composite_cube(f"{name}_HoverField", hover_pos, hover_scale, lavender_color)
        created_actors.append(hover["actor"])

        unreal.log(f"🧠 MIND DEMON created with {len(created_actors)} components (Hollywood Ready - Psychic)")
        return {
            "message": f"Created {name} (Mind Demon - Hollywood Ready - Psychic Intelligence)",
            "name": name,
            "type": "mind demon",
            "actors": created_actors
        }

    def _create_clay_demon_hollywood(self, parsed: dict) -> dict:
        """
        CLAY DEMON (Soft Lock - Battering Ram Specialist)
        - Massive siege form
        - Battering ram tactics
        - Amorphous mud body that can reshape
        - Cracked earth texture
        - Materials: drying clay, cracked mud, earth tones
        - Scale: Large terrestrial (6-9 feet tall)
        - Locomotion: Slow unstoppable advance
        """
        name = parsed.get("name") or "ClayDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("🏺 Creating CLAY DEMON (Hollywood Ready - Battering Ram Specialist)...")

        created_actors = []
        clay_color = (0.42, 0.35, 0.28)  # Brown clay
        crack_color = (0.28, 0.22, 0.18)  # Darker cracks
        dry_color = (0.52, 0.45, 0.35)  # Drying clay

        # MASSIVE BODY - Battering ram form
        body_scale = (scale * 1.0, scale * 0.9, scale * 1.8)
        body_pos = (position[0], position[1], position[2] + scale * 0.9)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, clay_color)
        created_actors.append(body["actor"])

        # Cracked mud texture all over body
        for i in range(15):
            crack_scale = (scale * 0.02, scale * 0.25, scale * 0.02)
            crack_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.35,
                position[1] + scale * 0.92,
                position[2] + scale * 0.3 + (i // 3) * scale * 0.3
            )
            crack = self._create_composite_cube(
                f"{name}_MudCrack_{i}", crack_pos, crack_scale, crack_color
            )
            created_actors.append(crack["actor"])

        # Wide shoulders for ramming
        for side in [-1, 1]:
            shoulder_scale = (scale * 0.5, scale * 0.45, scale * 0.6)
            shoulder_pos = (position[0] + side * scale * 0.7, position[1], position[2] + scale * 1.3)
            shoulder = self._create_composite_cube(
                f"{name}_Shoulder_{'L' if side < 0 else 'R'}", shoulder_pos, shoulder_scale, clay_color
            )
            created_actors.append(shoulder["actor"])

        # Head - Blunt battering ram shape
        head_scale = (scale * 0.5, scale * 0.6, scale * 0.35)
        head_pos = (position[0], position[1], position[2] + scale * 1.9)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, clay_color)
        created_actors.append(head["actor"])

        # Thick neck
        neck_scale = (scale * 0.35, scale * 0.35, scale * 0.3)
        neck_pos = (position[0], position[1], position[2] + scale * 1.6)
        neck = self._create_composite_cube(f"{name}_Neck", neck_pos, neck_scale, clay_color)
        created_actors.append(neck["actor"])

        # Earth-tone eyes
        eye_scale = (scale * 0.1, scale * 0.1, scale * 0.1)
        eye_pos_l = (head_pos[0] - scale * 0.15, head_pos[1] - scale * 0.3, head_pos[2])
        eye_pos_r = (head_pos[0] + scale * 0.15, head_pos[1] - scale * 0.3, head_pos[2])
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (0.7, 0.5, 0.3))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (0.7, 0.5, 0.3))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Massive ramming arms
        for side in [-1, 1]:
            for i in range(4):
                arm_scale = (scale * (0.25 - i * 0.02), scale * 0.25, scale * 0.25)
                arm_pos = (
                    position[0] + side * (scale * 0.6 + i * scale * 0.12),
                    position[1],
                    position[2] + scale * 1.2 - i * scale * 0.15
                )
                arm = self._create_composite_cube(
                    f"{name}_Arm_{'L' if side < 0 else 'R'}_{i}", arm_pos, arm_scale, clay_color
                )
                created_actors.append(arm["actor"])

        # Huge battering fists
        for side in [-1, 1]:
            fist_scale = (scale * 0.35, scale * 0.3, scale * 0.3)
            fist_pos = (position[0] + side * scale * 1.0, position[1] - scale * 0.35, position[2] + scale * 0.75)
            fist = self._create_composite_cube(
                f"{name}_Fist_{'L' if side < 0 else 'R'}", fist_pos, fist_scale, dry_color
            )
            created_actors.append(fist["actor"])

        # Thick pillar legs
        for side in [-1, 1]:
            leg_scale = (scale * 0.35, scale * 0.4, scale * 1.0)
            leg_pos = (position[0] + side * scale * 0.35, position[1], position[2])
            leg = self._create_composite_cube(
                f"{name}_Leg_{'L' if side < 0 else 'R'}", leg_pos, leg_scale, clay_color
            )
            created_actors.append(leg["actor"])

        # Wide feet for stability
        for side in [-1, 1]:
            foot_scale = (scale * 0.4, scale * 0.15, scale * 0.35)
            foot_pos = (position[0] + side * scale * 0.35, position[1], position[2] - scale * 0.55)
            foot = self._create_composite_cube(
                f"{name}_Foot_{'L' if side < 0 else 'R'}", foot_pos, foot_scale, dry_color
            )
            created_actors.append(foot["actor"])

        # Dripping mud details
        for i in range(8):
            drip_scale = (scale * 0.08, scale * 0.08, scale * 0.12)
            drip_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.5,
                position[1] + scale * 0.95,
                position[2] + scale * 0.2 + (i // 2) * scale * 0.4
            )
            drip = self._create_composite_cube(
                f"{name}_MudDrip_{i}", drip_pos, drip_scale, clay_color
            )
            created_actors.append(drip["actor"])

        unreal.log(f"🏺 CLAY DEMON created with {len(created_actors)} components (Hollywood Ready - Battering Ram)")
        return {
            "message": f"Created {name} (Clay Demon - Hollywood Ready - Battering Ram Specialist)",
            "name": name,
            "type": "clay demon",
            "actors": created_actors
        }

    def _create_wind_demon_hollywood(self, parsed: dict) -> dict:
        """
        WIND DEMON (High Confidence)
        - Flying with membrane wings
        - Bat-like leather wings
        - Vulnerable wing membranes (weakness)
        - Aerial predator
        - Materials: dark leather, translucent membranes, clawed limbs
        - Scale: Medium aerial (6-8 foot wingspan)
        - Locomotion: Flying aerial hunter
        """
        name = parsed.get("name") or "WindDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.3

        unreal.log("💨 Creating WIND DEMON (Hollywood Ready - Vulnerable Membranes)...")

        created_actors = []
        leather_color = (0.28, 0.24, 0.2)  # Dark leather
        membrane_color = (0.35, 0.32, 0.28)  # Translucent membrane
        claw_color = (0.2, 0.17, 0.15)  # Dark claws
        eye_color = (0.9, 0.3, 0.15)  # Glowing red eyes

        # LEAN BODY - Lightweight for flight
        body_scale = (scale * 0.35, scale * 0.25, scale * 1.0)
        body_pos = (position[0], position[1], position[2] + scale * 0.5)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, leather_color)
        created_actors.append(body["actor"])

        # BAT-LIKE HEAD
        head_scale = (scale * 0.2, scale * 0.25, scale * 0.22)
        head_pos = (position[0], position[1], position[2] + scale * 1.05)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, leather_color)
        created_actors.append(head["actor"])

        # Large ears
        for side in [-1, 1]:
            ear_scale = (scale * 0.12, scale * 0.15, scale * 0.08)
            ear_pos = (head_pos[0] + side * scale * 0.12, head_pos[1] - scale * 0.2, head_pos[2] + scale * 0.08)
            ear = self._create_composite_cube(
                f"{name}_Ear_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, leather_color
            )
            created_actors.append(ear["actor"])

        # Glowing red eyes
        eye_scale = (scale * 0.05, scale * 0.05, scale * 0.05)
        eye_pos_l = (head_pos[0] - scale * 0.06, head_pos[1] - scale * 0.24, head_pos[2] + scale * 0.02)
        eye_pos_r = (head_pos[0] + scale * 0.06, head_pos[1] - scale * 0.24, head_pos[2] + scale * 0.02)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, eye_color)
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, eye_color)
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # MASSIVE LEATHER WINGS - Vulnerable membranes
        for side in [-1, 1]:
            # Wing arm structure
            for i in range(3):
                wing_segment_scale = (scale * (1.5 - i * 0.3), scale * 0.04, scale * 0.15)
                wing_segment_pos = (
                    position[0] + side * (scale * 0.5 + i * scale * 0.4),
                    position[1] - scale * 0.1 + i * scale * 0.05,
                    position[2] + scale * 0.7 + i * scale * 0.1
                )
                wing_segment = self._create_composite_cube(
                    f"{name}_WingArm_{'L' if side < 0 else 'R'}_{i}", wing_segment_pos, wing_segment_scale, leather_color
                )
                created_actors.append(wing_segment["actor"])

            # Wing membrane - VULNERABLE
            membrane_scale = (scale * 1.8, scale * 0.02, scale * 1.2)
            membrane_pos = (
                position[0] + side * scale * 1.2,
                position[1] - scale * 0.1,
                position[2] + scale * 0.8
            )
            membrane = self._create_composite_cube(
                f"{name}_WingMembrane_{'L' if side < 0 else 'R'}", membrane_pos, membrane_scale, membrane_color
            )
            created_actors.append(membrane["actor"])

        # Clawed arms
        for side in [-1, 1]:
            arm_scale = (scale * 0.08, scale * 0.2, scale * 0.08)
            arm_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.45)
            arm = self._create_composite_cube(
                f"{name}_Arm_{'L' if side < 0 else 'R'}", arm_pos, arm_scale, leather_color
            )
            created_actors.append(arm["actor"])

            # Claws
            claw_scale = (scale * 0.06, scale * 0.1, scale * 0.06)
            claw_pos = (position[0] + side * scale * 0.35, position[1] - scale * 0.2, position[2] + scale * 0.35)
            claw = self._create_composite_cube(
                f"{name}_Claw_{'L' if side < 0 else 'R'}", claw_pos, claw_scale, claw_color
            )
            created_actors.append(claw["actor"])

        # Clawed legs
        for side in [-1, 1]:
            leg_scale = (scale * 0.08, scale * 0.25, scale * 0.08)
            leg_pos = (position[0] + side * scale * 0.2, position[1], position[2] + scale * 0.15)
            leg = self._create_composite_cube(
                f"{name}_Leg_{'L' if side < 0 else 'R'}", leg_pos, leg_scale, leather_color
            )
            created_actors.append(leg["actor"])

            # Foot claws
            foot_scale = (scale * 0.1, scale * 0.08, scale * 0.05)
            foot_pos = (position[0] + side * scale * 0.2, position[1] - scale * 0.15, position[2])
            foot = self._create_composite_cube(
                f"{name}_Foot_{'L' if side < 0 else 'R'}", foot_pos, foot_scale, claw_color
            )
            created_actors.append(foot["actor"])

        # Tail
        tail_scale = (scale * 0.05, scale * 0.3, scale * 0.05)
        tail_pos = (position[0], position[1] + scale * 0.25, position[2] + scale * 0.4)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, leather_color)
        created_actors.append(tail["actor"])

        unreal.log(f"💨 WIND DEMON created with {len(created_actors)} components (Hollywood Ready - Aerial)")
        return {
            "message": f"Created {name} (Wind Demon - Hollywood Ready - Vulnerable Membranes)",
            "name": name,
            "type": "wind demon",
            "actors": created_actors
        }

    def _create_lightning_demon_hollywood(self, parsed: dict) -> dict:
        """
        LIGHTNING DEMON (Soft Lock - Wind Demon Variant)
        - Like Wind Demon but with electrical abilities
        - Sparks and arcs around body
        - Faster, more erratic movement
        - Materials: dark ozone-burned skin, electric blue glow, crackling energy
        - Scale: Medium aerial (6-8 foot wingspan)
        - Locomotion: Erratic electric flight
        """
        name = parsed.get("name") or "LightningDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.3

        unreal.log("⚡ Creating LIGHTNING DEMON (Hollywood Ready - Wind Demon Variant)...")

        created_actors = []
        ozone_color = (0.25, 0.28, 0.3)  # Ozone-burned skin
        electric_color = (0.6, 0.8, 1)  # Electric blue
        spark_color = (0.9, 0.95, 1)  # Bright sparks
        eye_color = (0.5, 0.7, 1)  # Electric eyes

        # Body similar to Wind Demon but darker
        body_scale = (scale * 0.35, scale * 0.25, scale * 1.0)
        body_pos = (position[0], position[1], position[2] + scale * 0.5)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, ozone_color)
        created_actors.append(body["actor"])

        # Head
        head_scale = (scale * 0.2, scale * 0.25, scale * 0.22)
        head_pos = (position[0], position[1], position[2] + scale * 1.05)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, ozone_color)
        created_actors.append(head["actor"])

        # Electric eyes
        eye_scale = (scale * 0.05, scale * 0.05, scale * 0.05)
        eye_pos_l = (head_pos[0] - scale * 0.06, head_pos[1] - scale * 0.24, head_pos[2] + scale * 0.02)
        eye_pos_r = (head_pos[0] + scale * 0.06, head_pos[1] - scale * 0.24, head_pos[2] + scale * 0.02)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, eye_color)
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, eye_color)
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # ELECTRIC WINGS
        for side in [-1, 1]:
            # Wing frame
            for i in range(3):
                wing_segment_scale = (scale * (1.5 - i * 0.3), scale * 0.04, scale * 0.15)
                wing_segment_pos = (
                    position[0] + side * (scale * 0.5 + i * scale * 0.4),
                    position[1] - scale * 0.1 + i * scale * 0.05,
                    position[2] + scale * 0.7 + i * scale * 0.1
                )
                wing_segment = self._create_composite_cube(
                    f"{name}_WingArm_{'L' if side < 0 else 'R'}_{i}", wing_segment_pos, wing_segment_scale, ozone_color
                )
                created_actors.append(wing_segment["actor"])

            # Electric membrane
            membrane_scale = (scale * 1.8, scale * 0.02, scale * 1.2)
            membrane_pos = (
                position[0] + side * scale * 1.2,
                position[1] - scale * 0.1,
                position[2] + scale * 0.8
            )
            membrane = self._create_composite_cube(
                f"{name}_WingMembrane_{'L' if side < 0 else 'R'}", membrane_pos, membrane_scale, electric_color
            )
            created_actors.append(membrane["actor"])

        # Limbs
        for side in [-1, 1]:
            arm_scale = (scale * 0.08, scale * 0.2, scale * 0.08)
            arm_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.45)
            arm = self._create_composite_cube(
                f"{name}_Arm_{'L' if side < 0 else 'R'}", arm_pos, arm_scale, ozone_color
            )
            created_actors.append(arm["actor"])

            leg_scale = (scale * 0.08, scale * 0.25, scale * 0.08)
            leg_pos = (position[0] + side * scale * 0.2, position[1], position[2] + scale * 0.15)
            leg = self._create_composite_cube(
                f"{name}_Leg_{'L' if side < 0 else 'R'}", leg_pos, leg_scale, ozone_color
            )
            created_actors.append(leg["actor"])

        # ELECTRIC ARCS - Crackling energy around body
        for i in range(12):
            arc_scale = (scale * 0.03, scale * 0.2, scale * 0.03)
            angle = (2 * math.pi * i) / 12
            arc_pos = (
                position[0] + scale * 0.5 * math.cos(angle),
                position[1] + scale * 0.5 * math.sin(angle),
                position[2] + scale * 0.5 + (i % 3) * scale * 0.2
            )
            arc = self._create_composite_cube(
                f"{name}_ElectricArc_{i}", arc_pos, arc_scale, electric_color
            )
            created_actors.append(arc["actor"])

        # Sparks
        for i in range(16):
            spark_scale = (scale * 0.04, scale * 0.04, scale * 0.04)
            angle = (2 * math.pi * i) / 16
            spark_pos = (
                position[0] + scale * 0.6 * math.cos(angle),
                position[1] + scale * 0.6 * math.sin(angle),
                position[2] + scale * 0.4 + (i % 4) * scale * 0.15
            )
            spark = self._create_composite_cube(
                f"{name}_Spark_{i}", spark_pos, spark_scale, spark_color
            )
            created_actors.append(spark["actor"])

        # Tail
        tail_scale = (scale * 0.05, scale * 0.3, scale * 0.05)
        tail_pos = (position[0], position[1] + scale * 0.25, position[2] + scale * 0.4)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, ozone_color)
        created_actors.append(tail["actor"])

        unreal.log(f"⚡ LIGHTNING DEMON created with {len(created_actors)} components (Hollywood Ready - Electric)")
        return {
            "message": f"Created {name} (Lightning Demon - Hollywood Ready - Wind Variant)",
            "name": name,
            "type": "lightning demon",
            "actors": created_actors
        }

    def _create_marsh_demon_hollywood(self, parsed: dict) -> dict:
        """
        MARSH DEMON (Moderate Confidence - Wetland Wood Demon Variant)
        - Swamp-dwelling wood demon
        - Moss and algae covered
        - Wet, slimy bark texture
        - Amphibious capabilities
        - Materials: waterlogged wood, slimy moss, algae green, murky brown
        - Scale: Large terrestrial (6-8 feet tall)
        - Locomotion: Root-dragging swamp stalker
        """
        name = parsed.get("name") or "MarshDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("🌿 Creating MARSH DEMON (Hollywood Ready - Wetland Wood Demon)...")

        created_actors = []
        wood_color = (0.28, 0.26, 0.18)  # Waterlogged wood
        moss_color = (0.25, 0.38, 0.2)  # Slimy moss
        algae_color = (0.35, 0.42, 0.15)  # Algae green
        slime_color = (0.42, 0.48, 0.35)  # Murky slime

        # WATERLOGGED BODY
        body_scale = (scale * 0.65, scale * 0.55, scale * 1.8)
        body_pos = (position[0], position[1], position[2] + scale * 0.9)
        body = self._create_composite_cube(f"{name}_Trunk", body_pos, body_scale, wood_color)
        created_actors.append(body["actor"])

        # Wet moss covering
        for i in range(12):
            moss_scale = (scale * 0.6, scale * 0.06, scale * 0.3)
            moss_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.05,
                position[1] + ((i % 3) - 1) * scale * 0.28,
                position[2] + scale * 0.4 + (i // 3) * scale * 0.4
            )
            moss = self._create_composite_cube(
                f"{name}_WetMoss_{i}", moss_pos, moss_scale, moss_color
            )
            created_actors.append(moss["actor"])

        # Algae drips
        for i in range(8):
            algae_scale = (scale * 0.08, scale * 0.12, scale * 0.08)
            algae_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.35,
                position[1] + scale * 0.58,
                position[2] + scale * 0.3 + (i // 2) * scale * 0.5
            )
            algae = self._create_composite_cube(
                f"{name}_Algae_{i}", algae_pos, algae_scale, algae_color
            )
            created_actors.append(algae["actor"])

        # Head
        head_scale = (scale * 0.38, scale * 0.4, scale * 0.32)
        head_pos = (position[0], position[1], position[2] + scale * 1.95)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, wood_color)
        created_actors.append(head["actor"])

        # Root horns with slime
        for i in range(4):
            horn_scale = (scale * 0.07, scale * 0.07, scale * 0.25)
            angle = (math.pi * i) / 3
            horn_pos = (
                head_pos[0] + scale * 0.22 * math.cos(angle),
                head_pos[1] + scale * 0.22 * math.sin(angle),
                head_pos[2] + scale * 0.15
            )
            horn = self._create_composite_cube(
                f"{name}_RootHorn_{i}", horn_pos, horn_scale, wood_color
            )
            created_actors.append(horn["actor"])

        # Glowing green eyes
        eye_scale = (scale * 0.07, scale * 0.06, scale * 0.07)
        eye_pos_l = (head_pos[0] - scale * 0.1, head_pos[1] - scale * 0.28, head_pos[2] + scale * 0.02)
        eye_pos_r = (head_pos[0] + scale * 0.1, head_pos[1] - scale * 0.28, head_pos[2] + scale * 0.02)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, (0.4, 0.8, 0.3))
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, (0.4, 0.8, 0.3))
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Vine arms with slime
        for side in [-1, 1]:
            for i in range(4):
                vine_scale = (scale * 0.1, scale * 0.22, scale * 0.08)
                vine_pos = (
                    position[0] + side * (scale * 0.4 + i * scale * 0.1),
                    position[1],
                    position[2] + scale * 1.3 - i * scale * 0.18
                )
                vine = self._create_composite_cube(
                    f"{name}_VineArm_{'L' if side < 0 else 'R'}_{i}", vine_pos, vine_scale, moss_color
                )
                created_actors.append(vine["actor"])

        # Root legs adapted for swamp
        for i in range(5):
            root_scale = (scale * 0.16, scale * 0.16, scale * 0.7)
            angle = (2 * math.pi * i) / 5
            root_pos = (
                position[0] + scale * 0.32 * math.cos(angle),
                position[1] + scale * 0.32 * math.sin(angle),
                position[2] - scale * 0.25
            )
            root = self._create_composite_cube(
                f"{name}_SwampRoot_{i}", root_pos, root_scale, wood_color
            )
            created_actors.append(root["actor"])

        unreal.log(f"🌿 MARSH DEMON created with {len(created_actors)} components (Hollywood Ready - Wetland)")
        return {
            "message": f"Created {name} (Marsh Demon - Hollywood Ready - Wetland Wood)",
            "name": name,
            "type": "marsh demon",
            "actors": created_actors
        }

    def _create_bank_demon_hollywood(self, parsed: dict) -> dict:
        """
        BANK DEMON (Moderate-High Confidence)
        - Frog-like water's edge predator
        - Long sticky tongue for catching prey
        - Amphibious, can be in or near water
        - Ambush predator
        - Materials: slick skin, mottled green-brown, long tongue, bulging eyes
        - Scale: Medium quadrupedal (3-5 feet long)
        - Locomotion: Hopping/crawling water's edge hunter
        """
        name = parsed.get("name") or "BankDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.0

        unreal.log("🐸 Creating BANK DEMON (Hollywood Ready - Frog-like Tongue Attacker)...")

        created_actors = []
        skin_color = (0.35, 0.42, 0.28)  # Mottled green-brown
        belly_color = (0.55, 0.58, 0.45)  # Lighter belly
        tongue_color = (0.65, 0.35, 0.4)  # Pinkish tongue
        eye_color = (0.85, 0.9, 0.4)  # Bulging yellow-green eyes

        # CROUCHING BODY - Frog-like posture
        body_scale = (scale * 0.5, scale * 0.45, scale * 0.5)
        body_pos = (position[0], position[1], position[2] + scale * 0.35)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, skin_color)
        created_actors.append(body["actor"])

        # Belly patch
        belly_scale = (scale * 0.4, scale * 0.08, scale * 0.35)
        belly_pos = (position[0], position[1] + scale * 0.25, position[2] + scale * 0.35)
        belly = self._create_composite_cube(f"{name}_Belly", belly_pos, belly_pos, belly_color)
        created_actors.append(belly["actor"])

        # FROG HEAD
        head_scale = (scale * 0.3, scale * 0.28, scale * 0.2)
        head_pos = (position[0], position[1] - scale * 0.15, position[2] + scale * 0.55)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, skin_color)
        created_actors.append(head["actor"])

        # Bulging eyes
        eye_scale = (scale * 0.1, scale * 0.08, scale * 0.1)
        eye_pos_l = (head_pos[0] - scale * 0.12, head_pos[1] - scale * 0.25, head_pos[2] + scale * 0.05)
        eye_pos_r = (head_pos[0] + scale * 0.12, head_pos[1] - scale * 0.25, head_pos[2] + scale * 0.05)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, eye_color)
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, eye_color)
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Wide mouth
        mouth_scale = (scale * 0.2, scale * 0.06, scale * 0.12)
        mouth_pos = (position[0], position[1] - scale * 0.35, position[2] + scale * 0.48)
        mouth = self._create_composite_cube(f"{name}_Mouth", mouth_pos, mouth_scale, belly_color)
        created_actors.append(mouth["actor"])

        # LONG TONGUE - Extended for attack
        tongue_scale = (scale * 0.08, scale * 0.4, scale * 0.06)
        tongue_pos = (position[0], position[1] - scale * 0.55, position[2] + scale * 0.45)
        tongue = self._create_composite_cube(f"{name}_Tongue", tongue_pos, tongue_pos, tongue_color)
        created_actors.append(tongue["actor"])

        # Tongue tip - sticky pad
        tip_scale = (scale * 0.1, scale * 0.08, scale * 0.08)
        tip_pos = (position[0], position[1] - scale * 0.75, position[2] + scale * 0.45)
        tip = self._create_composite_cube(f"{name}_TongueTip", tip_pos, tip_scale, tongue_color)
        created_actors.append(tip["actor"])

        # Powerful hind legs
        for side in [-1, 1]:
            thigh_scale = (scale * 0.15, scale * 0.15, scale * 0.25)
            thigh_pos = (position[0] + side * scale * 0.2, position[1], position[2] + scale * 0.2)
            thigh = self._create_composite_cube(
                f"{name}_Thigh_{'L' if side < 0 else 'R'}", thigh_pos, thigh_scale, skin_color
            )
            created_actors.append(thigh["actor"])

            # Lower leg
            lower_scale = (scale * 0.1, scale * 0.12, scale * 0.2)
            lower_pos = (position[0] + side * scale * 0.2, position[1], position[2])
            lower = self._create_composite_cube(
                f"{name}_LowerLeg_{'L' if side < 0 else 'R'}", lower_pos, lower_scale, skin_color
            )
            created_actors.append(lower["actor"])

            # Webbed foot
            foot_scale = (scale * 0.15, scale * 0.06, scale * 0.08)
            foot_pos = (position[0] + side * scale * 0.2, position[1] - scale * 0.08, position[2] - scale * 0.05)
            foot = self._create_composite_cube(
                f"{name}_Foot_{'L' if side < 0 else 'R'}", foot_pos, foot_scale, belly_color
            )
            created_actors.append(foot["actor"])

        # Smaller front arms
        for side in [-1, 1]:
            arm_scale = (scale * 0.08, scale * 0.15, scale * 0.08)
            arm_pos = (position[0] + side * scale * 0.25, position[1], position[2] + scale * 0.35)
            arm = self._create_composite_cube(
                f"{name}_Arm_{'L' if side < 0 else 'R'}", arm_pos, arm_scale, skin_color
            )
            created_actors.append(arm["actor"])

        unreal.log(f"🐸 BANK DEMON created with {len(created_actors)} components (Hollywood Ready - Frog Predator)")
        return {
            "message": f"Created {name} (Bank Demon - Hollywood Ready - Frog-like Tongue Attacker)",
            "name": name,
            "type": "bank demon",
            "actors": created_actors
        }

    def _create_cave_demon_hollywood(self, parsed: dict) -> dict:
        """
        CAVE DEMON (High Confidence)
        - Arachnid silk trapper
        - Spider-like with multiple limbs
        - Web-spinning and trapping
        - Dark-dwelling predator
        - Materials: chitinous armor, silk webs, multiple eyes, venomous fangs
        - Scale: Large arachnid (4-6 feet across)
        - Locomotion: Scuttling cave predator
        """
        name = parsed.get("name") or "CaveDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.2

        unreal.log("🕷️ Creating CAVE DEMON (Hollywood Ready - Arachnid Silk Trapper)...")

        created_actors = []
        chitin_color = (0.25, 0.22, 0.18)  # Dark chitin
        silk_color = (0.92, 0.9, 0.88)  # Silk webs
        eye_color = (0.85, 0.75, 0.5)  // Multiple eyes
        venom_color = (0.7, 0.85, 0.3)  # Venomous green

        # ARACHNID BODY - Spider-like abdomen
        abdomen_scale = (scale * 0.5, scale * 0.4, scale * 0.6)
        abdomen_pos = (position[0], position[1] + scale * 0.3, position[2] + scale * 0.4)
        abdomen = self._create_composite_cube(f"{name}_Abdomen", abdomen_pos, abdomen_scale, chitin_color)
        created_actors.append(abdomen["actor"])

        # Silk spinneret
        spinneret_scale = (scale * 0.12, scale * 0.15, scale * 0.1)
        spinneret_pos = (position[0], position[1] + scale * 0.55, position[2] + scale * 0.35)
        spinneret = self._create_composite_cube(f"{name}_Spinneret", spinneret_pos, spinneret_scale, chitin_color)
        created_actors.append(spinneret["actor"])

        # Cephalothorax
        thorax_scale = (scale * 0.35, scale * 0.3, scale * 0.3)
        thorax_pos = (position[0], position[1] - scale * 0.15, position[2] + scale * 0.5)
        thorax = self._create_composite_cube(f"{name}_Thorax", thorax_pos, thorax_scale, chitin_color)
        created_actors.append(thorax["actor"])

        # Spider head
        head_scale = (scale * 0.25, scale * 0.25, scale * 0.2)
        head_pos = (position[0], position[1] - scale * 0.35, position[2] + scale * 0.55)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, chitin_color)
        created_actors.append(head["actor"])

        # MULTIPLE EYES - 8 eyes
        eye_positions = [
            (-0.08, -0.28, 0.08),  # Front left upper
            (0.08, -0.28, 0.08),   # Front right upper
            (-0.1, -0.32, 0.05),   # Side left upper
            (0.1, -0.32, 0.05),    # Side right upper
            (-0.06, -0.3, 0.02),   # Front left lower
            (0.06, -0.3, 0.02),    # Front right lower
            (-0.08, -0.34, 0),     # Side left lower
            (0.08, -0.34, 0)       # Side right lower
        ]

        for i, (off_x, off_y, off_z) in enumerate(eye_positions):
            eye_scale = (scale * 0.04, scale * 0.04, scale * 0.04)
            eye_pos = (head_pos[0] + off_x * scale, head_pos[1] + off_y * scale, head_pos[2] + off_z * scale)
            eye = self._create_composite_cube(f"{name}_Eye_{i}", eye_pos, eye_scale, eye_color)
            created_actors.append(eye["actor"])

        # Venomous fangs
        for side in [-1, 1]:
            fang_scale = (scale * 0.04, scale * 0.12, scale * 0.04)
            fang_pos = (head_pos[0] + side * scale * 0.08, head_pos[1] - scale * 0.4, head_pos[2] + scale * 0.02)
            fang = self._create_composite_cube(
                f"{name}_Fang_{'L' if side < 0 else 'R'}", fang_pos, fang_scale, venom_color
            )
            created_actors.append(fang["actor"])

        # EIGHT LEGS - Spider limbs
        for i in range(8):
            side = 1 if i % 2 == 0 else -1
            forward = 1 if i < 4 else -1

            # Upper leg segment
            upper_scale = (scale * 0.06, scale * 0.25, scale * 0.06)
            upper_pos = (
                position[0] + side * scale * 0.2,
                position[1] + forward * scale * 0.15,
                position[2] + scale * 0.4
            )
            upper = self._create_composite_cube(
                f"{name}_Leg{i}_Upper", upper_pos, upper_scale, chitin_color
            )
            created_actors.append(upper["actor"])

            # Lower leg segment
            lower_scale = (scale * 0.05, scale * 0.3, scale * 0.05)
            lower_pos = (
                position[0] + side * scale * 0.35,
                position[1] + forward * scale * 0.35,
                position[2] + scale * 0.25
            )
            lower = self._create_composite_cube(
                f"{name}_Leg{i}_Lower", lower_pos, lower_scale, chitin_color
            )
            created_actors.append(lower["actor"])

        # Silk webs around the demon
        for i in range(6):
            web_scale = (scale * 0.4, scale * 0.01, scale * 0.4)
            angle = (2 * math.pi * i) / 6
            web_pos = (
                position[0] + scale * 0.8 * math.cos(angle),
                position[1] + scale * 0.8 * math.sin(angle),
                position[2] + scale * 0.3
            )
            web = self._create_composite_cube(
                f"{name}_SilkWeb_{i}", web_pos, web_scale, silk_color
            )
            created_actors.append(web["actor"])

        unreal.log(f"🕷️ CAVE DEMON created with {len(created_actors)} components (Hollywood Ready - Arachnid)")
        return {
            "message": f"Created {name} (Cave Demon - Hollywood Ready - Silk Trapper)",
            "name": name,
            "type": "cave demon",
            "actors": created_actors
        }

    def _create_leviathan_hollywood(self, parsed: dict) -> dict:
        """
        LEVIATHAN (Moderate Confidence)
        - Giant fish-like sea monster
        - Ship-killer of the deep
        - Massive aquatic predator
        - Materials: scales, fins, immense jaws, deep ocean colors
        - Scale: GIGANTIC aquatic (30-50 feet long)
        - Locomotion: Powerful swimming
        """
        name = parsed.get("name") or "Leviathan"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 6.0

        unreal.log("🐋 Creating LEVIATHAN (Hollywood Ready - Giant Ship-Killer)...")

        created_actors = []
        scale_color = (0.15, 0.25, 0.32)  # Deep ocean blue
        belly_color = (0.25, 0.35, 0.38)  # Lighter belly
        fin_color = (0.12, 0.2, 0.28)  # Dark fins
        eye_color = (0.9, 0.85, 0.2)  # Glowing yellow eyes

        # MASSIVE BODY - Ship-sized
        body_scale = (scale * 1.2, scale * 0.8, scale * 4.0)
        body_pos = (position[0], position[1], position[2] + scale * 2.0)
        body = self._create_composite_cube(f"{name}_Body", body_pos, body_scale, scale_color)
        created_actors.append(body["actor"])

        # Scale patterns
        for i in range(20):
            scale_piece_scale = (scale * 1.25, scale * 0.04, scale * 0.3)
            scale_piece_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.05,
                position[1] + scale * 0.82,
                position[2] + scale * 0.3 + (i // 2) * scale * 0.35
            )
            scale_piece = self._create_composite_cube(
                f"{name}_Scale_{i}", scale_piece_pos, scale_piece_scale, belly_color
            )
            created_actors.append(scale_piece["actor"])

        # Dorsal fin
        for i in range(6):
            fin_scale = (scale * 0.3, scale * 0.04, scale * 0.6)
            fin_pos = (
                position[0],
                position[1] - scale * 0.82,
                position[2] + scale * 0.5 + i * scale * 0.55
            )
            fin = self._create_composite_cube(
                f"{name}_DorsalFin_{i}", fin_pos, fin_scale, fin_color
            )
            created_actors.append(fin["actor"])

        # MASSIVE HEAD
        head_scale = (scale * 1.0, scale * 0.9, scale * 1.2)
        head_pos = (position[0], position[1] - scale * 1.8, position[2] + scale * 2.5)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, scale_color)
        created_actors.append(head["actor"])

        # IMMENSE JAWS
        upper_jaw_scale = (scale * 0.9, scale * 0.3, scale * 0.5)
        upper_jaw_pos = (position[0], position[1] - scale * 2.5, position[2] + scale * 2.8)
        upper_jaw = self._create_composite_cube(f"{name}_UpperJaw", upper_jaw_pos, upper_jaw_scale, scale_color)
        created_actors.append(upper_jaw["actor"])

        lower_jaw_scale = (scale * 0.85, scale * 0.25, scale * 0.45)
        lower_jaw_pos = (position[0], position[1] - scale * 2.5, position[2] + scale * 2.3)
        lower_jaw = self._create_composite_cube(f"{name}_LowerJaw", lower_jaw_pos, lower_jaw_scale, belly_color)
        created_actors.append(lower_jaw["actor"])

        # TEETH - Multiple rows
        for i in range(12):
            tooth_scale = (scale * 0.08, scale * 0.15, scale * 0.08)
            tooth_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.75,
                position[1] - scale * 2.5,
                position[2] + scale * 2.6 + (i // 2) * scale * 0.15
            )
            tooth = self._create_composite_cube(
                f"{name}_Tooth_{i}", tooth_pos, tooth_scale, belly_color
            )
            created_actors.append(tooth["actor"])

        # Giant eyes
        eye_scale = (scale * 0.25, scale * 0.08, scale * 0.25)
        eye_pos_l = (head_pos[0] - scale * 0.35, head_pos[1] - scale * 0.65, head_pos[2] + scale * 0.3)
        eye_pos_r = (head_pos[0] + scale * 0.35, head_pos[1] - scale * 0.65, head_pos[2] + scale * 0.3)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, eye_color)
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, eye_color)
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Pectoral fins
        for side in [-1, 1]:
            fin_scale = (scale * 0.6, scale * 0.1, scale * 1.0)
            fin_pos = (position[0] + side * scale * 0.9, position[1], position[2] + scale * 2.0)
            fin = self._create_composite_cube(
                f"{name}_PectoralFin_{'L' if side < 0 else 'R'}", fin_pos, fin_scale, fin_color
            )
            created_actors.append(fin["actor"])

        # MASSIVE TAIL
        tail_scale = (scale * 0.7, scale * 0.6, scale * 2.5)
        tail_pos = (position[0], position[1] + scale * 3.0, position[2] + scale * 1.8)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, scale_color)
        created_actors.append(tail["actor"])

        # Tail fluke
        fluke_scale = (scale * 1.5, scale * 0.08, scale * 0.8)
        fluke_pos = (position[0], position[1] + scale * 4.8, position[2] + scale * 1.5)
        fluke = self._create_composite_cube(f"{name}_TailFluke", fluke_pos, fluke_scale, fin_color)
        created_actors.append(fluke["actor"])

        unreal.log(f"🐋 LEVIATHAN created with {len(created_actors)} components (Hollywood Ready - GIANT)")
        return {
            "message": f"Created {name} (Leviathan - Hollywood Ready - Ship-Killer)",
            "name": name,
            "type": "leviathan",
            "actors": created_actors
        }

    def _create_mimic_demon_hollywood(self, parsed: dict) -> dict:
        """
        MIMIC DEMON (High Confidence Function, Soft Form - Metamorphic)
        - Shapeshifting predator
        - Can mimic any form
        - Always has subtle tells
        - Materials: shifting surface, barely-there form, adaptive colors
        - Scale: VARIABLE (adapts to prey)
        - Locomotion: Adapts to mimicked form
        """
        name = parsed.get("name") or "MimicDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.5

        unreal.log("🎭 Creating MIMIC DEMON (Hollywood Ready - Metamorphic)...")

        created_actors = []
        base_color = (0.45, 0.42, 0.4)  # Shifting gray
        tell_color = (0.6, 0.35, 0.4)  # Subtle demonic tell
        eye_color = (0.85, 0.3, 0.2)  # Revealing eyes

        # AMORPHOUS BODY - Shifting form
        body_scale = (scale * 0.5, scale * 0.4, scale * 1.0)
        body_pos = (position[0], position[1], position[2] + scale * 0.5)
        body = self._create_composite_cube(f"{name}_ShiftingForm", body_pos, body_scale, base_color)
        created_actors.append(body["actor"])

        # Shifting surface ripples
        for i in range(10):
            ripple_scale = (scale * 0.45, scale * 0.04, scale * 0.15)
            ripple_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.02,
                position[1] + ((i % 3) - 1) * scale * 0.22,
                position[2] + scale * 0.2 + (i // 3) * scale * 0.25
            )
            ripple = self._create_composite_cube(
                f"{name}_SurfaceRipple_{i}", ripple_pos, ripple_scale, tell_color
            )
            created_actors.append(ripple["actor"])

        # Partially formed head
        head_scale = (scale * 0.25, scale * 0.25, scale * 0.25)
        head_pos = (position[0], position[1], position[2] + scale * 1.1)
        head = self._create_composite_cube(f"{name}_PartialHead", head_pos, head_scale, base_color)
        created_actors.append(head["actor"])

        # Revealing eyes - The tell
        eye_scale = (scale * 0.08, scale * 0.08, scale * 0.08)
        eye_pos_l = (head_pos[0] - scale * 0.08, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.08)
        eye_pos_r = (head_pos[0] + scale * 0.08, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.08)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, eye_color)
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, eye_color)
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Shifting limbs - not fully formed
        for side in [-1, 1]:
            limb_scale = (scale * 0.1, scale * 0.25, scale * 0.1)
            limb_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.45)
            limb = self._create_composite_cube(
                f"{name}_ShiftingLimb_{'L' if side < 0 else 'R'}", limb_pos, limb_scale, base_color
            )
            created_actors.append(limb["actor"])

        # Form instability particles
        for i in range(12):
            particle_scale = (scale * 0.06, scale * 0.06, scale * 0.06)
            angle = (2 * math.pi * i) / 12
            particle_pos = (
                position[0] + scale * 0.5 * math.cos(angle),
                position[1] + scale * 0.5 * math.sin(angle),
                position[2] + scale * 0.4 + (i % 4) * scale * 0.2
            )
            particle = self._create_composite_cube(
                f"{name}_FormParticle_{i}", particle_pos, particle_scale, tell_color
            )
            created_actors.append(particle["actor"])

        unreal.log(f"🎭 MIMIC DEMON created with {len(created_actors)} components (Hollywood Ready - Shapeshifter)")
        return {
            "message": f"Created {name} (Mimic Demon - Hollywood Ready - Metamorphic)",
            "name": name,
            "type": "mimic demon",
            "actors": created_actors
        }

    def _create_demon_queen_hollywood(self, parsed: dict) -> dict:
        """
        DEMON QUEEN / ALAGAI'TING KA (Moderate Confidence - Brood Sovereign)
        - Ruler of all Corelings
        - Largest and most powerful demon
        - Commands the demon host
        - Materials: obsidian armor, royal demon insignia, commanding presence
        - Scale: GIGANTIC (15-20 feet tall)
        - Locomotion: Imposing sovereign stride
        """
        name = parsed.get("name") or "AlagaiTingKa"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 5.0

        unreal.log("👑 Creating DEMON QUEEN / ALAGAI'TING KA (Hollywood Ready - Brood Sovereign)...")

        created_actors = []
        obsidian_color = (0.12, 0.1, 0.08)  # Obsidian black
        royal_color = (0.25, 0.2, 0.15)  # Royal accents
        crown_color = (0.6, 0.5, 0.3)  # demonic gold
        eye_color = (1, 0.4, 0.1)  # Sovereign orange eyes

        # COLOSSAL BODY - Sovereign form
        body_scale = (scale * 1.5, scale * 1.2, scale * 3.0)
        body_pos = (position[0], position[1], position[2] + scale * 1.5)
        body = self._create_composite_cube(f"{name}_RoyalBody", body_pos, body_scale, obsidian_color)
        created_actors.append(body["actor"])

        # Royal armor plates
        for i in range(12):
            armor_scale = (scale * 1.6, scale * 0.15, scale * 0.6)
            armor_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.05,
                position[1] + scale * 1.27,
                position[2] + scale * 0.4 + i * scale * 0.22
            )
            armor = self._create_composite_cube(
                f"{name}_RoyalArmor_{i}", armor_pos, armor_scale, royal_color
            )
            created_actors.append(armor["actor"])

        # Massive shoulders
        for side in [-1, 1]:
            shoulder_scale = (scale * 0.9, scale * 0.8, scale * 1.0)
            shoulder_pos = (position[0] + side * scale * 1.1, position[1], position[2] + scale * 2.5)
            shoulder = self._create_composite_cube(
                f"{name}_RoyalShoulder_{'L' if side < 0 else 'R'}", shoulder_pos, shoulder_scale, obsidian_color
            )
            created_actors.append(shoulder["actor"])

        # SOVEREIGN HEAD
        head_scale = (scale * 0.7, scale * 0.8, scale * 0.6)
        head_pos = (position[0], position[1], position[2] + scale * 3.3)
        head = self._create_composite_cube(f"{name}_SovereignHead", head_pos, head_scale, obsidian_color)
        created_actors.append(head["actor"])

        # ROYAL CROWN / HORNS
        for i in range(6):
            horn_scale = (scale * 0.15, scale * 0.15, scale * 0.8)
            angle = (math.pi * i) / 3
            horn_pos = (
                head_pos[0] + scale * 0.4 * math.cos(angle),
                head_pos[1] + scale * 0.4 * math.sin(angle),
                head_pos[2] + scale * 0.4
            )
            horn = self._create_composite_cube(
                f"{name}_RoyalHorn_{i}", horn_pos, horn_scale, crown_color
            )
            created_actors.append(horn["actor"])

        # Commanding eyes
        eye_scale = (scale * 0.15, scale * 0.12, scale * 0.15)
        eye_pos_l = (head_pos[0] - scale * 0.22, head_pos[1] - scale * 0.5, head_pos[2] + scale * 0.15)
        eye_pos_r = (head_pos[0] + scale * 0.22, head_pos[1] - scale * 0.5, head_pos[2] + scale * 0.15)
        eye_l = self._create_composite_cube(f"{name}_SovereignEye_L", eye_pos_l, eye_scale, eye_color)
        eye_r = self._create_composite_cube(f"{name}_SovereignEye_R", eye_pos_r, eye_scale, eye_color)
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Royal arms
        for side in [-1, 1]:
            upper_scale = (scale * 0.4, scale * 0.5, scale * 1.2)
            upper_pos = (position[0] + side * scale * 1.4, position[1], position[2] + scale * 2.0)
            upper = self._create_composite_cube(
                f"{name}_RoyalUpperArm_{'L' if side < 0 else 'R'}", upper_pos, upper_scale, obsidian_color
            )
            created_actors.append(upper["actor"])

            # Forearm
            forearm_scale = (scale * 0.35, scale * 0.45, scale * 1.0)
            forearm_pos = (position[0] + side * scale * 1.4, position[1] - scale * 0.5, position[2] + scale * 1.2)
            forearm = self._create_composite_cube(
                f"{name}_RoyalForearm_{'L' if side < 0 else 'R'}", forearm_pos, forearm_scale, obsidian_color
            )
            created_actors.append(forearm["actor"])

            # Royal hand
            hand_scale = (scale * 0.5, scale * 0.4, scale * 0.4)
            hand_pos = (position[0] + side * scale * 1.4, position[1] - scale * 1.1, position[2] + scale * 0.5)
            hand = self._create_composite_cube(
                f"{name}_RoyalHand_{'L' if side < 0 else 'R'}", hand_pos, hand_scale, royal_color
            )
            created_actors.append(hand["actor"])

        # Pillar legs
        for side in [-1, 1]:
            leg_scale = (scale * 0.5, scale * 0.6, scale * 1.5)
            leg_pos = (position[0] + side * scale * 0.6, position[1], position[2])
            leg = self._create_composite_cube(
                f"{name}_RoyalLeg_{'L' if side < 0 else 'R'}", leg_pos, leg_scale, obsidian_color
            )
            created_actors.append(leg["actor"])

        # Royal command aura
        for i in range(5):
            aura_scale = (scale * (1.8 + i * 0.3), scale * 0.04, scale * (1.8 + i * 0.3))
            aura_pos = (position[0], position[1], position[2] + scale * 1.0 + i * scale * 0.1)
            aura = self._create_composite_cube(
                f"{name}_CommandAura_{i}", aura_pos, aura_scale, crown_color
            )
            created_actors.append(aura["actor"])

        unreal.log(f"👑 DEMON QUEEN created with {len(created_actors)} components (Hollywood Ready - SOVEREIGN)")
        return {
            "message": f"Created {name} (Demon Queen / Alagai'ting Ka - Hollywood Ready - Brood Sovereign)",
            "name": name,
            "type": "demon queen",
            "actors": created_actors
        }

    def _create_sand_demon_hollywood(self, parsed: dict) -> dict:
        """
        SAND DEMON (High Confidence)
        - Quadrupedal pack hunter
        - Low-slung desert predator
        - Shifting sand form that blends with dunes
        - Pack coordination tactics
        - Materials: golden sand, darker ochre markings, crystalline dust
        - Scale: Medium quadrupedal (4-6 feet long)
        - Locomotion: Darting desert pack hunter
        """
        name = parsed.get("name") or "SandDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.2

        unreal.log("🏜️ Creating SAND DEMON (Hollywood Ready - Quadrupedal Pack Hunter)...")

        created_actors = []
        sand_color = (0.82, 0.76, 0.58)  # Golden sand
        ochre_color = (0.68, 0.62, 0.48)  # Darker ochre
        crystal_color = (0.92, 0.88, 0.78)  # Crystalline highlights
        eye_color = (1, 0.85, 0.2)  # Golden predator eyes

        # LOW-SLUNG BODY - Quadrupedal desert hunter
        body_scale = (scale * 0.5, scale * 0.35, scale * 1.0)
        body_pos = (position[0], position[1], position[2] + scale * 0.4)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, sand_color)
        created_actors.append(body["actor"])

        # Spine ridge - crystalline dorsal spikes
        for i in range(8):
            spine_scale = (scale * 0.05, scale * 0.05, scale * 0.08)
            spine_pos = (
                position[0],
                position[1] - scale * 0.14 + i * scale * 0.12,
                position[2] + scale * 0.85
            )
            spine = self._create_composite_cube(
                f"{name}_SpineRidge_{i}", spine_pos, spine_scale, crystal_color
            )
            created_actors.append(spine["actor"])

        # Head - Sleek desert predator
        head_scale = (scale * 0.25, scale * 0.35, scale * 0.2)
        head_pos = (position[0], position[1] - scale * 0.2, position[2] + scale * 0.5)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, sand_color)
        created_actors.append(head["actor"])

        # Snout
        snout_scale = (scale * 0.15, scale * 0.2, scale * 0.12)
        snout_pos = (position[0], position[1] - scale * 0.45, position[2] + scale * 0.45)
        snout = self._create_composite_cube(f"{name}_Snout", snout_pos, snout_scale, sand_color)
        created_actors.append(snout["actor"])

        # Jaw line
        jaw_scale = (scale * 0.18, scale * 0.08, scale * 0.08)
        jaw_pos = (position[0], position[1] - scale * 0.45, position[2] + scale * 0.38)
        jaw = self._create_composite_cube(f"{name}_Jaw", jaw_pos, jaw_scale, ochre_color)
        created_actors.append(jaw["actor"])

        # Golden predator eyes
        eye_scale = (scale * 0.06, scale * 0.06, scale * 0.06)
        eye_pos_l = (head_pos[0] - scale * 0.08, head_pos[1] - scale * 0.33, head_pos[2])
        eye_pos_r = (head_pos[0] + scale * 0.08, head_pos[1] - scale * 0.33, head_pos[2])
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, eye_color)
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, eye_color)
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # Ear ridges
        for side in [-1, 1]:
            ear_scale = (scale * 0.08, scale * 0.08, scale * 0.12)
            ear_pos = (head_pos[0] + side * scale * 0.12, head_pos[1] - scale * 0.15, head_pos[2] + scale * 0.08)
            ear = self._create_composite_cube(
                f"{name}_EarRidge_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, sand_color
            )
            created_actors.append(ear["actor"])

        # QUADRUPEDAL LEGS - Pack hunter limbs
        leg_positions = [
            (-1, -1, 0.7),   # Front left
            (1, -1, 0.7),    # Front right
            (-1, 1, 0.3),    # Back left
            (1, 1, 0.3)      # Back right
        ]

        for i, (side_x, side_y, forward_bias) in enumerate(leg_positions):
            # Upper leg
            upper_scale = (scale * 0.1, scale * 0.1, scale * 0.35)
            upper_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] + scale * 0.35
            )
            upper = self._create_composite_cube(
                f"{name}_UpperLeg_{i}", upper_pos, upper_scale, sand_color
            )
            created_actors.append(upper["actor"])

            # Lower leg
            lower_scale = (scale * 0.08, scale * 0.08, scale * 0.3)
            lower_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] + scale * 0.08
            )
            lower = self._create_composite_cube(
                f"{name}_LowerLeg_{i}", lower_pos, lower_scale, ochre_color
            )
            created_actors.append(lower["actor"])

            # Paw
            paw_scale = (scale * 0.12, scale * 0.08, scale * 0.06)
            paw_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] - scale * 0.08
            )
            paw = self._create_composite_cube(
                f"{name}_Paw_{i}", paw_pos, paw_scale, crystal_color
            )
            created_actors.append(paw["actor"])

        # Tail - Long balancing tail
        tail_scale = (scale * 0.06, scale * 0.4, scale * 0.06)
        tail_pos = (position[0], position[1] + scale * 0.4, position[2] + scale * 0.35)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, sand_color)
        created_actors.append(tail["actor"])

        # Tail tuft
        tuft_scale = (scale * 0.08, scale * 0.08, scale * 0.08)
        tuft_pos = (position[0], position[1] + scale * 0.65, position[2] + scale * 0.35)
        tuft = self._create_composite_cube(f"{name}_TailTuft", tuft_pos, tuft_scale, ochre_color)
        created_actors.append(tuft["actor"])

        # Desert camouflage markings
        for i in range(6):
            marking_scale = (scale * 0.12, scale * 0.02, scale * 0.15)
            marking_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.25,
                position[1] + scale * 0.36,
                position[2] + scale * 0.2 + (i // 2) * scale * 0.3
            )
            marking = self._create_composite_cube(
                f"{name}_Camouflage_{i}", marking_pos, marking_scale, ochre_color
            )
            created_actors.append(marking["actor"])

        # Sand dust aura
        for i in range(12):
            dust_scale = (scale * 0.05, scale * 0.05, scale * 0.05)
            angle = (2 * math.pi * i) / 12
            dust_pos = (
                position[0] + scale * 0.5 * math.cos(angle),
                position[1] + scale * 0.5 * math.sin(angle),
                position[2] + scale * 0.3 + (i % 3) * scale * 0.15
            )
            dust = self._create_composite_cube(
                f"{name}_SandDust_{i}", dust_pos, dust_scale, crystal_color
            )
            created_actors.append(dust["actor"])

        unreal.log(f"🏜️ SAND DEMON created with {len(created_actors)} components (Hollywood Ready - Pack Hunter)")
        return {
            "message": f"Created {name} (Sand Demon - Hollywood Ready - Quadrupedal Pack Hunter)",
            "name": name,
            "type": "sand demon",
            "actors": created_actors
        }

    def _create_snow_demon_hollywood(self, parsed: dict) -> dict:
        """
        SNOW DEMON (High Confidence - REPLACES Ice Demon)
        - Large cat-like mountain predator
        - Thick white fur coating
        - Visible horns/spikes protruding through fur
        - Feline massing and proportions
        - Powerful quiet ambush predator
        - Freezing spit/mechanism
        - Materials: dirty white, ice-gray, pale bone, frost blue undertones, storm shadow cools, cold weather fur
        - Scale: Large apex lesser demon (6-8 feet long)
        - Locomotion: Feline mountain avalanche-like
        """
        name = parsed.get("name") or "SnowDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.8

        unreal.log("❄️ Creating SNOW DEMON (Hollywood Ready - Cat-like Mountain Predator)...")

        created_actors = []
        fur_color = (0.92, 0.94, 0.95)  # Dirty white fur
        gray_fur = (0.82, 0.85, 0.88)  # Ice-gray patches
        bone_color = (0.88, 0.86, 0.82)  # Pale bone horns
        frost_color = (0.85, 0.9, 0.95)  # Frost blue undertones
        eye_color = (0.6, 0.85, 0.95)  # Cold blue eyes

        # FELINE BODY - Cat-like massing
        body_scale = (scale * 0.6, scale * 0.45, scale * 1.2)
        body_pos = (position[0], position[1], position[2] + scale * 0.6)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, fur_color)
        created_actors.append(body["actor"])

        # Thick fur layers - fluffier appearance
        for i in range(10):
            fur_patch_scale = (scale * 0.55, scale * 0.08, scale * 0.25)
            fur_patch_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.05,
                position[1] + ((i % 2) * 2 - 1) * scale * 0.25,
                position[2] + scale * 0.3 + (i // 2) * scale * 0.35
            )
            fur_patch = self._create_composite_cube(
                f"{name}_FurPatch_{i}", fur_patch_pos, fur_patch_scale, gray_fur
            )
            created_actors.append(fur_patch["actor"])

        # Chest fur ruff
        ruff_scale = (scale * 0.35, scale * 0.12, scale * 0.25)
        ruff_pos = (position[0], position[1] - scale * 0.25, position[2] + scale * 0.75)
        ruff = self._create_composite_cube(f"{name}_ChestRuff", ruff_pos, ruff_pos, fur_color)
        created_actors.append(ruff["actor"])

        # FELINE HEAD - Cat-like proportions
        head_scale = (scale * 0.28, scale * 0.35, scale * 0.25)
        head_pos = (position[0], position[1] - scale * 0.15, position[2] + scale * 0.85)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, fur_color)
        created_actors.append(head["actor"])

        # Muzzle
        muzzle_scale = (scale * 0.15, scale * 0.2, scale * 0.12)
        muzzle_pos = (position[0], position[1] - scale * 0.4, position[2] + scale * 0.8)
        muzzle = self._create_composite_cube(f"{name}_Muzzle", muzzle_pos, muzzle_scale, fur_color)
        created_actors.append(muzzle["actor"])

        # Ears - Tufted cat ears
        for side in [-1, 1]:
            ear_scale = (scale * 0.1, scale * 0.12, scale * 0.15)
            ear_pos = (head_pos[0] + side * scale * 0.15, head_pos[1] - scale * 0.2, head_pos[2] + scale * 0.15)
            ear = self._create_composite_cube(
                f"{name}_Ear_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, fur_color
            )
            created_actors.append(ear["actor"])

            # Ear tufts
            tuft_scale = (scale * 0.04, scale * 0.04, scale * 0.08)
            tuft_pos = (ear_pos[0], ear_pos[1], ear_pos[2] + scale * 0.1)
            tuft = self._create_composite_cube(
                f"{name}_EarTuft_{'L' if side < 0 else 'R'}", tuft_pos, tuft_scale, gray_fur
            )
            created_actors.append(tuft["actor"])

        # Cold blue eyes - Predator gaze
        eye_scale = (scale * 0.06, scale * 0.06, scale * 0.06)
        eye_pos_l = (head_pos[0] - scale * 0.08, head_pos[1] - scale * 0.33, head_pos[2] + scale * 0.02)
        eye_pos_r = (head_pos[0] + scale * 0.08, head_pos[1] - scale * 0.33, head_pos[2] + scale * 0.02)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, eye_color)
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, eye_color)
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # VISIBLE HORNS/SPIKES through fur
        # Crown horns - protruding through head fur
        for i in range(4):
            horn_scale = (scale * 0.05, scale * 0.05, scale * 0.18)
            angle = (math.pi * (i + 1)) / 5
            horn_pos = (
                head_pos[0] + scale * 0.18 * math.cos(angle),
                head_pos[1] + scale * 0.18 * math.sin(angle),
                head_pos[2] + scale * 0.18
            )
            horn = self._create_composite_cube(
                f"{name}_Horn_{i}", horn_pos, horn_scale, bone_color
            )
            created_actors.append(horn["actor"])

        # Spine spikes through back fur
        for i in range(6):
            spike_scale = (scale * 0.04, scale * 0.04, scale * 0.12)
            spike_pos = (
                position[0],
                position[1] - scale * 0.2 + i * scale * 0.15,
                position[2] + scale * 1.15
            )
            spike = self._create_composite_cube(
                f"{name}_SpineSpike_{i}", spike_pos, spike_scale, bone_color
            )
            created_actors.append(spike["actor"])

        # FELINE LEGS - Powerful quadrupedal
        leg_positions = [
            (-1, -1, 0.75),   # Front left
            (1, -1, 0.75),    # Front right
            (-1, 1, 0.35),    # Back left
            (1, 1, 0.35)      # Back right
        ]

        for i, (side_x, side_y, forward_bias) in enumerate(leg_positions):
            # Upper leg - muscular thigh
            upper_scale = (scale * 0.15, scale * 0.12, scale * 0.35)
            upper_pos = (
                position[0] + side_x * scale * 0.28,
                position[1] + side_y * scale * 0.18,
                position[2] + scale * 0.45
            )
            upper = self._create_composite_cube(
                f"{name}_UpperLeg_{i}", upper_pos, upper_scale, fur_color
            )
            created_actors.append(upper["actor"])

            # Lower leg - sleek
            lower_scale = (scale * 0.1, scale * 0.1, scale * 0.32)
            lower_pos = (
                position[0] + side_x * scale * 0.28,
                position[1] + side_y * scale * 0.18,
                position[2] + scale * 0.15
            )
            lower = self._create_composite_cube(
                f"{name}_LowerLeg_{i}", lower_pos, lower_scale, gray_fur
            )
            created_actors.append(lower["actor"])

            # Paw - Large cat paw
            paw_scale = (scale * 0.14, scale * 0.08, scale * 0.06)
            paw_pos = (
                position[0] + side_x * scale * 0.28,
                position[1] + side_y * scale * 0.18,
                position[2]
            )
            paw = self._create_composite_cube(
                f"{name}_Paw_{i}", paw_pos, paw_scale, fur_color
            )
            created_actors.append(paw["actor"])

        # Tail - Feline balancing tail
        tail_scale = (scale * 0.08, scale * 0.5, scale * 0.08)
        tail_pos = (position[0], position[1] + scale * 0.5, position[2] + scale * 0.55)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, fur_color)
        created_actors.append(tail["actor"])

        # Tail tuft
        tail_tuft_scale = (scale * 0.1, scale * 0.1, scale * 0.1)
        tail_tuft_pos = (position[0], position[1] + scale * 0.8, position[2] + scale * 0.55)
        tail_tuft = self._create_composite_cube(f"{name}_TailTuft", tail_tuft_pos, tail_tuft_scale, gray_fur)
        created_actors.append(tail_tuft["actor"])

        # Frost breath aura
        for i in range(5):
            frost_scale = (scale * 0.12, scale * 0.03, scale * 0.12)
            frost_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.08,
                position[1] - scale * 0.55 - i * scale * 0.05,
                position[2] + scale * 0.78
            )
            frost = self._create_composite_cube(
                f"{name}_FrostBreath_{i}", frost_pos, frost_scale, frost_color
            )
            created_actors.append(frost["actor"])

        unreal.log(f"❄️ SNOW DEMON created with {len(created_actors)} components (Hollywood Ready - Feline Predator)")
        return {
            "message": f"Created {name} (Snow Demon - Hollywood Ready - Cat-like Mountain Predator)",
            "name": name,
            "type": "snow demon",
            "actors": created_actors
        }

    def _create_field_demon_hollywood(self, parsed: dict) -> dict:
        """
        FIELD DEMON (Moderate Confidence)
        - Feline plains runner
        - Built for speed across open terrain
        - Grass-colored camouflage
        - Pack hunting behavior
        - Materials: tawny gold, grass green, earth brown, savanna tones
        - Scale: Medium quadrupedal (5-7 feet long)
        - Locomotion: Sprinting plains hunter
        """
        name = parsed.get("name") or "FieldDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.5

        unreal.log("🌾 Creating FIELD DEMON (Hollywood Ready - Feline Plains Runner)...")

        created_actors = []
        base_color = (0.75, 0.68, 0.45)  # Tawny gold
        grass_color = (0.58, 0.62, 0.35)  # Grass green
        earth_color = (0.52, 0.45, 0.32)  # Earth brown
        eye_color = (0.9, 0.75, 0.3)  # Golden predator eyes

        # FELINE BODY - Built for speed
        body_scale = (scale * 0.55, scale * 0.4, scale * 1.1)
        body_pos = (position[0], position[1], position[2] + scale * 0.55)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, base_color)
        created_actors.append(body["actor"])

        # Grass stripe camouflage
        for i in range(8):
            stripe_scale = (scale * 0.5, scale * 0.04, scale * 0.2)
            stripe_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.02,
                position[1] + ((i % 3) - 1) * scale * 0.2,
                position[2] + scale * 0.3 + (i // 3) * scale * 0.35
            )
            stripe = self._create_composite_cube(
                f"{name}_GrassStripe_{i}", stripe_pos, stripe_scale, grass_color
            )
            created_actors.append(stripe["actor"])

        # FELINE HEAD
        head_scale = (scale * 0.26, scale * 0.32, scale * 0.22)
        head_pos = (position[0], position[1] - scale * 0.12, position[2] + scale * 0.75)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, base_color)
        created_actors.append(head["actor"])

        # Muzzle
        muzzle_scale = (scale * 0.14, scale * 0.18, scale * 0.1)
        muzzle_pos = (position[0], position[1] - scale * 0.35, position[2] + scale * 0.7)
        muzzle = self._create_composite_cube(f"{name}_Muzzle", muzzle_pos, muzzle_scale, base_color)
        created_actors.append(muzzle["actor"])

        # Ears - Alert cat ears
        for side in [-1, 1]:
            ear_scale = (scale * 0.08, scale * 0.1, scale * 0.12)
            ear_pos = (head_pos[0] + side * scale * 0.14, head_pos[1] - scale * 0.2, head_pos[2] + scale * 0.12)
            ear = self._create_composite_cube(
                f"{name}_Ear_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, base_color
            )
            created_actors.append(ear["actor"])

        # Golden predator eyes
        eye_scale = (scale * 0.055, scale * 0.055, scale * 0.055)
        eye_pos_l = (head_pos[0] - scale * 0.07, head_pos[1] - scale * 0.3, head_pos[2] + scale * 0.02)
        eye_pos_r = (head_pos[0] + scale * 0.07, head_pos[1] - scale * 0.3, head_pos[2] + scale * 0.02)
        eye_l = self._create_composite_cube(f"{name}_Eye_L", eye_pos_l, eye_scale, eye_color)
        eye_r = self._create_composite_cube(f"{name}_Eye_R", eye_pos_r, eye_scale, eye_color)
        created_actors.append(eye_l["actor"])
        created_actors.append(eye_r["actor"])

        # QUADRUPEDAL LEGS - Sprinting limbs
        leg_positions = [
            (-1, -1, 0.7),   # Front left
            (1, -1, 0.7),    # Front right
            (-1, 1, 0.4),    # Back left
            (1, 1, 0.4)      # Back right
        ]

        for i, (side_x, side_y, forward_bias) in enumerate(leg_positions):
            # Upper leg - muscular
            upper_scale = (scale * 0.12, scale * 0.1, scale * 0.32)
            upper_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.16,
                position[2] + scale * 0.4
            )
            upper = self._create_composite_cube(
                f"{name}_UpperLeg_{i}", upper_pos, upper_scale, base_color
            )
            created_actors.append(upper["actor"])

            # Lower leg - sleek running
            lower_scale = (scale * 0.08, scale * 0.08, scale * 0.3)
            lower_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.16,
                position[2] + scale * 0.12
            )
            lower = self._create_composite_cube(
                f"{name}_LowerLeg_{i}", lower_pos, lower_scale, earth_color
            )
            created_actors.append(lower["actor"])

            # Paw - Running foot
            paw_scale = (scale * 0.12, scale * 0.06, scale * 0.05)
            paw_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.16,
                position[2] - scale * 0.02
            )
            paw = self._create_composite_cube(
                f"{name}_Paw_{i}", paw_pos, paw_scale, base_color
            )
            created_actors.append(paw["actor"])

        # Tail - Balancing tail
        tail_scale = (scale * 0.06, scale * 0.45, scale * 0.06)
        tail_pos = (position[0], position[1] + scale * 0.45, position[2] + scale * 0.5)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, base_color)
        created_actors.append(tail["actor"])

        # Tail tip - dark
        tip_scale = (scale * 0.07, scale * 0.08, scale * 0.07)
        tip_pos = (position[0], position[1] + scale * 0.75, position[2] + scale * 0.5)
        tip = self._create_composite_cube(f"{name}_TailTip", tip_pos, tip_scale, earth_color)
        created_actors.append(tip["actor"])

        unreal.log(f"🌾 FIELD DEMON created with {len(created_actors)} components (Hollywood Ready - Plains Runner)")
        return {
            "message": f"Created {name} (Field Demon - Hollywood Ready - Feline Plains Runner)",
            "name": name,
            "type": "field demon",
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
    "👹 Corelings (The Painted Man): wind, fire, water, rock, wood, mind, clay, sand, ice, forest demons",
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
    "create(\"a clay demon from the earth\")",
    "create(\"a sand demon in the desert\")",
    "create(\"an ice demon with frost armor\")",
    "create(\"a forest demon with antlers\")",
    "create(\"a wood demon camouflaged in the forest\")",
    "create(\"a mind demon with psychic aura\")",
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
