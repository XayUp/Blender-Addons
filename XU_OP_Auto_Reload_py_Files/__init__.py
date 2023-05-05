bl_info = {
    "name": "Auto Reload .py Files",
    "author": "XayUp",
    "category": "Python files"
}

import bpy

class XU_OP_Auto_Reload_py_Files(bpy.types.Header):
    bl_space_type = 'TEXT_EDITOR'

    def draw(self, context):
        layout =  self.layout
        layout.separator()
        layout = layout.row()
        layout.prop(context.scene, "XU_auto_reload_py_files_enabled", text='', icon='FILE_REFRESH')
        pass
    pass


def handler(scene):
    scene = bpy.context.scene
    if scene.XU_auto_reload_py_files_text_editor in bpy.context.screen.areas.values():
        if scene.XU_auto_reload_py_files_space.text != None:
            if scene.XU_auto_reload_py_files_space.text.is_modified:
                context = bpy.context.copy()
                context['area'] = scene.XU_auto_reload_py_files_text_editor
                context['region'] = scene.XU_auto_reload_py_files_text_editor.regions[-1]
                bpy.ops.text.resolve_conflict(context, resolution='RELOAD')
                pass
            pass
        else:
            bpy.context.scene.XU_auto_reload_py_files_enabled = False
        pass
    pass


def updater_switch(self, context):
    enabled = context.scene.XU_auto_reload_py_files_enabled
    if enabled:
        if have_text():
            try: bpy.app.handlers.scene_update_pre.append(handler)
            except: pass
        else:
            context.XU_auto_reload_py_files_enabled = False
    elif handler in  bpy.app.handlers.scene_update_pre:
        bpy.app.handlers.scene_update_pre.remove(handler)
    pass


def have_text() -> bool:
    for area in bpy.context.screen.areas:
        if area.type == 'TEXT_EDITOR':
            bpy.types.Scene.XU_auto_reload_py_files_text_editor = area
            for space in area.spaces:
                if space.rna_type.name == 'Space Text Editor':
                    bpy.types.Scene.XU_auto_reload_py_files_space = space
                    if space.text != None:
                        return True
    return False


classes = [
    XU_OP_Auto_Reload_py_Files
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.XU_auto_reload_py_files_enabled = bpy.props.BoolProperty(default=False, update=updater_switch)
    bpy.types.Scene.XU_auto_reload_py_files_text_editor = None
    bpy.types.Scene.XU_auto_reload_py_files_space = None
    pass


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.XU_auto_reload_py_files_space
    del bpy.types.Scene.XU_auto_reload_py_files_text_editor
    del bpy.types.Scene.XU_auto_reload_py_files_enabled
    
    pass


if __name__ == "__main__":
    register()
    pass