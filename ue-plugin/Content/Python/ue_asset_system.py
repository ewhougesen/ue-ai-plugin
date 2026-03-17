"""
UE AI Plugin - Simple Asset Management
Robust asset creation for Mac/UE
"""

import unreal
import http.client
import json
import urllib.request
import os
import tempfile


class AssetManager:
    """Simple asset management"""

    def __init__(self):
        self.temp_dir = tempfile.gettempdir()

    def download_file(self, url: str, local_path: str) -> bool:
        """Download file from URL"""
        try:
            unreal.log(f"Downloading: {url}")
            urllib.request.urlretrieve(url, local_path)
            unreal.log("Download complete")
            return True
        except Exception as e:
            unreal.log_error(f"Download failed: {e}")
            return False

    def import_fbx_model(self, fbx_path: str, asset_name: str) -> str:
        """Import FBX model"""
        try:
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

            import_task = unreal.AssetImportTask()
            import_task.set_editor_property('filename', fbx_path)
            import_task.set_editor_property('destination_path', '/Game/GeneratedModels')
            import_task.set_editor_property('automated', True)

            asset_tools.import_asset_task([import_task])

            asset_path = f"/Game/GeneratedModels/{asset_name}"
            unreal.log(f"Imported: {asset_path}")
            return asset_path

        except Exception as e:
            unreal.log_error(f"Import failed: {e}")
            return None

    def import_texture(self, texture_path: str, asset_name: str) -> str:
        """Import texture"""
        try:
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

            import_task = unreal.AssetImportTask()
            import_task.set_editor_property('filename', texture_path)
            import_task.set_editor_property('destination_path', '/Game/GeneratedTextures')
            import_task.set_editor_property('automated', True)

            asset_tools.import_asset_task([import_task])

            asset_path = f"/Game/GeneratedTextures/{asset_name}"
            unreal.log(f"Imported: {asset_path}")
            return asset_path

        except Exception as e:
            unreal.log_error(f"Import failed: {e}")
            return None

    def create_material_instance(self, material_name: str, base_color=None, roughness=0.5, metallic=0.0) -> str:
        """Create material"""
        try:
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

            material = asset_tools.create_asset(
                material_name,
                "/Game/GeneratedMaterials",
                unreal.Material,
                unreal.MaterialFactoryNew()
            )

            # Simple color setup
            if base_color and isinstance(base_color, tuple):
                mat_editing = unreal.MaterialEditingLibrary

                color_const = mat_editing.create_material_expression(
                    material,
                    unreal.MaterialExpressionConstant3Vector
                )
                color_const.set_editor_property(
                    "constant",
                    unreal.LinearColor(base_color[0], base_color[1], base_color[2], 1.0)
                )
                mat_editing.connect_material_property(
                    color_const, "Output", material, unreal.MaterialProperty.MP_BASE_COLOR
                )

                roughness_const = mat_editing.create_material_expression(
                    material, unreal.MaterialExpressionConstant
                )
                roughness_const.set_editor_property("r", roughness)
                mat_editing.connect_material_property(
                    roughness_const, "Output", material, unreal.MaterialProperty.MP_ROUGHNESS
                )

                metallic_const = mat_editing.create_material_expression(
                    material, unreal.MaterialExpressionConstant
                )
                metallic_const.set_editor_property("r", metallic)
                mat_editing.connect_material_property(
                    metallic_const, "Output", material, unreal.MaterialProperty.MP_METALLIC
                )

            unreal.log(f"Created material: {material_name}")
            return f"/Game/GeneratedMaterials/{material_name}"

        except Exception as e:
            unreal.log_error(f"Material creation failed: {e}")
            return None

    def spawn_actor_with_mesh(self, mesh_path: str, actor_name: str, location=(0, 0, 0)):
        """Spawn actor with mesh"""
        try:
            mesh_asset = unreal.load_asset(mesh_path, unreal.StaticMesh)
            if not mesh_asset:
                unreal.log_error(f"Could not load: {mesh_path}")
                return None

            loc = unreal.Vector(location[0], location[1], location[2])
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)

            mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
            mesh_component.set_static_mesh(mesh_asset)
            actor.set_actor_label(actor_name)

            unreal.log(f"Spawned: {actor_name}")
            return actor

        except Exception as e:
            unreal.log_error(f"Spawn failed: {e}")
            return None


# Global instance
asset_manager = AssetManager()
