# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty
from bpy.types import Operator

from . import import_cpmproject
from . import export_cpmproject

import importlib
importlib.reload(import_cpmproject)
importlib.reload(export_cpmproject)

class ImportCPMProject(Operator, ImportHelper):
    """Import Minecraft .cpmproject file"""
    bl_idname = "minecraft.import_cpmproject"
    bl_label = "Import a Minecraft .cpmproject model"
    bl_options = {"REGISTER", "UNDO"}

    # ImportHelper mixin class uses this
    filename_ext = ".cpmproject"

    filter_glob: StringProperty(
        default="*.cpmproject",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    import_uvs: BoolProperty(
        name="Import UVs",
        description="Import UVs",
        default=True,
    )

    recenter_to_origin: BoolProperty(
        name="Recenter to Origin",
        description="Recenter model median to origin",
        default=True,
    )

    def execute(self, context):
        args = self.as_keywords()
        return import_cpmproject.load(context, **args)

class ExportCPMProject(Operator, ExportHelper):
    """Export Minecraft .cpmproject file"""
    bl_idname = "minecraft.export_cpmproject"
    bl_label = "Export a Minecraft .cpmproject model"
    bl_options = {"REGISTER", "UNDO"}

    # ImportHelper mixin class uses this
    filename_ext = ".cpmproject"

    filter_glob: StringProperty(
        default="*.cpmproject",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    import_uvs: BoolProperty(
        name="Import UVs",
        description="Import UVs",
        default=True,
    )

    recenter_to_origin: BoolProperty(
        name="Recenter to Origin",
        description="Recenter model median to origin",
        default=True,
    )

    def execute(self, context):
        args = self.as_keywords()
        return export_cpmproject.load(context, **args)

# add io to menu
def menu_func_import(self, context):
    self.layout.operator(ImportCPMProject.bl_idname, text="Minecraft (.cpmproject)")

def menu_func_export(self, context):
    self.layout.operator(ExportCPMProject.bl_idname, text="Minecraft (.cpmproject)")


classes = [
    ImportCPMProject,
    ExportCPMProject,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()