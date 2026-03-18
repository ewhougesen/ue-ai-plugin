# Demon Material Updates - Detailed Specification

This document provides the exact material updates needed for three demon functions in `/Volumes/SERENADA_2/_elliott/Unreal Projects/UEAI-Plugin-Test/Plugins/UEAIPlugin/Content/Python/ue_infinite_creation.py`.

## Update Pattern

Change from:
```python
torso = self._create_composite_cube(f"{name}_Torso", torso_pos, torso_scale, basalt_dark)
```

To:
```python
torso = self._create_composite_cube(
    f"{name}_Torso", torso_pos, torso_scale, basalt_dark,
    material_type="stone",
    material_params={
        "secondary": granite_light,
        "weathering": 0.4,
        "roughness": 0.9,
        "cracks": True
    }
)
```

---

## 1. STONE DEMON (_create_stone_demon_hollywood) - Line 2872

### Material Strategy:
- **Main body parts**: Heavy weathered stone (roughness: 0.90+, weathering: 0.45+, cracks: true)
- **Joints**: Polished worn stone (roughness: 0.50-0.60, weathering: 0.30-0.40)
- **Deep cavities**: Dark stone (roughness: 0.96+, weathering: 0.60+, cracks: true)
- **Protruding features**: Medium weathering (roughness: 0.75-0.88, weathering: 0.38-0.48)

### Body Parts to Update:

#### TORSO & BODY
- `torso` (line 2923): limestone_base → stone, weathering: 0.5, roughness: 0.92, cracks: True
- `ab[i]` (line 2934): sandstone_light → stone, weathering: 0.35, roughness: 0.88, cracks: False
- `sternum` (line 2940): sandstone_light → stone, weathering: 0.42, roughness: 0.85, cracks: False

#### SHOULDERS & ARMS
- `delt` (line 2952): limestone_base → stone, weathering: 0.48, roughness: 0.90, cracks: True
- `clavicle` (line 2958): sandstone_light → stone, weathering: 0.38, roughness: 0.55, cracks: False
- `vertebra` (line 2965): limestone_base → stone, weathering: 0.45, roughness: 0.52, cracks: False
- `neck` (line 2970): limestone_base → stone, weathering: 0.46, roughness: 0.91, cracks: True

#### HEAD
- `skull` (line 2976): limestone_base → stone, weathering: 0.52, roughness: 0.94, cracks: True
- `brow` (line 2982): sandstone_light → stone, weathering: 0.40, roughness: 0.82, cracks: False
- `cheek` (line 2989): limestone_base → stone, weathering: 0.44, roughness: 0.89, cracks: False
- `jaw` (line 2995): limestone_base → stone, weathering: 0.50, roughness: 0.92, cracks: True
- `chin` (line 3001): limestone_base → stone, weathering: 0.55, roughness: 0.90, cracks: False

#### EYES
- `socket` (line 3009): stone_dark → stone, weathering: 0.6, roughness: 0.96, cracks: True
- `eyelid` (line 3021): limestone_base → stone, weathering: 0.42, roughness: 0.58, cracks: False

#### FACE FEATURES
- `nose` (line 3027): limestone_base → stone, weathering: 0.48, roughness: 0.86, cracks: False
- `nostril` (line 3034): stone_dark → stone, weathering: 0.65, roughness: 0.97, cracks: True
- `mouth` (line 3040): stone_dark → stone, weathering: 0.7, roughness: 0.96, cracks: True
- `tooth` (line 3051): sandstone_light → stone, weathering: 0.35, roughness: 0.55, cracks: False

#### HORNS
- `horn_base` (line 3059): limestone_base → stone, weathering: 0.45, roughness: 0.88, cracks: True
- `horn_seg[j]` (line 3070): sandstone_light → stone, weathering: 0.38+(j*0.05), roughness: 0.48+(j*0.08), cracks: False
- `horn_tip` (line 3076): wear_brown → stone, weathering: 0.6, roughness: 0.62, cracks: False
- `ear` (line 3083): limestone_base → stone, weathering: 0.43, roughness: 0.87, cracks: False

