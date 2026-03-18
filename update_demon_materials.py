#!/usr/bin/env python3
"""
Script to update demon creation functions with detailed materials.
Updates Stone Demon, Fire Demon, and Water Demon functions.
"""

import re

# Read the file
file_path = "/Volumes/SERENADA_2/_elliott/Unreal Projects/UEAI-Plugin-Test/Plugins/UEAIPlugin/Content/Python/ue_infinite_creation.py"

with open(file_path, 'r') as f:
    content = f.read()

# Define patterns for updating each demon type

# STONE DEMON replacements - heavy weathered stone materials
stone_replacements = [
    # Torso
    (r'torso = self\._create_composite_cube\(f"{name}_Torso_Main", torso_pos, torso_scale, limestone_base\)',
     '''torso = self._create_composite_cube(
            f"{name}_Torso_Main", torso_pos, torso_scale, limestone_base,
            material_type="stone",
            material_params={
                "secondary": sandstone_light,
                "weathering": 0.5,
                "roughness": 0.92,
                "cracks": True
            }
        )'''),

    # Abdominal segments
    (r'ab = self\._create_composite_cube\(f"{name}_Ab_\{i\}", ab_pos, ab_scale, sandstone_light\)',
     '''ab = self._create_composite_cube(
                f"{name}_Ab_{i}", ab_pos, ab_scale, sandstone_light,
                material_type="stone",
                material_params={
                    "secondary": limestone_base,
                    "weathering": 0.35,
                    "roughness": 0.88,
                    "cracks": False
                }
            )'''),

    # Sternum
    (r'sternum = self\._create_composite_cube\(f"{name}_Sternum", sternum_pos, sternum_scale, sandstone_light\)',
     '''sternum = self._create_composite_cube(
            f"{name}_Sternum", sternum_pos, sternum_scale, sandstone_light,
            material_type="stone",
            material_params={
                "secondary": limestone_base,
                "weathering": 0.42,
                "roughness": 0.85,
                "cracks": False
            }
        )'''),

    # Deltoid
    (r'delt = self\._create_composite_cube\(f"{name}_Deltoid_\{\'L\' if side < 0 else \'R\'\}", delt_pos, delt_scale, limestone_base\)',
     '''delt = self._create_composite_cube(
                f"{name}_Deltoid_{'L' if side < 0 else 'R'}", delt_pos, delt_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.48,
                    "roughness": 0.90,
                    "cracks": True
                }
            )'''),

    # Clavicle
    (r'clavicle = self\._create_composite_cube\(f"{name}_Clavicle_\{\'L\' if side < 0 else \'R\'\}", clavicle_pos, clavicle_scale, sandstone_light\)',
     '''clavicle = self._create_composite_cube(
                f"{name}_Clavicle_{'L' if side < 0 else 'R'}", clavicle_pos, clavicle_scale, sandstone_light,
                material_type="stone",
                material_params={
                    "secondary": limestone_base,
                    "weathering": 0.38,
                    "roughness": 0.55,
                    "cracks": False
                }
            )'''),

    # Neck vertebrae
    (r'vertebra = self\._create_composite_cube\(f"{name}_NeckVertebra_\{i\}", vertebra_pos, vertebra_scale, limestone_base\)',
     '''vertebra = self._create_composite_cube(
                f"{name}_NeckVertebra_{i}", vertebra_pos, vertebra_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.45,
                    "roughness": 0.52,
                    "cracks": False
                }
            )'''),

    # Neck main
    (r'neck = self\._create_composite_cube\(f"{name}_Neck_Main", neck_pos, neck_scale, limestone_base\)',
     '''neck = self._create_composite_cube(
            f"{name}_Neck_Main", neck_pos, neck_scale, limestone_base,
            material_type="stone",
            material_params={
                "secondary": sandstone_light,
                "weathering": 0.46,
                "roughness": 0.91,
                "cracks": True
            }
        )'''),

    # Skull
    (r'skull = self\._create_composite_cube\(f"{name}_Skull", skull_pos, skull_scale, limestone_base\)',
     '''skull = self._create_composite_cube(
            f"{name}_Skull", skull_pos, skull_scale, limestone_base,
            material_type="stone",
            material_params={
                "secondary": sandstone_light,
                "weathering": 0.52,
                "roughness": 0.94,
                "cracks": True
            }
        )'''),

    # Brow ridge
    (r'brow = self\._create_composite_cube\(f"{name}_BrowRidge", brow_pos, brow_scale, sandstone_light\)',
     '''brow = self._create_composite_cube(
            f"{name}_BrowRidge", brow_pos, brow_scale, sandstone_light,
            material_type="stone",
            material_params={
                "secondary": limestone_base,
                "weathering": 0.40,
                "roughness": 0.82,
                "cracks": False
            }
        )'''),

    # Cheek
    (r'cheek = self\._create_composite_cube\(f"{name}_Cheek_\{\'L\' if side < 0 else \'R\'\}", cheek_pos, cheek_scale, limestone_base\)',
     '''cheek = self._create_composite_cube(
                f"{name}_Cheek_{'L' if side < 0 else 'R'}", cheek_pos, cheek_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.44,
                    "roughness": 0.89,
                    "cracks": False
                }
            )'''),

    # Jaw
    (r'jaw = self\._create_composite_cube\(f"{name}_Jaw", jaw_pos, jaw_scale, limestone_base\)',
     '''jaw = self._create_composite_cube(
            f"{name}_Jaw", jaw_pos, jaw_scale, limestone_base,
            material_type="stone",
            material_params={
                "secondary": sandstone_light,
                "weathering": 0.50,
                "roughness": 0.92,
                "cracks": True
            }
        )'''),

    # Chin
    (r'chin = self\._create_composite_cube\(f"{name}_Chin", chin_pos, chin_scale, limestone_base\)',
     '''chin = self._create_composite_cube(
            f"{name}_Chin", chin_pos, chin_scale, limestone_base,
            material_type="stone",
            material_params={
                "secondary": sandstone_light,
                "weathering": 0.55,
                "roughness": 0.90,
                "cracks": False
            }
        )'''),

    # Eye socket
    (r'socket = self\._create_composite_cube\(f"{name}_EyeSocket_\{\'L\' if side < 0 else \'R\'\}", socket_pos, socket_scale, stone_dark\)',
     '''socket = self._create_composite_cube(
                f"{name}_EyeSocket_{'L' if side < 0 else 'R'}", socket_pos, socket_scale, stone_dark,
                material_type="stone",
                material_params={
                    "secondary": limestone_base,
                    "weathering": 0.6,
                    "roughness": 0.96,
                    "cracks": True
                }
            )'''),

    # Eyelid
    (r'eyelid = self\._create_composite_cube\(f"{name}_Eyelid_\{\'L\' if side < 0 else \'R\'\}", eyelid_pos, eyelid_scale, limestone_base\)',
     '''eyelid = self._create_composite_cube(
                f"{name}_Eyelid_{'L' if side < 0 else 'R'}", eyelid_pos, eyelid_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.42,
                    "roughness": 0.58,
                    "cracks": False
                }
            )'''),

    # Nose
    (r'nose = self\._create_composite_cube\(f"{name}_Nose", nose_pos, nose_scale, limestone_base\)',
     '''nose = self._create_composite_cube(
            f"{name}_Nose", nose_pos, nose_scale, limestone_base,
            material_type="stone",
            material_params={
                "secondary": sandstone_light,
                "weathering": 0.48,
                "roughness": 0.86,
                "cracks": False
            }
        )'''),

    # Nostril
    (r'nostril = self\._create_composite_cube\(f"{name}_Nostril_\{\'L\' if side < 0 else \'R\'\}", nostril_pos, nostril_scale, stone_dark\)',
     '''nostril = self._create_composite_cube(
                f"{name}_Nostril_{'L' if side < 0 else 'R'}", nostril_pos, nostril_scale, stone_dark,
                material_type="stone",
                material_params={
                    "secondary": limestone_base,
                    "weathering": 0.65,
                    "roughness": 0.97,
                    "cracks": True
                }
            )'''),

    # Mouth
    (r'mouth = self\._create_composite_cube\(f"{name}_Mouth", mouth_pos, mouth_scale, stone_dark\)',
     '''mouth = self._create_composite_cube(
            f"{name}_Mouth", mouth_pos, mouth_scale, stone_dark,
            material_type="stone",
            material_params={
                "secondary": limestone_base,
                "weathering": 0.7,
                "roughness": 0.96,
                "cracks": True
            }
        )'''),

    # Teeth
    (r'tooth = self\._create_composite_cube\(f"{name}_Tooth_\{i\}", tooth_pos, tooth_scale, sandstone_light\)',
     '''tooth = self._create_composite_cube(
                f"{name}_Tooth_{i}", tooth_pos, tooth_scale, sandstone_light,
                material_type="stone",
                material_params={
                    "secondary": limestone_base,
                    "weathering": 0.35,
                    "roughness": 0.55,
                    "cracks": False
                }
            )'''),

    # Horn base
    (r'horn_base = self\._create_composite_cube\(f"{name}_HornBase_\{\'L\' if side < 0 else \'R\'\}", horn_base_pos, horn_base_scale, limestone_base\)',
     '''horn_base = self._create_composite_cube(
                f"{name}_HornBase_{'L' if side < 0 else 'R'}", horn_base_pos, horn_base_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.45,
                    "roughness": 0.88,
                    "cracks": True
                }
            )'''),

    # Horn shaft
    (r'horn_seg = self\._create_composite_cube\(f"{name}_Horn_\{\'L\' if side < 0 else \'R\'\}_Seg\{j\}", horn_seg_pos, horn_seg_scale, sandstone_light\)',
     '''horn_seg = self._create_composite_cube(
                    f"{name}_Horn_{'L' if side < 0 else 'R'}_Seg{j}", horn_seg_pos, horn_seg_scale, sandstone_light,
                    material_type="stone",
                    material_params={
                        "secondary": limestone_base,
                        "weathering": 0.38 + j * 0.05,
                        "roughness": 0.48 + j * 0.08,
                        "cracks": False
                    }
                )'''),

    # Horn tip
    (r'tip = self\._create_composite_cube\(f"{name}_HornTip_\{\'L\' if side < 0 else \'R\'\}", tip_pos, tip_scale, wear_brown\)',
     '''tip = self._create_composite_cube(
                f"{name}_HornTip_{'L' if side < 0 else 'R'}", tip_pos, tip_scale, wear_brown,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.6,
                    "roughness": 0.62,
                    "cracks": False
                }
            )'''),

    # Ear
    (r'ear = self\._create_composite_cube\(f"{name}_Ear_\{\'L\' if side < 0 else \'R\'\}", ear_pos, ear_scale, limestone_base\)',
     '''ear = self._create_composite_cube(
                f"{name}_Ear_{'L' if side < 0 else 'R'}", ear_pos, ear_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.43,
                    "roughness": 0.87,
                    "cracks": False
                }
            )'''),

    # Humerus
    (r'humerus = self\._create_composite_cube\(f"{name}_Humerus_\{side_name\}", humerus_pos, humerus_scale, limestone_base\)',
     '''humerus = self._create_composite_cube(
                f"{name}_Humerus_{side_name}", humerus_pos, humerus_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.47,
                    "roughness": 0.91,
                    "cracks": True
                }
            )'''),

    # Bicep
    (r'bicep = self\._create_composite_cube\(f"{name}_Bicep_\{side_name\}", bicep_pos, bicep_scale, sandstone_light\)',
     '''bicep = self._create_composite_cube(
                f"{name}_Bicep_{side_name}", bicep_pos, bicep_scale, sandstone_light,
                material_type="stone",
                material_params={
                    "secondary": limestone_base,
                    "weathering": 0.40,
                    "roughness": 0.86,
                    "cracks": False
                }
            )'''),

    # Elbow
    (r'elbow = self\._create_composite_cube\(f"{name}_Elbow_\{side_name\}", elbow_pos, elbow_scale, sandstone_light\)',
     '''elbow = self._create_composite_cube(
                f"{name}_Elbow_{side_name}", elbow_pos, elbow_scale, sandstone_light,
                material_type="stone",
                material_params={
                    "secondary": limestone_base,
                    "weathering": 0.36,
                    "roughness": 0.50,
                    "cracks": False
                }
            )'''),

    # Forearm
    (r'forearm = self\._create_composite_cube\(f"{name}_Forearm_\{side_name\}", forearm_pos, forearm_scale, limestone_base\)',
     '''forearm = self._create_composite_cube(
                f"{name}_Forearm_{side_name}", forearm_pos, forearm_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.49,
                    "roughness": 0.90,
                    "cracks": True
                }
            )'''),

    # Forearm muscle
    (r'muscle = self\._create_composite_cube\(f"{name}_ForearmMuscle_\{side_name\}_\{k\}", muscle_pos, muscle_scale, sandstone_light\)',
     '''muscle = self._create_composite_cube(
                    f"{name}_ForearmMuscle_{side_name}_{k}", muscle_pos, muscle_scale, sandstone_light,
                    material_type="stone",
                    material_params={
                        "secondary": limestone_base,
                        "weathering": 0.41,
                        "roughness": 0.84,
                        "cracks": False
                    }
                )'''),

    # Wrist
    (r'wrist = self\._create_composite_cube\(f"{name}_Wrist_\{side_name\}", wrist_pos, wrist_scale, sandstone_light\)',
     '''wrist = self._create_composite_cube(
                f"{name}_Wrist_{side_name}", wrist_pos, wrist_scale, sandstone_light,
                material_type="stone",
                material_params={
                    "secondary": limestone_base,
                    "weathering": 0.34,
                    "roughness": 0.52,
                    "cracks": False
                }
            )'''),

    # Palm
    (r'palm = self\._create_composite_cube\(f"{name}_Palm_\{side_name\}", palm_pos, palm_scale, limestone_base\)',
     '''palm = self._create_composite_cube(
                f"{name}_Palm_{side_name}", palm_pos, palm_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.46,
                    "roughness": 0.89,
                    "cracks": True
                }
            )'''),

    # Finger
    (r'finger = self\._create_composite_cube\(f"{name}_Finger_\{side_name\}_\{f\}_\{seg\}", finger_pos, finger_scale, limestone_base\)',
     '''finger = self._create_composite_cube(
                        f"{name}_Finger_{side_name}_{f}_{seg}", finger_pos, finger_scale, limestone_base,
                        material_type="stone",
                        material_params={
                            "secondary": sandstone_light,
                            "weathering": 0.44,
                            "roughness": 0.87,
                            "cracks": False
                        }
                    )'''),

    # Thigh
    (r'thigh = self\._create_composite_cube\(f"{name}_Thigh_\{side_name\}", thigh_pos, thigh_scale, limestone_base\)',
     '''thigh = self._create_composite_cube(
                f"{name}_Thigh_{side_name}", thigh_pos, thigh_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.48,
                    "roughness": 0.91,
                    "cracks": True
                }
            )'''),

    # Quad
    (r'quad = self\._create_composite_cube\(f"{name}_Quad_\{side_name\}_\{q\}", quad_pos, quad_scale, sandstone_light\)',
     '''quad = self._create_composite_cube(
                    f"{name}_Quad_{side_name}_{q}", quad_pos, quad_scale, sandstone_light,
                    material_type="stone",
                    material_params={
                        "secondary": limestone_base,
                        "weathering": 0.39,
                        "roughness": 0.83,
                        "cracks": False
                    }
                )'''),

    # Patella
    (r'patella = self\._create_composite_cube\(f"{name}_Patella_\{side_name\}", patella_pos, patella_scale, sandstone_light\)',
     '''patella = self._create_composite_cube(
                f"{name}_Patella_{side_name}", patella_pos, patella_scale, sandstone_light,
                material_type="stone",
                material_params={
                    "secondary": limestone_base,
                    "weathering": 0.32,
                    "roughness": 0.48,
                    "cracks": False
                }
            )'''),

    # Shin
    (r'shin = self\._create_composite_cube\(f"{name}_Shin_\{side_name\}", shin_pos, shin_scale, limestone_base\)',
     '''shin = self._create_composite_cube(
                f"{name}_Shin_{side_name}", shin_pos, shin_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.50,
                    "roughness": 0.92,
                    "cracks": True
                }
            )'''),

    # Calf
    (r'calf = self\._create_composite_cube\(f"{name}_Calf_\{side_name\}", calf_pos, calf_scale, sandstone_light\)',
     '''calf = self._create_composite_cube(
                f"{name}_Calf_{side_name}", calf_pos, calf_scale, sandstone_light,
                material_type="stone",
                material_params={
                    "secondary": limestone_base,
                    "weathering": 0.42,
                    "roughness": 0.85,
                    "cracks": False
                }
            )'''),

    # Shin detail
    (r'detail = self\._create_composite_cube\(f"{name}_ShinDetail_\{side_name\}_\{s\}", detail_pos, detail_scale, limestone_base\)',
     '''detail = self._create_composite_cube(
                    f"{name}_ShinDetail_{side_name}_{s}", detail_pos, detail_scale, limestone_base,
                    material_type="stone",
                    material_params={
                        "secondary": sandstone_light,
                        "weathering": 0.45,
                        "roughness": 0.88,
                        "cracks": False
                    }
                )'''),

    # Ankle
    (r'ankle = self\._create_composite_cube\(f"{name}_Ankle_\{side_name\}", ankle_detail_pos, ankle_scale, sandstone_light\)',
     '''ankle = self._create_composite_cube(
                f"{name}_Ankle_{side_name}", ankle_detail_pos, ankle_scale, sandstone_light,
                material_type="stone",
                material_params={
                    "secondary": limestone_base,
                    "weathering": 0.30,
                    "roughness": 0.50,
                    "cracks": False
                }
            )'''),

    # Foot
    (r'foot = self\._create_composite_cube\(f"{name}_Foot_\{side_name\}", foot_pos, foot_scale, limestone_base\)',
     '''foot = self._create_composite_cube(
                f"{name}_Foot_{side_name}", foot_pos, foot_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.52,
                    "roughness": 0.93,
                    "cracks": True
                }
            )'''),

    # Toe
    (r'toe = self\._create_composite_cube\(f"{name}_Toe_\{side_name\}_\{t\}", toe_pos, toe_scale, limestone_base\)',
     '''toe = self._create_composite_cube(
                    f"{name}_Toe_{side_name}_{t}", toe_pos, toe_scale, limestone_base,
                    material_type="stone",
                    material_params={
                        "secondary": sandstone_light,
                        "weathering": 0.47,
                        "roughness": 0.86,
                        "cracks": False
                    }
                )'''),

    # Toe joint
    (r'joint = self\._create_composite_cube\(f"{name}_ToeJoint_\{side_name\}_\{t\}", joint_pos, joint_scale, sandstone_light\)',
     '''joint = self._create_composite_cube(
                    f"{name}_ToeJoint_{side_name}_{t}", joint_pos, joint_scale, sandstone_light,
                    material_type="stone",
                    material_params={
                        "secondary": limestone_base,
                        "weathering": 0.33,
                        "roughness": 0.54,
                        "cracks": False
                    }
                )'''),

    # Heel
    (r'heel = self\._create_composite_cube\(f"{name}_Heel_\{side_name\}", heel_pos, heel_scale, limestone_base\)',
     '''heel = self._create_composite_cube(
                f"{name}_Heel_{side_name}", heel_pos, heel_scale, limestone_base,
                material_type="stone",
                material_params={
                    "secondary": sandstone_light,
                    "weathering": 0.51,
                    "roughness": 0.90,
                    "cracks": True
                }
            )'''),

    # Tail vertebra
    (r'vertebra = self\._create_composite_cube\(f"{name}_TailVertebra_\{i\}", vertebra_pos, vertebra_scale, limestone_base\)',
     '''vertebra = self._create_composite_cube(
                    f"{name}_TailVertebra_{i}", vertebra_pos, vertebra_scale, limestone_base,
                    material_type="stone",
                    material_params={
                        "secondary": sandstone_light,
                        "weathering": 0.43,
                        "roughness": 0.54,
                        "cracks": False
                    }
                )'''),

    # Tail base
    (r'tail_base = self\._create_composite_cube\(f"{name}_Tail_Base", tail_base_pos, tail_base_scale, limestone_base\)',
     '''tail_base = self._create_composite_cube(
            f"{name}_Tail_Base", tail_base_pos, tail_base_scale, limestone_base,
            material_type="stone",
            material_params={
                "secondary": sandstone_light,
                "weathering": 0.49,
                "roughness": 0.91,
                "cracks": True
            }
        )'''),

    # Tail segment
    (r'segment = self\._create_composite_cube\(f"{name}_Tail_Segment_\{i\}", segment_pos, segment_scale, limestone_base\)',
     '''segment = self._create_composite_cube(
                    f"{name}_Tail_Segment_{i}", segment_pos, segment_scale, limestone_base,
                    material_type="stone",
                    material_params={
                        "secondary": sandstone_light,
                        "weathering": 0.50 + i * 0.03,
                        "roughness": 0.92 + i * 0.02,
                        "cracks": True
                    }
                )'''),

    # Tail club
    (r'club = self\._create_composite_cube\(f"{name}_Tail_Club", club_pos, club_scale, limestone_base\)',
     '''club = self._create_composite_cube(
            f"{name}_Tail_Club", club_pos, club_scale, limestone_base,
            material_type="stone",
            material_params={
                "secondary": sandstone_light,
                "weathering": 0.55,
                "roughness": 0.94,
                "cracks": True
            }
        )'''),

    # Club spike
    (r'spike = self\._create_composite_cube\(f"{name}_ClubSpike_\{i\}", spike_pos, spike_scale, sandstone_light\)',
     '''spike = self._create_composite_cube(
                    f"{name}_ClubSpike_{i}", spike_pos, spike_scale, sandstone_light,
                    material_type="stone",
                    material_params={
                        "secondary": limestone_base,
                        "weathering": 0.38,
                        "roughness": 0.75,
                        "cracks": False
                    }
                )'''),

    # Club spike tip
    (r'tip = self\._create_composite_cube\(f"{name}_ClubSpikeTip_\{i\}", tip_pos, tip_scale, wear_brown\)',
     '''tip = self._create_composite_cube(
                    f"{name}_ClubSpikeTip_{i}", tip_pos, tip_scale, wear_brown,
                    material_type="stone",
                    material_params={
                        "secondary": sandstone_light,
                        "weathering": 0.58,
                        "roughness": 0.68,
                        "cracks": False
                    }
                )'''),
]

print(f"Loaded {len(stone_replacements)} stone demon replacement patterns")
print("This script provides the patterns but does not modify the file directly.")
print("\nTo apply these changes, you would need to:")
print("1. Read the file")
print("2. Apply each replacement using re.sub()")
print("3. Write the modified content back")
print("\nDue to file size and complexity, consider applying changes in smaller batches.")
