import bpy
import sys
import io

class OC_HT_enable(bpy.types.Header):
    bl_space_type = 'CONSOLE'
    
    def draw(self, context):
        layout = self.layout.row()
        layout.separator()
        layout.prop(context.scene, "output_console", text="", icon="ERROR")
        pass
    pass


def update_console_output(scene):    
    if bpy.context.scene.console_area:
        if bpy.context.scene.console_area in bpy.context.screen.areas.values():
            bpy.ops.console.scrollback_append.poll(scene)
            bpy.ops.console.scrollback_append(text="", type='OUTPUT')
            pass
        else:
            bpy.context.scene.console_area = None
    else:
        print("Esta tela nao tem um Console")
    pass


def output_console_update(self, context):
    scn = context.scene
    try: 
        if bpy.context.scene.output_console == True:
            for area in bpy.context.screen.areas:
                if area.type == "CONSOLE":
                    bpy.types.Scene.console_area = area
                    break
            bpy.app.handlers.scene_update_post.append(update_console_output)
        else:
            bpy.app.handlers.scene_update_post.remove(update_console_output)
    except:
        print("Exeption")
        pass
    #update_console_output(context)
    pass


def load_setting(scene):
    if bpy.context.scene.output_console:
        bpy.context.scene.output_console = True
    pass


classes = [
    OC_HT_enable
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        pass
    bpy.types.Scene.output_console = bpy.props.BoolProperty(default=False, update=output_console_update)
    bpy.types.Scene.console_area = None
    #bpy.types.CONSOLE_HT_header.append(draw_button)
    
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        pass
    del bpy.types.Scene.output_console
    del bpy.types.Scene.console_area
    pass


if __name__ == "__main__":
    register()