#### ARMS (Upper)
- `humerus` (line 3098): limestone_base → stone, weathering: 0.47, roughness: 0.91, cracks: True
- `bicep` (line 3104): sandstone_light → stone, weathering: 0.40, roughness: 0.86, cracks: False
- `elbow` (line 3115): sandstone_light → stone, weathering: 0.36, roughness: 0.50, cracks: False

#### ARMS (Lower)
- `forearm` (line 3121): limestone_base → stone, weathering: 0.49, roughness: 0.90, cracks: True
- `muscle[k]` (line 3132): sandstone_light → stone, weathering: 0.41, roughness: 0.84, cracks: False
- `wrist` (line 3143): sandstone_light → stone, weathering: 0.34, roughness: 0.52, cracks: False

#### HANDS
- `palm` (line 3149): limestone_base → stone, weathering: 0.46, roughness: 0.89, cracks: True
- `finger` (line 3168): limestone_base → stone, weathering: 0.44, roughness: 0.87, cracks: False

#### LEGS (Upper)
- `thigh` (line 3183): limestone_base → stone, weathering: 0.48, roughness: 0.91, cracks: True
- `quad[q]` (line 3194): sandstone_light → stone, weathering: 0.39, roughness: 0.83, cracks: False
- `patella` (line 3205): sandstone_light → stone, weathering: 0.32, roughness: 0.48, cracks: False

#### LEGS (Lower)
- `shin` (line 3211): limestone_base → stone, weathering: 0.50, roughness: 0.92, cracks: True
- `calf` (line 3217): sandstone_light → stone, weathering: 0.42, roughness: 0.85, cracks: False
- `detail[s]` (line 3228): limestone_base → stone, weathering: 0.45, roughness: 0.88, cracks: False
- `ankle` (line 3239): sandstone_light → stone, weathering: 0.30, roughness: 0.50, cracks: False

#### FEET
- `foot` (line 3245): limestone_base → stone, weathering: 0.52, roughness: 0.93, cracks: True
- `toe` (line 3256): limestone_base → stone, weathering: 0.47, roughness: 0.86, cracks: False
- `joint` (line 3267): sandstone_light → stone, weathering: 0.33, roughness: 0.54, cracks: False
- `heel` (line 3273): limestone_base → stone, weathering: 0.51, roughness: 0.90, cracks: True

#### TAIL
- `vertebra[i]` (line 3281): limestone_base → stone, weathering: 0.43, roughness: 0.54, cracks: False
- `tail_base` (line 3287): limestone_base → stone, weathering: 0.49, roughness: 0.91, cracks: True
- `segment[i]` (line 3294): limestone_base → stone, weathering: 0.50+(i*0.03), roughness: 0.92+(i*0.02), cracks: True
- `club` (line 3300): limestone_base → stone, weathering: 0.55, roughness: 0.94, cracks: True
- `spike` (line 3312): sandstone_light → stone, weathering: 0.38, roughness: 0.75, cracks: False
- `tip` (line 3322): wear_brown → stone, weathering: 0.58, roughness: 0.68, cracks: False

---

## 2. FIRE DEMON (_create_fire_demon_hollywood) - Line 3391

### Material Strategy:
- **Body**: Charred stone (roughness: 0.85, heavy weathering)
- **Cracks**: Glowing ember effect (use darker material, high roughness)
- **Core**: Layered material with medium roughness (0.50)
- **Spikes**: Charred bone-like material (roughness: 0.78)

### Color Variables Available:
- `charred_black = (0.08, 0.06, 0.05)`
- `ash_gray = (0.28, 0.26, 0.24)`
- `ember_brown = (0.22, 0.14, 0.10)`
- `crack_dark = (0.05, 0.04, 0.03)`
- `wood_char = (0.15, 0.10, 0.08)`

