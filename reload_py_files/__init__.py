bl_info = {
    "name": "Reload .py files",
    "author": "XayUp and others",
    "version": (0, 0, 0),
    "blender": (2, 74, 0),
    "description": "Reload all .py files",
    "warning": "",
    "support": 'OFFICIAL',
    "category": "Python files",
}

import bpy

class ReloadAllPyFiles(bpy.types.Operator):

    bl_idname = "python.reload_all_py"
    bl_label = "Reload .py Files"
    bl_options = {'REGISTER', 'UNDO'}

    #def credits: 
    # https://blenderartists.org/forum/showthread.php209369-Synchronizing-text-with-changes-from-outside
    # https://blender.stackexchange.com/a/108443
    def execute(self, context):
        ctx = context.copy()
        #Ensure  context area is not None
        ctx['area'] = ctx['screen'].areas[0]
        for t in bpy.data.texts:
            if t.is_modified and not t.is_in_memory:
                print("  * Warning: Updating external script", t.name)
                # Change current context to contain a TEXT_EDITOR
                oldAreaType = ctx['area'].type
                ctx['area'].type = 'TEXT_EDITOR'
                ctx['edit_text'] = t
                bpy.ops.text.resolve_conflict(ctx, resolution='RELOAD')
                #Restore context
                ctx['area'].type = oldAreaType
        #Auto-Start Game Engine
        bpy.ops.view3d.game_start()   
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ReloadAllPyFiles)

def unregister():
    bpy.utils.unregister_class(ReloadAllPyFiles)

if __name__ == "__main__":
    register()
