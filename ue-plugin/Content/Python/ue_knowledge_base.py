"""
UE AI Plugin - Complete Knowledge Base
Comprehensive Unreal Engine knowledge for AI
"""

UE_KNOWLEDGE_BASE = {
    # Actors and Classes
    "actors": {
        "static_mesh_actor": {
            "description": "Actor that renders a static mesh",
            "properties": ["static_mesh", "materials", "collision", "render_custom_depth"],
            "creation": "unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, location)",
            "common_uses": ["props", "buildings", "environment objects"]
        },
        "blueprint_actor": {
            "description": "Actor created from Blueprint with custom logic",
            "properties": ["variables", "components", "graphs", "functions"],
            "creation": "Can only be created from existing Blueprint assets",
            "common_uses": ["interactive objects", "gameplay elements", "custom behaviors"]
        },
        "pawn": {
            "description": "Actor that can be controlled by a player or AI",
            "properties": ["controller", "input_component", "camera_manager"],
            "creation": "unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Pawn, location)",
            "common_uses": ["player characters", "AI characters"]
        },
        "character": {
            "description": "Pawn with character movement and capsule collision",
            "properties": ["character_movement", "capsule_component", "mesh"],
            "creation": "unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Character, location)",
            "common_uses": ["humanoid characters", "players"]
        },
        "camera_actor": {
            "description": "Camera that renders the scene from its perspective",
            "properties": ["field_of_view", "aspect_ratio", "post_process"],
            "creation": "unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CameraActor, location)",
            "common_uses": ["cinematic cameras", "security cameras", "player views"]
        },
        "point_light": {
            "description": "Omnidirectional light source that illuminates in all directions",
            "properties": ["intensity", "light_color", "attenuation_radius", "cast_shadows"],
            "creation": "unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLightActor, location)",
            "common_uses": ["lamps", "light bulbs", "ambient lighting"]
        },
        "spot_light": {
            "description": "Light that emits in a cone direction",
            "properties": ["inner_cone_angle", "outer_cone_angle", "intensity", "light_color"],
            "creation": "unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SpotLightActor, location)",
            "common_uses": ["flashlights", "spotlights", "headlights"]
        },
        "directional_light": {
            "description": "Simulates sunlight with parallel light rays",
            "properties": ["intensity", "light_color", "atmosphere_sun_light"],
            "creation": "unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLightActor, location)",
            "common_uses": ["sunlight", "moonlight", "outdoor scenes"]
        },
        "sky_light": {
            "description": "Captures the distant scene and applies it as lighting",
            "properties": ["intensity", "cubemap", "source_type"],
            "creation": "unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyLightActor, location)",
            "common_uses": ["outdoor ambient lighting", "sky simulation"]
        },
        "atmospheric_fog": {
            "description": "Adds atmospheric perspective and fog",
            "properties": ["fog_density", "fog_height", "inscattering_light_density"],
            "creation": "unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.AtmosphericFog, location)",
            "common_uses": ["distance fog", "atmosphere", "depth"]
        },
        "particle_system": {
            "description": "Emits particles for effects",
            "properties": ["template", "emitter", "max_count"],
            "creation": "Need to spawn actor and set template property",
            "common_uses": ["fire", "smoke", "explosions", "magic effects"]
        },
        "actor_spawn": {
            "description": "Spawn any actor by class path",
            "method": "Load asset class first, then spawn_actor_from_class"
        }
    },

    # Components
    "components": {
        "static_mesh_component": {
            "description": "Renders a static mesh",
            "properties": ["static_mesh", "materials", "cast_shadow", "override_materials"],
            "add_to": "actor.add_component_by_class(unreal.StaticMeshComponent)"
        },
        "sphere_component": {
            "description": "Simple sphere collision/shape",
            "properties": ["sphere_radius", "shape_color"],
            "add_to": "actor.add_component_by_class(unreal.SphereComponent)"
        },
        "box_component": {
            "description": "Box collision/shape",
            "properties": ["box_extent", "shape_color"],
            "add_to": "actor.add_component_by_class(unreal.BoxComponent)"
        },
        "capsule_component": {
            "description": "Capsule collision for characters",
            "properties": ["capsule_radius", "capsule_half_height"],
            "add_to": "actor.add_component_by_class(unreal.CapsuleComponent)"
        },
        "camera_component": {
            "description": "Camera for rendering",
            "properties": ["field_of_view", "aspect_ratio", "post_process"],
            "add_to": "actor.add_component_by_class(unreal.CameraComponent)"
        },
        "point_light_component": {
            "description": "Point light attached to actor",
            "properties": ["intensity", "light_color", "attenuation_radius"],
            "add_to": "actor.add_component_by_class(unreal.PointLightComponent)"
        },
        "audio_component": {
            "description": "Plays sound",
            "properties": ["sound", "volume_multiplier", "pitch_multiplier"],
            "add_to": "actor.add_component_by_class(unreal.AudioComponent)"
        },
        "particle_system_component": {
            "description": "Particle effects",
            "properties": ["template", "activator", "max_count"],
            "add_to": "actor.add_component_by_class(unreal.ParticleSystemComponent)"
        },
        "skeletal_mesh_component": {
            "description": "Animated mesh component",
            "properties": ["skeletal_mesh", "anim_class", "physics_asset"],
            "add_to": "actor.add_component_by_class(unreal.SkeletalMeshComponent)"
        },
        "spring_arm_component": {
            "description": "Spring arm for cameras (smooth follow)",
            "properties": ["target_arm_length", "socket_offset", "do_collision_test"],
            "add_to": "actor.add_component_by_class(unreal.SpringArmComponent)"
        },
        "rotating_movement_component": {
            "description": "Rotates actor continuously",
            "properties": ["rotation_rate", "pivot_offset"],
            "add_to": "actor.add_component_by_class(unreal.RotatingMovementComponent)"
        }
    },

    # Materials
    "materials": {
        "material": {
            "description": "Base material asset",
            "properties": {
                "base_color": "MaterialProperty.MP_BASE_COLOR - Color of the surface",
                "metallic": "MaterialProperty.MP_METALLIC - 0=non-metal, 1=metal",
                "roughness": "MaterialProperty.MP_ROUGHNESS - 0=smooth, 1=rough",
                "specular": "MaterialProperty.MP_SPECULAR - Specular highlight",
                "normal": "MaterialProperty.MP_NORMAL - Surface detail",
                "emissive_color": "MaterialProperty.MP_EMISSIVE_COLOR - Glow",
                "opacity": "MaterialProperty.MP_OPACITY - Transparency",
                "world_position_offset": "MaterialProperty.MP_WORLD_POSITION_OFFSET - Vertex displacement"
            },
            "expression_types": {
                "Constant": "Single float value",
                "Constant2Vector": "2D vector (2 floats)",
                "Constant3Vector": "RGB color (3 floats)",
                "Constant4Vector": "RGBA color (4 floats)",
                "TextureSample": "Sample a texture",
                "TextureSampleParameter2D": "Sample texture parameter",
                "LinearInterpolate": "Blend between two values",
                "Multiply": "Multiply two values",
                "Add": "Add two values",
                "Divide": "Divide two values",
                "Subtract": "Subtract two values",
                "Clamp": "Clamp value between min and max",
                "Power": "Raise value to power",
                "SquareRoot": "Square root",
                "OneMinus": "1 - value",
                "Fresnel": "Fresnel effect based on viewing angle",
                "NormalMap": "Convert normal map texture",
                "BumpOffset": "Parallax mapping",
                "WorldAlignedTexture": "Texture aligned to world space",
                "CameraPosition": "World space camera position",
                "WorldSpaceCameraPos": "Camera position in world space",
                "PixelNormal": "Surface normal in pixel shader",
                "VertexNormal": "Surface normal in vertex shader"
            }
        },
        "material_instance": {
            "description": "Instance of material with overridden parameters",
            "types": ["MaterialInstanceConstant", "MaterialInstanceDynamic"],
            "creation": "Create from parent material, set scalar/vector/texture parameters"
        }
    },

    # Textures
    "textures": {
        "texture_2d": {
            "description": "Standard 2D texture",
            "formats": ["RGBA8", "RGB8", "BGR8", "BGRA8", "R8", "G8", "A8"],
            "compression": ["Default", "UserInterface2D", "HDR", "RGBE", "EXR", "BC4", "BC5"],
            "settings": {
                "srgb": "Convert gamma space for color textures",
                "filter": "Texture filtering (Linear, Nearest)",
                "address_x": "Texture tiling (Wrap, Clamp, Mirror)",
                "address_y": "Texture tiling (Wrap, Clamp, Mirror)",
                "mip_gen_settings": "Mipmap generation",
                "lod_group": "Level of detail settings"
            },
            "common_types": ["diffuse/albedo", "normal", "roughness", "metallic", "emissive", "ao", "height", "opacity", "mask"]
        },
        "texture_cube": {
            "description": "Cubemap texture (6 faces)",
            "uses": ["skyboxes", "reflections", "environment lighting"],
            "creation": "Capture scene with SceneCaptureComponent2D"
        },
        "render_target": {
            "description": "Texture that can be rendered to",
            "uses": ["cameras", "mirrors", "post-processing", "offscreen rendering"],
            "settings": ["size", "format", "auto_clear", "capture_source"]
        }
    },

    # Static Meshes
    "static_meshes": {
        "description": "3D geometry that doesn't deform",
        "creation": ["Import FBX/OBJ", "Create in Blender/Maya", "Procedural generation"],
        "properties": {
            "lod_settings": "Level of detail configuration",
            "sections": "Material sections for different parts",
            "collision": "Simple or complex collision shapes",
            "build_settings": "Rebuild settings for lightmass/physics"
        },
        "modifying": {
            "edit_mesh": "Right-click -> Edit Static Mesh to modify geometry",
            "create_uv": "Generate UV mapping",
            "set_materials": "Assign materials to sections"
        }
    },

    # Skeletal Meshes
    "skeletal_meshes": {
        "description": "3D geometry with skeleton for animation",
        "creation": ["Import FBX with skeleton", "Create with skeleton"],
        "components": ["SkeletalMeshComponent for rendering"],
        "properties": {
            "skeleton": "Bone hierarchy",
            "physics_asset": "Physics for ragdoll",
            "anim_class": "Animation blueprint class"
        },
        "retargeting": "Can retarget animations between skeletons"
    },

    # Animations
    "animations": {
        "animation_sequence": {
            "description": "Raw animation data",
            "properties": ["rate_scale", "enable_root_motion"],
            "import": "Import from FBX with animation"
        },
        "animation_blueprint": {
            "description": "State machine for animation logic",
            "components": ["AnimGraph - visual scripting", "Event Graph - logic"],
            "states": ["Idle", "Running", "Jumping", "Attacking", etc.],
            "transitions": "Conditions between states",
            "blendspaces": "Smooth blending between animations"
        },
        "anim_montage": {
            "description": "Animation sequence with slots for layering",
            "uses": ["Attacks", "Reacts", "Specific animations that override"]
        },
        "aim_offset": {
            "description": "Aiming poses for upper body",
            "uses": ["First person shooters", "Aiming"]
        }
    },

    # Blueprints
    "blueprints": {
        "blueprint_class": {
            "description": "Create new actor or component class",
            "types": ["Actor", "Component", "GameMode", "HUD", "Widget", "Pawn", "Character"],
            "components": ["Add components to blueprint"],
            "variables": ["Expose to spawn", "Instance editable"],
            "functions": ["Custom functions in blueprint"],
            "events": ["Event Graph with lifecycle events"],
            "graphs": ["Construction Script, Event Graph, Macro, Function"]
        },
        "blueprint_macro_library": {
            "description": "Reusable blueprint nodes",
            "uses": ["Common operations", "Custom nodes"]
        },
        "blueprint_function_library": {
            "description": "Static functions callable from anywhere",
            "uses": ["Utility functions", "Math operations"]
        },
        "blueprint_interface": {
            "description": "Interface that blueprints can implement",
            "uses": ["Common functionality", "Communication between systems"]
        }
    },

    # Level Editing
    "levels": {
        "level_streaming": {
            "description": "Load/unload levels dynamically",
            "methods": ["Volume-based", "Always Loaded"],
            "uses": ["Open worlds", "Performance optimization"]
        },
        "level_instances": {
            "description": "Instance of level in main level",
            "uses": ["Modular design", "Repeating environments"]
        },
        "world_partition": {
            "description": "UE5 system for large worlds",
            "features": ["Grid-based loading", "Runtime editing", "HLOD"]
        },
        "folders": {
            "description": "Organize actors in level",
            "uses": ["Grouping", "Organization"]
        },
        "layers": {
            "description": "Organize actors into layers",
            "uses": ["Visibility control", "Selection"]
        }
    },

    # Lighting
    "lighting": {
        "lightmass": {
            "description": "Pre-computed global illumination",
            "build": "Build lighting to compute lightmaps",
            "settings": ["Quality level", "Compress lightmaps", "Use error color"],
            "lightmap_resolution": "Resolution per object"
        },
        "lumen": {
            "description": "UE5 dynamic global illumination",
            "settings": ["Quality", "Screen Probe Gutter", "Surface Cache"],
            "uses": ["Real-time GI", "No baking needed"]
        },
        "nanite": {
            "description": "Virtualized geometry for high-poly meshes",
            "settings": ["Cull distance", "Pixels per triangle"],
            "uses": ["Film-quality assets", "Massive scenes"]
        },
        "reflection": {
            "types": ["Reflection Capture", "Planar Reflection", "Screen Space Reflection"],
            "settings": ["Brightness", "Cubemap format", "Max roughness"]
        },
        "shadows": {
            "types": ["CSM - Cascaded Shadow Maps", "Raytraced shadows"],
            "settings": ["Resolution", "Shadow distance", "Cascades"]
        },
        "volumetric_fog": {
            "description": "Volumetric light scattering",
            "settings": ["Fog density", "Scattering distribution"]
        }
    },

    # Post Processing
    "post_processing": {
        "post_process_volume": {
            "description": "Defines post process settings in a region",
            "properties": {
                "exposure": "Brightness adjustment",
                "bloom": "Glow effect",
                "tone_mapper": "Tone mapping (ACES, Neutral)",
                "color_grading": "Color correction (LUT)",
                "ambient_occlusion": "SSAO settings",
                "motion_blur": "Camera motion blur",
                "depth_of_field": "Focus blur",
                "screen_space_reflections": "SSR settings",
                "lens_flares": "Lens effects",
                "anti_aliasing": ["FXAA", "TAA", "TSR", "DLSS", "FSR2"]
            },
            "methods": ["Infinite extent", "Global settings", "Unbound"]
        },
        "exposure": {
            "min_brightness": "Minimum brightness",
            "max_brightness": "Maximum brightness",
            "bias": "Exposure bias",
            "calibration": "Exposure calibration"
        }
    },

    # Physics
    "physics": {
        "rigid_body": {
            "description": "Object with physics simulation",
            "settings": {
                "simulate_physics": "Enable physics",
                "mass": "Object mass in kg",
                "linear_damping": "Slow down linear movement",
                "angular_damping": "Slow down rotation",
                "enable_gravity": "Affect by gravity"
            }
        },
        "constraints": {
            "physics_constraint": {
                "description": "Constrain physics bodies together",
                "types": ["Hinge", "Prismatic", "Spherical", "Planar", "Fixed"],
                "limits": "Constraint limits (angular, linear)"
            }
        },
        "collision": {
            "object_types": ["WorldStatic", "WorldDynamic", "Pawn", "Vehicle", "Destructible"],
            "responses": ["Ignore", "Overlap", "Block", "Physics only"],
            "channels": ["Default", "Pawn", "Vehicle", "Camera", "Visibility", "Weapon"],
            "presets": ["BlockAll", "OverlapAll", "PawnOnly", etc.]
        }
    },

    # Niagara
    "niagara": {
        "description": "Advanced particle system",
        "emitters": ["Spawn rate", "Burst", "Spawn Per Unit"],
        "modules": {
            "spawn": "When particles spawn",
            "update": "Every frame",
            "render": "How particles render",
            "event": "Trigger events"
        },
        "data_types": ["float", "vector", "color", "mesh", "texture"],
        "common_systems": ["Fire", "Smoke", "Explosion", "Magic", "Water", "Dust"]
    },

    # UMG (Unreal Motion Graphics)
    "umg": {
        "widget": {
            "description": "Base UI element",
            "common_widgets": {
                "CanvasPanel": "Container for other widgets",
                "Image": "Display texture/color",
                "Text": "Display text",
                "Button": "Clickable button",
                "CheckBox": "Toggle option",
                "ComboBox": "Dropdown selection",
                "Slider": "Value slider",
                "SpinBox": "Number input",
                "EditableTextBox": "Text input",
                "ProgressBar": "Progress display",
                "ListView": "List of items",
                "TreeView": "Hierarchical list",
                "GridPanel": "Grid layout",
                "VerticalBox": "Vertical stack",
                "HorizontalBox": "Horizontal stack",
                "SizeBox": "Fixed size container",
                "Border": "Container with image",
                "RetainerBox": "Cached rendering"
            },
            "events": ["OnClicked", "OnHovered", "OnUnhovered", "OnTextChanged", "OnValueChanged"],
            "creation": ["Create widget", "Add to viewport", "Remove from viewport"]
        },
        "animation": {
            "description": "Animate widget properties",
            "tracks": ["Color", "Opacity", "Transform", "Rotation", "Scale"],
            "curves": ["Linear", "Cubic", "Auto", "User"],
            "events": ["Keyframe events"]
        }
    },

    # Input
    "input": {
        "action_mappings": {
            "description": "Map input to action",
            "types": ["Button", "Axis1D", "Axis2D", "Axis3D"],
            "triggers": ["Pressed", "Released", "Repeat"]
        },
        "axis_mappings": {
            "description": "Map input to continuous value",
            "scale": "Multiplier for input value"
        },
        "input_components": {
            "enhanced_input": {
                "description": "UE5 input system",
                "features": ["Input Actions", "Input Modifiers", "Input Triggers"],
                "contexts": "Different input setups for different situations"
            },
            "player_input": {
                "description": "Legacy input component",
                "features": ["Action mappings", "Axis mappings"]
            }
        },
        "common_bindings": {
            "keyboard": "Keys like W, A, S, D, Space, Escape, etc.",
            "mouse": "Left/Right/Middle buttons, scroll wheel",
            "gamepad": "Buttons, sticks, triggers",
            "touch": "Tap, pinch, swipe (mobile)"
        }
    },

    # Gameplay Framework
    "gameplay": {
        "game_mode": {
            "description": "Defines rules of the game",
            "properties": ["Default Pawn Class", "Player Controller Class", "HUD Class"],
            "functions": ["StartPlay", "RestartGame", "EndPlay"]
        },
        "player_controller": {
            "description": "Controls player pawn and processes input",
            "features": ["Input processing", "Camera control", "HUD management"]
        },
        "game_state": {
            "description": "Replicated game state",
            "uses": ["Score", "Match state", "Game time"]
        },
        "player_state": {
            "description": "Replicated player state",
            "uses": ["Player name", "Score", "Team"]
        },
        "hud": {
            "description": "Heads Up Display",
            "creation": ["Blueprint HUD", "UMG widgets"]
        }
    },

    # Networking
    "networking": {
        "replication": {
            "description": "Sync data between server and clients",
            "variables": ["Replicated", "RepNotify", "OnRep functions"],
            "functions": ["Server", "Client", "Multicast", "NetMulticast"],
            "conditions": ["WithValidation", "Reliable", "Unreliable"]
        },
        "relevancy": {
            "description": "What actors get replicated to clients",
            "types": ["Always relevant", "NetRelevancy strategies"]
        },
        "replication_graph": {
            "description": "Optimize network bandwidth",
            "uses": ["Large worlds", "Many actors"]
        }
    },

    # Audio
    "audio": {
        "sound_wave": {
            "description": "Audio file asset",
            "formats": ["WAV", "OGG", "MP3"],
            "compression": ["Compressed", "PCM", "ADPCM"],
            "settings": ["Sample rate", "Channels", "Bit depth"]
        },
        "sound_cue": {
            "description": "Sound graph for mixing",
            "nodes": [
                "Sound Wave - Play audio",
                "Modulator - Pitch/volume modulation",
                "Attenuation - Distance falloff",
                "Mixer - Audio mixing",
                "Delay - Delay playback",
                "Looping - Loop sound",
                "Random - Random selection"
            ]
        },
        "audio_component": {
            "description": "Component to play sounds",
            "properties": ["Sound", "Volume", "Pitch", "Attenuation"]
        },
        "ambient_sound": {
            "description": "Background sound in level",
            "uses": ["Music", "Ambience", "Environment"]
        }
    },

    # AI
    "ai": {
        "ai_controller": {
            "description": "Controls AI pawns",
            "components": {
                "behavior_tree": "AI logic tree",
                "blackboard": "Data storage",
                "perception": "Sense environment",
                "navigation": "Pathfinding"
            }
        },
        "behavior_tree": {
            "description": "Hierarchical AI logic",
            "nodes": {
                "composite": ["Sequence", "Selector", "Parallel", "Simple Parallel"],
                "decorator": ["Blackboard", "Cooldown", "Compare Blackboard"],
                "task": ["Move To", "Wait", "Play Animation", "Run Blueprint"]
            }
        },
        "env_query": {
            "description": "Environment queries for AI",
            "uses": ["Find locations", "Find random points", "Trace testing"]
        },
        "navigation": {
            "nav_mesh": {
                "description": "Walkable surface for AI",
                "generation": "Build nav mesh from geometry",
                "modifiers": "Adjust nav properties"
            },
            "nav_links": {
                "description": "Connect nav mesh areas",
                "uses": ["Jumps", "drops", "custom paths"]
            }
        }
    },

    # Rendering
    "rendering": {
        "materials_advanced": {
            "material_functions": {
                "description": "Reusable material logic",
                "uses": ["Common operations", "Material layering"]
            },
            "material_layers": {
                "description": "Blend materials based on landscape layers",
                "uses": ["Terrain", "Blending"]
            },
            "material_attributes": {
                "description": "Custom material properties",
                "uses": ["Complex materials", "Data-driven"]
            }
        },
        "mesh_processing": {
            "spline_meshes": {
                "description": "Mesh that follows a spline",
                "uses": ["Pipes", "Roads", "Cables"]
            },
            "procedural_mesh": {
                "description": "Runtime mesh generation",
                "uses": ["Terrain", "Custom geometry"]
            },
            "geometry_collection": {
                "description": "Chaos destruction system",
                "uses": ["Destruction", "Fracture"]
            }
        },
        "virtual_texturing": {
            "description": "Stream texture tiles",
            "uses": ["Large textures", "Open worlds", "Memory optimization"]
        }
    },

    # Tools
    "tools": {
        "blutility": {
            "description": "Blueprint utility for batch operations",
            "uses": ["Level operations", "Asset management"]
        },
        "editor_scripting": {
            "description": "Python scripts for editor automation",
            "modules": [
                "unreal - Main module",
                "unreal.EditorLevelLibrary - Level operations",
                "unreal.EditorAssetLibrary - Asset operations",
                "unreal.EditorFilterLibrary - Filtering",
                "unral.MaterialEditingLibrary - Material editing",
                "unreal.BlueprintPaletteLibrary - Blueprint utilities"
            ]
        },
        "commandlets": {
            "description": "Command-line tools",
            "uses": ["Batch processing", "Automation", "Cooking"]
        }
    },

    # Project Settings
    "settings": {
        "rendering": [
            "Global Clip Plane",
            "Instanced Stereo",
            "MSAA Sample Count",
            "Screen Percentage",
            "Global Illumination",
            "Reflections",
            "Translucency",
            "Ray Tracing"
        ],
        "gameplay": [
            "Default GameMode",
            "Max Smoothed Frame Rate",
            "Use Fixed Frame Rate",
            "Network Settings"
        ],
        "engine": [
            "Scalability Settings",
            "Streaming Settings",
            "Physics Settings",
            "Audio Settings"
        ],
        "editor": [
            "Performance Data",
            "Blueprint Editor",
            "Content Editors",
            "Automation"
        ]
    },

    # File Paths and Organization
    "project_structure": {
        "content_folders": {
            "Game/Content": "All game content",
            "Engine/Content": "Engine content (read-only)",
            "Plugins/PluginName/Content": "Plugin content"
        },
        "organization": [
            "Assets/ - Source assets (FBX, textures)",
            "Meshes/ - Static and skeletal meshes",
            "Materials/ - Material instances",
            "Textures/ - Texture files",
            "Audio/ - Sound files",
            "UI/ - Widget blueprints",
            "Blueprints/ - Blueprint classes",
            "Maps/ - Level files"
        ]
    }
}