### Body Parts to Update:

#### BODY
- `torso` (line 3437): charred_black → stone, weathering: 0.7, roughness: 0.85, cracks: True
- `chest` (line 3443): ash_gray → stone, weathering: 0.5, roughness: 0.78, cracks: False
- `ridge[i]` (line 3454): ember_brown → stone, weathering: 0.65, roughness: 0.82, cracks: True

#### NECK & HEAD
- `neck[i]` (line 3461): charred_black → stone, weathering: 0.68, roughness: 0.84, cracks: True
- `neck_main` (line 3466): charred_black → stone, weathering: 0.70, roughness: 0.86, cracks: True
- `skull` (line 3472): charred_black → stone, weathering: 0.72, roughness: 0.87, cracks: True
- `brow` (line 3479): ash_gray → stone, weathering: 0.55, roughness: 0.75, cracks: False
- `snout` (line 3485): charred_black → stone, weathering: 0.69, roughness: 0.83, cracks: True
- `jaw` (line 3491): charred_black → stone, weathering: 0.71, roughness: 0.85, cracks: True

#### EYES & FACE
- `socket` (line 3499): crack_dark → stone, weathering: 0.8, roughness: 0.95, cracks: True
- `eye` (line 3505): (0.25, 0.18, 0.15) → layered, roughness: 0.50, layers: 3
- `nostril` (line 3512): crack_dark → stone, weathering: 0.82, roughness: 0.96, cracks: True
- `tooth` (line 3523): ash_gray → stone, weathering: 0.45, roughness: 0.60, cracks: False

#### HORNS
- `horn_base` (line 3530): charred_black → stone, weathering: 0.67, roughness: 0.81, cracks: True
- `horn_shaft` (line 3536): ash_gray → stone, weathering: 0.52, roughness: 0.68, cracks: False
- `tip` (line 3542): ember_brown → stone, weathering: 0.60, roughness: 0.72, cracks: False
- `ear` (line 3549): charred_black → stone, weathering: 0.65, roughness: 0.80, cracks: True

#### LEGS
- `upper_leg` (line 3577): charred_black → stone, weathering: 0.69, roughness: 0.84, cracks: True
- `muscle` (line 3587): ash_gray → stone, weathering: 0.50, roughness: 0.72, cracks: False
- `joint_detail` (line 3601): ash_gray → stone, weathering: 0.45, roughness: 0.55, cracks: False
- `lower_leg` (line 3611): charred_black → stone, weathering: 0.70, roughness: 0.85, cracks: True
- `paw` (line 3630): charred_black → stone, weathering: 0.71, roughness: 0.86, cracks: True
- `toe` (line 3641): ash_gray → stone, weathering: 0.48, roughness: 0.65, cracks: False
- `claw` (line 3652): ember_brown → stone, weathering: 0.55, roughness: 0.70, cracks: False

#### TAIL
- `tail_base` (line 3658): charred_black → stone, weathering: 0.68, roughness: 0.83, cracks: True
- `vertebra[i]` (line 3665): charred_black → stone, weathering: 0.66+(i*0.02), roughness: 0.82+(i*0.02), cracks: True
- `tip` (line 3671): ember_brown → stone, weathering: 0.62, roughness: 0.74, cracks: False

#### SURFACE DETAILS
- `crack[i]` (line 3683): crack_dark → stone, weathering: 0.85, roughness: 0.97, cracks: True
- `ash[i]` (line 3694): ash_gray → stone, weathering: 0.40, roughness: 0.70, cracks: False
- `scorch[i]` (line 3705): ember_brown → stone, weathering: 0.58, roughness: 0.76, cracks: True
- `texture[i]` (line 3716): conditional → stone, weathering: 0.52, roughness: 0.74, cracks: False

---

## 3. WATER DEMON (_create_water_demon_hollywood) - Line 3729

