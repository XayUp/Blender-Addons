import bpy

from bpy.app.handlers import persistent
#from . import Utility_Function



if bpy.app.version >= (2, 80, 0):
    update_post = bpy.app.handlers.depsgraph_update_post
else:
    update_post = bpy.app.handlers.scene_update_post

@persistent
def load_setting(scene):
    if bpy.context.scene.FR_TU_Autofit_Keyframe:
        bpy.context.scene.FR_TU_Autofit_Keyframe = True


@persistent
def handler_fit_keyframe(scene):
    scn = bpy.context.scene
    
    ranges_start = []
    ranges_end = []
    
    if scn.FR_TU_Auto_Frame_Range_Settings.Mode == "ACTION":
        if scn.FR_TU_Auto_Frame_Range_Settings.Selected:
            objects = bpy.context.selected_objects
        else:
            objects = scn.objects
        
        if scn.FR_TU_Auto_Frame_Range_Settings.Action_Mode == "KEYFRAME":
            for object in objects:
                if object.animation_data and object.animation_data.action:
                    ranges_start.append(object.animation_data.action.frame_range[0])
                    ranges_end.append(object.animation_data.action.frame_range[1])
                
        elif scn.FR_TU_Auto_Frame_Range_Settings.Action_Mode == "ACTION":
            for object in objects:
                LAM = object.LAM
                if len(LAM) > 0:
                    Active_Slot = LAM[object.LAM_Index]
                    if Active_Slot.Action:
                        if Active_Slot.Range_Mode == "ACTION":
                            ranges_start.append(Active_Slot.Start)
                            ranges_end.append(Active_Slot.End)
                        elif Active_Slot.Range_Mode == "KEYFRAME":
                            ranges_start.append(Active_Slot.Action.frame_range[0])
                            ranges_end.append(Active_Slot.Action.frame_range[1])

        update_frame_range(scn, ranges_start, ranges_end)

    elif scn.FR_TU_Auto_Frame_Range_Settings.Mode == "NLA":   
        objects = scn.objects
        
        for object in objects:
            if object.animation_data and object.animation_data.nla_tracks:
                for track in object.animation_data.nla_tracks:
                    if track.strips:
                        for strip in track.strips:
                            if scn.FR_TU_Auto_Frame_Range_Settings.Selected:
                                if strip.select:
                                    ranges_start.append(strip.frame_start)
                                    ranges_end.append(strip.frame_end+1)
                            else:
                                ranges_start.append(strip.frame_start)
                                ranges_end.append(strip.frame_end+1)
        
        update_frame_range(scn, ranges_start, ranges_end, [0, -1])

    elif scn.FR_TU_Auto_Frame_Range_Settings.Mode == "SEQUENCE" and bpy.context.sequences != None:
        for sequence in bpy.context.sequences:
            if scn.FR_TU_Auto_Frame_Range_Settings.Selected:
                if sequence.select:
                    list_start.append(sequence.frame_final_start)
                    list_end.append(sequence.frame_final_end)
            else:
                list_start.append(sequence.frame_final_start)
                list_end.append(sequence.frame_final_end)

        update_frame_range(scn, ranges_start, ranges_end, [0, -1])
        
                
def update_frame_range(scene, ranges_start, ranges_end, increment = [0, 0]):
    if len(ranges_start)> 0:
        if scene.use_preview_range:
            scene.frame_preview_start = int(min(ranges_start) + increment[0])
        else:
            scene.frame_start         = int(min(ranges_start) + increment[0])
    if len(ranges_end)  > 0:
        if scene.use_preview_range:
            scene.frame_preview_end   = int(max(ranges_end) + increment[1])
        else:
            scene.frame_end           = int(max(ranges_end) + increment[1])
    pass


def autofit_keyframe(self, context):
    scn = context.scene

    if context.area.rna_type == "SEQUENCE_EDITOR":
        scn.FR_TU_Auto_Frame_Range_Settings.Mode = "SEQUENCE"
    elif context.area.rna_type == "NLA_EDITOR":
        scn.FR_TU_Auto_Frame_Range_Settings.Mode = "NLA"

    try:
        if context.scene.FR_TU_Autofit_Keyframe == False:
            update_post.remove(handler_fit_keyframe)
        else:
            update_post.append(handler_fit_keyframe)
    except:
        pass

    handler_fit_keyframe(context)


def draw_item_keyframe(self, context):
    layout = self.layout
    layout.separator()
    layout = layout.row(True)
    layout.prop(context.scene, "FR_TU_Autofit_Keyframe", text="", icon="TIME")
 
    if bpy.app.version < (2, 80, 0):
        if context.area.type == "DOPESHEET_EDITOR":
            layout = layout.row(True)
            layout.operator("fr_pt_tu.auto_frame_range", text="", icon="TRIA_DOWN")
            layout.enabled = context.scene.FR_TU_Autofit_Keyframe
    else:
        layout.popover(
            panel="FR_PT_TU_auto_frame_range",
            text="",
        )


