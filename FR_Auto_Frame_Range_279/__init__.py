
bl_info = {
    "name": "Frame Ranger Lite - Auto Fit Frame Range",
    "author": "BlenderBoi",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "description": "Automatically match the frame range to the action you are working on",
    "warning": "",
    "wiki_url": "",
    "category": "Utility",
}

import bpy
import addon_utils
from . import Autofit_Framerange

modules =  [Autofit_Framerange]

def register():
    for mod in addon_utils.modules():
        if mod.bl_info.get('name', (-1, -1, -1)) == "Frame Ranger" and mod.bl_info.get('author', (-1, -1, -1)) == "BlenderBoi":
            if addon_utils.check(mod.__name__)[1]:
                addon_utils.disable(mod.__name__, default_set=True, handle_error=None)


    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