# Common tasks and workflows
WORKFLOWS = {
    "create_basic_actor": """
    1. Determine actor type needed
    2. Use spawn_actor_from_class with appropriate class
    3. Set location (unreal.Vector)
    4. Set rotation (unreal.Rotator)
    5. Set scale (unreal.Vector)
    6. Set actor label
    7. Configure components/properties
    """,

    "create_material_from_texture": """
    1. Create material in /Game/Materials
    2. Add TextureSample node
    3. Set texture asset
    4. Connect to Base Color
    5. Add other properties as needed (Roughness, Normal, etc.)
    """,

    "setup_basic_lighting": """
    1. Add DirectionalLight (sun)
    2. Add SkyLight for ambient
    3. Add AtmosphericFog for depth
    4. Add PointLights/SpotLights as needed
    5. Add Reflection Capture (box or sphere)
    6. Build lighting (if using Lightmass)
    """,

    "import_fbx_model": """
    1. Place FBX in project Assets folder
    2. Use FBX Import dialog
    3. Set import options:
       - Mesh Type (Static/Skeletal)
       - Materials (Import or Create)
       - Collision (Auto or Rebuild)
       - Transform (scale, rotation)
    4. Import to /Game/Meshes
    5. Create materials if needed
    6. Place in level
    """,

    "create_animating_blueprint": """
    1. Create Blueprint Class (Actor or Pawn)
    2. Add StaticMesh or SkeletalMesh component
    3. Set mesh asset
    4. Add Timeline component or use Event Tick
    5. In Event Graph or Timeline, update properties:
       - Set Actor Rotation
       - Set Actor Location
       - Update Material parameters
    6. Compile and test
    """,

    "setup_character_controller": """
    1. Create Blueprint Class based on Character
    2. Add SpringArm component
    3. Add Camera component to SpringArm
    4. Create Input Action mappings (WASD, Mouse)
    5. In Blueprint Event Graph:
       - Add InputAction events
       - Move character with InputAxis
       - Control camera rotation
       - Add Jump action
    6. Set as Default Pawn Class in GameMode
    """,

    "create_ui_widget": """
    1. Create Widget Blueprint
    2. Add CanvasPanel (root)
    3. Add UI elements:
       - Image for backgrounds
       - Text for labels
       - Button for interaction
    4. Layout elements:
       - Set size and position
       - Set anchors for responsive
       - Bind to variables
    5. Add events (OnClicked, etc.)
    6. In Blueprint: Create widget and add to viewport
    """,

    "setup_post_processing": """
    1. Create PostProcessVolume
    2. Set Settings (Infinite extent)
    3. Configure effects:
       - Bloom > Intensity
       - Tone Mapper > Method
       - Color Grading > LUT
       - Exposure > Min/Max Brightness
    4. Add cinematic effects:
       - Depth of Field
       - Motion Blur
       - Film Grain
    5. Test in PIE
    """,

    "create_particle_effect": """
    1. Create Niagara System
    2. Add Emitter (Spawn Rate or Burst)
    3. Configure Spawn module
    4. Add Initialize modules:
       - Position (sphere, box, etc.)
       - Velocity (directional)
       - Color
       - Size
       - Lifetime
    5. Add Update modules:
       - Color over life
       - Size over life
       - Velocity drag
    6. Add Render module (Sprites, Meshes, Ribbons)
    7. Test and iterate
    """,

    "create_landscape": """
    1. Create Landscape in Modes > Landscape
    2. Choose:
       - Material (for layers)
       - Size (sections, quads)
    3. Sculpt terrain:
       - Sculpt tool
       - Flatten tool
       - Smooth tool
    4. Paint layers
    5. Add Grass:
       - Create Grass Type
       - Assign to Landscape
    6. Add Foliage:
       - Create Foliage Type
       - Paint with Foliage tool
    """
}


