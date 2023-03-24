import bpy
import os
import AA

from bpy.props import (StringProperty)
from bpy.types import (Operator, Panel)
from bpy_extras.io_utils import ImportHelper

currentArm = ""   

class AA_IMPORTARM(bpy.types.Operator, ImportHelper):
    bl_idname = "xayup.aa_importarm"
    bl_label = "Import armature"
    bl_description = "Importar uma Armadura"
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext = ".fbx"
    filter_glob = StringProperty(default="*.fbx", options={'HIDDEN'})
    supported_extensions = ['fbx']
    def importfbx(self, context, filedir):
        global currentArm
        filedir = self.filepath
        bpy.ops.import_scene.fbx(filepath = filedir)
        currentArm = bpy.context.object
        if currentArm.animation_data is None:
            currentArm.animation_data_create()                
        for action in bpy.data.actions:
            if action.tag == False:
                track = currentArm.animation_data.nla_tracks.new()
                track.name = action.name      
                track.strips.new(action.name, action.frame_range[0], action)
                currentArm.animation_data.action = action
    def blendtag(self, context):
        for anins in bpy.data.actions:
            anins.tag = 1
    def execute(self, context):
        global currentArm
        self.blendtag(context)        
        self.importfbx(context, self.filepath)        
        if currentArm.animation_data.action.name.__contains__('Armature|mixamo.com|Layer0'):
            currentArm.animation_data.action.name = 'T-Pose'
        bpy.context.scene.objects.active = currentArm
        if bpy.context.object.type == 'ARMATURE':
            currentArm = bpy.context.object
            self.report({'INFO'}, 'Amadura importada com sucesso!')
            AA.currentArm = currentArm.name
        else:                
            self.report({'ERROR'}, 'Armadura inválida!')
            bpy.ops.object.delete()
            return {'CANCELLED'}
        return {'FINISHED'}

class AA_SETTARGET(bpy.types.Operator):
    bl_idname = "xayup.aa_settarget"
    bl_label = "Set as default"
    bl_description = "Selecione a armadura e clique para tornala padrão (para trabalho)."
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        global currentArm
        if bpy.context.object.type == 'ARMATURE':
            currentArm = bpy.context.object
            if len(currentArm.animation_data.nla_tracks) > 0:
                for anins in bpy.data.actions:
                    anins.tag = 1
            self.report({'INFO'}, 'Armadura definida como padrão com sucesso!')
            AA.currentArm = currentArm.name
        else:
            self.report({'ERROR'}, 'Objeto selecionado não é uma armadura')
            return {'CANCELLED'}
        return {'FINISHED'}

class AA_IMPORTACT(bpy.types.Operator, ImportHelper):
    bl_idname = "xayup.aa_importact"
    bl_label = "Import actions"
    bl_description = "Importar uma animação para a armadura atual e armazenar no mesmo."
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext = ".fbx"
    filter_glob = StringProperty(default="*.fbx", options={'HIDDEN'})
    supported_extensions = ['fbx']        
    def importfbx(self, context, filedir):        
        filedir = self.filepath
        bpy.ops.import_scene.fbx(filepath = filedir)
        filewex = os.path.split(filedir)[1]
        obj = bpy.context.object
        if len(obj.animation_data.nla_tracks) > 0:
            for track in bpy.context.object.animation_data.nla_tracks:
                track.name = os.path.splitext(filewex)[0]
        else:
            obj.animation_data.action.name = os.path.splitext(filewex)[0]
        bpy.ops.object.delete()
        return {'FINISHED'}

    def execute(self, context):
        global currentArm
        if currentArm != "":
            self.importfbx(context, self.filepath)
            bpy.context.scene.objects.active = currentArm
            currentArm.select = True
            if currentArm.animation_data is None:
                currentArm.animation_data_create()                
            for action in bpy.data.actions:
                if action.tag == False:
                    track = currentArm.animation_data.nla_tracks.new()
                    track.name = action.name
                    track.strips.new(action.name, action.frame_range[0], action)
                    currentArm.animation_data.action = action
        else:
            self.report({'ERROR'},'Nenhuma armadura foi definida!')
            return {'CANCELLED'}
        self.report({'INFO'},'Animação importada com sucesso!')
        return {'FINISHED'}

class AA_ALLCURRENT(bpy.types.Operator):
    bl_idname = "xayup.aa_allcurrent"
    bl_label = "Set all actions"
    bl_description = "Guardar TODAS as ações para a armadura 'padrão'"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        global currentArm
        if currentArm != "":
            if currentArm.animation_data is None:
                currentArm.animation_data_create()                
            for action in bpy.data.actions:
                track = currentArm.animation_data.nla_tracks.new()
                track.name = action.name      
                track.strips.new(action.name, action.frame_range[0], action)
                currentArm.animation_data.action = action
        else:
            self.report({'ERROR'},'Nenhuma armadura foi definida!')
            return {'CANCELLED'}
        self.report({'INFO'}, 'Ações definidas com sucesso!')
        return {'FINISHED'}       
        
class AA_CLEANLOOSE(bpy.types.Operator):
    bl_idname = "xayup.aa_cleanloose"
    bl_label = "Clean up loose actions"
    bl_description = "Deletar animações não lincados à armadura 'padrão'"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        global currentArm
        if currentArm != "":
            if len(currentArm.animation_data.nla_tracks) > 0:
                for blendact in bpy.data.actions:
                    notcnt = True
                    for armact in currentArm.animation_data.nla_tracks:
                        if armact.name == blendact.name:
                            notcnt = False
                            break
                    if notcnt:
                        bpy.data.actions.remove(blendact)
            else:
                self.report({'ERROR'},'Use a opção "Delete all animations"')
                return {'CANCELLED'} 
        else:
            self.report({'ERROR'},'Nenhuma animação padrão!')
            return {'CANCELLED'}
        self.report({'INFO'}, 'Todas as animações foram deletadas!')
        return {'FINISHED'}
        
class AA_DELANINS(bpy.types.Operator):
    bl_idname = "xayup.aa_delanins"
    bl_label = "Delete all animations"
    bl_description = "CUIDADO: Isso deletará todas as animações existentes!"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        for anins in bpy.data.actions:
            bpy.data.actions.remove(anins)
        self.report({'INFO'}, 'Todas as animações foram deletadas!')
        return {'FINISHED'}