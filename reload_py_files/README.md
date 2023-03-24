# Reload all .py Files
- UPBGE 0.2.5

## What is this?
This Add-on makes it easy when you write python code externally. This "Reloads" the python scripts avoiding doing it manually one by one (That "float" that appears when the script is modified outside of Blender's text editor).

## How to instal?
- Copy the "reload_py_files" folder to your UPBGE 0.2.5 add-ons folder (Usually '2.79\scripts\addons')
- Open UPBGE, go to "File > User Preferences > Add-ons > and, in "Categories", select Python files and check "Reload .py files".
- In "Inputs" search and expand "3D View", "Object Mode" and, scrolling down, click on "+ Add New". Expand "none" (just created), and change "none" to "python.reload_all_py". Hit enter and configure a key for this trigger.

When you press the key you configured, all the scripts used in the project will automatically be reloaded and the game will start automatically.

## Credits
### Scripts:
- https://blenderartists.org/forum/showthread.php209369-Synchronizing-text-with-changes-from-outside
- https://blender.stackexchange.com/a/108443