class FR_PT_TU_Auto_Frame_Range_op(bpy.types.Operator):
                # < 2.80 #
    bl_idname = "fr_pt_tu.auto_frame_range"
    bl_label = "Auto Frame Range"
    
    def execute(self, context):
        return {'FINISHED'}
        pass
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.label(self.bl_label, icon="ACTION")
        layout.prop(scn.FR_TU_Auto_Frame_Range_Settings, "Mode", text="Mode", expand=True)
        if scn.FR_TU_Auto_Frame_Range_Settings.Mode == "ACTION":
            layout.prop(scn.FR_TU_Auto_Frame_Range_Settings, "Action_Mode", text="Only Selected", expand=True)
        layout.prop(scn.FR_TU_Auto_Frame_Range_Settings, "Selected", text="Only Selected")
        
    def invoke(self, context, event):
        return bpy.context.window_manager.invoke_popup(self)
        pass        
    
    
class FR_PT_TU_Auto_Frame_Range(bpy.types.Panel):
    bl_label = "Auto Frame Range"
    bl_idname = "FR_PT_TU_auto_frame_range"
    bl_options = {'HIDE_HEADER'}
    bl_region_type = 'HEADER'
    bl_space_type = 'DOPESHEET_EDITOR'

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn.FR_TU_Auto_Frame_Range_Settings, "Mode", text="Mode", expand=True)
        if scn.FR_TU_Auto_Frame_Range_Settings.Mode == "ACTION":
            layout.prop(scn.FR_TU_Auto_Frame_Range_Settings, "Action_Mode", text="Only Selected", expand=True)
        layout.prop(scn.FR_TU_Auto_Frame_Range_Settings, "Selected", text="Only Selected")
        

#Mode = [("ACTION","Action","Action"),("NLA","NLA","NLA Strips"),("SEQUENCE","Sequence","Sequencer Strips")]
#Action_Mode = [("KEYFRAME","Keyframe","Keyframe"),("ACTION","Action","Action")]
class FR_TU_Auto_Frame_Range_Settings(bpy.types.PropertyGroup):
    Mode : bpy.props.EnumProperty(items=[("ACTION","Action","Action"),("NLA","NLA","NLA Strips"),("SEQUENCE","Sequence","Sequencer Strips")])
    Action_Mode : bpy.props.EnumProperty(items=[("KEYFRAME","Keyframe","Keyframe"),("ACTION","Action","Action")], default="KEYFRAME")
    Selected: bpy.props.BoolProperty(default=False)
    
    
classes = [
    FR_TU_Auto_Frame_Range_Settings
]
classes_280 = [
    FR_PT_TU_Auto_Frame_Range
]
classes_279 = [
    FR_PT_TU_Auto_Frame_Range_op
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    if bpy.app.version < (2, 80, 0):
        for cls in classes_279:
            bpy.utils.register_class(cls)
    else:
        for cls in classes_280:
            bpy.utils.register_class(cls)

    bpy.types.Scene.FR_TU_Autofit_Keyframe = bpy.props.BoolProperty(default=False, update=autofit_keyframe)
    bpy.types.Scene.FR_TU_Auto_Frame_Range_Settings = bpy.props.PointerProperty(type=FR_TU_Auto_Frame_Range_Settings)

    bpy.types.TIME_HT_header.append(draw_item_keyframe)
    bpy.types.DOPESHEET_HT_header.append(draw_item_keyframe)
    bpy.types.GRAPH_HT_header.append(draw_item_keyframe)
    bpy.types.NLA_HT_header.append(draw_item_keyframe)
    bpy.types.SEQUENCER_HT_header.append(draw_item_keyframe)

    bpy.app.handlers.load_post.append(load_setting)


def unregister():
    if handler_fit_keyframe in update_post :
        update_post.remove(handler_fit_keyframe)
    
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    if bpy.app.version < (2, 80, 0):
        for cls in classes_279:
            bpy.utils.unregister_class(cls)
    else:
        for cls in classes_280:
            bpy.utils.unregister_class(cls)

    bpy.app.handlers.load_post.remove(load_setting)
    bpy.types.TIME_HT_header.remove(draw_item_keyframe)
    bpy.types.DOPESHEET_HT_header.remove(draw_item_keyframe)
    bpy.types.GRAPH_HT_header.remove(draw_item_keyframe)
    bpy.types.NLA_HT_header.remove(draw_item_keyframe)
    bpy.types.SEQUENCER_HT_header.remove(draw_item_keyframe)

    del bpy.types.Scene.FR_TU_Autofit_Keyframe
    del bpy.types.Scene.FR_TU_Auto_Frame_Range_Settings


if __name__ == "__main__":
    register()