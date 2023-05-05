bl_info = {
    "Name", "Blender Data Manager",
    "Author", "XayUp",
    "About", "Easy manager all data inside on this blend file",
    "category", "Utils"
}

import bpy

class XU_DRAW_Window(bpy.types.Operator):
    bl_label = 'Blender Data Manager'
    bl_idname = "xu_bdm.draw_window"

    def execute(self, context):
        return {'FINISHED'}
       
    def draw(self, context):
        layout = self.layout
        window = context.space_data
        layout = layout.row()
        
        pass

    def invoke(self, context, event):
        return bpy.types.WindowManager.invoke_popup(self)
        pass

def open_window_item_menu(self, context):
    self.layout.operator(XU_DRAW_Window.bl_idname, icon='PACKAGE')
    pass


classes = [
    XU_DRAW_Window
]

def register():
    for cls in classes: bpy.utils.register_class(cls)
    bpy.types.INFO_MT_file.append(open_window_item_menu)
    pass

def unregister():
    for cls in classes: bpy.utils.unregister_class(cls)
    bpy.types.INFO_MT_file.remove(open_window_item_menu)
    pass

if __name__ == "__main__":
    register()