# Auto Animations for Blender
A small addon for Blender in order to facilitate some animation settings, such as importing animations for the current armature (the animation must contain the same bone as the selected armature), cleaning animations from the blender file and just the basics. Only ".fbx" files!
# How it works?
Simple!:
- Import Armature: This will open the explorer so you can select the armor you want to work with.
- Import actions: This will open the explorer for you to select the animation (inside the fbx) and set the animations in the file in your current armature.
- Set as default: If you already have an armature already in the scene and you want to work with it, set it as default with this option only by selecting the armature (in the schematizer window by clicking on the armature) and using this button and a message of success if it goes well.
- Clean up loose actions: CAUTION! This option will erase all animations present in the current blender project. If you are already working with an armor that was not imported via "Import armature", all animations will be deleted using this option, otherwise only animations not imported via "Import armature" and "Import actions" will be deleted.
- Set all actions: If you use the "Set as Default" option, this will be useful to save the animations already present in your current blender project. ATTENTION! Literally all animations contained in the current project will be guarded in your current armor.
- Delete all animations: This option will delete all animations present in your current project, useful for cleaning up animations that are "garbage". Remembering that it literally erases all animations, and if your current armaturre was not imported via "Import Armature" or "Import actions" they will also all be deleted.
# Supported files
The addon only supports importing ".fbx" files, but you can use the other options normally with armatures imported by Blender itself
# Closing statements:
The Addon was tested only with Mixamo armatures and animations but feel free to experiment with other armatures, but remembering that the animation will have to be compatible with the current armature, in this case the bones!

Only "Automation" Addon, don't expect too much. Feel free to "Twirl" the codes, use it as a base and... anyway, do what you want :)
Good luck!