# Common problems and solutions
TROUBLESHOOTING = {
    "actor_not_visible": """
    Possible causes:
    - Scale is 0
    - Hidden in level
    - No static mesh assigned
    - Material has 0 opacity
    - Outside camera view
    Solutions:
    - Check scale in Details panel
    - Ensure Visible in viewport
    - Assign valid Static Mesh
    - Check material opacity
    - Use "Pilot" actor to find it
    """,

    "material_appears_black": """
    Possible causes:
    - No material assigned
    - Material has no Base Color
    - Material function compile error
    - Wrong shading model
    Solutions:
    - Assign material to material slot
    - Check Base Color is connected
    - Click Apply on material
    - Use Default Material for testing
    """,

    "physics_not_working": """
    Possible causes:
    - Simulate Physics not enabled
    - Mass is 0
    - No collision set
    - Object is static
    Solutions:
    - Enable Simulate Physics on actor
    - Set Mass > 0
    - Check Collision preset
    - Use Move instead of Static
    """,

    "lighting_looks_bad": """
    Possible causes:
    - No lightmass built
    - Lightmap resolution too low
    - No reflection capture
    - Wrong exposure settings
    Solutions:
    - Build lighting
    - Increase Lightmap Resolution
    - Add Reflection Capture
    - Adjust Exposure settings
    - Enable Lumen (UE5)
    """,

    "animation_not_playing": """
    Possible causes:
    - No Animation Blueprint assigned
    - Animation not in state machine
    - No event triggering anim
    - Asset not linked
    Solutions:
    - Assign AnimBlueprint to skeletal mesh
    - Check Animation Blueprint graph
    - Verify asset is in state machine
    - Use Play Anim node
    """,

    "blueprint_not_compiling": """
    Possible causes:
    - Circular dependency
    - Wrong variable type
    - Missing asset
    - Syntax error
    Solutions:
    - Check Compile Output window
    - Fix errors in red
    - Ensure assets exist
    - Check variable connections
    """
}


