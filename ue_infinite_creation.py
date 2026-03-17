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
        ROCK DEMON (High Confidence) - REALISTIC ANIMATABLE VERSION
        - Enormous upright siege brute (8-12 feet)
        - Massive shoulders, barrel torso, thick neck
        - Weighty club tail with crushing force
        - Horned mineral armor plates
        - Slow unstoppable locomotion
        - FULLY BONED FOR ANIMATION
        - Materials: Real basalt, granite, slate, iron-rich stone, natural weathering
        """
        name = parsed.get("name") or "RockDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 3.0

        unreal.log("🪨 Creating ROCK DEMON (Realistic + Fully Boned)...")

        created_actors = []
        bones = {}  # Store bone references for animation

        # REALISTIC MATERIAL COLORS - No magical glow
        basalt_dark = (0.22, 0.20, 0.17)      # Dark basalt base
        basalt_mid = (0.26, 0.24, 0.20)        # Mid-tone basalt
        granite_light = (0.32, 0.30, 0.26)     # Weathered granite
        iron_oxide = (0.28, 0.18, 0.14)        # Iron staining (rust color)
        lichen_green = (0.35, 0.32, 0.25)      # Natural lichen growth
        scratch_dark = (0.15, 0.13, 0.11)      # Deep scratches/wear
        dust_gray = (0.40, 0.38, 0.35)         # Surface dust layer

        # ============================================================
        # SKELETON / BONE STRUCTURE - For Animation Rigging
        # ============================================================

        # Root/Pelvis bone (center of mass)
        pelvis_bone = self._create_bone_joint(f"{name}_Pelvis_Root", position, scale)
        bones["pelvis"] = pelvis_bone
        created_actors.append(pelvis_bone["actor"])

        # Spine column - articulated vertebrae
        spine_bones = []
        for i in range(5):
            spine_pos = (position[0], position[1], position[2] + scale * (0.5 + i * 0.4))
            spine_bone = self._create_bone_joint(f"{name}_Spine_{i+1}", spine_pos, scale)
            spine_bones.append(spine_bone)
            created_actors.append(spine_bone["actor"])
        bones["spine"] = spine_bones

        # Rib cage
        for i in range(8):
            rib_angle = (math.pi * i) / 8
            for rib_level in range(3):
                rib_pos = (
                    position[0] + scale * 0.5 * math.cos(rib_angle),
                    position[1] + scale * 0.5 * math.sin(rib_angle),
                    position[2] + scale * (1.0 + rib_level * 0.3)
                )
                rib_bone = self._create_bone_joint(f"{name}_Rib_{i}_{rib_level}", rib_pos, scale)
                created_actors.append(rib_bone["actor"])

        # ============================================================
        # TORSO / BODY - Multi-layer construction
        # ============================================================

        # Main torso block (core muscle mass)
        torso_scale = (scale * 1.15, scale * 0.85, scale * 1.9)
        torso_pos = (position[0], position[1], position[2] + scale * 1.0)
        torso = self._create_composite_cube(f"{name}_Torso_Main", torso_pos, torso_scale, basalt_dark)
        created_actors.append(torso["actor"])

        # Abdominal muscle definition (stone "abs")
        for i in range(6):
            ab_scale = (scale * 1.1, scale * 0.08, scale * 0.25)
            ab_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.02,
                position[1] + scale * 0.88,
                position[2] + scale * 0.3 + (i // 2) * scale * 0.35
            )
            ab = self._create_composite_cube(f"{name}_Ab_{i}", ab_pos, ab_scale, basalt_mid)
            created_actors.append(ab["actor"])

        # Chest plate (sternum)
        sternum_scale = (scale * 0.8, scale * 0.12, scale * 0.6)
        sternum_pos = (position[0], position[1] + scale * 0.88, position[2] + scale * 1.4)
        sternum = self._create_composite_cube(f"{name}_Sternum", sternum_pos, sternum_scale, granite_light)
        created_actors.append(sternum["actor"])

        # Pectoral muscles
        for side in [-1, 1]:
            pec_scale = (scale * 0.5, scale * 0.15, scale * 0.4)
            pec_pos = (position[0] + side * scale * 0.55, position[1] + scale * 0.82, position[2] + scale * 1.35)
            pec = self._create_composite_cube(f"{name}_Pectoral_{'L' if side < 0 else 'R'}", pec_pos, pec_scale, basalt_mid)
            created_actors.append(pec["actor"])

        # ============================================================
        # MASSIVE SHOULDERS - Boulders of muscle and stone
        # ============================================================

        for side in [-1, 1]:
            # Shoulder joint bone
            shoulder_joint_pos = (position[0] + side * scale * 0.85, position[1], position[2] + scale * 1.6)
            shoulder_joint = self._create_bone_joint(f"{name}_ShoulderJoint_{'L' if side < 0 else 'R'}", shoulder_joint_pos, scale)
            created_actors.append(shoulder_joint["actor"])

            # Deltoid muscle (main shoulder mass)
            delt_scale = (scale * 0.65, scale * 0.55, scale * 0.7)
            delt_pos = (position[0] + side * scale * 0.85, position[1], position[2] + scale * 1.65)
            delt = self._create_composite_cube(f"{name}_Deltoid_{'L' if side < 0 else 'R'}", delt_pos, delt_scale, basalt_mid)
            created_actors.append(delt["actor"])

            # Shoulder armor plate (clavicle equivalent)
            clavicle_scale = (scale * 0.5, scale * 0.12, scale * 0.25)
            clavicle_pos = (position[0] + side * scale * 0.7, position[1], position[2] + scale * 1.85)
            clavicle = self._create_composite_cube(f"{name}_Clavicle_{'L' if side < 0 else 'R'}", clavicle_pos, clavicle_scale, granite_light)
            created_actors.append(clavicle["actor"])

            # Weathering cracks on shoulders
            for j in range(4):
                crack_scale = (scale * 0.35, scale * 0.02, scale * 0.15)
                crack_pos = (
                    position[0] + side * scale * 0.85,
                    position[1] + ((j % 2) - 0.5) * scale * 0.28,
                    position[2] + scale * 1.5 + (j // 2) * scale * 0.2
                )
                crack = self._create_composite_cube(f"{name}_ShoulderCrack_{'L' if side < 0 else 'R'}_{j}", crack_pos, crack_scale, scratch_dark)
                created_actors.append(crack["actor"])

        # ============================================================
        # NECK - Column of solid rock with vertebrae
        # ============================================================

        # Neck vertebrae (visible structure)
        for i in range(4):
            vertebra_scale = (scale * 0.35, scale * 0.35, scale * 0.12)
            vertebra_pos = (position[0], position[1], position[2] + scale * (2.0 + i * 0.15))
            vertebra = self._create_composite_cube(f"{name}_NeckVertebra_{i}", vertebra_pos, vertebra_scale, basalt_mid)
            created_actors.append(vertebra["actor"])

        # Neck muscle mass
        neck_scale = (scale * 0.45, scale * 0.42, scale * 0.5)
        neck_pos = (position[0], position[1], position[2] + scale * 2.1)
        neck = self._create_composite_cube(f"{name}_Neck_Main", neck_pos, neck_scale, basalt_dark)
        created_actors.append(neck["actor"])

        # Neck tendons (columnar details)
        for side in [-1, 1]:
            tendon_scale = (scale * 0.08, scale * 0.12, scale * 0.45)
            tendon_pos = (position[0] + side * scale * 0.2, position[1], position[2] + scale * 2.0)
            tendon = self._create_composite_cube(f"{name}_NeckTendon_{'L' if side < 0 else 'R'}", tendon_pos, tendon_scale, basalt_mid)
            created_actors.append(tendon["actor"])

        # ============================================================
        # HEAD - Blocky cranium with realistic features
        # ============================================================

        # Skull base
        skull_scale = (scale * 0.55, scale * 0.65, scale * 0.45)
        skull_pos = (position[0], position[1], position[2] + scale * 2.45)
        skull = self._create_composite_cube(f"{name}_Skull_Base", skull_pos, skull_scale, basalt_dark)
        created_actors.append(skull["actor"])

        # Brow ridge (heavy, protruding)
        brow_scale = (scale * 0.5, scale * 0.12, scale * 0.15)
        brow_pos = (position[0], position[1] - scale * 0.32, position[2] + scale * 2.7)
        brow = self._create_composite_cube(f"{name}_BrowRidge", brow_pos, brow_scale, granite_light)
        created_actors.append(brow["actor"])

        # Cheek bones
        for side in [-1, 1]:
            cheek_scale = (scale * 0.18, scale * 0.15, scale * 0.2)
            cheek_pos = (position[0] + side * scale * 0.25, position[1] - scale * 0.3, position[2] + scale * 2.5)
            cheek = self._create_composite_cube(f"{name}_CheekBone_{'L' if side < 0 else 'R'}", cheek_pos, cheek_scale, basalt_mid)
            created_actors.append(cheek["actor"])

        # Jaw (heavy, blocky)
        jaw_scale = (scale * 0.4, scale * 0.2, scale * 0.25)
        jaw_pos = (position[0], position[1] - scale * 0.35, position[2] + scale * 2.35)
        jaw = self._create_composite_cube(f"{name}_Jaw_Main", jaw_pos, jaw_pos, basalt_mid)
        created_actors.append(jaw["actor"])

        # Chin
        chin_scale = (scale * 0.2, scale * 0.15, scale * 0.15)
        chin_pos = (position[0], position[1] - scale * 0.4, position[2] + scale * 2.3)
        chin = self._create_composite_cube(f"{name}_Chin", chin_pos, chin_scale, basalt_dark)
        created_actors.append(chin["actor"])

        # REALISTIC EYES - No glow, deep-set in stone sockets
        for side in [-1, 1]:
            # Eye socket (deep hollow)
            socket_scale = (scale * 0.12, scale * 0.1, scale * 0.12)
            socket_pos = (position[0] + side * scale * 0.18, position[1] - scale * 0.32, position[2] + scale * 2.55)
            socket = self._create_composite_cube(f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, scratch_dark)
            created_actors.append(socket["actor"])

            # Eye itself (dull stone-like, not glowing)
            eye_scale = (scale * 0.08, scale * 0.08, scale * 0.06)
            eye_pos = (position[0] + side * scale * 0.18, position[1] - scale * 0.35, position[2] + scale * 2.55)
            eye = self._create_composite_cube(f"{name}_Eye_{'L' if side < 0 else 'R'}", eye_pos, eye_scale, (0.35, 0.28, 0.22))
            created_actors.append(eye["actor"])

            # Eyelid/ridge
            eyelid_scale = (scale * 0.1, scale * 0.04, scale * 0.08)
            eyelid_pos = (position[0] + side * scale * 0.18, position[1] - scale * 0.3, position[2] + scale * 2.62)
            eyelid = self._create_composite_cube(f"{name}_Eyelid_{'L' if side < 0 else 'R'}", eyelid_pos, eyelid_scale, basalt_dark)
            created_actors.append(eyelid["actor"])

        # Nose (flat, wide)
        nose_scale = (scale * 0.15, scale * 0.15, scale * 0.1)
        nose_pos = (position[0], position[1] - scale * 0.5, position[2] + scale * 2.5)
        nose = self._create_composite_cube(f"{name}_Nose", nose_pos, nose_pos, basalt_mid)
        created_actors.append(nose["actor"])

        # Nostrils
        for side in [-1, 1]:
            nostril_scale = (scale * 0.04, scale * 0.06, scale * 0.04)
            nostril_pos = (position[0] + side * scale * 0.05, position[1] - scale * 0.52, position[2] + scale * 2.48)
            nostril = self._create_composite_cube(f"{name}_Nostril_{'L' if side < 0 else 'R'}", nostril_pos, nostril_scale, scratch_dark)
            created_actors.append(nostril["actor"])

        # MOUTH - Realistic stone lips/jaw line
        mouth_scale = (scale * 0.35, scale * 0.06, scale * 0.08)
        mouth_pos = (position[0], position[1] - scale * 0.42, position[2] + scale * 2.3)
        mouth = self._create_composite_cube(f"{name}_Mouth", mouth_pos, mouth_scale, scratch_dark)
        created_actors.append(mouth["actor"])

        # Teeth (stone, not ivory)
        for i in range(6):
            tooth_scale = (scale * 0.04, scale * 0.08, scale * 0.04)
            tooth_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.12,
                position[1] - scale * 0.43,
                position[2] + scale * 2.32 + (i // 2) * scale * 0.05
            )
            tooth = self._create_composite_cube(f"{name}_Tooth_{i}", tooth_pos, tooth_scale, granite_light)
            created_actors.append(tooth["actor"])

        # HORNS - Multiple mineral crowns (realistic weathered stone)
        # Main crown horns
        for i in range(4):
            angle = (math.pi * i) / 4
            # Horn base
            horn_base_scale = (scale * 0.12, scale * 0.12, scale * 0.08)
            horn_base_pos = (
                head_pos[0] + scale * 0.32 * math.cos(angle),
                head_pos[1] + scale * 0.32 * math.sin(angle),
                head_pos[2] + scale * 0.2
            )
            horn_base = self._create_composite_cube(f"{name}_Horn{i}_Base", horn_base_pos, horn_base_scale, basalt_mid)
            created_actors.append(horn_base["actor"])

            # Horn shaft (curved)
            for j in range(3):
                horn_segment_scale = (scale * (0.1 - j * 0.02), scale * (0.1 - j * 0.02), scale * 0.15)
                horn_segment_pos = (
                    head_pos[0] + scale * (0.32 + j * 0.08) * math.cos(angle),
                    head_pos[1] + scale * (0.32 + j * 0.08) * math.sin(angle),
                    head_pos[2] + scale * (0.25 + j * 0.12)
                )
                horn_segment = self._create_composite_cube(f"{name}_Horn{i}_Segment{j}", horn_segment_pos, horn_segment_scale, iron_oxide)
                created_actors.append(horn_segment["actor"])

            # Horn tip (worn, weathered)
            tip_scale = (scale * 0.04, scale * 0.04, scale * 0.06)
            tip_pos = (
                head_pos[0] + scale * 0.5 * math.cos(angle),
                head_pos[1] + scale * 0.5 * math.sin(angle),
                head_pos[2] + scale * 0.65
            )
            tip = self._create_composite_cube(f"{name}_Horn{i}_Tip", tip_pos, tip_scale, scratch_dark)
            created_actors.append(tip["actor"])

        # Smaller forehead horns
        for i in range(3):
            small_horn_scale = (scale * 0.06, scale * 0.06, scale * 0.15)
            angle = (math.pi * (i + 1)) / 4
            small_horn_pos = (
                head_pos[0] + scale * 0.2 * math.cos(angle),
                head_pos[1] + scale * 0.2 * math.sin(angle),
                head_pos[2] + scale * 0.1
            )
            small_horn = self._create_composite_cube(f"{name}_SmallHorn_{i}", small_horn_pos, small_horn_scale, basalt_mid)
            created_actors.append(small_horn["actor"])

        # Ears (small, pointed, stone-like)
        for side in [-1, 1]:
            ear_scale = (scale * 0.08, scale * 0.12, scale * 0.1)
            ear_pos = (position[0] + side * scale * 0.28, position[1] - scale * 0.15, head_pos[2] + scale * 0.05)
            ear = self._create_composite_cube(f"{name}_Ear_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, basalt_mid)
            created_actors.append(ear["actor"])

        # ============================================================
        # ARMS - Complete anatomical structure with bones
        # ============================================================

        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Shoulder joint bone
            shoulder_pos = (position[0] + side * scale * 0.85, position[1], position[2] + scale * 1.6)
            shoulder_bone = self._create_bone_joint(f"{name}_Shoulder_{side_name}", shoulder_pos, scale)
            created_actors.append(shoulder_bone["actor"])

            # Upper arm (humerus)
            humerus_scale = (scale * 0.35, scale * 0.35, scale * 0.7)
            humerus_pos = (position[0] + side * scale * 1.0, position[1], position[2] + scale * 1.3)
            humerus = self._create_composite_cube(f"{name}_Humerus_{side_name}", humerus_pos, humerus_scale, basalt_dark)
            created_actors.append(humerus["actor"])

            # Bicep/tricep muscle definition
            bicep_scale = (scale * 0.38, scale * 0.18, scale * 0.5)
            bicep_pos = (position[0] + side * scale * 1.05, position[1] - scale * 0.15, position[2] + scale * 1.35)
            bicep = self._create_composite_cube(f"{name}_Bicep_{side_name}", bicep_pos, bicep_scale, basalt_mid)
            created_actors.append(bicep["actor"])

            tricep_scale = (scale * 0.32, scale * 0.16, scale * 0.45)
            tricep_pos = (position[0] + side * scale * 1.05, position[1] + scale * 0.15, position[2] + scale * 1.35)
            tricep = self._create_composite_cube(f"{name}_Tricep_{side_name}", tricep_pos, tricep_scale, basalt_mid)
            created_actors.append(tricep["actor"])

            # Elbow joint
            elbow_pos = (position[0] + side * scale * 1.0, position[1], position[2] + scale * 0.9)
            elbow_bone = self._create_bone_joint(f"{name}_Elbow_{side_name}", elbow_pos, scale)
            created_actors.append(elbow_bone["actor"])

            # Elbow joint detail
            elbow_scale = (scale * 0.25, scale * 0.25, scale * 0.2)
            elbow_detail_pos = (position[0] + side * scale * 1.0, position[1], position[2] + scale * 0.9)
            elbow = self._create_composite_cube(f"{name}_Elbow_{side_name}", elbow_detail_pos, elbow_scale, granite_light)
            created_actors.append(elbow["actor"])

            # Forearm (radius/ulna)
            forearm_scale = (scale * 0.3, scale * 0.35, scale * 0.8)
            forearm_pos = (position[0] + side * scale * 1.0, position[1], position[2] + scale * 0.6)
            forearm = self._create_composite_cube(f"{name}_Forearm_{side_name}", forearm_pos, forearm_scale, basalt_dark)
            created_actors.append(forearm["actor"])

            # Forearm muscle definition
            for k in range(3):
                muscle_scale = (scale * 0.28, scale * 0.08, scale * 0.25)
                muscle_pos = (
                    position[0] + side * scale * 1.0,
                    position[1] + ((k % 2) - 0.5) * scale * 0.2,
                    position[2] + scale * 0.5 + k * scale * 0.15
                )
                muscle = self._create_composite_cube(f"{name}_ForearmMuscle_{side_name}_{k}", muscle_pos, muscle_scale, basalt_mid)
                created_actors.append(muscle["actor"])

            # Wrist joint
            wrist_pos = (position[0] + side * scale * 1.0, position[1], position[2] + scale * 0.2)
            wrist_bone = self._create_bone_joint(f"{name}_Wrist_{side_name}", wrist_pos, scale)
            created_actors.append(wrist_bone["actor"])

            # Wrist detail
            wrist_scale = (scale * 0.22, scale * 0.2, scale * 0.12)
            wrist_detail_pos = (position[0] + side * scale * 1.0, position[1], position[2] + scale * 0.2)
            wrist = self._create_composite_cube(f"{name}_Wrist_{side_name}", wrist_detail_pos, wrist_scale, granite_light)
            created_actors.append(wrist["actor"])

            # HAND - Massive battering ram fist
            palm_scale = (scale * 0.4, scale * 0.25, scale * 0.3)
            palm_pos = (position[0] + side * scale * 1.0, position[1] - scale * 0.25, position[2] + scale * 0.15)
            palm = self._create_composite_cube(f"{name}_Palm_{side_name}", palm_pos, palm_scale, basalt_mid)
            created_actors.append(palm["actor"])

            # Fingers (5 fingers - thumb + 4)
            finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
            finger_offsets = [(-0.2, -0.35, 0.25), (0.15, -0.4, 0.35), (0.22, -0.4, 0.32), (0.15, -0.38, 0.28), (0.08, -0.35, 0.22)]

            for f, finger_name in enumerate(finger_names):
                # Finger joints (3 segments per finger)
                for seg in range(3):
                    finger_scale = (
                        scale * (0.12 - seg * 0.02),  # Tapering
                        scale * 0.1,
                        scale * (0.1 - seg * 0.015)
                    )
                    finger_pos = (
                        position[0] + side * scale * (1.0 + finger_offsets[f][0] + seg * 0.08),
                        position[1] + scale * finger_offsets[f][1],
                        position[2] + scale * (0.15 + finger_offsets[f][2] + seg * 0.08)
                    )
                    finger = self._create_composite_cube(
                        f"{name}_Finger_{side_name}_{finger_name}_{seg}",
                        finger_pos, finger_scale, basalt_dark
                    )
                    created_actors.append(finger["actor"])

                    # Finger joint (knuckle)
                    if seg < 2:
                        knuckle_scale = (scale * 0.11, scale * 0.11, scale * 0.08)
                        knuckle_pos = (
                            position[0] + side * scale * (1.0 + finger_offsets[f][0] + (seg + 1) * 0.08),
                            position[1] + scale * finger_offsets[f][1],
                            position[2] + scale * (0.15 + finger_offsets[f][2] + seg * 0.08)
                        )
                        knuckle = self._create_composite_cube(
                            f"{name}_Knuckle_{side_name}_{finger_name}_{seg}",
                            knuckle_pos, knuckle_scale, granite_light
                        )
                        created_actors.append(knuckle["actor"])

            # Knuckles (weathered/worn)
            for f in range(4):
                knuckle_wear_scale = (scale * 0.08, scale * 0.04, scale * 0.06)
                knuckle_wear_pos = (
                    position[0] + side * scale * 1.15,
                    position[1] - scale * 0.38,
                    position[2] + scale * (0.45 + f * 0.04)
                )
                knuckle_wear = self._create_composite_cube(
                    f"{name}_KnuckleWear_{side_name}_{f}",
                    knuckle_wear_pos, knuckle_wear_scale, scratch_dark
                )
                created_actors.append(knuckle_wear["actor"])

        # ============================================================
        # LEGS - Complete anatomical structure
        # ============================================================

        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Hip joint
            hip_pos = (position[0] + side * scale * 0.4, position[1], position[2] + scale * 0.4)
            hip_bone = self._create_bone_joint(f"{name}_Hip_{side_name}", hip_pos, scale)
            created_actors.append(hip_bone["actor"])

            # Thigh (femur)
            thigh_scale = (scale * 0.4, scale * 0.45, scale * 1.0)
            thigh_pos = (position[0] + side * scale * 0.4, position[1], position[2] + scale * 0.2)
            thigh = self._create_composite_cube(f"{name}_Thigh_{side_name}", thigh_pos, thigh_scale, basalt_dark)
            created_actors.append(thigh["actor"])

            # Quadriceps muscle definition
            for q in range(4):
                quad_scale = (scale * 0.38, scale * 0.1, scale * 0.25)
                quad_pos = (
                    position[0] + side * scale * 0.4,
                    position[1] + ((q % 2) - 0.5) * scale * 0.22,
                    position[2] + scale * (0.15 + (q // 2) * scale * 0.25)
                )
                quad = self._create_composite_cube(f"{name}_Quad_{side_name}_{q}", quad_pos, quad_scale, basalt_mid)
                created_actors.append(quad["actor"])

            # Knee joint
            knee_pos = (position[0] + side * scale * 0.4, position[1], position[2] - scale * 0.5)
            knee_bone = self._create_bone_joint(f"{name}_Knee_{side_name}", knee_pos, scale)
            created_actors.append(knee_bone["actor"])

            # Knee detail (patella)
            patella_scale = (scale * 0.25, scale * 0.2, scale * 0.15)
            patella_pos = (position[0] + side * scale * 0.4, position[1], position[2] - scale * 0.5)
            patella = self._create_composite_cube(f"{name}_Patella_{side_name}", patella_pos, patella_scale, granite_light)
            created_actors.append(patella["actor"])

            # Lower leg (tibia/fibula)
            shin_scale = (scale * 0.3, scale * 0.35, scale * 0.9)
            shin_pos = (position[0] + side * scale * 0.4, position[1], position[2] - scale * 1.0)
            shin = self._create_composite_cube(f"{name}_Shin_{side_name}", shin_pos, shin_scale, basalt_dark)
            created_actors.append(shin["actor"])

            # Calf muscle
            calf_scale = (scale * 0.32, scale * 0.2, scale * 0.5)
            calf_pos = (position[0] + side * scale * 0.4, position[1] - scale * 0.15, position[2] - scale * 1.1)
            calf = self._create_composite_cube(f"{name}_Calf_{side_name}", calf_pos, calf_scale, basalt_mid)
            created_actors.append(calf["actor"])

            # Shin bone detail
            for s in range(3):
                shin_detail_scale = (scale * 0.28, scale * 0.06, scale * 0.28)
                shin_detail_pos = (
                    position[0] + side * scale * 0.4,
                    position[1] + ((s % 2) - 0.5) * scale * 0.18,
                    position[2] + scale * (-1.2 + s * scale * 0.25)
                )
                shin_detail = self._create_composite_cube(f"{name}_ShinDetail_{side_name}_{s}", shin_detail_pos, shin_detail_scale, basalt_mid)
                created_actors.append(shin_detail["actor"])

            # Ankle joint
            ankle_pos = (position[0] + side * scale * 0.4, position[1], position[2] - scale * 1.6)
            ankle_bone = self._create_bone_joint(f"{name}_Ankle_{side_name}", ankle_pos, scale)
            created_actors.append(ankle_bone["actor"])

            # Ankle detail
            ankle_scale = (scale * 0.22, scale * 0.18, scale * 0.12)
            ankle_detail_pos = (position[0] + side * scale * 0.4, position[1], position[2] - scale * 1.6)
            ankle = self._create_composite_cube(f"{name}_Ankle_{side_name}", ankle_detail_pos, ankle_scale, granite_light)
            created_actors.append(ankle["actor"])

            # FOOT - Massive weight-bearing structure
            foot_scale = (scale * 0.35, scale * 0.2, scale * 0.5)
            foot_pos = (position[0] + side * scale * 0.4, position[1] - scale * 0.15, position[2] - scale * 2.0)
            foot = self._create_composite_cube(f"{name}_Foot_{side_name}", foot_pos, foot_scale, basalt_dark)
            created_actors.append(foot["actor"])

            # Toes (3 main toes)
            for t in range(3):
                toe_scale = (scale * 0.12, scale * 0.15, scale * 0.25)
                toe_pos = (
                    position[0] + side * scale * 0.4 + (t - 1) * scale * 0.08,
                    position[1] - scale * 0.25,
                    position[2] - scale * (2.2 + t * scale * 0.1)
                )
                toe = self._create_composite_cube(f"{name}_Toe_{side_name}_{t}", toe_pos, toe_scale, basalt_mid)
                created_actors.append(toe["actor"])

            # Toe joints
            for t in range(3):
                joint_scale = (scale * 0.1, scale * 0.12, scale * 0.08)
                joint_pos = (
                    position[0] + side * scale * 0.4 + (t - 1) * scale * 0.08,
                    position[1] - scale * 0.25,
                    position[2] - scale * (2.1 + t * scale * 0.1)
                )
                joint = self._create_composite_cube(f"{name}_ToeJoint_{side_name}_{t}", joint_pos, joint_scale, granite_light)
                created_actors.append(joint["actor"])

            # Heel
            heel_scale = (scale * 0.2, scale * 0.15, scale * 0.15)
            heel_pos = (position[0] + side * scale * 0.4, position[1] - scale * 0.15, position[2] - scale * 2.15)
            heel = self._create_composite_cube(f"{name}_Heel_{side_name}", heel_pos, heel_scale, basalt_dark)
            created_actors.append(heel["actor"])

        # ============================================================
        # TAIL - Weighty club with anatomical structure
        # ============================================================

        # Tail vertebrae (spine structure)
        for i in range(5):
            vertebra_scale = (scale * 0.35, scale * 0.35, scale * 0.12)
            vertebra_pos = (position[0], position[1] + scale * (0.8 + i * 0.25), position[2] + scale * 0.3)
            vertebra = self._create_composite_cube(f"{name}_TailVertebra_{i}", vertebra_pos, vertebra_scale, basalt_mid)
            created_actors.append(vertebra["actor"])

        # Tail base muscle
        tail_base_scale = (scale * 0.4, scale * 0.4, scale * 0.6)
        tail_base_pos = (position[0], position[1] + scale * 0.8, position[2] + scale * 0.3)
        tail_base = self._create_composite_cube(f"{name}_Tail_Base", tail_base_pos, tail_base_scale, basalt_dark)
        created_actors.append(tail_base["actor"])

        # Tail segments
        for i in range(4):
            segment_scale = (scale * (0.38 - i * 0.05), scale * (0.38 - i * 0.05), scale * 0.5)
            segment_pos = (position[0], position[1] + scale * (1.1 + i * 0.4), position[2] + scale * 0.25)
            segment = self._create_composite_cube(f"{name}_Tail_Segment_{i}", segment_pos, segment_scale, basalt_dark)
            created_actors.append(segment["actor"])

        # Tail club (massive crushing weapon)
        club_scale = (scale * 0.7, scale * 0.7, scale * 0.8)
        club_pos = (position[0], position[1] + scale * 2.5, position[2] + scale * 0.2)
        club = self._create_composite_cube(f"{name}_Tail_Club", club_pos, club_pos, basalt_dark)
        created_actors.append(club["actor"])

        # Club spikes (6 spikes around the club)
        for i in range(6):
            spike_scale = (scale * 0.1, scale * 0.3, scale * 0.1)
            angle = (2 * math.pi * i) / 6
            spike_pos = (
                position[0] + scale * 0.5 * math.cos(angle),
                position[1] + scale * 2.5 + scale * 0.5 * math.sin(angle),
                position[2] + scale * 0.2
            )
            spike = self._create_composite_cube(f"{name}_ClubSpike_{i}", spike_pos, spike_scale, iron_oxide)
            created_actors.append(spike["actor"])

            # Spike wear/damage at tips
            tip_scale = (scale * 0.04, scale * 0.08, scale * 0.04)
            tip_pos = (
                position[0] + scale * 0.65 * math.cos(angle),
                position[1] + scale * 2.5 + scale * 0.65 * math.sin(angle),
                position[2] + scale * 0.2
            )
            tip = self._create_composite_cube(f"{name}_ClubSpikeTip_{i}", tip_pos, tip_pos, scratch_dark)
            created_actors.append(tip["actor"])

        # ============================================================
        # SURFACE DETAIL - Weathering, damage, lichen
        # ============================================================

        # Lichen patches (natural growth on stone)
        for i in range(8):
            lichen_scale = (scale * 0.2, scale * 0.03, scale * 0.2)
            lichen_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.5,
                position[1] + ((i // 4) % 2) * scale * 0.5,
                position[2] + scale * (0.5 + (i // 2) * scale * 0.6)
            )
            lichen = self._create_composite_cube(f"{name}_Lichen_{i}", lichen_pos, lichen_scale, lichen_green)
            created_actors.append(lichen["actor"])

        # Scratch marks (battle damage)
        for i in range(5):
            scratch_scale = (scale * 0.4, scale * 0.02, scale * 0.08)
            scratch_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.3,
                position[1] + scale * 0.9,
                position[2] + scale * (0.8 + i * scale * 0.3)
            )
            scratch = self._create_composite_cube(f"{name}_Scratch_{i}", scratch_pos, scratch_scale, scratch_dark)
            created_actors.append(scratch["actor"])

        # Dust/dirt accumulation in crevices
        for i in range(10):
            dust_scale = (scale * 0.15, scale * 0.02, scale * 0.12)
            dust_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.4,
                position[1] + scale * 0.92,
                position[2] + scale * (0.3 + (i // 3) * scale * 0.5)
            )
            dust = self._create_composite_cube(f"{name}_Dust_{i}", dust_pos, dust_scale, dust_gray)
            created_actors.append(dust["actor"])

        # Iron oxide staining (rust streaks)
        for i in range(4):
            stain_scale = (scale * 0.08, scale * 0.4, scale * 0.04)
            stain_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.6,
                position[1] + scale * 0.9,
                position[2] + scale * (0.6 + (i // 2) * scale * 0.7)
            )
            stain = self._create_composite_cube(f"{name}_IronStain_{i}", stain_pos, stain_scale, iron_oxide)
            created_actors.append(stain["actor"])

        # Surface texture variation (different stone types)
        for i in range(12):
            texture_scale = (scale * 0.2, scale * 0.04, scale * 0.2)
            texture_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.35,
                position[1] + ((i // 4) % 2) * scale * 0.5,
                position[2] + scale * (0.3 + (i // 6) * scale * 0.4)
            )
            texture = self._create_composite_cube(f"{name}_Texture_{i}", texture_pos, texture_scale,
                                                 granite_light if i % 2 == 0 else basalt_mid)
            created_actors.append(texture["actor"])

        unreal.log(f"🪨 ROCK DEMON created with {len(created_actors)} components (Realistic + Boned)")
        return {
            "message": f"Created {name} (Rock Demon - Realistic + Fully Boned)",
            "name": name,
            "type": "rock demon",
            "actors": created_actors,
            "bones": bones  # Return bone references for animation
        }
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
        STONE DEMON (Soft Lock) - REALISTIC ANIMATABLE VERSION
        Compact, quicker version of Rock Demon (5-7 feet)
        Smaller but heavily armored, faster locomotion
        Materials: Real limestone, sandstone, weathered stone surfaces
        Full bone structure for animation
        """
        name = parsed.get("name") or "StoneDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.8

        unreal.log("🗿 Creating STONE DEMON (Realistic + Boned)...")

        created_actors = []
        bones = {}

        # REALISTIC STONE COLORS - Natural weathered appearance
        limestone_base = (0.42, 0.40, 0.35)      # Weathered limestone
        sandstone_light = (0.52, 0.48, 0.40)     # Sandstone highlights
        stone_dark = (0.28, 0.26, 0.22)          # Deep stone cracks
        moss_gray = (0.38, 0.36, 0.32)           # Natural moss growth
        wear_brown = (0.32, 0.28, 0.24)          # Edge wear/damage
        dust_tan = (0.48, 0.45, 0.40)            # Surface dust accumulation

        # SKELETON - BONE STRUCTURE
        pelvis_bone = self._create_bone_joint(f"{name}_Pelvis_Root", position, scale)
        bones["pelvis"] = pelvis_bone
        created_actors.append(pelvis_bone["actor"])

        # Spine (4 articulated vertebrae)
        for i in range(4):
            spine_pos = (position[0], position[1], position[2] + scale * (0.4 + i * 0.35))
            spine_bone = self._create_bone_joint(f"{name}_Spine_{i+1}", spine_pos, scale)
            created_actors.append(spine_bone["actor"])

        # Rib structure
        for i in range(6):
            rib_angle = (math.pi * i) / 6
            rib_pos = (
                position[0] + scale * 0.4 * math.cos(rib_angle),
                position[1] + scale * 0.4 * math.sin(rib_angle),
                position[2] + scale * (0.8 + (i % 2) * 0.25)
            )
            rib_bone = self._create_bone_joint(f"{name}_Rib_{i}", rib_pos, scale)
            created_actors.append(rib_bone["actor"])

        # TORSO - Compact but detailed
        torso_scale = (scale * 0.75, scale * 0.55, scale * 1.3)
        torso_pos = (position[0], position[1], position[2] + scale * 0.65)
        torso = self._create_composite_cube(f"{name}_Torso_Main", torso_pos, torso_scale, limestone_base)
        created_actors.append(torso["actor"])

        # Abdominal definition
        for i in range(4):
            ab_scale = (scale * 0.7, scale * 0.06, scale * 0.2)
            ab_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.02,
                position[1] + scale * 0.57,
                position[2] + scale * 0.25 + (i // 2) * scale * 0.3
            )
            ab = self._create_composite_cube(f"{name}_Ab_{i}", ab_pos, ab_scale, sandstone_light)
            created_actors.append(ab["actor"])

        # Chest plate
        sternum_scale = (scale * 0.55, scale * 0.1, scale * 0.4)
        sternum_pos = (position[0], position[1] + scale * 0.57, position[2] + scale * 0.95)
        sternum = self._create_composite_cube(f"{name}_Sternum", sternum_pos, sternum_scale, sandstone_light)
        created_actors.append(sternum["actor"])

        # SHOULDERS - Streamlined but powerful
        for side in [-1, 1]:
            shoulder_joint_pos = (position[0] + side * scale * 0.5, position[1], position[2] + scale * 1.05)
            shoulder_joint = self._create_bone_joint(f"{name}_ShoulderJoint_{'L' if side < 0 else 'R'}", shoulder_joint_pos, scale)
            created_actors.append(shoulder_joint["actor"])

            # Deltoid muscle
            delt_scale = (scale * 0.35, scale * 0.3, scale * 0.45)
            delt_pos = (position[0] + side * scale * 0.5, position[1], position[2] + scale * 1.05)
            delt = self._create_composite_cube(f"{name}_Deltoid_{'L' if side < 0 else 'R'}", delt_pos, delt_scale, limestone_base)
            created_actors.append(delt["actor"])

            # Clavicle
            clavicle_scale = (scale * 0.35, scale * 0.08, scale * 0.18)
            clavicle_pos = (position[0] + side * scale * 0.4, position[1], position[2] + scale * 1.2)
            clavicle = self._create_composite_cube(f"{name}_Clavicle_{'L' if side < 0 else 'R'}", clavicle_pos, clavicle_scale, sandstone_light)
            created_actors.append(clavicle["actor"])

        # NECK - Streamlined column
        for i in range(3):
            vertebra_scale = (scale * 0.25, scale * 0.25, scale * 0.1)
            vertebra_pos = (position[0], position[1], position[2] + scale * (1.45 + i * 0.12))
            vertebra = self._create_composite_cube(f"{name}_NeckVertebra_{i}", vertebra_pos, vertebra_scale, limestone_base)
            created_actors.append(vertebra["actor"])

        neck_scale = (scale * 0.35, scale * 0.32, scale * 0.35)
        neck_pos = (position[0], position[1], position[2] + scale * 1.5)
        neck = self._create_composite_cube(f"{name}_Neck_Main", neck_pos, neck_scale, limestone_base)
        created_actors.append(neck["actor"])

        # HEAD - Compact horned cranium
        skull_scale = (scale * 0.35, scale * 0.42, scale * 0.32)
        skull_pos = (position[0], position[1], position[2] + scale * 1.75)
        skull = self._create_composite_cube(f"{name}_Skull", skull_pos, skull_scale, limestone_base)
        created_actors.append(skull["actor"])

        # Brow ridge
        brow_scale = (scale * 0.32, scale * 0.08, scale * 0.1)
        brow_pos = (position[0], position[1] - scale * 0.22, position[2] + scale * 1.9)
        brow = self._create_composite_cube(f"{name}_BrowRidge", brow_pos, brow_scale, sandstone_light)
        created_actors.append(brow["actor"])

        # Cheek bones
        for side in [-1, 1]:
            cheek_scale = (scale * 0.12, scale * 0.1, scale * 0.12)
            cheek_pos = (position[0] + side * scale * 0.16, position[1] - scale * 0.2, position[2] + scale * 1.75)
            cheek = self._create_composite_cube(f"{name}_Cheek_{'L' if side < 0 else 'R'}", cheek_pos, cheek_scale, limestone_base)
            created_actors.append(cheek["actor"])

        # Jaw
        jaw_scale = (scale * 0.28, scale * 0.12, scale * 0.18)
        jaw_pos = (position[0], position[1] - scale * 0.25, position[2] + scale * 1.65)
        jaw = self._create_composite_cube(f"{name}_Jaw", jaw_pos, jaw_scale, limestone_base)
        created_actors.append(jaw["actor"])

        # Chin
        chin_scale = (scale * 0.15, scale * 0.1, scale * 0.1)
        chin_pos = (position[0], position[1] - scale * 0.28, position[2] + scale * 1.62)
        chin = self._create_composite_cube(f"{name}_Chin", chin_pos, chin_scale, limestone_base)
        created_actors.append(chin["actor"])

        # REALISTIC EYES - Deep set, dull stone appearance (NO GLOW)
        for side in [-1, 1]:
            # Eye socket (deep hollow)
            socket_scale = (scale * 0.08, scale * 0.07, scale * 0.08)
            socket_pos = (position[0] + side * scale * 0.12, position[1] - scale * 0.22, position[2] + scale * 1.8)
            socket = self._create_composite_cube(f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, stone_dark)
            created_actors.append(socket["actor"])

            # Eye (dull stone gray)
            eye_scale = (scale * 0.05, scale * 0.05, scale * 0.04)
            eye_pos = (position[0] + side * scale * 0.12, position[1] - scale * 0.25, position[2] + scale * 1.8)
            eye = self._create_composite_cube(f"{name}_Eye_{'L' if side < 0 else 'R'}", eye_pos, eye_scale, (0.38, 0.32, 0.28))
            created_actors.append(eye["actor"])

            # Eyelid
            eyelid_scale = (scale * 0.06, scale * 0.03, scale * 0.05)
            eyelid_pos = (position[0] + side * scale * 0.12, position[1] - scale * 0.2, position[2] + scale * 1.85)
            eyelid = self._create_composite_cube(f"{name}_Eyelid_{'L' if side < 0 else 'R'}", eyelid_pos, eyelid_scale, limestone_base)
            created_actors.append(eyelid["actor"])

        # Nose (broad, flat)
        nose_scale = (scale * 0.1, scale * 0.1, scale * 0.08)
        nose_pos = (position[0], position[1] - scale * 0.32, position[2] + scale * 1.75)
        nose = self._create_composite_cube(f"{name}_Nose", nose_pos, nose_scale, limestone_base)
        created_actors.append(nose["actor"])

        # Nostrils
        for side in [-1, 1]:
            nostril_scale = (scale * 0.025, scale * 0.04, scale * 0.025)
            nostril_pos = (position[0] + side * scale * 0.035, position[1] - scale * 0.34, position[2] + scale * 1.73)
            nostril = self._create_composite_cube(f"{name}_Nostril_{'L' if side < 0 else 'R'}", nostril_pos, nostril_scale, stone_dark)
            created_actors.append(nostril["actor"])

        # Mouth
        mouth_scale = (scale * 0.25, scale * 0.04, scale * 0.06)
        mouth_pos = (position[0], position[1] - scale * 0.27, position[2] + scale * 1.62)
        mouth = self._create_composite_cube(f"{name}_Mouth", mouth_pos, mouth_scale, stone_dark)
        created_actors.append(mouth["actor"])

        # Teeth (worn stone)
        for i in range(4):
            tooth_scale = (scale * 0.03, scale * 0.05, scale * 0.03)
            tooth_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.08,
                position[1] - scale * 0.28,
                position[2] + scale * (1.62 + (i // 2) * scale * 0.04)
            )
            tooth = self._create_composite_cube(f"{name}_Tooth_{i}", tooth_pos, tooth_scale, sandstone_light)
            created_actors.append(tooth["actor"])

        # HORNS - Two main weathered horns
        for side in [-1, 1]:
            # Horn base
            horn_base_scale = (scale * 0.08, scale * 0.08, scale * 0.06)
            horn_base_pos = (position[0] + side * scale * 0.18, position[1], position[2] + scale * 1.87)
            horn_base = self._create_composite_cube(f"{name}_HornBase_{'L' if side < 0 else 'R'}", horn_base_pos, horn_base_scale, limestone_base)
            created_actors.append(horn_base["actor"])

            # Horn shaft (curved)
            for j in range(2):
                horn_seg_scale = (scale * (0.07 - j * 0.015), scale * (0.07 - j * 0.015), scale * 0.12)
                horn_seg_pos = (
                    position[0] + side * scale * (0.18 + j * 0.06),
                    position[1],
                    position[2] + scale * (1.9 + j * 0.1)
                )
                horn_seg = self._create_composite_cube(f"{name}_Horn_{'L' if side < 0 else 'R'}_Seg{j}", horn_seg_pos, horn_seg_scale, sandstone_light)
                created_actors.append(horn_seg["actor"])

            # Horn tip (weathered)
            tip_scale = (scale * 0.035, scale * 0.035, scale * 0.05)
            tip_pos = (position[0] + side * scale * 0.26, position[1], position[2] + scale * 2.05)
            tip = self._create_composite_cube(f"{name}_HornTip_{'L' if side < 0 else 'R'}", tip_pos, tip_scale, wear_brown)
            created_actors.append(tip["actor"])

        # Ears (small pointed)
        for side in [-1, 1]:
            ear_scale = (scale * 0.06, scale * 0.08, scale * 0.08)
            ear_pos = (position[0] + side * scale * 0.2, position[1] - scale * 0.1, position[2] + scale * 1.75)
            ear = self._create_composite_cube(f"{name}_Ear_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, limestone_base)
            created_actors.append(ear["actor"])

        # ARMS - Complete anatomical structure
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Upper arm bone
            humerus_pos = (position[0] + side * scale * 0.55, position[1], position[2] + scale * 0.85)
            humerus_bone = self._create_bone_joint(f"{name}_Humerus_{side_name}", humerus_pos, scale)
            created_actors.append(humerus_bone["actor"])

            # Humerus muscle
            humerus_scale = (scale * 0.22, scale * 0.22, scale * 0.5)
            humerus_pos = (position[0] + side * scale * 0.55, position[1], position[2] + scale * 0.85)
            humerus = self._create_composite_cube(f"{name}_Humerus_{side_name}", humerus_pos, humerus_scale, limestone_base)
            created_actors.append(humerus["actor"])

            # Bicep
            bicep_scale = (scale * 0.24, scale * 0.1, scale * 0.35)
            bicep_pos = (position[0] + side * scale * 0.58, position[1] - scale * 0.1, position[2] + scale * 0.9)
            bicep = self._create_composite_cube(f"{name}_Bicep_{side_name}", bicep_pos, bicep_scale, sandstone_light)
            created_actors.append(bicep["actor"])

            # Elbow joint
            elbow_pos = (position[0] + side * scale * 0.55, position[1], position[2] + scale * 0.55)
            elbow_bone = self._create_bone_joint(f"{name}_Elbow_{side_name}", elbow_pos, scale)
            created_actors.append(elbow_bone["actor"])

            # Elbow detail
            elbow_scale = (scale * 0.18, scale * 0.18, scale * 0.15)
            elbow_pos = (position[0] + side * scale * 0.55, position[1], position[2] + scale * 0.55)
            elbow = self._create_composite_cube(f"{name}_Elbow_{side_name}", elbow_pos, elbow_scale, sandstone_light)
            created_actors.append(elbow["actor"])

            # Forearm
            forearm_scale = (scale * 0.18, scale * 0.2, scale * 0.55)
            forearm_pos = (position[0] + side * scale * 0.55, position[1], position[2] + scale * 0.4)
            forearm = self._create_composite_cube(f"{name}_Forearm_{side_name}", forearm_pos, forearm_scale, limestone_base)
            created_actors.append(forearm["actor"])

            # Forearm muscles
            for k in range(2):
                muscle_scale = (scale * 0.17, scale * 0.06, scale * 0.18)
                muscle_pos = (
                    position[0] + side * scale * 0.55,
                    position[1] + ((k % 2) - 0.5) * scale * 0.15,
                    position[2] + scale * (0.35 + k * scale * 0.15)
                )
                muscle = self._create_composite_cube(f"{name}_ForearmMuscle_{side_name}_{k}", muscle_pos, muscle_scale, sandstone_light)
                created_actors.append(muscle["actor"])

            # Wrist joint
            wrist_pos = (position[0] + side * scale * 0.55, position[1], position[2] + scale * 0.1)
            wrist_bone = self._create_bone_joint(f"{name}_Wrist_{side_name}", wrist_pos, scale)
            created_actors.append(wrist_bone["actor"])

            # Wrist detail
            wrist_scale = (scale * 0.15, scale * 0.15, scale * 0.1)
            wrist_pos = (position[0] + side * scale * 0.55, position[1], position[2] + scale * 0.1)
            wrist = self._create_composite_cube(f"{name}_Wrist_{side_name}", wrist_pos, wrist_scale, sandstone_light)
            created_actors.append(wrist["actor"])

            # HAND - Compact but detailed
            palm_scale = (scale * 0.28, scale * 0.18, scale * 0.2)
            palm_pos = (position[0] + side * scale * 0.55, position[1] - scale * 0.2, position[2] + scale * 0.05)
            palm = self._create_composite_cube(f"{name}_Palm_{side_name}", palm_pos, palm_scale, limestone_base)
            created_actors.append(palm["actor"])

            # Fingers (4 fingers + thumb)
            finger_offsets = [
                (-0.12, -0.28, 0.18),  # Thumb
                (0.1, -0.32, 0.22),    # Index
                (0.14, -0.31, 0.2),     # Middle
                (0.1, -0.29, 0.18)      # Ring
            ]

            for f in range(4):
                for seg in range(2):
                    finger_scale = (scale * (0.08 - seg * 0.015), scale * 0.08, scale * (0.06 - seg * 0.01))
                    finger_pos = (
                        position[0] + side * scale * (0.55 + finger_offsets[f][0] + seg * 0.06),
                        position[1] + scale * finger_offsets[f][1],
                        position[2] + scale * (0.05 + finger_offsets[f][2] + seg * 0.06)
                    )
                    finger = self._create_composite_cube(f"{name}_Finger_{side_name}_{f}_{seg}", finger_pos, finger_scale, limestone_base)
                    created_actors.append(finger["actor"])

        # LEGS - Complete anatomical structure
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Hip joint
            hip_pos = (position[0] + side * scale * 0.25, position[1], position[2] + scale * 0.3)
            hip_bone = self._create_bone_joint(f"{name}_Hip_{side_name}", hip_pos, scale)
            created_actors.append(hip_bone["actor"])

            # Thigh
            thigh_scale = (scale * 0.28, scale * 0.3, scale * 0.7)
            thigh_pos = (position[0] + side * scale * 0.25, position[1], position[2] + scale * 0.15)
            thigh = self._create_composite_cube(f"{name}_Thigh_{side_name}", thigh_pos, thigh_scale, limestone_base)
            created_actors.append(thigh["actor"])

            # Quadriceps
            for q in range(3):
                quad_scale = (scale * 0.26, scale * 0.08, scale * 0.18)
                quad_pos = (
                    position[0] + side * scale * 0.25,
                    position[1] + ((q % 2) - 0.5) * scale * 0.18,
                    position[2] + scale * (0.1 + (q // 2) * scale * 0.2)
                )
                quad = self._create_composite_cube(f"{name}_Quad_{side_name}_{q}", quad_pos, quad_scale, sandstone_light)
                created_actors.append(quad["actor"])

            # Knee joint
            knee_pos = (position[0] + side * scale * 0.25, position[1], position[2] - scale * 0.35)
            knee_bone = self._create_bone_joint(f"{name}_Knee_{side_name}", knee_pos, scale)
            created_actors.append(knee_bone["actor"])

            # Knee detail (patella)
            patella_scale = (scale * 0.18, scale * 0.15, scale * 0.12)
            patella_pos = (position[0] + side * scale * 0.25, position[1], position[2] - scale * 0.35)
            patella = self._create_composite_cube(f"{name}_Patella_{side_name}", patella_pos, patella_scale, sandstone_light)
            created_actors.append(patella["actor"])

            # Shin
            shin_scale = (scale * 0.2, scale * 0.25, scale * 0.6)
            shin_pos = (position[0] + side * scale * 0.25, position[1], position[2] - scale * 0.65)
            shin = self._create_composite_cube(f"{name}_Shin_{side_name}", shin_pos, shin_scale, limestone_base)
            created_actors.append(shin["actor"])

            # Calf muscle
            calf_scale = (scale * 0.22, scale * 0.12, scale * 0.35)
            calf_pos = (position[0] + side * scale * 0.25, position[1] - scale * 0.1, position[2] - scale * 0.75)
            calf = self._create_composite_cube(f"{name}_Calf_{side_name}", calf_pos, calf_scale, sandstone_light)
            created_actors.append(calf["actor"])

            # Shin bone detail
            for s in range(2):
                detail_scale = (scale * 0.18, scale * 0.05, scale * 0.2)
                detail_pos = (
                    position[0] + side * scale * 0.25,
                    position[1] + ((s % 2) - 0.5) * scale * 0.13,
                    position[2] + scale * (-0.85 + s * scale * 0.3)
                )
                detail = self._create_composite_cube(f"{name}_ShinDetail_{side_name}_{s}", detail_pos, detail_scale, limestone_base)
                created_actors.append(detail["actor"])

            # Ankle joint
            ankle_pos = (position[0] + side * scale * 0.25, position[1], position[2] - scale * 1.0)
            ankle_bone = self._create_bone_joint(f"{name}_Ankle_{side_name}", ankle_pos, scale)
            created_actors.append(ankle_bone["actor"])

            # Ankle detail
            ankle_scale = (scale * 0.16, scale * 0.13, scale * 0.1)
            ankle_detail_pos = (position[0] + side * scale * 0.25, position[1], position[2] - scale * 1.0)
            ankle = self._create_composite_cube(f"{name}_Ankle_{side_name}", ankle_detail_pos, ankle_scale, sandstone_light)
            created_actors.append(ankle["actor"])

            # FOOT
            foot_scale = (scale * 0.25, scale * 0.15, scale * 0.35)
            foot_pos = (position[0] + side * scale * 0.25, position[1] - scale * 0.1, position[2] - scale * 1.25)
            foot = self._create_composite_cube(f"{name}_Foot_{side_name}", foot_pos, foot_scale, limestone_base)
            created_actors.append(foot["actor"])

            # Toes (3 main toes)
            for t in range(3):
                toe_scale = (scale * 0.08, scale * 0.1, scale * 0.18)
                toe_pos = (
                    position[0] + side * scale * 0.25 + (t - 1) * scale * 0.06,
                    position[1] - scale * 0.18,
                    position[2] - scale * (1.35 + t * scale * 0.08)
                )
                toe = self._create_composite_cube(f"{name}_Toe_{side_name}_{t}", toe_pos, toe_scale, limestone_base)
                created_actors.append(toe["actor"])

            # Toe joints
            for t in range(3):
                joint_scale = (scale * 0.07, scale * 0.08, scale * 0.06)
                joint_pos = (
                    position[0] + side * scale * 0.25 + (t - 1) * scale * 0.06,
                    position[1] - scale * 0.18,
                    position[2] - scale * (1.28 + t * scale * 0.07)
                )
                joint = self._create_composite_cube(f"{name}_ToeJoint_{side_name}_{t}", joint_pos, joint_scale, sandstone_light)
                created_actors.append(joint["actor"])

            # Heel
            heel_scale = (scale * 0.14, scale * 0.1, scale * 0.1)
            heel_pos = (position[0] + side * scale * 0.25, position[1] - scale * 0.1, position[2] - scale * 1.38)
            heel = self._create_composite_cube(f"{name}_Heel_{side_name}", heel_pos, heel_scale, limestone_base)
            created_actors.append(heel["actor"])

        # TAIL - Streamlined club
        # Tail vertebrae
        for i in range(3):
            vertebra_scale = (scale * 0.25, scale * 0.25, scale * 0.1)
            vertebra_pos = (position[0], position[1] + scale * (0.6 + i * 0.2), position[2] + scale * 0.2)
            vertebra = self._create_composite_cube(f"{name}_TailVertebra_{i}", vertebra_pos, vertebra_scale, limestone_base)
            created_actors.append(vertebra["actor"])

        # Tail base
        tail_base_scale = (scale * 0.28, scale * 0.28, scale * 0.4)
        tail_base_pos = (position[0], position[1] + scale * 0.6, position[2] + scale * 0.2)
        tail_base = self._create_composite_cube(f"{name}_Tail_Base", tail_base_pos, tail_base_scale, limestone_base)
        created_actors.append(tail_base["actor"])

        # Tail segments
        for i in range(2):
            segment_scale = (scale * (0.26 - i * 0.04), scale * (0.26 - i * 0.04), scale * 0.35)
            segment_pos = (position[0], position[1] + scale * (0.85 + i * 0.3), position[2] + scale * 0.18)
            segment = self._create_composite_cube(f"{name}_Tail_Segment_{i}", segment_pos, segment_scale, limestone_base)
            created_actors.append(segment["actor"])

        # Tail club (smaller than Rock Demon but still formidable)
        club_scale = (scale * 0.45, scale * 0.45, scale * 0.5)
        club_pos = (position[0], position[1] + scale * 1.35, position[2] + scale * 0.15)
        club = self._create_composite_cube(f"{name}_Tail_Club", club_pos, club_scale, limestone_base)
        created_actors.append(club["actor"])

        # Club spikes (4 spikes)
        for i in range(4):
            spike_scale = (scale * 0.08, scale * 0.22, scale * 0.08)
            angle = (2 * math.pi * i) / 4
            spike_pos = (
                position[0] + scale * 0.4 * math.cos(angle),
                position[1] + scale * 1.35 + scale * 0.35 * math.sin(angle),
                position[2] + scale * 0.15
            )
            spike = self._create_composite_cube(f"{name}_ClubSpike_{i}", spike_pos, spike_scale, sandstone_light)
            created_actors.append(spike["actor"])

            # Spike wear at tips
            tip_scale = (scale * 0.035, scale * 0.06, scale * 0.035)
            tip_pos = (
                position[0] + scale * 0.52 * math.cos(angle),
                position[1] + scale * 1.35 + scale * 0.45 * math.sin(angle),
                position[2] + scale * 0.15
            )
            tip = self._create_composite_cube(f"{name}_ClubSpikeTip_{i}", tip_pos, tip_scale, wear_brown)
            created_actors.append(tip["actor"])

        # SURFACE DETAIL - Realistic weathering
        # Moss patches (natural growth in crevices)
        for i in range(5):
            moss_scale = (scale * 0.15, scale * 0.025, scale * 0.15)
            moss_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.35,
                position[1] + scale * 0.57,
                position[2] + scale * (0.4 + i * scale * 0.45)
            )
            moss = self._create_composite_cube(f"{name}_Moss_{i}", moss_pos, moss_scale, moss_gray)
            created_actors.append(moss["actor"])

        # Scratch marks (battle damage)
        for i in range(3):
            scratch_scale = (scale * 0.3, scale * 0.015, scale * 0.06)
            scratch_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.25,
                position[1] + scale * 0.57,
                position[2] + scale * (0.6 + i * scale * 0.35)
            )
            scratch = self._create_composite_cube(f"{name}_Scratch_{i}", scratch_pos, scratch_scale, stone_dark)
            created_actors.append(scratch["actor"])

        # Dust accumulation
        for i in range(6):
            dust_scale = (scale * 0.12, scale * 0.015, scale * 0.1)
            dust_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.3,
                position[1] + scale * 0.57,
                position[2] + scale * (0.25 + (i // 3) * scale * 0.35)
            )
            dust = self._create_composite_cube(f"{name}_Dust_{i}", dust_pos, dust_scale, dust_tan)
            created_actors.append(dust["actor"])

        # Surface texture variation
        for i in range(8):
            texture_scale = (scale * 0.15, scale * 0.03, scale * 0.15)
            texture_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.25,
                position[1] + ((i // 4) % 2) * scale * 0.3,
                position[2] + scale * (0.2 + (i // 4) * scale * 0.3)
            )
            texture = self._create_composite_cube(f"{name}_Texture_{i}", texture_pos, texture_scale,
                                                 sandstone_light if i % 2 == 0 else limestone_base)
            created_actors.append(texture["actor"])

        # Wear patterns on edges
        for i in range(4):
            wear_scale = (scale * 0.2, scale * 0.025, scale * 0.08)
            wear_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.4,
                position[1] + scale * 0.58,
                position[2] + scale * (0.3 + i * scale * 0.5)
            )
            wear = self._create_composite_cube(f"{name}_Wear_{i}", wear_pos, wear_scale, wear_brown)
            created_actors.append(wear["actor"])

        unreal.log(f"🗿 STONE DEMON created with {len(created_actors)} components (Realistic + Boned)")
        return {
            "message": f"Created {name} (Stone Demon - Realistic + Fully Boned)",
            "name": name,
            "type": "stone demon",
            "actors": created_actors,
            "bones": bones
        }

    def _create_fire_demon_hollywood(self, parsed: dict) -> dict:
        """
        FIRE DEMON - REALISTIC QUADRUPEDAL ANIMATABLE VERSION
        SMALLEST demon - quadrupedal (2-3 feet long)
        Low profile, agile, darting movement
        Materials: Real charred wood/obsidian, ash, scorch marks (NO GLOW)
        Full quadrupedal bone structure for animation
        """
        name = parsed.get("name") or "FireDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 0.8

        unreal.log("🔥 Creating FIRE DEMON (Realistic + Boned)...")

        created_actors = []
        bones = {}

        # REALISTIC CHARRED COLORS - Natural fire-damaged appearance
        charred_black = (0.08, 0.06, 0.05)       # Deep charred wood/obsidian
        ash_gray = (0.28, 0.26, 0.24)            # Ash coating
        ember_brown = (0.22, 0.14, 0.10)         # Scorched brown
        crack_dark = (0.05, 0.04, 0.03)          # Deep cracks
        wood_char = (0.15, 0.10, 0.08)           # Charred wood texture

        # QUADRUPEDAL SKELETON - Spine and limb structure
        # Spine vertebrae (neck to tail)
        for i in range(8):
            spine_pos = (position[0], position[1] - scale * 0.15 + i * scale * 0.18, position[2] + scale * 0.55)
            spine_bone = self._create_bone_joint(f"{name}_Spine_{i}", spine_pos, scale)
            created_actors.append(spine_bone["actor"])

        # Rib cage
        for i in range(5):
            rib_angle = (math.pi * i) / 5
            rib_pos = (
                position[0] + scale * 0.22 * math.cos(rib_angle),
                position[1] + scale * 0.5 + scale * 0.22 * math.sin(rib_angle),
                position[2] + scale * 0.6
            )
            rib_bone = self._create_bone_joint(f"{name}_Rib_{i}", rib_pos, scale)
            created_actors.append(rib_bone["actor"])

        # BODY - Low profile quadrupedal torso
        torso_scale = (scale * 0.5, scale * 0.35, scale * 0.9)
        torso_pos = (position[0], position[1], position[2] + scale * 0.4)
        torso = self._create_composite_cube(f"{name}_Torso", torso_pos, torso_scale, charred_black)
        created_actors.append(torso["actor"])

        # Chest definition
        chest_scale = (scale * 0.45, scale * 0.08, scale * 0.35)
        chest_pos = (position[0], position[1] + scale * 0.37, position[2] + scale * 0.55)
        chest = self._create_composite_cube(f"{name}_Chest", chest_pos, chest_scale, ash_gray)
        created_actors.append(chest["actor"])

        # Spine ridge (charred, NOT glowing)
        for i in range(6):
            ridge_scale = (scale * 0.06, scale * 0.06, scale * 0.08)
            ridge_pos = (
                position[0],
                position[1] - scale * 0.15 + i * scale * 0.16,
                position[2] + scale * 0.78
            )
            ridge = self._create_composite_cube(f"{name}_SpineRidge_{i}", ridge_pos, ridge_scale, ember_brown)
            created_actors.append(ridge["actor"])

        # NECK - Flexible column
        for i in range(3):
            neck_scale = (scale * 0.12, scale * 0.12, scale * 0.08)
            neck_pos = (position[0], position[1] - scale * (0.35 + i * 0.1), position[2] + scale * 0.62)
            neck = self._create_composite_cube(f"{name}_NeckVertebra_{i}", neck_pos, neck_scale, charred_black)
            created_actors.append(neck["actor"])

        neck_main_scale = (scale * 0.18, scale * 0.18, scale * 0.2)
        neck_main_pos = (position[0], position[1] - scale * 0.35, position[2] + scale * 0.58)
        neck_main = self._create_composite_cube(f"{name}_Neck_Main", neck_main_pos, neck_main_scale, charred_black)
        created_actors.append(neck_main["actor"])

        # HEAD - Angular reptilian skull
        skull_scale = (scale * 0.25, scale * 0.35, scale * 0.2)
        skull_pos = (position[0], position[1] - scale * 0.55, position[2] + scale * 0.5)
        skull = self._create_composite_cube(f"{name}_Skull", skull_pos, skull_scale, charred_black)
        created_actors.append(skull["actor"])

        # Brow ridges
        for side in [-1, 1]:
            brow_scale = (scale * 0.1, scale * 0.04, scale * 0.06)
            brow_pos = (position[0] + side * scale * 0.08, position[1] - scale * 0.6, position[2] + scale * 0.55)
            brow = self._create_composite_cube(f"{name}_Brow_{'L' if side < 0 else 'R'}", brow_pos, brow_scale, ash_gray)
            created_actors.append(brow["actor"])

        # Snout
        snout_scale = (scale * 0.15, scale * 0.2, scale * 0.12)
        snout_pos = (position[0], position[1] - scale * 0.75, position[2] + scale * 0.45)
        snout = self._create_composite_cube(f"{name}_Snout", snout_pos, snout_scale, charred_black)
        created_actors.append(snout["actor"])

        # Jaw
        jaw_scale = (scale * 0.2, scale * 0.1, scale * 0.1)
        jaw_pos = (position[0], position[1] - scale * 0.7, position[2] + scale * 0.42)
        jaw = self._create_composite_cube(f"{name}_Jaw", jaw_pos, jaw_scale, charred_black)
        created_actors.append(jaw["actor"])

        # REALISTIC EYES - Dull charred appearance (NO GLOW)
        for side in [-1, 1]:
            # Eye socket
            socket_scale = (scale * 0.07, scale * 0.06, scale * 0.07)
            socket_pos = (position[0] + side * scale * 0.08, position[1] - scale * 0.62, position[2] + scale * 0.52)
            socket = self._create_composite_cube(f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, crack_dark)
            created_actors.append(socket["actor"])

            # Eye (dull ember gray)
            eye_scale = (scale * 0.045, scale * 0.045, scale * 0.04)
            eye_pos = (position[0] + side * scale * 0.08, position[1] - scale * 0.65, position[2] + scale * 0.52)
            eye = self._create_composite_cube(f"{name}_Eye_{'L' if side < 0 else 'R'}", eye_pos, eye_scale, (0.25, 0.18, 0.15))
            created_actors.append(eye["actor"])

        # Nostrils
        for side in [-1, 1]:
            nostril_scale = (scale * 0.025, scale * 0.035, scale * 0.025)
            nostril_pos = (position[0] + side * scale * 0.04, position[1] - scale * 0.82, position[2] + scale * 0.45)
            nostril = self._create_composite_cube(f"{name}_Nostril_{'L' if side < 0 else 'R'}", nostril_pos, nostril_scale, crack_dark)
            created_actors.append(nostril["actor"])

        # Teeth (sharp, charred)
        for i in range(6):
            tooth_scale = (scale * 0.025, scale * 0.04, scale * 0.025)
            tooth_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.06,
                position[1] - scale * 0.75,
                position[2] + scale * (0.43 + (i // 3) * scale * 0.03)
            )
            tooth = self._create_composite_cube(f"{name}_Tooth_{i}", tooth_pos, tooth_scale, ash_gray)
            created_actors.append(tooth["actor"])

        # Horns - Small charred spikes
        for side in [-1, 1]:
            horn_base_scale = (scale * 0.04, scale * 0.04, scale * 0.04)
            horn_base_pos = (position[0] + side * scale * 0.1, position[1] - scale * 0.5, position[2] + scale * 0.58)
            horn_base = self._create_composite_cube(f"{name}_HornBase_{'L' if side < 0 else 'R'}", horn_base_pos, horn_base_scale, charred_black)
            created_actors.append(horn_base["actor"])

            # Horn shaft
            horn_shaft_scale = (scale * 0.03, scale * 0.03, scale * 0.1)
            horn_shaft_pos = (position[0] + side * scale * 0.1, position[1] - scale * 0.5, position[2] + scale * 0.64)
            horn_shaft = self._create_composite_cube(f"{name}_Horn_{'L' if side < 0 else 'R'}", horn_shaft_pos, horn_shaft_scale, ash_gray)
            created_actors.append(horn_shaft["actor"])

            # Horn tip (scorched)
            tip_scale = (scale * 0.018, scale * 0.018, scale * 0.04)
            tip_pos = (position[0] + side * scale * 0.1, position[1] - scale * 0.5, position[2] + scale * 0.72)
            tip = self._create_composite_cube(f"{name}_HornTip_{'L' if side < 0 else 'R'}", tip_pos, tip_scale, ember_brown)
            created_actors.append(tip["actor"])

        # Ears - Small pointed
        for side in [-1, 1]:
            ear_scale = (scale * 0.05, scale * 0.06, scale * 0.05)
            ear_pos = (position[0] + side * scale * 0.12, position[1] - scale * 0.48, position[2] + scale * 0.55)
            ear = self._create_composite_cube(f"{name}_Ear_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, charred_black)
            created_actors.append(ear["actor"])

        # QUADRUPEDAL LEGS - Four legs with full anatomy
        leg_positions = [
            (-1, -1, "FrontLeft"),   # Front left
            (1, -1, "FrontRight"),   # Front right
            (-1, 1, "BackLeft"),     # Back left
            (1, 1, "BackRight")      # Back right
        ]

        for side_x, side_y, leg_name in leg_positions:
            # Shoulder/Hip joint
            joint_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] + scale * 0.35
            )
            joint_bone = self._create_bone_joint(f"{name}_LegJoint_{leg_name}", joint_pos, scale)
            created_actors.append(joint_bone["actor"])

            # Upper leg (humerus/femur)
            upper_leg_scale = (scale * 0.1, scale * 0.1, scale * 0.25)
            upper_leg_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] + scale * 0.25
            )
            upper_leg = self._create_composite_cube(f"{name}_UpperLeg_{leg_name}", upper_leg_pos, upper_leg_scale, charred_black)
            created_actors.append(upper_leg["actor"])

            # Muscle definition
            muscle_scale = (scale * 0.09, scale * 0.07, scale * 0.15)
            muscle_pos = (
                position[0] + side_x * scale * 0.27,
                position[1] + side_y * scale * 0.15 - scale * 0.05,
                position[2] + scale * 0.28
            )
            muscle = self._create_composite_cube(f"{name}_LegMuscle_{leg_name}", muscle_pos, muscle_scale, ash_gray)
            created_actors.append(muscle["actor"])

            # Elbow/Knee joint
            elbow_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] + scale * 0.12
            )
            elbow_bone = self._create_bone_joint(f"{name}_ElbowKnee_{leg_name}", elbow_pos, scale)
            created_actors.append(elbow_bone["actor"])

            # Joint detail
            joint_detail_scale = (scale * 0.08, scale * 0.08, scale * 0.06)
            joint_detail = self._create_composite_cube(f"{name}_Joint_{leg_name}", elbow_pos, joint_detail_scale, ash_gray)
            created_actors.append(joint_detail["actor"])

            # Lower leg (radius/tibia)
            lower_leg_scale = (scale * 0.07, scale * 0.07, scale * 0.2)
            lower_leg_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] - scale * 0.05
            )
            lower_leg = self._create_composite_cube(f"{name}_LowerLeg_{leg_name}", lower_leg_pos, lower_leg_scale, charred_black)
            created_actors.append(lower_leg["actor"])

            # Ankle/Wrist joint
            ankle_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] - scale * 0.2
            )
            ankle_bone = self._create_bone_joint(f"{name}_AnkleWrist_{leg_name}", ankle_pos, scale)
            created_actors.append(ankle_bone["actor"])

            # Paw/foot
            paw_scale = (scale * 0.1, scale * 0.12, scale * 0.06)
            paw_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.2,
                position[2] - scale * 0.28
            )
            paw = self._create_composite_cube(f"{name}_Paw_{leg_name}", paw_pos, paw_scale, charred_black)
            created_actors.append(paw["actor"])

            # Toes (3 toes per paw)
            for t in range(3):
                toe_scale = (scale * 0.025, scale * 0.04, scale * 0.06)
                toe_pos = (
                    position[0] + side_x * scale * 0.25 + (t - 1) * scale * 0.03,
                    position[1] + side_y * scale * 0.25,
                    position[2] - scale * 0.32
                )
                toe = self._create_composite_cube(f"{name}_Toe_{leg_name}_{t}", toe_pos, toe_scale, ash_gray)
                created_actors.append(toe["actor"])

            # Claws
            for t in range(3):
                claw_scale = (scale * 0.015, scale * 0.02, scale * 0.025)
                claw_pos = (
                    position[0] + side_x * scale * 0.25 + (t - 1) * scale * 0.03,
                    position[1] + side_y * scale * 0.29,
                    position[2] - scale * 0.35
                )
                claw = self._create_composite_cube(f"{name}_Claw_{leg_name}_{t}", claw_pos, claw_scale, ember_brown)
                created_actors.append(claw["actor"])

        # TAIL - Tapered, segmented
        tail_base_scale = (scale * 0.08, scale * 0.15, scale * 0.08)
        tail_base_pos = (position[0], position[1] + scale * 0.5, position[2] + scale * 0.35)
        tail_base = self._create_composite_cube(f"{name}_Tail_Base", tail_base_pos, tail_base_scale, charred_black)
        created_actors.append(tail_base["actor"])

        # Tail vertebrae
        for i in range(4):
            vertebra_scale = (scale * (0.07 - i * 0.012), scale * 0.12, scale * (0.07 - i * 0.012))
            vertebra_pos = (position[0], position[1] + scale * (0.6 + i * 0.12), position[2] + scale * 0.35)
            vertebra = self._create_composite_cube(f"{name}_TailVertebra_{i}", vertebra_pos, vertebra_scale, charred_black)
            created_actors.append(vertebra["actor"])

        # Tail tip (charred, NOT flame)
        tip_scale = (scale * 0.025, scale * 0.08, scale * 0.025)
        tip_pos = (position[0], position[1] + scale * 1.1, position[2] + scale * 0.35)
        tip = self._create_composite_cube(f"{name}_Tail_Tip", tip_pos, tip_scale, ember_brown)
        created_actors.append(tip["actor"])

        # SURFACE DETAIL - Realistic fire damage
        # Charred cracks (NOT magma, just cracks)
        for i in range(8):
            crack_scale = (scale * 0.15, scale * 0.02, scale * 0.3)
            crack_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.3,
                position[1] + scale * 0.37,
                position[2] + scale * 0.3 + (i // 2) * scale * 0.15
            )
            crack = self._create_composite_cube(f"{name}_CharCrack_{i}", crack_pos, crack_scale, crack_dark)
            created_actors.append(crack["actor"])

        # Ash coating patches
        for i in range(6):
            ash_scale = (scale * 0.12, scale * 0.025, scale * 0.12)
            ash_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.25,
                position[1] + scale * 0.37,
                position[2] + scale * (0.25 + i * scale * 0.12)
            )
            ash = self._create_composite_cube(f"{name}_Ash_{i}", ash_pos, ash_scale, ash_gray)
            created_actors.append(ash["actor"])

        # Scorch marks
        for i in range(4):
            scorch_scale = (scale * 0.18, scale * 0.02, scale * 0.08)
            scorch_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.2,
                position[1] + scale * 0.38,
                position[2] + scale * (0.35 + i * scale * 0.15)
            )
            scorch = self._create_composite_cube(f"{name}_Scorch_{i}", scorch_pos, scorch_scale, ember_brown)
            created_actors.append(scorch["actor"])

        # Texture variation
        for i in range(10):
            texture_scale = (scale * 0.08, scale * 0.025, scale * 0.08)
            texture_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.2,
                position[1] + ((i // 3) % 2) * scale * 0.25,
                position[2] + scale * (0.2 + (i // 6) * scale * 0.25)
            )
            texture = self._create_composite_cube(f"{name}_Texture_{i}", texture_pos, texture_scale,
                                                wood_char if i % 2 == 0 else ash_gray)
            created_actors.append(texture["actor"])

        unreal.log(f"🔥 FIRE DEMON created with {len(created_actors)} components (Realistic + Boned)")
        return {
            "message": f"Created {name} (Fire Demon - Realistic + Fully Boned)",
            "name": name,
            "type": "fire demon",
            "actors": created_actors,
            "bones": bones
        }

    def _create_water_demon_hollywood(self, parsed: dict) -> dict:
        """
        WATER/LAKE DEMON - REALISTIC TENTACLED ANIMATABLE VERSION
        Massive aquatic predator (8-15 feet long with tentacles)
        Multiple tentacles with gripping suckers
        Materials: Real slick scales, muddy algae, sucker pads (NO BIOLUMINESCENCE)
        Full bone structure for animation
        """
        name = parsed.get("name") or "WaterDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.5

        unreal.log("🌊 Creating WATER/LAKE DEMON (Realistic + Boned)...")

        created_actors = []
        bones = {}

        # REALISTIC AQUATIC COLORS - Natural swamp predator appearance
        swamp_green = (0.15, 0.28, 0.25)         # Deep swamp green
        algae_brown = (0.22, 0.25, 0.18)         # Algae coating
        scale_mud = (0.18, 0.22, 0.20)           # Muddy scales
        sucker_gray = (0.25, 0.28, 0.26)          # Natural sucker color
        slime_coat = (0.20, 0.24, 0.22)           # Slimy coating
        barnacle_white = (0.65, 0.62, 0.58)       # Barnacle growth

        # SKELETON - Aquatic predator structure
        # Spine vertebrae
        for i in range(8):
            spine_pos = (position[0], position[1], position[2] + scale * (0.5 + i * 0.18))
            spine_bone = self._create_bone_joint(f"{name}_Spine_{i}", spine_pos, scale)
            created_actors.append(spine_bone["actor"])

        # Rib cage
        for i in range(6):
            rib_angle = (math.pi * i) / 6
            rib_pos = (
                position[0] + scale * 0.4 * math.cos(rib_angle),
                position[1] + scale * 0.4 * math.sin(rib_angle),
                position[2] + scale * 1.2
            )
            rib_bone = self._create_bone_joint(f"{name}_Rib_{i}", rib_pos, scale)
            created_actors.append(rib_bone["actor"])

        # MASSIVE BODY - Streamlined aquatic form
        body_scale = (scale * 0.9, scale * 0.7, scale * 1.8)
        body_pos = (position[0], position[1], position[2] + scale * 0.9)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, swamp_green)
        created_actors.append(body["actor"])

        # Scale patterns on body
        for i in range(12):
            scale_piece_scale = (scale * 0.2, scale * 0.03, scale * 0.15)
            scale_piece_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.3,
                position[1] + scale * 0.72,
                position[2] + scale * 0.4 + (i // 3) * scale * 0.35
            )
            scale_piece = self._create_composite_cube(f"{name}_Scale_{i}", scale_piece_pos, scale_piece_scale, scale_mud)
            created_actors.append(scale_piece["actor"])

        # Algae stripes (NOT bioluminescent)
        for i in range(6):
            algae_scale = (scale * 0.08, scale * 0.02, scale * 0.4)
            algae_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.4,
                position[1] + scale * 0.72,
                position[2] + scale * 0.5 + (i // 2) * scale * 0.4
            )
            algae = self._create_composite_cube(f"{name}_AlgaeStripe_{i}", algae_pos, algae_scale, algae_brown)
            created_actors.append(algae["actor"])

        # Head - Aquatic predator
        head_scale = (scale * 0.5, scale * 0.6, scale * 0.4)
        head_pos = (position[0], position[1] - scale * 0.35, position[2] + scale * 1.0)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, swamp_green)
        created_actors.append(head["actor"])

        # Jaw line
        jaw_scale = (scale * 0.4, scale * 0.15, scale * 0.15)
        jaw_pos = (position[0], position[1] - scale * 0.7, position[2] + scale * 0.85)
        jaw = self._create_composite_cube(f"{name}_Jaw", jaw_pos, jaw_scale, swamp_green)
        created_actors.append(jaw["actor"])

        # REALISTIC EYES - Muddy aquatic eyes (NOT bioluminescent)
        for side in [-1, 1]:
            # Eye socket
            socket_scale = (scale * 0.13, scale * 0.1, scale * 0.13)
            socket_pos = (position[0] + side * scale * 0.18, position[1] - scale * 0.55, head_pos[2] + scale * 0.05)
            socket = self._create_composite_cube(f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, (0.10, 0.12, 0.10))
            created_actors.append(socket["actor"])

            # Eye (muddy yellow-green)
            eye_scale = (scale * 0.1, scale * 0.08, scale * 0.1)
            eye_pos = (position[0] + side * scale * 0.18, position[1] - scale * 0.58, head_pos[2] + scale * 0.05)
            eye = self._create_composite_cube(f"{name}_Eye_{'L' if side < 0 else 'R'}", eye_pos, eye_scale, (0.45, 0.42, 0.28))
            created_actors.append(eye["actor"])

        # Nostrils
        for side in [-1, 1]:
            nostril_scale = (scale * 0.04, scale * 0.06, scale * 0.04)
            nostril_pos = (position[0] + side * scale * 0.12, position[1] - scale * 0.82, position[2] + scale * 0.95)
            nostril = self._create_composite_cube(f"{name}_Nostril_{'L' if side < 0 else 'R'}", nostril_pos, nostril_scale, (0.12, 0.10, 0.08))
            created_actors.append(nostril["actor"])

        # Teeth (multiple rows)
        for i in range(8):
            tooth_scale = (scale * 0.035, scale * 0.06, scale * 0.035)
            tooth_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.08,
                position[1] - scale * 0.72,
                position[2] + scale * (0.82 + (i // 4) * scale * 0.04)
            )
            tooth = self._create_composite_cube(f"{name}_Tooth_{i}", tooth_pos, tooth_scale, (0.55, 0.52, 0.48))
            created_actors.append(tooth["actor"])

        # MASSIVE TENTACLES - 8 main tentacles with bone structure
        for i in range(8):
            angle = (2 * math.pi * i) / 8

            # Tentacle root joint
            root_pos = (
                position[0] + scale * 0.45 * math.cos(angle),
                position[1] + scale * 0.45 * math.sin(angle),
                position[2] + scale * 0.6
            )
            root_bone = self._create_bone_joint(f"{name}_TentacleRoot_{i}", root_pos, scale)
            created_actors.append(root_bone["actor"])

            # Base of tentacle
            tentacle_base_scale = (scale * 0.25, scale * 0.25, scale * 0.3)
            tentacle_base_pos = (
                position[0] + scale * 0.5 * math.cos(angle),
                position[1] + scale * 0.5 * math.sin(angle),
                position[2] + scale * 0.7
            )
            tentacle_base = self._create_composite_cube(f"{name}_Tentacle{i}_Base", tentacle_base_pos, tentacle_base_scale, swamp_green)
            created_actors.append(tentacle_base["actor"])

            # Tentacle segments (4 segments per tentacle)
            for j in range(4):
                # Tentacle joint
                joint_pos = (
                    position[0] + (scale * 0.55 + j * scale * 0.35) * math.cos(angle),
                    position[1] + (scale * 0.55 + j * scale * 0.35) * math.sin(angle),
                    position[2] + scale * (0.65 - j * scale * 0.18)
                )
                joint_bone = self._create_bone_joint(f"{name}_Tentacle{i}_Joint{j}", joint_pos, scale)
                created_actors.append(joint_bone["actor"])

                segment_scale = (scale * (0.22 - j * 0.03), scale * 0.2, scale * 0.25)
                segment_pos = (
                    position[0] + (scale * 0.6 + j * scale * 0.35) * math.cos(angle),
                    position[1] + (scale * 0.6 + j * scale * 0.35) * math.sin(angle),
                    position[2] + scale * 0.7 - j * scale * 0.15
                )
                segment = self._create_composite_cube(f"{name}_Tentacle{i}_Segment{j}", segment_pos, segment_scale, swamp_green)
                created_actors.append(segment["actor"])

                # Sucker pads on each segment (natural, not glowing)
                for k in range(3):
                    sucker_angle = (2 * math.pi * k) / 3
                    sucker_scale = (scale * 0.06, scale * 0.02, scale * 0.06)
                    sucker_pos = (
                        segment_pos[0] + scale * 0.15 * math.cos(sucker_angle),
                        segment_pos[1] + scale * 0.15 * math.sin(sucker_angle),
                        segment_pos[2]
                    )
                    sucker = self._create_composite_cube(f"{name}_Tentacle{i}_Sucker{j}_{k}", sucker_pos, sucker_scale, sucker_gray)
                    created_actors.append(sucker["actor"])

        # Tail - Powerful aquatic propulsion
        tail_scale = (scale * 0.3, scale * 0.9, scale * 0.15)
        tail_pos = (position[0], position[1] + scale * 1.0, position[2] + scale * 0.6)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, swamp_green)
        created_actors.append(tail["actor"])

        # Tail vertebrae
        for i in range(4):
            vertebra_scale = (scale * 0.25, scale * 0.2, scale * 0.1)
            vertebra_pos = (position[0], position[1] + scale * (1.1 + i * 0.2), position[2] + scale * 0.6)
            vertebra = self._create_composite_cube(f"{name}_TailVertebra_{i}", vertebra_pos, vertebra_scale, scale_mud)
            created_actors.append(vertebra["actor"])

        # Tail fin
        fin_scale = (scale * 0.6, scale * 0.05, scale * 0.3)
        fin_pos = (position[0], position[1] + scale * 1.4, position[2] + scale * 0.55)
        fin = self._create_composite_cube(f"{name}_TailFin", fin_pos, fin_scale, scale_mud)
        created_actors.append(fin["actor"])

        # SURFACE DETAIL - Realistic aquatic weathering
        # Algae patches
        for i in range(8):
            algae_patch_scale = (scale * 0.15, scale * 0.025, scale * 0.15)
            algae_patch_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.35,
                position[1] + scale * 0.73,
                position[2] + scale * (0.3 + (i // 4) * scale * 0.3)
            )
            algae_patch = self._create_composite_cube(f"{name}_AlgaePatch_{i}", algae_patch_pos, algae_patch_scale, algae_brown)
            created_actors.append(algae_patch["actor"])

        # Barnacle growth
        for i in range(6):
            barnacle_scale = (scale * 0.08, scale * 0.06, scale * 0.08)
            barnacle_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.45,
                position[1] + scale * 0.73,
                position[2] + scale * (0.5 + i * scale * 0.15)
            )
            barnacle = self._create_composite_cube(f"{name}_Barnacle_{i}", barnacle_pos, barnacle_scale, barnacle_white)
            created_actors.append(barnacle["actor"])

        # Slime coating
        for i in range(10):
            slime_scale = (scale * 0.12, scale * 0.025, scale * 0.12)
            slime_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.25,
                position[1] + ((i // 4) % 2) * scale * 0.3,
                position[2] + scale * (0.2 + (i // 8) * scale * 0.25)
            )
            slime = self._create_composite_cube(f"{name}_Slime_{i}", slime_pos, slime_scale, slime_coat)
            created_actors.append(slime["actor"])

        # Water damage/discoloration
        for i in range(7):
            damage_scale = (scale * 0.18, scale * 0.025, scale * 0.12)
            damage_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.3,
                position[1] + scale * 0.74,
                position[2] + scale * (0.35 + i * scale * 0.18)
            )
            damage = self._create_composite_cube(f"{name}_WaterDamage_{i}", damage_pos, damage_scale, (0.12, 0.15, 0.12))
            created_actors.append(damage["actor"])

        unreal.log(f"🌊 WATER/LAKE DEMON created with {len(created_actors)} components (Realistic + Boned)")
        return {
            "message": f"Created {name} (Water/Lake Demon - Realistic + Fully Boned)",
            "name": name,
            "type": "water demon",
            "actors": created_actors,
            "bones": bones
        }

    def _create_wood_demon_hollywood(self, parsed: dict) -> dict:
        """
        WOOD DEMON - REALISTIC ANIMATABLE VERSION
        Arboreal bark armor (7-10 feet tall)
        Tree-like camouflage with root locomotion
        Materials: Real rough bark, twisted vines, moss, fungus (NO MAGICAL GLOW)
        Full bone structure for animation
        """
        name = parsed.get("name") or "WoodDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.2

        unreal.log("🌲 Creating WOOD DEMON (Realistic + Boned)...")

        created_actors = []
        bones = {}

        # REALISTIC WOOD COLORS - Natural forest appearance
        bark_brown = (0.28, 0.22, 0.15)         # Dark brown bark
        vine_green = (0.28, 0.32, 0.12)          # Dried vine color
        moss_gray = (0.22, 0.26, 0.18)           # Gray moss
        leaf_brown = (0.18, 0.28, 0.10)          # Dead leaves
        rot_dark = (0.15, 0.12, 0.08)            # Rot pockets
        fungus_white = (0.65, 0.62, 0.55)        # Fungus growth

        # SKELETON - Tree-like structure
        # Spine vertebrae
        for i in range(10):
            spine_pos = (position[0], position[1], position[2] + scale * (0.5 + i * 0.18))
            spine_bone = self._create_bone_joint(f"{name}_Spine_{i}", spine_pos, scale)
            created_actors.append(spine_bone["actor"])

        # Branch ribs
        for i in range(5):
            rib_angle = (math.pi * i) / 5
            rib_pos = (
                position[0] + scale * 0.35 * math.cos(rib_angle),
                position[1] + scale * 0.35 * math.sin(rib_angle),
                position[2] + scale * 1.5
            )
            rib_bone = self._create_bone_joint(f"{name}_BranchRib_{i}", rib_pos, scale)
            created_actors.append(rib_bone["actor"])

        # TALL BODY - Tree-like trunk
        body_scale = (scale * 0.7, scale * 0.6, scale * 2.0)
        body_pos = (position[0], position[1], position[2] + scale * 1.0)
        body = self._create_composite_cube(f"{name}_Trunk", body_pos, body_scale, bark_brown)
        created_actors.append(body["actor"])

        # Bark armor plates - overlapping protection
        for i in range(10):
            plate_scale = (scale * 0.75, scale * 0.1, scale * 0.35)
            plate_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.05,
                position[1] + scale * 0.62,
                position[2] + scale * 0.3 + i * scale * 0.18
            )
            plate = self._create_composite_cube(f"{name}_BarkPlate_{i}", plate_pos, plate_scale, (0.25, 0.20, 0.12))
            created_actors.append(plate["actor"])

        # Moss patches on bark
        for i in range(8):
            moss_scale = (scale * 0.15, scale * 0.03, scale * 0.2)
            moss_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.4,
                position[1] + scale * 0.63,
                position[2] + scale * 0.5 + (i // 2) * scale * 0.35
            )
            moss = self._create_composite_cube(f"{name}_Moss_{i}", moss_pos, moss_scale, moss_gray)
            created_actors.append(moss["actor"])

        # Fungus growth
        for i in range(4):
            fungus_scale = (scale * 0.12, scale * 0.04, scale * 0.12)
            fungus_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.35,
                position[1] + scale * 0.64,
                position[2] + scale * (0.6 + i * scale * 0.4)
            )
            fungus = self._create_composite_cube(f"{name}_Fungus_{i}", fungus_pos, fungus_scale, fungus_white)
            created_actors.append(fungus["actor"])

        # Head - Knotted wood cranium
        head_scale = (scale * 0.4, scale * 0.45, scale * 0.35)
        head_pos = (position[0], position[1], position[2] + scale * 2.2)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, bark_brown)
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
            horn = self._create_composite_cube(f"{name}_RootHorn_{i}", horn_pos, horn_scale, (0.22, 0.18, 0.10))
            created_actors.append(horn["actor"])

        # REALISTIC EYES - Wood knot eyes (NOT glowing)
        for side in [-1, 1]:
            # Eye socket (knot hole)
            socket_scale = (scale * 0.1, scale * 0.08, scale * 0.08)
            socket_pos = (position[0] + side * scale * 0.12, position[1] - scale * 0.25, head_pos[2])
            socket = self._create_composite_cube(f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, rot_dark)
            created_actors.append(socket["actor"])

            # Eye (wood knot, dull brown)
            eye_scale = (scale * 0.06, scale * 0.06, scale * 0.06)
            eye_pos = (position[0] + side * scale * 0.12, position[1] - scale * 0.25, head_pos[2])
            eye = self._create_composite_cube(f"{name}_Eye_{'L' if side < 0 else 'R'}", eye_pos, eye_scale, (0.35, 0.28, 0.20))
            created_actors.append(eye["actor"])

        # Nose - Bark knot
        nose_scale = (scale * 0.08, scale * 0.1, scale * 0.08)
        nose_pos = (position[0], position[1] - scale * 0.42, position[2] + scale * 2.15)
        nose = self._create_composite_cube(f"{name}_Nose", nose_pos, nose_scale, (0.20, 0.16, 0.10))
        created_actors.append(nose["actor"])

        # Mouth - Bark split
        mouth_scale = (scale * 0.15, scale * 0.04, scale * 0.08)
        mouth_pos = (position[0], position[1] - scale * 0.42, position[2] + scale * 2.05)
        mouth = self._create_composite_cube(f"{name}_Mouth", mouth_pos, mouth_scale, rot_dark)
        created_actors.append(mouth["actor"])

        # Vine-wrapped arms - Branch-like limbs with bone structure
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Shoulder joint
            shoulder_pos = (position[0] + side * scale * 0.45, position[1], position[2] + scale * 1.6)
            shoulder_bone = self._create_bone_joint(f"{name}_Shoulder_{side_name}", shoulder_pos, scale)
            created_actors.append(shoulder_bone["actor"])

            # Main branch arm
            for i in range(4):
                vine_scale = (scale * 0.12, scale * 0.25, scale * 0.1)
                vine_pos = (
                    position[0] + side * (scale * 0.45 + i * scale * 0.1),
                    position[1],
                    position[2] + scale * 1.5 - i * scale * 0.2
                )
                vine = self._create_composite_cube(f"{name}_VineArm_{side_name}_{i}", vine_pos, vine_scale, vine_green)
                created_actors.append(vine["actor"])

                # Branch joint
                if i < 3:
                    joint_pos = (
                        position[0] + side * (scale * 0.45 + (i + 1) * scale * 0.1),
                        position[1],
                        position[2] + scale * (1.3 - i * scale * 0.25)
                    )
                    joint_bone = self._create_bone_joint(f"{name}_ArmJoint_{side_name}_{i}", joint_pos, scale)
                    created_actors.append(joint_bone["actor"])

            # Twig fingers
            for j in range(3):
                twig_scale = (scale * 0.04, scale * 0.12, scale * 0.04)
                twig_pos = (
                    position[0] + side * scale * 0.8,
                    position[1] + (j - 1) * scale * 0.08,
                    position[2] + scale * 0.8
                )
                twig = self._create_composite_cube(f"{name}_Twig_{side_name}_{j}", twig_pos, twig_scale, (0.22, 0.18, 0.08))
                created_actors.append(twig["actor"])

                # Twig joint
                twig_joint_pos = (
                    position[0] + side * scale * 0.8,
                    position[1] + (j - 1) * scale * 0.08,
                    position[2] + scale * 0.88
                )
                twig_joint = self._create_bone_joint(f"{name}_TwigJoint_{side_name}_{j}", twig_joint_pos, scale)
                created_actors.append(twig_joint["actor"])

        # Root-like legs - Spreading root base with joints
        for i in range(5):
            angle = (2 * math.pi * i) / 5

            # Root joint
            root_joint_pos = (
                position[0] + scale * 0.3 * math.cos(angle),
                position[1] + scale * 0.3 * math.sin(angle),
                position[2] - scale * 0.2
            )
            root_joint = self._create_bone_joint(f"{name}_RootJoint_{i}", root_joint_pos, scale)
            created_actors.append(root_joint["actor"])

            # Root leg
            root_scale = (scale * 0.18, scale * 0.18, scale * 0.8)
            root_pos = (
                position[0] + scale * 0.35 * math.cos(angle),
                position[1] + scale * 0.35 * math.sin(angle),
                position[2] - scale * 0.3
            )
            root = self._create_composite_cube(f"{name}_RootLeg_{i}", root_pos, root_scale, (0.24, 0.18, 0.10))
            created_actors.append(root["actor"])

            # Root hairs (smaller roots)
            for r in range(3):
                hair_scale = (scale * 0.06, scale * 0.06, scale * 0.2)
                hair_pos = (
                    position[0] + scale * (0.35 + r * 0.08) * math.cos(angle + r * 0.3),
                    position[1] + scale * (0.35 + r * 0.08) * math.sin(angle + r * 0.3),
                    position[2] - scale * (0.5 + r * 0.15)
                )
                hair = self._create_composite_cube(f"{name}_RootHair_{i}_{r}", hair_pos, hair_scale, vine_green)
                created_actors.append(hair["actor"])

        # Leaf camouflage - Scattered foliage (dead leaves, not magical)
        for i in range(12):
            leaf_scale = (scale * 0.12, scale * 0.02, scale * 0.1)
            leaf_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.35,
                position[1] + ((i // 4) % 3 - 1) * scale * 0.4,
                position[2] + scale * 1.0 + (i // 12) * scale * 0.5
            )
            leaf = self._create_composite_cube(f"{name}_Leaf_{i}", leaf_pos, leaf_scale, leaf_brown)
            created_actors.append(leaf["actor"])

        # Vine wraps around body (natural vines, not magical)
        for i in range(6):
            vine_wrap_scale = (scale * 0.06, scale * 0.72, scale * 0.06)
            vine_wrap_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.4,
                position[1],
                position[2] + scale * 0.5 + i * scale * 0.25
            )
            vine_wrap = self._create_composite_cube(f"{name}_VineWrap_{i}", vine_wrap_pos, vine_wrap_scale, vine_green)
            created_actors.append(vine_wrap["actor"])

        # SURFACE DETAIL - Realistic wood weathering
        # Insect damage holes
        for i in range(5):
            hole_scale = (scale * 0.06, scale * 0.06, scale * 0.06)
            hole_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.3,
                position[1] + scale * 0.63,
                position[2] + scale * (0.6 + i * scale * 0.3)
            )
            hole = self._create_composite_cube(f"{name}_InsectHole_{i}", hole_pos, hole_scale, rot_dark)
            created_actors.append(hole["actor"])

        # Crack patterns in bark
        for i in range(6):
            crack_scale = (scale * 0.2, scale * 0.025, scale * 0.12)
            crack_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.35,
                position[1] + scale * 0.63,
                position[2] + scale * (0.35 + i * scale * 0.25)
            )
            crack = self._create_composite_cube(f"{name}_BarkCrack_{i}", crack_pos, crack_scale, rot_dark)
            created_actors.append(crack["actor"])

        # Weathering stains
        for i in range(8):
            stain_scale = (scale * 0.15, scale * 0.025, scale * 0.15)
            stain_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.25,
                position[1] + ((i // 4) % 2) * scale * 0.3,
                position[2] + scale * (0.25 + i * scale * 0.2)
            )
            stain = self._create_composite_cube(f"{name}_WeatherStain_{i}", stain_pos, stain_scale, (0.20, 0.16, 0.12))
            created_actors.append(stain["actor"])

        unreal.log(f"🌲 WOOD DEMON created with {len(created_actors)} components (Realistic + Boned)")
        return {
            "message": f"Created {name} (Wood Demon - Realistic + Fully Boned)",
            "name": name,
            "type": "wood demon",
            "actors": created_actors,
            "bones": bones
        }

    def _create_mind_demon_hollywood(self, parsed: dict) -> dict:
        """
        MIND DEMON - REALISTIC EMACIATED HUMANOID VERSION
        Gaunt psychic predator (5-6 feet tall)
        Wasted body with enlarged cranium
        Materials: Pale sickly flesh, sunken veins, emaciated muscle (NO PSYCHIC GLOW)
        Full bone structure for animation
        """
        name = parsed.get("name") or "MindDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.2

        unreal.log("🧠 Creating MIND DEMON (Realistic + Boned)...")

        created_actors = []
        bones = {}

        # REALISTIC FLESH COLORS - Gaunt predator appearance
        flesh_pale = (0.82, 0.78, 0.72)           # Sickly pale flesh
        flesh_gray = (0.72, 0.68, 0.65)           # Gray undertones
        vein_blue = (0.55, 0.52, 0.58)            # Visible veins
        shadow_dark = (0.42, 0.38, 0.35)          # Deep shadows
        eye_white = (0.88, 0.85, 0.82)            # Bloodshot white
        iris_pale = (0.58, 0.55, 0.52)            # Pale gray iris (NOT purple)
        bruise_purple = (0.52, 0.42, 0.48)        # Natural bruising

        # EMACIATED SKELETON - Wasted humanoid structure
        # Pelvis
        pelvis_pos = (position[0], position[1], position[2] + scale * 0.5)
        pelvis_bone = self._create_bone_joint(f"{name}_Pelvis", pelvis_pos, scale)
        created_actors.append(pelvis_bone["actor"])

        # Spine vertebrae (extended for enlarged cranium)
        for i in range(9):
            spine_pos = (position[0], position[1], position[2] + scale * (0.55 + i * 0.12))
            spine_bone = self._create_bone_joint(f"{name}_Spine_{i}", spine_pos, scale)
            created_actors.append(spine_bone["actor"])

        # Rib cage (visible due to emaciation)
        for i in range(6):
            rib_angle = (math.pi * i) / 6
            rib_pos = (
                position[0] + scale * 0.12 * math.cos(rib_angle),
                position[1] + scale * 0.12 * math.sin(rib_angle),
                position[2] + scale * 0.75
            )
            rib_bone = self._create_bone_joint(f"{name}_Rib_{i}", rib_pos, scale)
            created_actors.append(rib_bone["actor"])

        # EMACIATED TORSO - Wasted body
        torso_scale = (scale * 0.2, scale * 0.12, scale * 0.55)
        torso_pos = (position[0], position[1], position[2] + scale * 0.6)
        torso = self._create_composite_cube(f"{name}_Torso", torso_pos, torso_scale, flesh_pale)
        created_actors.append(torso["actor"])

        # Visible ribcage (emaciation)
        for i in range(4):
            rib_scale = (scale * 0.18, scale * 0.025, scale * 0.08)
            rib_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.05,
                position[1] + scale * 0.13,
                position[2] + scale * 0.55 + i * scale * 0.1
            )
            rib = self._create_composite_cube(f"{name}_VisibleRib_{i}", rib_pos, rib_scale, shadow_dark)
            created_actors.append(rib["actor"])

        # LARGE ENLARGED CRANIUM - Biological brain case
        skull_scale = (scale * 0.2, scale * 0.22, scale * 0.28)
        skull_pos = (position[0], position[1], position[2] + scale * 1.55)
        skull = self._create_composite_cube(f"{name}_Skull", skull_pos, skull_scale, flesh_pale)
        created_actors.append(skull["actor"])

        # Visible veins on skull (sunken, not glowing)
        for i in range(8):
            vein_scale = (scale * 0.02, scale * 0.12, scale * 0.02)
            vein_pos = (
                skull_pos[0] + ((i % 2) - 0.5) * scale * 0.08,
                skull_pos[1] + scale * 0.22,
                skull_pos[2] - scale * 0.05 + (i // 2) * scale * 0.1
            )
            vein = self._create_composite_cube(f"{name}_SkullVein_{i}", vein_pos, vein_scale, vein_blue)
            created_actors.append(vein["actor"])

        # GAUNT FACIAL FEATURES
        # Sunken eye sockets
        for side in [-1, 1]:
            socket_scale = (scale * 0.08, scale * 0.06, scale * 0.08)
            socket_pos = (skull_pos[0] + side * scale * 0.06, skull_pos[1] - scale * 0.1, skull_pos[2] + scale * 0.08)
            socket = self._create_composite_cube(f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, shadow_dark)
            created_actors.append(socket["actor"])

            # Sunken eye (bloodshot, pale iris, NOT purple)
            eye_scale = (scale * 0.05, scale * 0.04, scale * 0.05)
            eye_pos = (skull_pos[0] + side * scale * 0.06, skull_pos[1] - scale * 0.11, skull_pos[2] + scale * 0.08)
            eye = self._create_composite_cube(f"{name}_Eye_{'L' if side < 0 else 'R'}", eye_pos, eye_scale, iris_pale)
            created_actors.append(eye["actor"])

            # Bloodshot vessels in eyes
            for v in range(3):
                vessel_scale = (scale * 0.01, scale * 0.035, scale * 0.01)
                vessel_pos = (
                    eye_pos[0] + ((v % 2) - 0.5) * scale * 0.015,
                    eye_pos[1] - scale * 0.005,
                    eye_pos[2] + (v - 1) * scale * 0.015
                )
                vessel = self._create_composite_cube(f"{name}_Bloodshot_{'L' if side < 0 else 'R'}_{v}", vessel_pos, vessel_scale, (0.65, 0.32, 0.35))
                created_actors.append(vessel["actor"])

        # Gaunt nose (prominent due to wasting)
        nose_scale = (scale * 0.04, scale * 0.06, scale * 0.05)
        nose_pos = (skull_pos[0], skull_pos[1] - scale * 0.18, skull_pos[2] + scale * 0.05)
        nose = self._create_composite_cube(f"{name}_Nose", nose_pos, nose_scale, flesh_gray)
        created_actors.append(nose["actor"])

        # Sunken cheeks (visible bone structure)
        for side in [-1, 1]:
            cheek_scale = (scale * 0.07, scale * 0.04, scale * 0.08)
            cheek_pos = (skull_pos[0] + side * scale * 0.1, skull_pos[1] - scale * 0.12, skull_pos[2])
            cheek = self._create_composite_cube(f"{name}_SunkenCheek_{'L' if side < 0 else 'R'}", cheek_pos, cheek_scale, shadow_dark)
            created_actors.append(cheek["actor"])

        # Thin lips
        lip_scale = (scale * 0.06, scale * 0.02, scale * 0.03)
        lip_pos = (skull_pos[0], skull_pos[1] - scale * 0.2, skull_pos[2] + scale * 0.02)
        lip = self._create_composite_cube(f"{name}_Lips", lip_pos, lip_scale, bruise_purple)
        created_actors.append(lip["actor"])

        # EMACIATED LIMBS - Wasted arms with joints
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Shoulder joint
            shoulder_pos = (position[0] + side * scale * 0.15, position[1], position[2] + scale * 0.95)
            shoulder_bone = self._create_bone_joint(f"{name}_Shoulder_{side_name}", shoulder_pos, scale)
            created_actors.append(shoulder_bone["actor"])

            # Upper arm (extremely thin)
            upper_scale = (scale * 0.04, scale * 0.04, scale * 0.25)
            upper_pos = (position[0] + side * scale * 0.15, position[1], position[2] + scale * 0.8)
            upper = self._create_composite_cube(f"{name}_UpperArm_{side_name}", upper_pos, upper_scale, flesh_pale)
            created_actors.append(upper["actor"])

            # Visible humerus bone
            humerus_scale = (scale * 0.018, scale * 0.018, scale * 0.18)
            humerus_pos = (position[0] + side * scale * 0.15, position[1] + scale * 0.025, position[2] + scale * 0.8)
            humerus = self._create_composite_cube(f"{name}_Humerus_{side_name}", humerus_pos, humerus_scale, shadow_dark)
            created_actors.append(humerus["actor"])

            # Elbow joint
            elbow_pos = (position[0] + side * scale * 0.15, position[1], position[2] + scale * 0.62)
            elbow_bone = self._create_bone_joint(f"{name}_Elbow_{side_name}", elbow_pos, scale)
            created_actors.append(elbow_bone["actor"])

            # Forearm (extremely thin)
            forearm_scale = (scale * 0.035, scale * 0.035, scale * 0.22)
            forearm_pos = (position[0] + side * scale * 0.15, position[1], position[2] + scale * 0.5)
            forearm = self._create_composite_cube(f"{name}_Forearm_{side_name}", forearm_pos, forearm_scale, flesh_pale)
            created_actors.append(forearm["actor"])

            # Wrist joint
            wrist_pos = (position[0] + side * scale * 0.15, position[1], position[2] + scale * 0.38)
            wrist_bone = self._create_bone_joint(f"{name}_Wrist_{side_name}", wrist_pos, scale)
            created_actors.append(wrist_bone["actor"])

            # Gaunt hand (bony)
            hand_scale = (scale * 0.05, scale * 0.03, scale * 0.06)
            hand_pos = (position[0] + side * scale * 0.15, position[1] - scale * 0.02, position[2] + scale * 0.35)
            hand = self._create_composite_cube(f"{name}_Hand_{side_name}", hand_pos, hand_scale, flesh_pale)
            created_actors.append(hand["actor"])

            # Emaciated fingers (bony, visible joints)
            for f in range(4):
                finger_scale = (scale * 0.012, scale * 0.06, scale * 0.012)
                finger_pos = (
                    position[0] + side * scale * 0.15 + (f - 1.5) * scale * 0.012,
                    position[1] - scale * 0.04,
                    position[2] + scale * 0.32
                )
                finger = self._create_composite_cube(f"{name}_Finger_{side_name}_{f}", finger_pos, finger_scale, flesh_gray)
                created_actors.append(finger["actor"])

                # Knuckle joints
                knuckle_pos = (
                    position[0] + side * scale * 0.15 + (f - 1.5) * scale * 0.012,
                    position[1] - scale * 0.04,
                    position[2] + scale * 0.26
                )
                knuckle = self._create_bone_joint(f"{name}_Knuckle_{side_name}_{f}", knuckle_pos, scale)
                created_actors.append(knuckle["actor"])

        # EMACIATED LEGS - Wasted lower body with joints
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Hip joint
            hip_pos = (position[0] + side * scale * 0.1, position[1], position[2] + scale * 0.48)
            hip_bone = self._create_bone_joint(f"{name}_Hip_{side_name}", hip_pos, scale)
            created_actors.append(hip_bone["actor"])

            # Upper leg (extremely thin)
            upper_leg_scale = (scale * 0.05, scale * 0.05, scale * 0.25)
            upper_leg_pos = (position[0] + side * scale * 0.1, position[1], position[2] + scale * 0.35)
            upper_leg = self._create_composite_cube(f"{name}_UpperLeg_{side_name}", upper_leg_pos, upper_leg_scale, flesh_pale)
            created_actors.append(upper_leg["actor"])

            # Visible femur bone
            femur_scale = (scale * 0.02, scale * 0.02, scale * 0.18)
            femur_pos = (position[0] + side * scale * 0.1, position[1] + scale * 0.028, position[2] + scale * 0.35)
            femur = self._create_composite_cube(f"{name}_Femur_{side_name}", femur_pos, femur_scale, shadow_dark)
            created_actors.append(femur["actor"])

            # Knee joint
            knee_pos = (position[0] + side * scale * 0.1, position[1], position[2] + scale * 0.22)
            knee_bone = self._create_bone_joint(f"{name}_Knee_{side_name}", knee_pos, scale)
            created_actors.append(knee_bone["actor"])

            # Visible kneecap
            kneecap_scale = (scale * 0.025, scale * 0.02, scale * 0.025)
            kneecap_pos = (position[0] + side * scale * 0.1, position[1] - scale * 0.018, position[2] + scale * 0.22)
            kneecap = self._create_composite_cube(f"{name}_Kneecap_{side_name}", kneecap_pos, kneecap_scale, flesh_gray)
            created_actors.append(kneecap["actor"])

            # Lower leg (extremely thin)
            lower_leg_scale = (scale * 0.04, scale * 0.04, scale * 0.22)
            lower_leg_pos = (position[0] + side * scale * 0.1, position[1], position[2] + scale * 0.1)
            lower_leg = self._create_composite_cube(f"{name}_LowerLeg_{side_name}", lower_leg_pos, lower_leg_scale, flesh_pale)
            created_actors.append(lower_leg["actor"])

            # Ankle joint
            ankle_pos = (position[0] + side * scale * 0.1, position[1], position[2])
            ankle_bone = self._create_bone_joint(f"{name}_Ankle_{side_name}", ankle_pos, scale)
            created_actors.append(ankle_bone["actor"])

            # Emaciated foot
            foot_scale = (scale * 0.04, scale * 0.08, scale * 0.02)
            foot_pos = (position[0] + side * scale * 0.1, position[1] - scale * 0.02, position[2] - scale * 0.02)
            foot = self._create_composite_cube(f"{name}_Foot_{side_name}", foot_pos, foot_scale, flesh_gray)
            created_actors.append(foot["actor"])

        # SURFACE DETAIL - Emaciation and wasting
        # Stretch marks
        for i in range(6):
            mark_scale = (scale * 0.08, scale * 0.015, scale * 0.06)
            mark_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.08,
                position[1] + scale * 0.13,
                position[2] + scale * (0.5 + i * scale * 0.08)
            )
            mark = self._create_composite_cube(f"{name}_StretchMark_{i}", mark_pos, mark_scale, shadow_dark)
            created_actors.append(mark["actor"])

        # Bruising (natural, not magical)
        for i in range(4):
            bruise_scale = (scale * 0.06, scale * 0.02, scale * 0.06)
            bruise_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.1,
                position[1] + scale * 0.13,
                position[2] + scale * (0.6 + i * scale * 0.12)
            )
            bruise = self._create_composite_cube(f"{name}_Bruise_{i}", bruise_pos, bruise_scale, bruise_purple)
            created_actors.append(bruise["actor"])

        # Skin deterioration
        for i in range(5):
            deterioration_scale = (scale * 0.07, scale * 0.02, scale * 0.07)
            deterioration_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.09,
                position[1] + ((i // 3) % 2) * scale * 0.12,
                position[2] + scale * (0.65 + i * scale * 0.1)
            )
            deterioration = self._create_composite_cube(f"{name}_SkinDeterioration_{i}", deterioration_pos, deterioration_scale, flesh_gray)
            created_actors.append(deterioration["actor"])

        unreal.log(f"🧠 MIND DEMON created with {len(created_actors)} components (Realistic + Boned)")
        return {
            "message": f"Created {name} (Mind Demon - Realistic + Fully Boned)",
            "name": name,
            "type": "mind demon",
            "actors": created_actors,
            "bones": bones
        }

    def _create_clay_demon_hollywood(self, parsed: dict) -> dict:
        """
        CLAY DEMON - REALISTIC BATTERING RAM VERSION
        Massive siege form (6-9 feet tall)
        Slow unstoppable advance
        Materials: Real drying clay, cracked mud, earth weathering (NO MAGICAL EFFECTS)
        Full bone structure for animation
        """
        name = parsed.get("name") or "ClayDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 2.0

        unreal.log("🏺 Creating CLAY DEMON (Realistic + Boned)...")

        created_actors = []
        bones = {}

        # REALISTIC CLAY COLORS - Natural earth drying
        clay_brown = (0.42, 0.35, 0.28)           # Wet brown clay
        clay_dry = (0.52, 0.45, 0.35)             # Drying clay
        crack_dark = (0.28, 0.22, 0.18)           # Deep cracks
        mud_wet = (0.38, 0.32, 0.25)              # Wet mud
        earth_gray = (0.48, 0.42, 0.38)           # Weathered earth
        pebble_brown = (0.35, 0.30, 0.25)         # Embedded stones

        # MASSIVE SKELETON - Heavy bone structure for battering
        # Pelvis (massive for weight distribution)
        pelvis_pos = (position[0], position[1], position[2] + scale * 0.8)
        pelvis_bone = self._create_bone_joint(f"{name}_Pelvis", pelvis_pos, scale)
        created_actors.append(pelvis_bone["actor"])

        # Spine vertebrae (thick, heavy bones)
        for i in range(7):
            spine_pos = (position[0], position[1], position[2] + scale * (0.9 + i * 0.18))
            spine_bone = self._create_bone_joint(f"{name}_Spine_{i}", spine_pos, scale)
            created_actors.append(spine_bone["actor"])

        # Rib cage (massive barrel chest)
        for i in range(8):
            rib_angle = (math.pi * i) / 8
            rib_pos = (
                position[0] + scale * 0.45 * math.cos(rib_angle),
                position[1] + scale * 0.45 * math.sin(rib_angle),
                position[2] + scale * 1.2
            )
            rib_bone = self._create_bone_joint(f"{name}_Rib_{i}", rib_pos, scale)
            created_actors.append(rib_bone["actor"])

        # MASSIVE BODY - Battering ram form
        body_scale = (scale * 1.0, scale * 0.9, scale * 1.8)
        body_pos = (position[0], position[1], position[2] + scale * 0.9)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, clay_brown)
        created_actors.append(body["actor"])

        # Chest muscle mass (clay-built power)
        for i in range(6):
            chest_scale = (scale * 0.9, scale * 0.08, scale * 0.25)
            chest_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.02,
                position[1] + scale * 0.92,
                position[2] + scale * 1.1 + (i // 2) * scale * 0.35
            )
            chest = self._create_composite_cube(f"{name}_ChestMuscle_{i}", chest_pos, chest_scale, clay_dry)
            created_actors.append(chest["actor"])

        # Abdominal sections
        for i in range(4):
            ab_scale = (scale * 0.85, scale * 0.08, scale * 0.2)
            ab_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.02,
                position[1] + scale * 0.92,
                position[2] + scale * 0.4 + i * scale * 0.18
            )
            ab = self._create_composite_cube(f"{name}_Abdomen_{i}", ab_pos, ab_scale, clay_dry)
            created_actors.append(ab["actor"])

        # Cracked mud texture all over body (extensive cracking)
        for i in range(20):
            crack_scale = (scale * 0.02, scale * 0.25, scale * 0.02)
            crack_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.3,
                position[1] + scale * 0.92,
                position[2] + scale * 0.25 + (i // 4) * scale * 0.25
            )
            crack = self._create_composite_cube(f"{name}_MudCrack_{i}", crack_pos, crack_scale, crack_dark)
            created_actors.append(crack["actor"])

        # Drying patterns (lighter areas)
        for i in range(12):
            dry_scale = (scale * 0.15, scale * 0.04, scale * 0.15)
            dry_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.35,
                position[1] + scale * 0.93,
                position[2] + scale * (0.3 + (i // 5) * scale * 0.35)
            )
            dry = self._create_composite_cube(f"{name}_DryPatch_{i}", dry_pos, dry_scale, clay_dry)
            created_actors.append(dry["actor"])

        # Wide shoulders for ramming (massive bone structure)
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Shoulder joint
            shoulder_pos = (position[0] + side * scale * 0.65, position[1], position[2] + scale * 1.45)
            shoulder_bone = self._create_bone_joint(f"{name}_Shoulder_{side_name}", shoulder_pos, scale)
            created_actors.append(shoulder_bone["actor"])

            shoulder_scale = (scale * 0.5, scale * 0.45, scale * 0.6)
            shoulder_pos = (position[0] + side * scale * 0.7, position[1], position[2] + scale * 1.3)
            shoulder = self._create_composite_cube(f"{name}_Shoulder_{side_name}", shoulder_pos, shoulder_scale, clay_brown)
            created_actors.append(shoulder["actor"])

            # Deltoid muscle (clay-built)
            deltoid_scale = (scale * 0.25, scale * 0.2, scale * 0.25)
            deltoid_pos = (position[0] + side * scale * 0.55, position[1] - scale * 0.08, position[2] + scale * 1.35)
            deltoid = self._create_composite_cube(f"{name}_Deltoid_{side_name}", deltoid_pos, deltoid_scale, clay_dry)
            created_actors.append(deltoid["actor"])

        # THICK NECK - Battering support
        neck_scale = (scale * 0.35, scale * 0.35, scale * 0.3)
        neck_pos = (position[0], position[1], position[2] + scale * 1.6)
        neck = self._create_composite_cube(f"{name}_Neck", neck_pos, neck_scale, clay_brown)
        created_actors.append(neck["actor"])

        # Neck vertebrae
        for i in range(3):
            neck_v_scale = (scale * 0.12, scale * 0.12, scale * 0.08)
            neck_v_pos = (position[0], position[1], position[2] + scale * (1.55 + i * 0.12))
            neck_v = self._create_composite_cube(f"{name}_NeckVertebra_{i}", neck_v_pos, neck_v_scale, earth_gray)
            created_actors.append(neck_v["actor"])

        # Head - Blunt battering ram shape
        head_scale = (scale * 0.5, scale * 0.6, scale * 0.35)
        head_pos = (position[0], position[1], position[2] + scale * 1.9)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, clay_brown)
        created_actors.append(head["actor"])

        # Brow ridge (protection for ramming)
        brow_scale = (scale * 0.45, scale * 0.1, scale * 0.12)
        brow_pos = (head_pos[0], head_pos[1] - scale * 0.32, head_pos[2] + scale * 0.1)
        brow = self._create_composite_cube(f"{name}_BrowRidge", brow_pos, brow_scale, clay_dry)
        created_actors.append(brow["actor"])

        # REALISTIC EYES - Earth-tone, embedded in clay
        for side in [-1, 1]:
            # Eye socket (deep in clay)
            socket_scale = (scale * 0.12, scale * 0.08, scale * 0.1)
            socket_pos = (head_pos[0] + side * scale * 0.15, head_pos[1] - scale * 0.3, head_pos[2])
            socket = self._create_composite_cube(f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, crack_dark)
            created_actors.append(socket["actor"])

            # Eye (muddy brown)
            eye_scale = (scale * 0.08, scale * 0.06, scale * 0.08)
            eye_pos = (head_pos[0] + side * scale * 0.15, head_pos[1] - scale * 0.32, head_pos[2])
            eye = self._create_composite_cube(f"{name}_Eye_{'L' if side < 0 else 'R'}", eye_pos, eye_scale, (0.52, 0.42, 0.32))
            created_actors.append(eye["actor"])

        # Flat nose (blunt for ramming)
        nose_scale = (scale * 0.15, scale * 0.12, scale * 0.1)
        nose_pos = (head_pos[0], head_pos[1] - scale * 0.62, head_pos[2] - scale * 0.05)
        nose = self._create_composite_cube(f"{name}_Nose", nose_pos, nose_scale, earth_gray)
        created_actors.append(nose["actor"])

        # Slit mouth
        mouth_scale = (scale * 0.2, scale * 0.04, scale * 0.08)
        mouth_pos = (head_pos[0], head_pos[1] - scale * 0.62, head_pos[2] - scale * 0.15)
        mouth = self._create_composite_cube(f"{name}_Mouth", mouth_pos, mouth_scale, crack_dark)
        created_actors.append(mouth["actor"])

        # MASSIVE BATTERING ARMS - Built for impact
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Upper arm (massive clay muscle)
            for i in range(4):
                arm_scale = (scale * (0.25 - i * 0.02), scale * 0.25, scale * 0.25)
                arm_pos = (
                    position[0] + side * (scale * 0.6 + i * scale * 0.12),
                    position[1],
                    position[2] + scale * 1.2 - i * scale * 0.15
                )
                arm = self._create_composite_cube(f"{name}_UpperArm_{side_name}_{i}", arm_pos, arm_scale, clay_brown)
                created_actors.append(arm["actor"])

            # Bicep muscle
            bicep_scale = (scale * 0.22, scale * 0.22, scale * 0.35)
            bicep_pos = (position[0] + side * scale * 0.7, position[1] - scale * 0.12, position[2] + scale * 1.1)
            bicep = self._create_composite_cube(f"{name}_Bicep_{side_name}", bicep_pos, bicep_scale, clay_dry)
            created_actors.append(bicep["actor"])

            # Tricep muscle
            tricep_scale = (scale * 0.2, scale * 0.18, scale * 0.3)
            tricep_pos = (position[0] + side * scale * 0.7, position[1] + scale * 0.12, position[2] + scale * 1.1)
            tricep = self._create_composite_cube(f"{name}_Tricep_{side_name}", tricep_pos, tricep_scale, clay_dry)
            created_actors.append(tricep["actor"])

            # Elbow joint
            elbow_pos = (position[0] + side * scale * 0.95, position[1], position[2] + scale * 0.85)
            elbow_bone = self._create_bone_joint(f"{name}_Elbow_{side_name}", elbow_pos, scale)
            created_actors.append(elbow_bone["actor"])

            # Forearm (massive)
            for i in range(3):
                forearm_scale = (scale * (0.22 - i * 0.025), scale * 0.22, scale * 0.22)
                forearm_pos = (
                    position[0] + side * (scale * 0.95 + i * scale * 0.1),
                    position[1],
                    position[2] + scale * 0.75 - i * scale * 0.12
                )
                forearm = self._create_composite_cube(f"{name}_Forearm_{side_name}_{i}", forearm_pos, forearm_scale, clay_brown)
                created_actors.append(forearm["actor"])

            # Wrist joint
            wrist_pos = (position[0] + side * scale * 1.15, position[1], position[2] + scale * 0.55)
            wrist_bone = self._create_bone_joint(f"{name}_Wrist_{side_name}", wrist_pos, scale)
            created_actors.append(wrist_bone["actor"])

            # HUGE BATTERING FIST
            fist_scale = (scale * 0.35, scale * 0.3, scale * 0.3)
            fist_pos = (position[0] + side * scale * 1.0, position[1] - scale * 0.35, position[2] + scale * 0.55)
            fist = self._create_composite_cube(f"{name}_Fist_{side_name}", fist_pos, fist_scale, clay_dry)
            created_actors.append(fist["actor"])

            # Knuckles (protruding)
            for k in range(4):
                knuckle_scale = (scale * 0.08, scale * 0.08, scale * 0.08)
                knuckle_pos = (
                    position[0] + side * scale * 1.0 + (k - 1.5) * scale * 0.08,
                    position[1] - scale * 0.52,
                    position[2] + scale * 0.58
                )
                knuckle = self._create_composite_cube(f"{name}_Knuckle_{side_name}_{k}", knuckle_pos, knuckle_scale, earth_gray)
                created_actors.append(knuckle["actor"])

                # Finger joint
                finger_joint_pos = (
                    position[0] + side * scale * 1.0 + (k - 1.5) * scale * 0.08,
                    position[1] - scale * 0.58,
                    position[2] + scale * 0.55
                )
                finger_joint = self._create_bone_joint(f"{name}_FingerJoint_{side_name}_{k}", finger_joint_pos, scale)
                created_actors.append(finger_joint["actor"])

        # THICK PILLAR LEGS - Stability for battering
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Hip joint
            hip_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.75)
            hip_bone = self._create_bone_joint(f"{name}_Hip_{side_name}", hip_pos, scale)
            created_actors.append(hip_bone["actor"])

            # Upper leg (massive pillar)
            leg_scale = (scale * 0.35, scale * 0.4, scale * 1.0)
            leg_pos = (position[0] + side * scale * 0.35, position[1], position[2])
            leg = self._create_composite_cube(f"{name}_UpperLeg_{side_name}", leg_pos, leg_scale, clay_brown)
            created_actors.append(leg["actor"])

            # Quadriceps muscle
            quad_scale = (scale * 0.32, scale * 0.08, scale * 0.5)
            quad_pos = (position[0] + side * scale * 0.35, position[1] - scale * 0.25, position[2] + scale * 0.35)
            quad = self._create_composite_cube(f"{name}_Quadriceps_{side_name}", quad_pos, quad_scale, clay_dry)
            created_actors.append(quad["actor"])

            # Knee joint
            knee_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.15)
            knee_bone = self._create_bone_joint(f"{name}_Knee_{side_name}", knee_pos, scale)
            created_actors.append(knee_bone["actor"])

            # Kneecap (massive)
            kneecap_scale = (scale * 0.15, scale * 0.12, scale * 0.12)
            kneecap_pos = (position[0] + side * scale * 0.35, position[1] - scale * 0.32, position[2] + scale * 0.2)
            kneecap = self._create_composite_cube(f"{name}_Kneecap_{side_name}", kneecap_pos, kneecap_scale, earth_gray)
            created_actors.append(kneecap["actor"])

            # Lower leg
            lower_scale = (scale * 0.32, scale * 0.35, scale * 0.85)
            lower_pos = (position[0] + side * scale * 0.35, position[1], position[2] - scale * 0.25)
            lower = self._create_composite_cube(f"{name}_LowerLeg_{side_name}", lower_pos, lower_scale, clay_brown)
            created_actors.append(lower["actor"])

            # Calf muscle
            calf_scale = (scale * 0.28, scale * 0.1, scale * 0.4)
            calf_pos = (position[0] + side * scale * 0.35, position[1] + scale * 0.25, position[2] - scale * 0.1)
            calf = self._create_composite_cube(f"{name}_Calf_{side_name}", calf_pos, calf_scale, clay_dry)
            created_actors.append(calf["actor"])

            # Ankle joint
            ankle_pos = (position[0] + side * scale * 0.35, position[1], position[2] - scale * 0.6)
            ankle_bone = self._create_bone_joint(f"{name}_Ankle_{side_name}", ankle_pos, scale)
            created_actors.append(ankle_bone["actor"])

            # WIDE FOOT for stability
            foot_scale = (scale * 0.4, scale * 0.15, scale * 0.35)
            foot_pos = (position[0] + side * scale * 0.35, position[1], position[2] - scale * 0.8)
            foot = self._create_composite_cube(f"{name}_Foot_{side_name}", foot_pos, foot_scale, clay_dry)
            created_actors.append(foot["actor"])

        # SURFACE DETAIL - Realistic clay weathering
        # Dripping mud details (wet clay)
        for i in range(10):
            drip_scale = (scale * 0.08, scale * 0.08, scale * 0.12)
            drip_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.5,
                position[1] + scale * 0.95,
                position[2] + scale * 0.2 + (i // 2) * scale * 0.35
            )
            drip = self._create_composite_cube(f"{name}_MudDrip_{i}", drip_pos, drip_scale, mud_wet)
            created_actors.append(drip["actor"])

        # Embedded pebbles/debris
        for i in range(8):
            pebble_scale = (scale * 0.06, scale * 0.06, scale * 0.06)
            pebble_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.35,
                position[1] + scale * 0.96,
                position[2] + scale * (0.4 + (i // 4) * scale * 0.5)
            )
            pebble = self._create_composite_cube(f"{name}_Pebble_{i}", pebble_pos, pebble_scale, pebble_brown)
            created_actors.append(pebble["actor"])

        # Weathering cracks on legs
        for i in range(6):
            leg_crack_scale = (scale * 0.025, scale * 0.2, scale * 0.025)
            leg_crack_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.4,
                position[1] + scale * 0.42,
                position[2] + scale * (0.1 + i * scale * 0.15)
            )
            leg_crack = self._create_composite_cube(f"{name}_LegCrack_{i}", leg_crack_pos, leg_crack_scale, crack_dark)
            created_actors.append(leg_crack["actor"])

        # Erosion patterns
        for i in range(5):
            erosion_scale = (scale * 0.12, scale * 0.03, scale * 0.12)
            erosion_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.45,
                position[1] + scale * 0.93,
                position[2] + scale * (0.5 + i * scale * 0.25)
            )
            erosion = self._create_composite_cube(f"{name}_Erosion_{i}", erosion_pos, erosion_scale, earth_gray)
            created_actors.append(erosion["actor"])

        unreal.log(f"🏺 CLAY DEMON created with {len(created_actors)} components (Realistic + Boned)")
        return {
            "message": f"Created {name} (Clay Demon - Realistic + Fully Boned)",
            "name": name,
            "type": "clay demon",
            "actors": created_actors,
            "bones": bones
        }

    def _create_wind_demon_hollywood(self, parsed: dict) -> dict:
        """
        WIND DEMON - REALISTIC BAT-LIKE VERSION
        Aerial predator (6-8 foot wingspan)
        Flying hunter with membrane wings
        Materials: Real leather, translucent membrane, fur patches (NO GLOWING EYES)
        Full bone structure for animation
        """
        name = parsed.get("name") or "WindDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.3

        unreal.log("💨 Creating WIND DEMON (Realistic + Boned)...")

        created_actors = []
        bones = {}

        # REALISTIC BAT COLORS - Natural aerial predator appearance
        leather_brown = (0.28, 0.24, 0.20)       # Dark leather skin
        membrane_pink = (0.42, 0.38, 0.35)       # Natural membrane (not glowing)
        fur_dark = (0.22, 0.20, 0.18)            # Dark brown fur
        claw_bone = (0.35, 0.32, 0.28)           # Bone claws
        eye_dark = (0.15, 0.12, 0.10)            # Dark bat eyes (NOT red)
        skin_pink = (0.48, 0.42, 0.38)           # Pinkish skin patches

        # BAT SKELETON - Lightweight flying structure
        # Spine vertebrae (flexible for flight)
        for i in range(10):
            spine_pos = (position[0], position[1], position[2] + scale * (0.4 + i * 0.1))
            spine_bone = self._create_bone_joint(f"{name}_Spine_{i}", spine_pos, scale)
            created_actors.append(spine_bone["actor"])

        # Rib cage (lightweight)
        for i in range(6):
            rib_angle = (math.pi * i) / 6
            rib_pos = (
                position[0] + scale * 0.12 * math.cos(rib_angle),
                position[1] + scale * 0.12 * math.sin(rib_angle),
                position[2] + scale * 0.7
            )
            rib_bone = self._create_bone_joint(f"{name}_Rib_{i}", rib_pos, scale)
            created_actors.append(rib_bone["actor"])

        # LEAN BODY - Lightweight for flight
        body_scale = (scale * 0.35, scale * 0.25, scale * 1.0)
        body_pos = (position[0], position[1], position[2] + scale * 0.5)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, leather_brown)
        created_actors.append(body["actor"])

        # Fur patches on body
        for i in range(8):
            fur_scale = (scale * 0.12, scale * 0.035, scale * 0.15)
            fur_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.18,
                position[1] + scale * 0.26,
                position[2] + scale * (0.35 + (i // 2) * scale * 0.3)
            )
            fur = self._create_composite_cube(f"{name}_FurPatch_{i}", fur_pos, fur_scale, fur_dark)
            created_actors.append(fur["actor"])

        # BAT-LIKE HEAD
        head_scale = (scale * 0.2, scale * 0.25, scale * 0.22)
        head_pos = (position[0], position[1], position[2] + scale * 1.05)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, leather_brown)
        created_actors.append(head["actor"])

        # REALISTIC BAT EARS - Large for echolocation
        for side in [-1, 1]:
            # Outer ear
            ear_scale = (scale * 0.12, scale * 0.15, scale * 0.08)
            ear_pos = (head_pos[0] + side * scale * 0.12, head_pos[1] - scale * 0.2, head_pos[2] + scale * 0.08)
            ear = self._create_composite_cube(f"{name}_Ear_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, leather_brown)
            created_actors.append(ear["actor"])

            # Inner ear (pink membrane)
            inner_scale = (scale * 0.08, scale * 0.1, scale * 0.05)
            inner_pos = (ear_pos[0], ear_pos[1], ear_pos[2] + scale * 0.015)
            inner = self._create_composite_cube(f"{name}_InnerEar_{'L' if side < 0 else 'R'}", inner_pos, inner_scale, skin_pink)
            created_actors.append(inner["actor"])

        # REALISTIC EYES - Dark bat eyes (NOT red)
        for side in [-1, 1]:
            # Eye socket
            socket_scale = (scale * 0.05, scale * 0.04, scale * 0.05)
            socket_pos = (head_pos[0] + side * scale * 0.06, head_pos[1] - scale * 0.24, head_pos[2] + scale * 0.02)
            socket = self._create_composite_cube(f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, eye_dark)
            created_actors.append(socket["actor"])

            # Eye (dark brown-black)
            eye_scale = (scale * 0.035, scale * 0.035, scale * 0.035)
            eye_pos = (head_pos[0] + side * scale * 0.06, head_pos[1] - scale * 0.25, head_pos[2] + scale * 0.02)
            eye = self._create_composite_cube(f"{name}_Eye_{'L' if side < 0 else 'R'}", eye_pos, eye_scale, (0.18, 0.15, 0.12))
            created_actors.append(eye["actor"])

        # Bat nose
        nose_scale = (scale * 0.06, scale * 0.06, scale * 0.05)
        nose_pos = (head_pos[0], head_pos[1] - scale * 0.32, head_pos[2] - scale * 0.02)
        nose = self._create_composite_cube(f"{name}_Nose", nose_pos, nose_scale, skin_pink)
        created_actors.append(nose["actor"])

        # MASSIVE LEATHER WINGS - Realistic bat wing structure with visible bones
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Shoulder joint for wing
            shoulder_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.8)
            shoulder_bone = self._create_bone_joint(f"{name}_WingShoulder_{side_name}", shoulder_pos, scale)
            created_actors.append(shoulder_bone["actor"])

            # Wing arm bones (like elongated fingers)
            # Main wing bone (humerus equivalent)
            humerus_scale = (scale * 0.06, scale * 0.06, scale * 0.5)
            humerus_pos = (position[0] + side * (scale * 0.4 + scale * 0.3), position[1] - scale * 0.1, position[2] + scale * 0.75)
            humerus = self._create_composite_cube(f"{name}_WingHumerus_{side_name}", humerus_pos, humerus_scale, leather_brown)
            created_actors.append(humerus["actor"])

            # Elbow joint
            elbow_pos = (position[0] + side * (scale * 0.45 + scale * 0.5), position[1] - scale * 0.08, position[2] + scale * 0.7)
            elbow_bone = self._create_bone_joint(f"{name}_WingElbow_{side_name}", elbow_pos, scale)
            created_actors.append(elbow_bone["actor"])

            # Radiating wing bones (like bat fingers)
            for f in range(4):
                # Finger bone
                finger_scale = (scale * 0.04, scale * 0.04, scale * (0.6 - f * 0.1))
                finger_pos = (
                    position[0] + side * (scale * 0.5 + (f + 1) * scale * 0.35),
                    position[1] - scale * 0.08 + f * scale * 0.03,
                    position[2] + scale * (0.65 + f * scale * 0.05)
                )
                finger = self._create_composite_cube(f"{name}_WingFinger_{side_name}_{f}", finger_pos, finger_scale, leather_brown)
                created_actors.append(finger["actor"])

                # Finger joint
                joint_pos = (
                    position[0] + side * (scale * 0.55 + (f + 1) * scale * 0.4),
                    position[1] - scale * 0.06 + f * scale * 0.03,
                    position[2] + scale * (0.6 + f * scale * 0.04)
                )
                joint_bone = self._create_bone_joint(f"{name}_WingFingerJoint_{side_name}_{f}", joint_pos, scale)
                created_actors.append(joint_bone["actor"])

            # Wing membranes between fingers (natural, translucent)
            for f in range(3):
                membrane_scale = (scale * 0.6, scale * 0.015, scale * (0.7 - f * 0.15))
                membrane_pos = (
                    position[0] + side * (scale * 0.7 + f * scale * 0.35),
                    position[1] - scale * 0.08,
                    position[2] + scale * 0.7
                )
                membrane = self._create_composite_cube(f"{name}_WingMembrane_{side_name}_{f}", membrane_pos, membrane_scale, membrane_pink)
                created_actors.append(membrane["actor"])

            # Main wing membrane
            main_membrane_scale = (scale * 1.6, scale * 0.018, scale * 1.0)
            main_membrane_pos = (
                position[0] + side * scale * 1.2,
                position[1] - scale * 0.1,
                position[2] + scale * 0.75
            )
            main_membrane = self._create_composite_cube(f"{name}_MainWingMembrane_{side_name}", main_membrane_pos, main_membrane_scale, membrane_pink)
            created_actors.append(main_membrane["actor"])

        # CLAWED ARMS - Smaller arms separate from wings
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Shoulder joint for arm
            arm_shoulder_pos = (position[0] + side * scale * 0.25, position[1], position[2] + scale * 0.65)
            arm_shoulder_bone = self._create_bone_joint(f"{name}_ArmShoulder_{side_name}", arm_shoulder_pos, scale)
            created_actors.append(arm_shoulder_bone["actor"])

            # Upper arm
            arm_scale = (scale * 0.08, scale * 0.08, scale * 0.25)
            arm_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.5)
            arm = self._create_composite_cube(f"{name}_Arm_{side_name}", arm_pos, arm_scale, leather_brown)
            created_actors.append(arm["actor"])

            # Elbow joint
            elbow_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.4)
            elbow_bone = self._create_bone_joint(f"{name}_ArmElbow_{side_name}", elbow_pos, scale)
            created_actors.append(elbow_bone["actor"])

            # Forearm
            forearm_scale = (scale * 0.06, scale * 0.06, scale * 0.2)
            forearm_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.3)
            forearm = self._create_composite_cube(f"{name}_Forearm_{side_name}", forearm_pos, forearm_scale, leather_brown)
            created_actors.append(forearm["actor"])

            # Wrist joint
            wrist_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.22)
            wrist_bone = self._create_bone_joint(f"{name}_Wrist_{side_name}", wrist_pos, scale)
            created_actors.append(wrist_bone["actor"])

            # Hand
            hand_scale = (scale * 0.07, scale * 0.06, scale * 0.06)
            hand_pos = (position[0] + side * scale * 0.35, position[1] - scale * 0.04, position[2] + scale * 0.2)
            hand = self._create_composite_cube(f"{name}_Hand_{side_name}", hand_pos, hand_scale, leather_brown)
            created_actors.append(hand["actor"])

            # Claws (3 per hand)
            for c in range(3):
                claw_scale = (scale * 0.025, scale * 0.08, scale * 0.025)
                claw_pos = (
                    position[0] + side * scale * 0.35 + (c - 1) * scale * 0.02,
                    position[1] - scale * 0.1,
                    position[2] + scale * 0.18
                )
                claw = self._create_composite_cube(f"{name}_Claw_{side_name}_{c}", claw_pos, claw_scale, claw_bone)
                created_actors.append(claw["actor"])

                # Finger joint
                finger_joint_pos = (
                    position[0] + side * scale * 0.35 + (c - 1) * scale * 0.02,
                    position[1] - scale * 0.12,
                    position[2] + scale * 0.14
                )
                finger_joint = self._create_bone_joint(f"{name}_HandFingerJoint_{side_name}_{c}", finger_joint_pos, scale)
                created_actors.append(finger_joint["actor"])

        # CLAWED LEGS - Hooked for perching
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            # Hip joint
            hip_pos = (position[0] + side * scale * 0.15, position[1], position[2] + scale * 0.45)
            hip_bone = self._create_bone_joint(f"{name}_Hip_{side_name}", hip_pos, scale)
            created_actors.append(hip_bone["actor"])

            # Upper leg
            leg_scale = (scale * 0.08, scale * 0.08, scale * 0.25)
            leg_pos = (position[0] + side * scale * 0.2, position[1], position[2] + scale * 0.35)
            leg = self._create_composite_cube(f"{name}_UpperLeg_{side_name}", leg_pos, leg_scale, leather_brown)
            created_actors.append(leg["actor"])

            # Knee joint
            knee_pos = (position[0] + side * scale * 0.2, position[1], position[2] + scale * 0.22)
            knee_bone = self._create_bone_joint(f"{name}_Knee_{side_name}", knee_pos, scale)
            created_actors.append(knee_bone["actor"])

            # Lower leg
            lower_scale = (scale * 0.06, scale * 0.06, scale * 0.2)
            lower_pos = (position[0] + side * scale * 0.2, position[1], position[2] + scale * 0.12)
            lower = self._create_composite_cube(f"{name}_LowerLeg_{side_name}", lower_pos, lower_scale, leather_brown)
            created_actors.append(lower["actor"])

            # Ankle joint
            ankle_pos = (position[0] + side * scale * 0.2, position[1], position[2])
            ankle_bone = self._create_bone_joint(f"{name}_Ankle_{side_name}", ankle_pos, scale)
            created_actors.append(ankle_bone["actor"])

            # Foot (hooked for perching)
            foot_scale = (scale * 0.1, scale * 0.08, scale * 0.05)
            foot_pos = (position[0] + side * scale * 0.2, position[1] - scale * 0.15, position[2] - scale * 0.02)
            foot = self._create_composite_cube(f"{name}_Foot_{side_name}", foot_pos, foot_scale, claw_bone)
            created_actors.append(foot["actor"])

        # Tail membrane (between legs)
        tail_scale = (scale * 0.05, scale * 0.3, scale * 0.05)
        tail_pos = (position[0], position[1] + scale * 0.25, position[2] + scale * 0.4)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, leather_brown)
        created_actors.append(tail["actor"])

        # Tail membrane
        tail_membrane_scale = (scale * 0.15, scale * 0.2, scale * 0.015)
        tail_membrane_pos = (position[0], position[1] + scale * 0.35, position[2] + scale * 0.35)
        tail_membrane = self._create_composite_cube(f"{name}_TailMembrane", tail_membrane_pos, tail_membrane_scale, membrane_pink)
        created_actors.append(tail_membrane["actor"])

        # SURFACE DETAIL - Realistic bat weathering
        # Skin folds
        for i in range(6):
            fold_scale = (scale * 0.08, scale * 0.02, scale * 0.08)
            fold_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.15,
                position[1] + scale * 0.26,
                position[2] + scale * (0.45 + i * scale * 0.08)
            )
            fold = self._create_composite_cube(f"{name}_SkinFold_{i}", fold_pos, fold_scale, skin_pink)
            created_actors.append(fold["actor"])

        # Wear on wing membranes
        for i in range(4):
            wear_scale = (scale * 0.2, scale * 0.015, scale * 0.15)
            wear_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 1.1,
                position[1] - scale * 0.1,
                position[2] + scale * (0.65 + i * scale * 0.1)
            )
            wear = self._create_composite_cube(f"{name}_WingWear_{i}", wear_pos, wear_scale, leather_brown)
            created_actors.append(wear["actor"])

        unreal.log(f"💨 WIND DEMON created with {len(created_actors)} components (Realistic + Boned)")
        return {
            "message": f"Created {name} (Wind Demon - Realistic + Fully Boned)",
            "name": name,
            "type": "wind demon",
            "actors": created_actors,
            "bones": bones
        }

    def _create_lightning_demon_hollywood(self, parsed: dict) -> dict:
        """
        LIGHTNING DEMON - REALISTIC CHARRED BAT VERSION
        Aerial predator variant (6-8 foot wingspan)
        Fast, agile flying hunter
        Materials: Charred leather, dark membrane, ozone-weathered skin (NO ELECTRIC EFFECTS)
        Full bone structure for animation
        """
        name = parsed.get("name") or "LightningDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.3

        unreal.log("⚡ Creating LIGHTNING DEMON (Realistic + Boned)...")

        created_actors = []
        bones = {}

        # REALISTIC CHARRED BAT COLORS - Weathered aerial predator
        leather_charred = (0.22, 0.20, 0.18)     # Charred leather
        membrane_dark = (0.28, 0.26, 0.24)        # Dark membrane
        fur_black = (0.15, 0.14, 0.12)            # Blackened fur
        claw_charred = (0.28, 0.26, 0.24)         # Charred bone
        eye_black = (0.12, 0.10, 0.08)            # Black eyes
        skin_gray = (0.35, 0.33, 0.30)            # Weathered skin

        # BAT SKELETON - Lightweight structure
        for i in range(10):
            spine_pos = (position[0], position[1], position[2] + scale * (0.4 + i * 0.1))
            spine_bone = self._create_bone_joint(f"{name}_Spine_{i}", spine_pos, scale)
            created_actors.append(spine_bone["actor"])

        for i in range(6):
            rib_angle = (math.pi * i) / 6
            rib_pos = (
                position[0] + scale * 0.12 * math.cos(rib_angle),
                position[1] + scale * 0.12 * math.sin(rib_angle),
                position[2] + scale * 0.7
            )
            rib_bone = self._create_bone_joint(f"{name}_Rib_{i}", rib_pos, scale)
            created_actors.append(rib_bone["actor"])

        # LEAN BODY
        body_scale = (scale * 0.35, scale * 0.25, scale * 1.0)
        body_pos = (position[0], position[1], position[2] + scale * 0.5)
        body = self._create_composite_cube(f"{name}_Torso", body_pos, body_scale, leather_charred)
        created_actors.append(body["actor"])

        # BAT HEAD
        head_scale = (scale * 0.2, scale * 0.25, scale * 0.22)
        head_pos = (position[0], position[1], position[2] + scale * 1.05)
        head = self._create_composite_cube(f"{name}_Head", head_pos, head_scale, leather_charred)
        created_actors.append(head["actor"])

        # Ears
        for side in [-1, 1]:
            ear_scale = (scale * 0.12, scale * 0.15, scale * 0.08)
            ear_pos = (head_pos[0] + side * scale * 0.12, head_pos[1] - scale * 0.2, head_pos[2] + scale * 0.08)
            ear = self._create_composite_cube(f"{name}_Ear_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, leather_charred)
            created_actors.append(ear["actor"])

        # REALISTIC EYES - Dark, not electric
        for side in [-1, 1]:
            socket_scale = (scale * 0.05, scale * 0.04, scale * 0.05)
            socket_pos = (head_pos[0] + side * scale * 0.06, head_pos[1] - scale * 0.24, head_pos[2] + scale * 0.02)
            socket = self._create_composite_cube(f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, eye_black)
            created_actors.append(socket["actor"])

            eye_scale = (scale * 0.035, scale * 0.035, scale * 0.035)
            eye_pos = (head_pos[0] + side * scale * 0.06, head_pos[1] - scale * 0.25, head_pos[2] + scale * 0.02)
            eye = self._create_composite_cube(f"{name}_Eye_{'L' if side < 0 else 'R'}", eye_pos, eye_scale, (0.15, 0.12, 0.10))
            created_actors.append(eye["actor"])

        # DARK WINGS - Realistic structure
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            shoulder_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.8)
            shoulder_bone = self._create_bone_joint(f"{name}_WingShoulder_{side_name}", shoulder_pos, scale)
            created_actors.append(shoulder_bone["actor"])

            for i in range(3):
                wing_segment_scale = (scale * (1.5 - i * 0.3), scale * 0.04, scale * 0.15)
                wing_segment_pos = (
                    position[0] + side * (scale * 0.5 + i * scale * 0.4),
                    position[1] - scale * 0.1 + i * scale * 0.05,
                    position[2] + scale * 0.7 + i * scale * 0.1
                )
                wing_segment = self._create_composite_cube(f"{name}_WingArm_{side_name}_{i}", wing_segment_pos, wing_segment_scale, leather_charred)
                created_actors.append(wing_segment["actor"])

                # Joint
                joint_pos = (wing_segment_pos[0], wing_segment_pos[1], wing_segment_pos[2] + scale * 0.05)
                joint_bone = self._create_bone_joint(f"{name}_WingJoint_{side_name}_{i}", joint_pos, scale)
                created_actors.append(joint_bone["actor"])

            # Wing membrane
            membrane_scale = (scale * 1.8, scale * 0.02, scale * 1.2)
            membrane_pos = (position[0] + side * scale * 1.2, position[1] - scale * 0.1, position[2] + scale * 0.8)
            membrane = self._create_composite_cube(f"{name}_WingMembrane_{side_name}", membrane_pos, membrane_scale, membrane_dark)
            created_actors.append(membrane["actor"])

        # LIMBS with joints
        for side in [-1, 1]:
            side_name = 'L' if side < 0 else 'R'

            arm_shoulder_pos = (position[0] + side * scale * 0.25, position[1], position[2] + scale * 0.65)
            arm_shoulder_bone = self._create_bone_joint(f"{name}_ArmShoulder_{side_name}", arm_shoulder_pos, scale)
            created_actors.append(arm_shoulder_bone["actor"])

            arm_scale = (scale * 0.08, scale * 0.08, scale * 0.25)
            arm_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.5)
            arm = self._create_composite_cube(f"{name}_Arm_{side_name}", arm_pos, arm_scale, leather_charred)
            created_actors.append(arm["actor"])

            elbow_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.4)
            elbow_bone = self._create_bone_joint(f"{name}_Elbow_{side_name}", elbow_pos, scale)
            created_actors.append(elbow_bone["actor"])

            forearm_scale = (scale * 0.06, scale * 0.06, scale * 0.2)
            forearm_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.3)
            forearm = self._create_composite_cube(f"{name}_Forearm_{side_name}", forearm_pos, forearm_scale, leather_charred)
            created_actors.append(forearm["actor"])

            wrist_pos = (position[0] + side * scale * 0.35, position[1], position[2] + scale * 0.22)
            wrist_bone = self._create_bone_joint(f"{name}_Wrist_{side_name}", wrist_pos, scale)
            created_actors.append(wrist_bone["actor"])

            # Claws
            for c in range(3):
                claw_scale = (scale * 0.025, scale * 0.08, scale * 0.025)
                claw_pos = (position[0] + side * scale * 0.35 + (c - 1) * scale * 0.02, position[1] - scale * 0.1, position[2] + scale * 0.18)
                claw = self._create_composite_cube(f"{name}_Claw_{side_name}_{c}", claw_pos, claw_scale, claw_charred)
                created_actors.append(claw["actor"])

            hip_pos = (position[0] + side * scale * 0.15, position[1], position[2] + scale * 0.45)
            hip_bone = self._create_bone_joint(f"{name}_Hip_{side_name}", hip_pos, scale)
            created_actors.append(hip_bone["actor"])

            leg_scale = (scale * 0.08, scale * 0.08, scale * 0.25)
            leg_pos = (position[0] + side * scale * 0.2, position[1], position[2] + scale * 0.35)
            leg = self._create_composite_cube(f"{name}_Leg_{side_name}", leg_pos, leg_scale, leather_charred)
            created_actors.append(leg["actor"])

            knee_pos = (position[0] + side * scale * 0.2, position[1], position[2] + scale * 0.22)
            knee_bone = self._create_bone_joint(f"{name}_Knee_{side_name}", knee_pos, scale)
            created_actors.append(knee_bone["actor"])

            lower_scale = (scale * 0.06, scale * 0.06, scale * 0.2)
            lower_pos = (position[0] + side * scale * 0.2, position[1], position[2] + scale * 0.12)
            lower = self._create_composite_cube(f"{name}_LowerLeg_{side_name}", lower_pos, lower_scale, leather_charred)
            created_actors.append(lower["actor"])

            ankle_pos = (position[0] + side * scale * 0.2, position[1], position[2])
            ankle_bone = self._create_bone_joint(f"{name}_Ankle_{side_name}", ankle_pos, scale)
            created_actors.append(ankle_bone["actor"])

            foot_scale = (scale * 0.1, scale * 0.08, scale * 0.05)
            foot_pos = (position[0] + side * scale * 0.2, position[1] - scale * 0.15, position[2] - scale * 0.02)
            foot = self._create_composite_cube(f"{name}_Foot_{side_name}", foot_pos, foot_scale, claw_charred)
            created_actors.append(foot["actor"])

        # Tail
        tail_scale = (scale * 0.05, scale * 0.3, scale * 0.05)
        tail_pos = (position[0], position[1] + scale * 0.25, position[2] + scale * 0.4)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, leather_charred)
        created_actors.append(tail["actor"])

        # SURFACE DETAIL - Weathering
        for i in range(8):
            weather_scale = (scale * 0.08, scale * 0.02, scale * 0.08)
            weather_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.15,
                position[1] + scale * 0.26,
                position[2] + scale * (0.45 + i * scale * 0.1)
            )
            weather = self._create_composite_cube(f"{name}_Weather_{i}", weather_pos, weather_scale, skin_gray)
            created_actors.append(weather["actor"])

        unreal.log(f"⚡ LIGHTNING DEMON created with {len(created_actors)} components (Realistic + Boned)")
        return {
            "message": f"Created {name} (Lightning Demon - Realistic + Fully Boned)",
            "name": name,
            "type": "lightning demon",
            "actors": created_actors,
            "bones": bones
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
        SAND DEMON - REALISTIC QUADRUPEDAL ANIMATABLE VERSION
        Quadrupedal pack hunter (4-6 feet long)
        Low-slung desert predator
        Materials: Real desert sandstone, sun-bleached bone, wind-eroded surfaces (NO GLOW)
        Full quadrupedal bone structure for animation
        """
        name = parsed.get("name") or "SandDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.2

        unreal.log("🏜️ Creating SAND DEMON (Realistic + Boned)...")

        created_actors = []
        bones = {}

        # REALISTIC DESERT COLORS - Natural sandstone appearance
        sand_base = (0.78, 0.72, 0.58)           # Desert sandstone
        sand_dark = (0.65, 0.58, 0.45)           # Shaded sand
        sun_bleached = (0.88, 0.82, 0.70)        # Sun-bleached surfaces
        erosion_brown = (0.58, 0.50, 0.40)       # Wind-eroded areas
        crack_shadow = (0.45, 0.40, 0.32)        # Deep crack shadows
        sand_dust = (0.85, 0.80, 0.68)           # Surface dust

        # QUADRUPEDAL SKELETON - Desert predator structure
        # Spine vertebrae (neck to tail)
        for i in range(9):
            spine_pos = (position[0], position[1] - scale * 0.2 + i * scale * 0.12, position[2] + scale * 0.55)
            spine_bone = self._create_bone_joint(f"{name}_Spine_{i}", spine_pos, scale)
            created_actors.append(spine_bone["actor"])

        # Rib cage
        for i in range(6):
            rib_angle = (math.pi * i) / 6
            rib_pos = (
                position[0] + scale * 0.24 * math.cos(rib_angle),
                position[1] + scale * 0.5 + scale * 0.24 * math.sin(rib_angle),
                position[2] + scale * 0.6
            )
            rib_bone = self._create_bone_joint(f"{name}_Rib_{i}", rib_pos, scale)
            created_actors.append(rib_bone["actor"])

        # BODY - Low-slung desert hunter torso
        torso_scale = (scale * 0.5, scale * 0.35, scale * 1.0)
        torso_pos = (position[0], position[1], position[2] + scale * 0.4)
        torso = self._create_composite_cube(f"{name}_Torso", torso_pos, torso_scale, sand_base)
        created_actors.append(torso["actor"])

        # Chest definition
        chest_scale = (scale * 0.45, scale * 0.08, scale * 0.35)
        chest_pos = (position[0], position[1] + scale * 0.37, position[2] + scale * 0.55)
        chest = self._create_composite_cube(f"{name}_Chest", chest_pos, chest_scale, sun_bleached)
        created_actors.append(chest["actor"])

        # Spine ridge (sand-colored, NOT crystalline glowing)
        for i in range(8):
            ridge_scale = (scale * 0.05, scale * 0.05, scale * 0.08)
            ridge_pos = (
                position[0],
                position[1] - scale * 0.14 + i * scale * 0.12,
                position[2] + scale * 0.85
            )
            ridge = self._create_composite_cube(f"{name}_SpineRidge_{i}", ridge_pos, ridge_scale, sun_bleached)
            created_actors.append(ridge["actor"])

        # NECK - Flexible desert predator neck
        for i in range(3):
            neck_scale = (scale * 0.12, scale * 0.12, scale * 0.08)
            neck_pos = (position[0], position[1] - scale * (0.35 + i * 0.08), position[2] + scale * 0.58)
            neck = self._create_composite_cube(f"{name}_NeckVertebra_{i}", neck_pos, neck_scale, sand_base)
            created_actors.append(neck["actor"])

        neck_main_scale = (scale * 0.18, scale * 0.18, scale * 0.18)
        neck_main_pos = (position[0], position[1] - scale * 0.35, position[2] + scale * 0.54)
        neck_main = self._create_composite_cube(f"{name}_Neck_Main", neck_main_pos, neck_main_scale, sand_base)
        created_actors.append(neck_main["actor"])

        # HEAD - Sleek desert predator skull
        skull_scale = (scale * 0.25, scale * 0.35, scale * 0.2)
        skull_pos = (position[0], position[1] - scale * 0.5, position[2] + scale * 0.48)
        skull = self._create_composite_cube(f"{name}_Skull", skull_pos, skull_scale, sand_base)
        created_actors.append(skull["actor"])

        # Brow ridges
        for side in [-1, 1]:
            brow_scale = (scale * 0.1, scale * 0.04, scale * 0.06)
            brow_pos = (position[0] + side * scale * 0.08, position[1] - scale * 0.53, position[2] + scale * 0.53)
            brow = self._create_composite_cube(f"{name}_Brow_{'L' if side < 0 else 'R'}", brow_pos, brow_scale, sun_bleached)
            created_actors.append(brow["actor"])

        # Snout
        snout_scale = (scale * 0.15, scale * 0.2, scale * 0.12)
        snout_pos = (position[0], position[1] - scale * 0.7, position[2] + scale * 0.45)
        snout = self._create_composite_cube(f"{name}_Snout", snout_pos, snout_scale, sand_base)
        created_actors.append(snout["actor"])

        # Jaw
        jaw_scale = (scale * 0.18, scale * 0.08, scale * 0.08)
        jaw_pos = (position[0], position[1] - scale * 0.68, position[2] + scale * 0.4)
        jaw = self._create_composite_cube(f"{name}_Jaw", jaw_pos, jaw_scale, sand_dark)
        created_actors.append(jaw["actor"])

        # Chin
        chin_scale = (scale * 0.1, scale * 0.06, scale * 0.06)
        chin_pos = (position[0], position[1] - scale * 0.72, position[2] + scale * 0.42)
        chin = self._create_composite_cube(f"{name}_Chin", chin_pos, chin_scale, sand_base)
        created_actors.append(chin["actor"])

        # REALISTIC EYES - Amber predator eyes (NOT glowing gold)
        for side in [-1, 1]:
            # Eye socket
            socket_scale = (scale * 0.07, scale * 0.06, scale * 0.07)
            socket_pos = (position[0] + side * scale * 0.08, position[1] - scale * 0.55, position[2] + scale * 0.5)
            socket = self._create_composite_cube(f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, crack_shadow)
            created_actors.append(socket["actor"])

            # Eye (realistic amber)
            eye_scale = (scale * 0.05, scale * 0.05, scale * 0.045)
            eye_pos = (position[0] + side * scale * 0.08, position[1] - scale * 0.57, position[2] + scale * 0.5)
            eye = self._create_composite_cube(f"{name}_Eye_{'L' if side < 0 else 'R'}", eye_pos, eye_scale, (0.75, 0.58, 0.32))
            created_actors.append(eye["actor"])

            # Eyelid
            eyelid_scale = (scale * 0.055, scale * 0.025, scale * 0.05)
            eyelid_pos = (position[0] + side * scale * 0.08, position[1] - scale * 0.52, position[2] + scale * 0.53)
            eyelid = self._create_composite_cube(f"{name}_Eyelid_{'L' if side < 0 else 'R'}", eyelid_pos, eyelid_scale, sand_base)
            created_actors.append(eyelid["actor"])

        # Nostrils
        for side in [-1, 1]:
            nostril_scale = (scale * 0.02, scale * 0.035, scale * 0.02)
            nostril_pos = (position[0] + side * scale * 0.035, position[1] - scale * 0.82, position[2] + scale * 0.45)
            nostril = self._create_composite_cube(f"{name}_Nostril_{'L' if side < 0 else 'R'}", nostril_pos, nostril_scale, crack_shadow)
            created_actors.append(nostril["actor"])

        # Teeth (desert predator teeth)
        for i in range(6):
            tooth_scale = (scale * 0.025, scale * 0.04, scale * 0.025)
            tooth_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.05,
                position[1] - scale * 0.7,
                position[2] + scale * (0.42 + (i // 3) * scale * 0.025)
            )
            tooth = self._create_composite_cube(f"{name}_Tooth_{i}", tooth_pos, tooth_scale, sun_bleached)
            created_actors.append(tooth["actor"])

        # Ear ridges
        for side in [-1, 1]:
            ear_scale = (scale * 0.08, scale * 0.08, scale * 0.12)
            ear_pos = (position[0] + side * scale * 0.12, position[1] - scale * 0.4, position[2] + scale * 0.54)
            ear = self._create_composite_cube(f"{name}_EarRidge_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, sand_base)
            created_actors.append(ear["actor"])

        # QUADRUPEDAL LEGS - Pack hunter limbs with full anatomy
        leg_positions = [
            (-1, -1, "FrontLeft"),   # Front left
            (1, -1, "FrontRight"),   # Front right
            (-1, 1, "BackLeft"),     # Back left
            (1, 1, "BackRight")      # Back right
        ]

        for side_x, side_y, leg_name in leg_positions:
            # Shoulder/Hip joint
            joint_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] + scale * 0.35
            )
            joint_bone = self._create_bone_joint(f"{name}_LegJoint_{leg_name}", joint_pos, scale)
            created_actors.append(joint_bone["actor"])

            # Upper leg (humerus/femur)
            upper_leg_scale = (scale * 0.1, scale * 0.1, scale * 0.35)
            upper_leg_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] + scale * 0.25
            )
            upper_leg = self._create_composite_cube(f"{name}_UpperLeg_{leg_name}", upper_leg_pos, upper_leg_scale, sand_base)
            created_actors.append(upper_leg["actor"])

            # Muscle definition
            muscle_scale = (scale * 0.09, scale * 0.07, scale * 0.18)
            muscle_pos = (
                position[0] + side_x * scale * 0.27,
                position[1] + side_y * scale * 0.15 - scale * 0.05,
                position[2] + scale * 0.28
            )
            muscle = self._create_composite_cube(f"{name}_LegMuscle_{leg_name}", muscle_pos, muscle_scale, sun_bleached)
            created_actors.append(muscle["actor"])

            # Elbow/Knee joint
            elbow_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] + scale * 0.08
            )
            elbow_bone = self._create_bone_joint(f"{name}_ElbowKnee_{leg_name}", elbow_pos, scale)
            created_actors.append(elbow_bone["actor"])

            # Joint detail
            joint_detail_scale = (scale * 0.08, scale * 0.08, scale * 0.06)
            joint_detail = self._create_composite_cube(f"{name}_Joint_{leg_name}", elbow_pos, joint_detail_scale, sun_bleached)
            created_actors.append(joint_detail["actor"])

            # Lower leg (radius/tibia)
            lower_leg_scale = (scale * 0.08, scale * 0.08, scale * 0.3)
            lower_leg_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] - scale * 0.08
            )
            lower_leg = self._create_composite_cube(f"{name}_LowerLeg_{leg_name}", lower_leg_pos, lower_leg_scale, sand_dark)
            created_actors.append(lower_leg["actor"])

            # Ankle/Wrist joint
            ankle_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.15,
                position[2] - scale * 0.25
            )
            ankle_bone = self._create_bone_joint(f"{name}_AnkleWrist_{leg_name}", ankle_pos, scale)
            created_actors.append(ankle_bone["actor"])

            # Paw/foot
            paw_scale = (scale * 0.12, scale * 0.1, scale * 0.06)
            paw_pos = (
                position[0] + side_x * scale * 0.25,
                position[1] + side_y * scale * 0.18,
                position[2] - scale * 0.32
            )
            paw = self._create_composite_cube(f"{name}_Paw_{leg_name}", paw_pos, paw_scale, sand_base)
            created_actors.append(paw["actor"])

            # Pads on paw
            for p in range(3):
                pad_scale = (scale * 0.025, scale * 0.025, scale * 0.015)
                pad_pos = (
                    position[0] + side_x * scale * 0.25 + (p - 1) * scale * 0.025,
                    position[1] + side_y * scale * 0.23,
                    position[2] - scale * 0.33
                )
                pad = self._create_composite_cube(f"{name}_Pad_{leg_name}_{p}", pad_pos, pad_scale, erosion_brown)
                created_actors.append(pad["actor"])

            # Claws
            for t in range(3):
                claw_scale = (scale * 0.018, scale * 0.025, scale * 0.03)
                claw_pos = (
                    position[0] + side_x * scale * 0.25 + (t - 1) * scale * 0.025,
                    position[1] + side_y * scale * 0.25,
                    position[2] - scale * 0.38
                )
                claw = self._create_composite_cube(f"{name}_Claw_{leg_name}_{t}", claw_pos, claw_scale, sun_bleached)
                created_actors.append(claw["actor"])

        # TAIL - Long balancing tail
        tail_base_scale = (scale * 0.08, scale * 0.15, scale * 0.08)
        tail_base_pos = (position[0], position[1] + scale * 0.4, position[2] + scale * 0.35)
        tail_base = self._create_composite_cube(f"{name}_Tail_Base", tail_base_pos, tail_base_scale, sand_base)
        created_actors.append(tail_base["actor"])

        # Tail vertebrae
        for i in range(5):
            vertebra_scale = (scale * (0.07 - i * 0.01), scale * 0.12, scale * (0.07 - i * 0.01))
            vertebra_pos = (position[0], position[1] + scale * (0.5 + i * 0.12), position[2] + scale * 0.35)
            vertebra = self._create_composite_cube(f"{name}_TailVertebra_{i}", vertebra_pos, vertebra_scale, sand_base)
            created_actors.append(vertebra["actor"])

        # Tail tuft (hair-like, NOT magical)
        tuft_scale = (scale * 0.08, scale * 0.08, scale * 0.08)
        tuft_pos = (position[0], position[1] + scale * 1.1, position[2] + scale * 0.35)
        tuft = self._create_composite_cube(f"{name}_TailTuft", tuft_pos, tuft_scale, sand_dark)
        created_actors.append(tuft["actor"])

        # SURFACE DETAIL - Realistic desert weathering
        # Desert camouflage markings (natural coloration)
        for i in range(6):
            marking_scale = (scale * 0.12, scale * 0.02, scale * 0.15)
            marking_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.25,
                position[1] + scale * 0.36,
                position[2] + scale * 0.2 + (i // 2) * scale * 0.3
            )
            marking = self._create_composite_cube(f"{name}_Camouflage_{i}", marking_pos, marking_scale, sand_dark)
            created_actors.append(marking["actor"])

        # Wind erosion patterns
        for i in range(5):
            erosion_scale = (scale * 0.15, scale * 0.025, scale * 0.1)
            erosion_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.3,
                position[1] + scale * 0.37,
                position[2] + scale * (0.3 + i * scale * 0.15)
            )
            erosion = self._create_composite_cube(f"{name}_Erosion_{i}", erosion_pos, erosion_scale, erosion_brown)
            created_actors.append(erosion["actor"])

        # Sun-bleached patches
        for i in range(8):
            bleach_scale = (scale * 0.1, scale * 0.025, scale * 0.1)
            bleach_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.2,
                position[1] + ((i // 3) % 2) * scale * 0.25,
                position[2] + scale * (0.25 + (i // 6) * scale * 0.2)
            )
            bleach = self._create_composite_cube(f"{name}_Bleached_{i}", bleach_pos, bleach_scale, sun_bleached)
            created_actors.append(bleach["actor"])

        # Sand abrasion marks
        for i in range(4):
            abrasion_scale = (scale * 0.2, scale * 0.015, scale * 0.06)
            abrasion_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.28,
                position[1] + scale * 0.38,
                position[2] + scale * (0.35 + i * scale * 0.18)
            )
            abrasion = self._create_composite_cube(f"{name}_Abrasion_{i}", abrasion_pos, abrasion_scale, crack_shadow)
            created_actors.append(abrasion["actor"])

        # Surface dust accumulation
        for i in range(10):
            dust_scale = (scale * 0.06, scale * 0.02, scale * 0.06)
            dust_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.18,
                position[1] + ((i // 4) % 2) * scale * 0.2,
                position[2] + scale * (0.2 + (i // 8) * scale * 0.25)
            )
            dust = self._create_composite_cube(f"{name}_SurfaceDust_{i}", dust_pos, dust_scale, sand_dust)
            created_actors.append(dust["actor"])

        # Texture variation
        for i in range(12):
            texture_scale = (scale * 0.08, scale * 0.025, scale * 0.08)
            texture_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.15,
                position[1] + ((i // 4) % 3) * scale * 0.12,
                position[2] + scale * (0.15 + (i // 12) * scale * 0.2)
            )
            texture = self._create_composite_cube(f"{name}_Texture_{i}", texture_pos, texture_scale,
                                                sand_base if i % 2 == 0 else sun_bleached)
            created_actors.append(texture["actor"])

        unreal.log(f"🏜️ SAND DEMON created with {len(created_actors)} components (Realistic + Boned)")
        return {
            "message": f"Created {name} (Sand Demon - Realistic + Fully Boned)",
            "name": name,
            "type": "sand demon",
            "actors": created_actors,
            "bones": bones
        }

    def _create_snow_demon_hollywood(self, parsed: dict) -> dict:
        """
        SNOW DEMON - REALISTIC QUADRUPEDAL FELINE ANIMATABLE VERSION
        Large cat-like mountain predator (6-8 feet long)
        Thick white fur coating with visible horns/spikes
        Materials: Real dirty white fur, ice-gray, pale bone (NO FROST MAGIC)
        Full feline quadrupedal bone structure for animation
        """
        name = parsed.get("name") or "SnowDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.8

        unreal.log("❄️ Creating SNOW DEMON (Realistic + Boned)...")

        created_actors = []
        bones = {}

        # REALISTIC FUR COLORS - Natural mountain predator appearance
        fur_white = (0.92, 0.94, 0.95)          # Dirty white fur
        fur_gray = (0.82, 0.85, 0.88)           # Ice-gray patches
        fur_cream = (0.88, 0.86, 0.82)          # Cream underfur
        horn_bone = (0.78, 0.75, 0.70)          # Weathered bone horns
        shadow_gray = (0.65, 0.68, 0.72)        # Deep fur shadows
        frost_burn = (0.75, 0.78, 0.82)         # Frost-burned tips

        # QUADRUPEDAL FELINE SKELETON - Mountain predator structure
        # Spine vertebrae (flexible feline spine)
        for i in range(10):
            spine_pos = (position[0], position[1] - scale * 0.15 + i * scale * 0.11, position[2] + scale * 0.75)
            spine_bone = self._create_bone_joint(f"{name}_Spine_{i}", spine_pos, scale)
            created_actors.append(spine_bone["actor"])

        # Rib cage (barrel chest for feline)
        for i in range(7):
            rib_angle = (math.pi * i) / 7
            rib_pos = (
                position[0] + scale * 0.26 * math.cos(rib_angle),
                position[1] + scale * 0.5 + scale * 0.26 * math.sin(rib_angle),
                position[2] + scale * 0.8
            )
            rib_bone = self._create_bone_joint(f"{name}_Rib_{i}", rib_pos, scale)
            created_actors.append(rib_bone["actor"])

        # FELINE BODY - Cat-like massing
        torso_scale = (scale * 0.6, scale * 0.45, scale * 1.2)
        torso_pos = (position[0], position[1], position[2] + scale * 0.6)
        torso = self._create_composite_cube(f"{name}_Torso", torso_pos, torso_scale, fur_white)
        created_actors.append(torso["actor"])

        # Thick fur layers - natural fluffy appearance
        for i in range(10):
            fur_patch_scale = (scale * 0.55, scale * 0.08, scale * 0.25)
            fur_patch_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.05,
                position[1] + ((i % 2) * 2 - 1) * scale * 0.25,
                position[2] + scale * 0.3 + (i // 2) * scale * 0.35
            )
            fur_patch = self._create_composite_cube(f"{name}_FurPatch_{i}", fur_patch_pos, fur_patch_scale, fur_gray)
            created_actors.append(fur_patch["actor"])

        # Chest fur ruff
        ruff_scale = (scale * 0.35, scale * 0.12, scale * 0.25)
        ruff_pos = (position[0], position[1] - scale * 0.25, position[2] + scale * 0.75)
        ruff = self._create_composite_cube(f"{name}_ChestRuff", ruff_pos, ruff_scale, fur_cream)
        created_actors.append(ruff["actor"])

        # Spine spikes through back fur (natural bone, NOT magical)
        for i in range(6):
            spike_scale = (scale * 0.04, scale * 0.04, scale * 0.12)
            spike_pos = (
                position[0],
                position[1] - scale * 0.2 + i * scale * 0.15,
                position[2] + scale * 1.15
            )
            spike = self._create_composite_cube(f"{name}_SpineSpike_{i}", spike_pos, spike_scale, horn_bone)
            created_actors.append(spike["actor"])

        # NECK - Thick feline neck
        for i in range(4):
            neck_scale = (scale * 0.2, scale * 0.2, scale * 0.1)
            neck_pos = (position[0], position[1] - scale * (0.2 + i * 0.08), position[2] + scale * 0.82)
            neck = self._create_composite_cube(f"{name}_NeckVertebra_{i}", neck_pos, neck_scale, fur_white)
            created_actors.append(neck["actor"])

        neck_main_scale = (scale * 0.25, scale * 0.25, scale * 0.2)
        neck_main_pos = (position[0], position[1] - scale * 0.2, position[2] + scale * 0.78)
        neck_main = self._create_composite_cube(f"{name}_Neck_Main", neck_main_pos, neck_main_scale, fur_white)
        created_actors.append(neck_main["actor"])

        # FELINE HEAD - Cat-like proportions
        skull_scale = (scale * 0.28, scale * 0.35, scale * 0.25)
        skull_pos = (position[0], position[1] - scale * 0.15, position[2] + scale * 0.85)
        skull = self._create_composite_cube(f"{name}_Skull", skull_pos, skull_scale, fur_white)
        created_actors.append(skull["actor"])

        # Muzzle
        muzzle_scale = (scale * 0.15, scale * 0.2, scale * 0.12)
        muzzle_pos = (position[0], position[1] - scale * 0.4, position[2] + scale * 0.8)
        muzzle = self._create_composite_cube(f"{name}_Muzzle", muzzle_pos, muzzle_scale, fur_white)
        created_actors.append(muzzle["actor"])

        # REALISTIC EYES - Feline hunter eyes (NOT magical cold blue)
        for side in [-1, 1]:
            # Eye socket (deep set)
            socket_scale = (scale * 0.08, scale * 0.06, scale * 0.08)
            socket_pos = (position[0] + side * scale * 0.08, position[1] - scale * 0.25, position[2] + scale * 0.87)
            socket = self._create_composite_cube(f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, shadow_gray)
            created_actors.append(socket["actor"])

            # Eye (natural amber-green)
            eye_scale = (scale * 0.055, scale * 0.055, scale * 0.05)
            eye_pos = (position[0] + side * scale * 0.08, position[1] - scale * 0.28, position[2] + scale * 0.87)
            eye = self._create_composite_cube(f"{name}_Eye_{'L' if side < 0 else 'R'}", eye_pos, eye_scale, (0.65, 0.58, 0.42))
            created_actors.append(eye["actor"])

            # Eyelid
            eyelid_scale = (scale * 0.06, scale * 0.03, scale * 0.055)
            eyelid_pos = (position[0] + side * scale * 0.08, position[1] - scale * 0.22, position[2] + scale * 0.9)
            eyelid = self._create_composite_cube(f"{name}_Eyelid_{'L' if side < 0 else 'R'}", eyelid_pos, eyelid_scale, fur_white)
            created_actors.append(eyelid["actor"])

        # Nose
        nose_scale = (scale * 0.08, scale * 0.08, scale * 0.05)
        nose_pos = (position[0], position[1] - scale * 0.52, position[2] + scale * 0.78)
        nose = self._create_composite_cube(f"{name}_Nose", nose_pos, nose_scale, shadow_gray)
        created_actors.append(nose["actor"])

        # Nostrils
        for side in [-1, 1]:
            nostril_scale = (scale * 0.02, scale * 0.035, scale * 0.02)
            nostril_pos = (position[0] + side * scale * 0.025, position[1] - scale * 0.55, position[2] + scale * 0.77)
            nostril = self._create_composite_cube(f"{name}_Nostril_{'L' if side < 0 else 'R'}", nostril_pos, nostril_scale, (0.35, 0.32, 0.30))
            created_actors.append(nostril["actor"])

        # Fangs
        for i in range(4):
            fang_scale = (scale * 0.025, scale * 0.05, scale * 0.025)
            fang_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.05,
                position[1] - scale * 0.42,
                position[2] + scale * (0.78 + (i // 2) * scale * 0.03)
            )
            fang = self._create_composite_cube(f"{name}_Fang_{i}", fang_pos, fang_scale, fur_cream)
            created_actors.append(fang["actor"])

        # Whiskers (visible as lines)
        for side in [-1, 1]:
            for w in range(4):
                whisker_scale = (scale * 0.12, scale * 0.008, scale * 0.008)
                whisker_pos = (
                    position[0] + side * scale * (0.15 + w * 0.02),
                    position[1] - scale * 0.45,
                    position[2] + scale * (0.78 + w * 0.015)
                )
                whisker = self._create_composite_cube(f"{name}_Whisker_{'L' if side < 0 else 'R'}_{w}", whisker_pos, whisker_scale, fur_gray)
                created_actors.append(whisker["actor"])

        # Ears - Tufted cat ears
        for side in [-1, 1]:
            ear_scale = (scale * 0.1, scale * 0.12, scale * 0.15)
            ear_pos = (skull_pos[0] + side * scale * 0.15, skull_pos[1] - scale * 0.2, skull_pos[2] + scale * 0.15)
            ear = self._create_composite_cube(f"{name}_Ear_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, fur_white)
            created_actors.append(ear["actor"])

            # Ear tufts (fur, NOT magical)
            tuft_scale = (scale * 0.04, scale * 0.04, scale * 0.08)
            tuft_pos = (ear_pos[0], ear_pos[1], ear_pos[2] + scale * 0.1)
            tuft = self._create_composite_cube(f"{name}_EarTuft_{'L' if side < 0 else 'R'}", tuft_pos, tuft_scale, fur_gray)
            created_actors.append(tuft["actor"])

        # VISIBLE HORNS/SPIKES through fur (natural bone)
        # Crown horns
        for i in range(4):
            horn_scale = (scale * 0.05, scale * 0.05, scale * 0.18)
            angle = (math.pi * (i + 1)) / 5
            horn_pos = (
                skull_pos[0] + scale * 0.18 * math.cos(angle),
                skull_pos[1] + scale * 0.18 * math.sin(angle),
                skull_pos[2] + scale * 0.18
            )
            horn = self._create_composite_cube(f"{name}_Horn_{i}", horn_pos, horn_scale, horn_bone)
            created_actors.append(horn["actor"])

        # FELINE LEGS - Powerful quadrupedal
        leg_positions = [
            (-1, -1, "FrontLeft"),   # Front left
            (1, -1, "FrontRight"),   # Front right
            (-1, 1, "BackLeft"),     # Back left
            (1, 1, "BackRight")      # Back right
        ]

        for side_x, side_y, leg_name in leg_positions:
            # Shoulder/Hip joint
            joint_pos = (
                position[0] + side_x * scale * 0.28,
                position[1] + side_y * scale * 0.18,
                position[2] + scale * 0.55
            )
            joint_bone = self._create_bone_joint(f"{name}_LegJoint_{leg_name}", joint_pos, scale)
            created_actors.append(joint_bone["actor"])

            # Upper leg - muscular thigh
            upper_scale = (scale * 0.15, scale * 0.12, scale * 0.35)
            upper_pos = (
                position[0] + side_x * scale * 0.28,
                position[1] + side_y * scale * 0.18,
                position[2] + scale * 0.45
            )
            upper = self._create_composite_cube(f"{name}_UpperLeg_{leg_name}", upper_pos, upper_scale, fur_white)
            created_actors.append(upper["actor"])

            # Muscle definition
            muscle_scale = (scale * 0.14, scale * 0.08, scale * 0.2)
            muscle_pos = (
                position[0] + side_x * scale * 0.3,
                position[1] + side_y * scale * 0.18 - scale * 0.05,
                position[2] + scale * 0.48
            )
            muscle = self._create_composite_cube(f"{name}_LegMuscle_{leg_name}", muscle_pos, muscle_scale, fur_gray)
            created_actors.append(muscle["actor"])

            # Elbow/Knee joint
            elbow_pos = (
                position[0] + side_x * scale * 0.28,
                position[1] + side_y * scale * 0.18,
                position[2] + scale * 0.2
            )
            elbow_bone = self._create_bone_joint(f"{name}_ElbowKnee_{leg_name}", elbow_pos, scale)
            created_actors.append(elbow_bone["actor"])

            # Lower leg - sleek
            lower_scale = (scale * 0.1, scale * 0.1, scale * 0.32)
            lower_pos = (
                position[0] + side_x * scale * 0.28,
                position[1] + side_y * scale * 0.18,
                position[2] + scale * 0.15
            )
            lower = self._create_composite_cube(f"{name}_LowerLeg_{leg_name}", lower_pos, lower_scale, fur_gray)
            created_actors.append(lower["actor"])

            # Ankle/Wrist joint
            ankle_pos = (
                position[0] + side_x * scale * 0.28,
                position[1] + side_y * scale * 0.18,
                position[2] + scale * 0.02
            )
            ankle_bone = self._create_bone_joint(f"{name}_AnkleWrist_{leg_name}", ankle_pos, scale)
            created_actors.append(ankle_bone["actor"])

            # Paw - Large cat paw
            paw_scale = (scale * 0.14, scale * 0.1, scale * 0.06)
            paw_pos = (
                position[0] + side_x * scale * 0.28,
                position[1] + side_y * scale * 0.2,
                position[2]
            )
            paw = self._create_composite_cube(f"{name}_Paw_{leg_name}", paw_pos, paw_scale, fur_white)
            created_actors.append(paw["actor"])

            # Paw pads
            for p in range(4):
                pad_scale = (scale * 0.03, scale * 0.03, scale * 0.015)
                pad_pos = (
                    position[0] + side_x * scale * 0.28 + (p - 1.5) * scale * 0.025,
                    position[1] + side_y * scale * 0.25,
                    position[2] - scale * 0.01
                )
                pad = self._create_composite_cube(f"{name}_Pad_{leg_name}_{p}", pad_pos, pad_scale, shadow_gray)
                created_actors.append(pad["actor"])

            # Claws (retractable, visible)
            for c in range(4):
                claw_scale = (scale * 0.015, scale * 0.025, scale * 0.035)
                claw_pos = (
                    position[0] + side_x * scale * 0.28 + (c - 1.5) * scale * 0.025,
                    position[1] + side_y * scale * 0.27,
                    position[2] - scale * 0.05
                )
                claw = self._create_composite_cube(f"{name}_Claw_{leg_name}_{c}", claw_pos, claw_scale, fur_cream)
                created_actors.append(claw["actor"])

        # Tail - Feline balancing tail
        tail_base_scale = (scale * 0.1, scale * 0.15, scale * 0.1)
        tail_base_pos = (position[0], position[1] + scale * 0.5, position[2] + scale * 0.55)
        tail_base = self._create_composite_cube(f"{name}_Tail_Base", tail_base_pos, tail_base_scale, fur_white)
        created_actors.append(tail_base["actor"])

        # Tail vertebrae
        for i in range(6):
            vertebra_scale = (scale * (0.08 - i * 0.01), scale * 0.12, scale * (0.08 - i * 0.01))
            vertebra_pos = (position[0], position[1] + scale * (0.6 + i * 0.12), position[2] + scale * 0.55)
            vertebra = self._create_composite_cube(f"{name}_TailVertebra_{i}", vertebra_pos, vertebra_scale, fur_white)
            created_actors.append(vertebra["actor"])

        # Tail main (furry tail)
        tail_scale = (scale * 0.08, scale * 0.5, scale * 0.08)
        tail_pos = (position[0], position[1] + scale * 0.5, position[2] + scale * 0.55)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, fur_white)
        created_actors.append(tail["actor"])

        # Tail tuft
        tail_tuft_scale = (scale * 0.1, scale * 0.1, scale * 0.1)
        tail_tuft_pos = (position[0], position[1] + scale * 0.8, position[2] + scale * 0.55)
        tail_tuft = self._create_composite_cube(f"{name}_TailTuft", tail_tuft_pos, tail_tuft_scale, fur_gray)
        created_actors.append(tail_tuft["actor"])

        # SURFACE DETAIL - Realistic mountain weathering
        # Frost-burned fur tips
        for i in range(8):
            burn_scale = (scale * 0.12, scale * 0.025, scale * 0.12)
            burn_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.2,
                position[1] + ((i // 3) % 2) * scale * 0.3,
                position[2] + scale * (0.3 + (i // 6) * scale * 0.3)
            )
            burn = self._create_composite_cube(f"{name}_FrostBurn_{i}", burn_pos, burn_scale, frost_burn)
            created_actors.append(burn["actor"])

        # Ice crystal accumulation (NOT magical frost)
        for i in range(6):
            ice_scale = (scale * 0.06, scale * 0.02, scale * 0.06)
            ice_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.3,
                position[1] + scale * 0.48,
                position[2] + scale * (0.4 + i * scale * 0.15)
            )
            ice = self._create_composite_cube(f"{name}_IceCrystal_{i}", ice_pos, ice_scale, shadow_gray)
            created_actors.append(ice["actor"])

        # Snow accumulation in fur
        for i in range(10):
            snow_scale = (scale * 0.08, scale * 0.025, scale * 0.08)
            snow_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.15,
                position[1] + ((i // 4) % 2) * scale * 0.25,
                position[2] + scale * (0.25 + (i // 8) * scale * 0.25)
            )
            snow = self._create_composite_cube(f"{name}_SnowAccum_{i}", snow_pos, snow_scale, fur_cream)
            created_actors.append(snow["actor"])

        # Fur texture variation
        for i in range(12):
            texture_scale = (scale * 0.1, scale * 0.025, scale * 0.1)
            texture_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.12,
                position[1] + ((i // 4) % 3) * scale * 0.15,
                position[2] + scale * (0.2 + (i // 12) * scale * 0.25)
            )
            texture = self._create_composite_cube(f"{name}_FurTexture_{i}", texture_pos, texture_scale,
                                                fur_white if i % 2 == 0 else fur_gray)
            created_actors.append(texture["actor"])

        unreal.log(f"❄️ SNOW DEMON created with {len(created_actors)} components (Realistic + Boned)")
        return {
            "message": f"Created {name} (Snow Demon - Realistic + Fully Boned)",
            "name": name,
            "type": "snow demon",
            "actors": created_actors,
            "bones": bones
        }

    def _create_field_demon_hollywood(self, parsed: dict) -> dict:
        """
        FIELD DEMON - REALISTIC QUADRUPEDAL FELINE ANIMATABLE VERSION
        Feline plains runner (5-7 feet long)
        Built for speed across open terrain
        Materials: Real tawny fur, grass tones, earth brown (NO MAGICAL EFFECTS)
        Full feline quadrupedal bone structure for animation
        """
        name = parsed.get("name") or "FieldDemon"
        props = parsed["properties"]
        position = props["position"]
        scale = props["size"] or 1.5

        unreal.log("🌾 Creating FIELD DEMON (Realistic + Boned)...")

        created_actors = []
        bones = {}

        # REALISTIC PLAINS COLORS - Natural savanna predator appearance
        tawny_gold = (0.75, 0.68, 0.45)          # Tawny gold base
        grass_green = (0.58, 0.62, 0.35)         # Grass undertones
        earth_brown = (0.52, 0.45, 0.32)         # Earth brown
        cream_under = (0.85, 0.80, 0.68)         # Cream underfur
        shadow_dark = (0.42, 0.38, 0.28)         # Deep shadows
        dust_tan = (0.68, 0.62, 0.52)            # Dust coating

        # QUADRUPEDAL FELINE SKELETON - Sprinting predator structure
        # Spine vertebrae (flexible for running)
        for i in range(9):
            spine_pos = (position[0], position[1] - scale * 0.12 + i * scale * 0.12, position[2] + scale * 0.7)
            spine_bone = self._create_bone_joint(f"{name}_Spine_{i}", spine_pos, scale)
            created_actors.append(spine_bone["actor"])

        # Rib cage (lean but strong)
        for i in range(6):
            rib_angle = (math.pi * i) / 6
            rib_pos = (
                position[0] + scale * 0.24 * math.cos(rib_angle),
                position[1] + scale * 0.45 + scale * 0.24 * math.sin(rib_angle),
                position[2] + scale * 0.75
            )
            rib_bone = self._create_bone_joint(f"{name}_Rib_{i}", rib_pos, scale)
            created_actors.append(rib_bone["actor"])

        # FELINE BODY - Built for speed
        torso_scale = (scale * 0.55, scale * 0.4, scale * 1.1)
        torso_pos = (position[0], position[1], position[2] + scale * 0.55)
        torso = self._create_composite_cube(f"{name}_Torso", torso_pos, torso_scale, tawny_gold)
        created_actors.append(torso["actor"])

        # Grass stripe camouflage (natural coloration)
        for i in range(8):
            stripe_scale = (scale * 0.5, scale * 0.04, scale * 0.2)
            stripe_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.02,
                position[1] + ((i % 3) - 1) * scale * 0.2,
                position[2] + scale * 0.3 + (i // 3) * scale * 0.35
            )
            stripe = self._create_composite_cube(f"{name}_GrassStripe_{i}", stripe_pos, stripe_scale, grass_green)
            created_actors.append(stripe["actor"])

        # Chest definition (lean runner)
        chest_scale = (scale * 0.4, scale * 0.08, scale * 0.3)
        chest_pos = (position[0], position[1] - scale * 0.25, position[2] + scale * 0.7)
        chest = self._create_composite_cube(f"{name}_Chest", chest_pos, chest_scale, cream_under)
        created_actors.append(chest["actor"])

        # NECK - Lean runner neck
        for i in range(3):
            neck_scale = (scale * 0.16, scale * 0.16, scale * 0.08)
            neck_pos = (position[0], position[1] - scale * (0.2 + i * 0.07), position[2] + scale * 0.68)
            neck = self._create_composite_cube(f"{name}_NeckVertebra_{i}", neck_pos, neck_scale, tawny_gold)
            created_actors.append(neck["actor"])

        neck_main_scale = (scale * 0.2, scale * 0.2, scale * 0.18)
        neck_main_pos = (position[0], position[1] - scale * 0.2, position[2] + scale * 0.65)
        neck_main = self._create_composite_cube(f"{name}_Neck_Main", neck_main_pos, neck_main_scale, tawny_gold)
        created_actors.append(neck_main["actor"])

        # FELINE HEAD
        skull_scale = (scale * 0.26, scale * 0.32, scale * 0.22)
        skull_pos = (position[0], position[1] - scale * 0.12, position[2] + scale * 0.75)
        skull = self._create_composite_cube(f"{name}_Skull", skull_pos, skull_scale, tawny_gold)
        created_actors.append(skull["actor"])

        # Muzzle
        muzzle_scale = (scale * 0.14, scale * 0.18, scale * 0.1)
        muzzle_pos = (position[0], position[1] - scale * 0.35, position[2] + scale * 0.7)
        muzzle = self._create_composite_cube(f"{name}_Muzzle", muzzle_pos, muzzle_scale, tawny_gold)
        created_actors.append(muzzle["actor"])

        # REALISTIC EYES - Feline hunter eyes (NOT glowing gold)
        for side in [-1, 1]:
            # Eye socket
            socket_scale = (scale * 0.07, scale * 0.055, scale * 0.07)
            socket_pos = (position[0] + side * scale * 0.07, position[1] - scale * 0.22, position[2] + scale * 0.77)
            socket = self._create_composite_cube(f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, shadow_dark)
            created_actors.append(socket["actor"])

            # Eye (natural amber-brown)
            eye_scale = (scale * 0.05, scale * 0.05, scale * 0.045)
            eye_pos = (position[0] + side * scale * 0.07, position[1] - scale * 0.25, position[2] + scale * 0.77)
            eye = self._create_composite_cube(f"{name}_Eye_{'L' if side < 0 else 'R'}", eye_pos, eye_scale, (0.72, 0.58, 0.35))
            created_actors.append(eye["actor"])

            # Eyelid
            eyelid_scale = (scale * 0.055, scale * 0.025, scale * 0.05)
            eyelid_pos = (position[0] + side * scale * 0.07, position[1] - scale * 0.19, position[2] + scale * 0.8)
            eyelid = self._create_composite_cube(f"{name}_Eyelid_{'L' if side < 0 else 'R'}", eyelid_pos, eyelid_scale, tawny_gold)
            created_actors.append(eyelid["actor"])

        # Nose
        nose_scale = (scale * 0.07, scale * 0.07, scale * 0.045)
        nose_pos = (position[0], position[1] - scale * 0.48, position[2] + scale * 0.7)
        nose = self._create_composite_cube(f"{name}_Nose", nose_pos, nose_scale, shadow_dark)
        created_actors.append(nose["actor"])

        # Nostrils
        for side in [-1, 1]:
            nostril_scale = (scale * 0.018, scale * 0.03, scale * 0.018)
            nostril_pos = (position[0] + side * scale * 0.02, position[1] - scale * 0.5, position[2] + scale * 0.69)
            nostril = self._create_composite_cube(f"{name}_Nostril_{'L' if side < 0 else 'R'}", nostril_pos, nostril_scale, (0.32, 0.28, 0.25))
            created_actors.append(nostril["actor"])

        # Fangs
        for i in range(4):
            fang_scale = (scale * 0.022, scale * 0.045, scale * 0.022)
            fang_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.045,
                position[1] - scale * 0.38,
                position[2] + scale * (0.7 + (i // 2) * scale * 0.025)
            )
            fang = self._create_composite_cube(f"{name}_Fang_{i}", fang_pos, fang_scale, cream_under)
            created_actors.append(fang["actor"])

        # Ears - Alert cat ears
        for side in [-1, 1]:
            ear_scale = (scale * 0.09, scale * 0.1, scale * 0.14)
            ear_pos = (skull_pos[0] + side * scale * 0.14, skull_pos[1] - scale * 0.18, skull_pos[2] + scale * 0.12)
            ear = self._create_composite_cube(f"{name}_Ear_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, tawny_gold)
            created_actors.append(ear["actor"])

            # Inner ear
            inner_scale = (scale * 0.05, scale * 0.05, scale * 0.08)
            inner_pos = (ear_pos[0], ear_pos[1], ear_pos[2] + scale * 0.02)
            inner = self._create_composite_cube(f"{name}_InnerEar_{'L' if side < 0 else 'R'}", inner_pos, inner_scale, cream_under)
            created_actors.append(inner["actor"])

        # FELINE LEGS - Built for speed
        leg_positions = [
            (-1, -1, "FrontLeft"),   # Front left
            (1, -1, "FrontRight"),   # Front right
            (-1, 1, "BackLeft"),     # Back left
            (1, 1, "BackRight")      # Back right
        ]

        for side_x, side_y, leg_name in leg_positions:
            # Shoulder/Hip joint
            joint_pos = (
                position[0] + side_x * scale * 0.26,
                position[1] + side_y * scale * 0.16,
                position[2] + scale * 0.5
            )
            joint_bone = self._create_bone_joint(f"{name}_LegJoint_{leg_name}", joint_pos, scale)
            created_actors.append(joint_bone["actor"])

            # Upper leg - lean muscular
            upper_scale = (scale * 0.13, scale * 0.1, scale * 0.32)
            upper_pos = (
                position[0] + side_x * scale * 0.26,
                position[1] + side_y * scale * 0.16,
                position[2] + scale * 0.4
            )
            upper = self._create_composite_cube(f"{name}_UpperLeg_{leg_name}", upper_pos, upper_scale, tawny_gold)
            created_actors.append(upper["actor"])

            # Muscle definition (streamlined for speed)
            muscle_scale = (scale * 0.12, scale * 0.07, scale * 0.18)
            muscle_pos = (
                position[0] + side_x * scale * 0.28,
                position[1] + side_y * scale * 0.16 - scale * 0.04,
                position[2] + scale * 0.42
            )
            muscle = self._create_composite_cube(f"{name}_LegMuscle_{leg_name}", muscle_pos, muscle_scale, earth_brown)
            created_actors.append(muscle["actor"])

            # Elbow/Knee joint
            elbow_pos = (
                position[0] + side_x * scale * 0.26,
                position[1] + side_y * scale * 0.16,
                position[2] + scale * 0.18
            )
            elbow_bone = self._create_bone_joint(f"{name}_ElbowKnee_{leg_name}", elbow_pos, scale)
            created_actors.append(elbow_bone["actor"])

            # Lower leg - sleek
            lower_scale = (scale * 0.09, scale * 0.09, scale * 0.28)
            lower_pos = (
                position[0] + side_x * scale * 0.26,
                position[1] + side_y * scale * 0.16,
                position[2] + scale * 0.12
            )
            lower = self._create_composite_cube(f"{name}_LowerLeg_{leg_name}", lower_pos, lower_scale, grass_green)
            created_actors.append(lower["actor"])

            # Ankle/Wrist joint
            ankle_pos = (
                position[0] + side_x * scale * 0.26,
                position[1] + side_y * scale * 0.16,
                position[2]
            )
            ankle_bone = self._create_bone_joint(f"{name}_AnkleWrist_{leg_name}", ankle_pos, scale)
            created_actors.append(ankle_bone["actor"])

            # Paw - runner paw
            paw_scale = (scale * 0.12, scale * 0.08, scale * 0.05)
            paw_pos = (
                position[0] + side_x * scale * 0.26,
                position[1] + side_y * scale * 0.18,
                position[2] - scale * 0.03
            )
            paw = self._create_composite_cube(f"{name}_Paw_{leg_name}", paw_pos, paw_scale, tawny_gold)
            created_actors.append(paw["actor"])

            # Paw pads
            for p in range(3):
                pad_scale = (scale * 0.025, scale * 0.025, scale * 0.012)
                pad_pos = (
                    position[0] + side_x * scale * 0.26 + (p - 1) * scale * 0.022,
                    position[1] + side_y * scale * 0.22,
                    position[2] - scale * 0.035
                )
                pad = self._create_composite_cube(f"{name}_Pad_{leg_name}_{p}", pad_pos, pad_scale, shadow_dark)
                created_actors.append(pad["actor"])

            # Claws
            for c in range(3):
                claw_scale = (scale * 0.012, scale * 0.022, scale * 0.03)
                claw_pos = (
                    position[0] + side_x * scale * 0.26 + (c - 1) * scale * 0.022,
                    position[1] + side_y * scale * 0.24,
                    position[2] - scale * 0.07
                )
                claw = self._create_composite_cube(f"{name}_Claw_{leg_name}_{c}", claw_pos, claw_scale, cream_under)
                created_actors.append(claw["actor"])

        # Tail - Balancing tail
        tail_base_scale = (scale * 0.08, scale * 0.12, scale * 0.08)
        tail_base_pos = (position[0], position[1] + scale * 0.45, position[2] + scale * 0.5)
        tail_base = self._create_composite_cube(f"{name}_Tail_Base", tail_base_pos, tail_base_scale, tawny_gold)
        created_actors.append(tail_base["actor"])

        # Tail vertebrae
        for i in range(5):
            vertebra_scale = (scale * (0.07 - i * 0.01), scale * 0.1, scale * (0.07 - i * 0.01))
            vertebra_pos = (position[0], position[1] + scale * (0.55 + i * 0.1), position[2] + scale * 0.5)
            vertebra = self._create_composite_cube(f"{name}_TailVertebra_{i}", vertebra_pos, vertebra_scale, tawny_gold)
            created_actors.append(vertebra["actor"])

        # Tail main
        tail_scale = (scale * 0.07, scale * 0.45, scale * 0.07)
        tail_pos = (position[0], position[1] + scale * 0.45, position[2] + scale * 0.5)
        tail = self._create_composite_cube(f"{name}_Tail", tail_pos, tail_scale, tawny_gold)
        created_actors.append(tail["actor"])

        # Tail tip (dark)
        tip_scale = (scale * 0.06, scale * 0.08, scale * 0.06)
        tip_pos = (position[0], position[1] + scale * 0.9, position[2] + scale * 0.5)
        tip = self._create_composite_cube(f"{name}_Tail_Tip", tip_pos, tip_scale, earth_brown)
        created_actors.append(tip["actor"])

        # SURFACE DETAIL - Realistic savanna weathering
        # Dust accumulation
        for i in range(8):
            dust_scale = (scale * 0.1, scale * 0.025, scale * 0.1)
            dust_pos = (
                position[0] + ((i % 3) - 1) * scale * 0.15,
                position[1] + ((i // 3) % 2) * scale * 0.25,
                position[2] + scale * (0.25 + (i // 6) * scale * 0.2)
            )
            dust = self._create_composite_cube(f"{name}_Dust_{i}", dust_pos, dust_scale, dust_tan)
            created_actors.append(dust["actor"])

        # Grass stain marks
        for i in range(5):
            stain_scale = (scale * 0.12, scale * 0.02, scale * 0.08)
            stain_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.25,
                position[1] + scale * 0.43,
                position[2] + scale * (0.3 + i * scale * 0.15)
            )
            stain = self._create_composite_cube(f"{name}_GrassStain_{i}", stain_pos, stain_scale, grass_green)
            created_actors.append(stain["actor"])

        # Sun-bleached patches
        for i in range(6):
            bleach_scale = (scale * 0.1, scale * 0.025, scale * 0.1)
            bleach_pos = (
                position[0] + ((i % 2) - 0.5) * scale * 0.2,
                position[1] + ((i // 3) % 2) * scale * 0.22,
                position[2] + scale * (0.22 + i * scale * 0.12)
            )
            bleach = self._create_composite_cube(f"{name}_Bleached_{i}", bleach_pos, bleach_scale, cream_under)
            created_actors.append(bleach["actor"])

        # Fur texture variation
        for i in range(10):
            texture_scale = (scale * 0.08, scale * 0.025, scale * 0.08)
            texture_pos = (
                position[0] + ((i % 4) - 1.5) * scale * 0.12,
                position[1] + ((i // 4) % 2) * scale * 0.18,
                position[2] + scale * (0.18 + (i // 8) * scale * 0.2)
            )
            texture = self._create_composite_cube(f"{name}_FurTexture_{i}", texture_pos, texture_scale,
                                                tawny_gold if i % 2 == 0 else earth_brown)
            created_actors.append(texture["actor"])

        unreal.log(f"🌾 FIELD DEMON created with {len(created_actors)} components (Realistic + Boned)")
        return {
            "message": f"Created {name} (Field Demon - Realistic + Fully Boned)",
            "name": name,
            "type": "field demon",
            "actors": created_actors,
            "bones": bones
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

    def _create_bone_joint(self, name: str, position: Tuple[float, float, float],
                           scale: float) -> dict:
        """
        Create a bone joint for animation rigging
        This creates a visual marker and returns bone reference for animation system
        """
        try:
            loc = unreal.Vector(position[0], position[1], position[2])

            # Create a small cube as bone/joint visual
            bone_scale = (scale * 0.08, scale * 0.08, scale * 0.08)
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
            actor.set_actor_label(name)
            actor.set_actor_scale3d(unreal.Vector(bone_scale[0], bone_scale[1], bone_scale[2]))

            # Create bone material (subtle gray for joints)
            bone_color = (0.3, 0.3, 0.3)
            mat_name = f"BoneJoint_Mat"
            mat_path = self._create_simple_material_for_name(mat_name, bone_color)

            material = unreal.load_asset(mat_path, unreal.Material)
            if material:
                mesh_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
                if mesh_comp:
                    mesh_comp.set_material(0, material)

            # Store bone position for rigging
            bone_data = {
                "name": name,
                "actor": actor,
                "position": position,
                "scale": scale,
                "type": "joint",
                "children": []
            }

            return bone_data

        except Exception as e:
            unreal.log_error(f"Bone joint creation failed: {e}")
            return {"error": str(e)}

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