### Material Strategy:
- **Body**: Wet flesh material (subsurface: 0.4, wetness: 0.5, roughness: 0.35)
- **Scales**: Chitin material with glossiness (0.6)
- **Fins**: Translucent layered material (roughness: 0.25)
- **Webbing**: Layered organic (roughness: 0.30)
- **Teeth**: Bone-colored stone (roughness: 0.55)

### Color Variables Available:
- `swamp_green = (0.15, 0.28, 0.25)`
- `algae_brown = (0.22, 0.25, 0.18)`
- `scale_mud = (0.18, 0.22, 0.20)`
- `sucker_gray = (0.25, 0.28, 0.26)`
- `slime_coat = (0.20, 0.24, 0.22)`
- `barnacle_white = (0.65, 0.62, 0.58)`

### Body Parts to Update:

#### BODY
- `body` (line 3776): swamp_green → flesh, subsurface: 0.4, wetness: 0.5, roughness: 0.35
- `scale_piece[i]` (line 3787): scale_mud → chitin, glossiness: 0.6, roughness: 0.40
- `algae[i]` (line 3798): algae_brown → layered, roughness: 0.45, layers: 2

#### HEAD
- `head` (line 3804): swamp_green → flesh, subsurface: 0.35, wetness: 0.45, roughness: 0.38
- `jaw` (line 3810): swamp_green → flesh, subsurface: 0.38, wetness: 0.48, roughness: 0.40

#### EYES & FACE
- `socket` (line 3818): (0.10, 0.12, 0.10) → stone, weathering: 0.5, roughness: 0.75, cracks: False
- `eye` (line 3824): (0.45, 0.42, 0.28) → layered, roughness: 0.35, layers: 3
- `nostril` (line 3831): (0.12, 0.10, 0.08) → stone, weathering: 0.55, roughness: 0.80, cracks: True
- `tooth` (line 3842): (0.55, 0.52, 0.48) → stone, weathering: 0.35, roughness: 0.55, cracks: False

#### TENTACLES
- `tentacle_base` (line 3865): swamp_green → flesh, subsurface: 0.42, wetness: 0.52, roughness: 0.36
- `segment` (line 3885): swamp_green → flesh, subsurface: 0.40, wetness: 0.50, roughness: 0.35
- `sucker` (line 3897): sucker_gray → chitin, glossiness: 0.55, roughness: 0.45

#### TAIL
- `tail` (line 3903): swamp_green → flesh, subsurface: 0.38, wetness: 0.48, roughness: 0.37
- `vertebra[i]` (line 3910): scale_mud → chitin, glossiness: 0.5, roughness: 0.48
- `fin` (line 3916): scale_mud → layered, roughness: 0.25, layers: 3

#### SURFACE DETAILS
- `algae_patch[i]` (line 3928): algae_brown → layered, roughness: 0.50, layers: 2
- `barnacle[i]` (line 3939): barnacle_white → stone, weathering: 0.4, roughness: 0.65, cracks: False
- `slime[i]` (line 3950): slime_coat → flesh, subsurface: 0.5, wetness: 0.6, roughness: 0.30
- `damage[i]` (line 3961): (0.12, 0.15, 0.12) → stone, weathering: 0.6, roughness: 0.85, cracks: True

---

## Implementation Notes

1. **Secondary Colors**: For stone materials, always specify a secondary color (usually the lighter variant)
2. **Joints vs Body**: Joints should always have lower roughness (0.50-0.60) and lower weathering (0.30-0.40)
3. **Cracks**: Only set `cracks: True` for main body parts and dark cavities
4. **Layered Materials**: Use for eyes, fins, and organic features with translucency
5. **Flesh Materials**: Use for Water Demon body parts with subsurface scattering
6. **Chitin Materials**: Use for scales and hard aquatic surfaces

## Testing

After implementing these changes:
1. Spawn each demon type in Unreal
2. Verify materials appear correctly
3. Check that joints are smoother than body
4. Ensure cracks appear only on appropriate surfaces
5. Validate that different body parts have visual variety