# Asset creation templates
ASSET_TEMPLATES = {
    "standard_material": {
        "nodes": [
            "TextureSample -> Base Color",
            "Constant -> Roughness",
            "Constant -> Metallic",
            "Constant -> Normal -> Normal"
        ]
    },
    "glass_material": {
        "nodes": [
            "Constant3Vector (0.8, 0.9, 1.0, 0.3) -> Base Color",
            "Constant (0) -> Roughness",
            "Constant (0) -> Metallic",
            "Fresnel -> Opacity with OneMinus"
        ]
    },
    "emissive_material": {
        "nodes": [
            "TextureSample -> Base Color AND Emissive Color",
            "Constant (1) -> Emissive"
        ]
    },
    "water_material": {
        "nodes": [
            "TextureSample -> Normal -> Normal",
            "Constant3Vector (0.0, 0.3, 0.5) -> Base Color",
            "Fresnel -> Roughness (multiplied)",
            "WorldAlignedTexture -> Base Color (blended)"
        ]
    },
    "hologram_material": {
        "nodes": [
            "Constant3Vector (0.0, 1.0, 0.8, 1.0) -> Emissive Color",
            "Time -> Sine -> Opacity",
            "Fresnel -> Opacity (multiplied)",
            "ScreenPosition -> Base Color"
        ]
    }
}


