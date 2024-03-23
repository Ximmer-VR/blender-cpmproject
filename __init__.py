bl_info = {
    "name": "Minecraft CPMProject",
    "author": "Ximmer",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D",
    "description": "Minecraft CPMProject import/export",
    "warning": "",
    "tracker_url": "",
    "category": "Import-Export",
}

from . import io_scene_cpmproject

# reload imported modules
import importlib
importlib.reload(io_scene_cpmproject)

def register():
    io_scene_cpmproject.register()

def unregister():
    io_scene_cpmproject.unregister()