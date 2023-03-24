import types
import bpy

from bpy.types import (Panel, Operator, PropertyGroup)

bl_info = {
    "name" : "Auto Animations",
    "author" : "XayUp",
    "description" : "2.7: Automatizar o armazenamento de ações na armadura ao importar.",
    "version" : (1, 0, 0),
    "location" : "",
    "blender" : (2, 79, 7),
    "warning" : "",
    "category" : "Armatures"
}

from .operadores.import_armature import (
    AA_IMPORTARM,
    AA_IMPORTACT,
    AA_SETTARGET,
    AA_ALLCURRENT,
    AA_CLEANLOOSE,
    AA_DELANINS
)
currentArm = "Nenhum"
class AA_MAIN_MENU(bpy.types.Panel):
    bl_idname = "xayup.aa_main_menu"
    bl_label = "Animação da armação"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):       
        layout = self.layout
        row = layout.row()    
        row.label(text="Current: " + currentArm)
        box = layout.box()
        box.label(text="Armature", icon='ARMATURE_DATA')
        box.operator("xayup.aa_importarm", icon="OUTLINER_OB_ARMATURE")        
        box.operator("xayup.aa_importact", icon="IMPORT")
        box.operator("xayup.aa_settarget", icon="MOD_ARMATURE")
        box.operator("xayup.aa_cleanloose", icon="POSE_DATA")
        box = layout.box()
        box.label(text="Actions", icon='ACTION')
        box.operator("xayup.aa_allcurrent", icon="ACTION_TWEAK")        
        box.operator("xayup.aa_delanins", icon="X")

cls = (
    AA_MAIN_MENU,
    AA_IMPORTARM,
    AA_IMPORTACT,
    AA_SETTARGET,
    AA_ALLCURRENT,
    AA_CLEANLOOSE,
    AA_DELANINS
)

def register():
    from bpy.utils import register_class
    for clss in cls:
        register_class(clss)

def unregister():
    from bpy.utils import unregister_class
    for clss in reversed(cls):
        unregister_class(clss)

if __name__ == "__main__":
    register()