def search_knowledge(query: str) -> dict:
    """Search the knowledge base for relevant information"""
    query = query.lower()
    results = {}

    for category, data in UE_KNOWLEDGE_BASE.items():
        if isinstance(data, dict):
            for key, value in data.items():
                if query in str(value).lower() or query in key.lower():
                    if category not in results:
                        results[category] = {}
                    results[category][key] = value

    return results


def get_workflow(task_name: str) -> str:
    """Get workflow for a specific task"""
    for key, workflow in WORKFLOWS.items():
        if task_name.lower() in key.lower() or key.lower() in task_name.lower():
            return workflow
    return None


def solve_problem(problem: str) -> str:
    """Get solution for common problem"""
    for key, solution in TROUBLESHOOTING.items():
        if problem.lower() in key.lower():
            return solution
    return None


def get_asset_template(template_name: str) -> dict:
    """Get asset template"""
    for key, template in ASSET_TEMPLATES.items():
        if template_name.lower() in key.lower():
            return template
    return None


# Export everything
__all__ = [
    'UE_KNOWLEDGE_BASE',
    'WORKFLOWS',
    'TROUBLESHOOTING',
    'ASSET_TEMPLATES',
    'search_knowledge',
    'get_workflow',
    'solve_problem',
    'get_asset_template'
]
