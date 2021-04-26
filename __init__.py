from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import Operator, AddonPreferences
from bpy.props import *
import tempfile
import time
import glob
import bpy
import os
bl_info = {
    "name": "Temporizer: Save Temporary Version File",
    "author": "Kursad Karatas",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "File menu",
    "warning": "",
    "description": "Versioning files without versioning files",
    "category": "User Interface"
}


APIVER = str(bpy.app.version[0])+str(bpy.app.version[1])


def defineSceneProps():

    bpy.types.Scene.temporizer_issaved = BoolProperty(name="Untitled",
                                                      description="Is it saved before",
                                                      default=False)


def removeSceneProps():

    del bpy.context.scene.temporizer_issaved


def hashedName(fname):

    txtime = str(time.time()).split(".")[0]

    txtime = time.strftime("%d%m%Y_%H%M_%S")

    return fname+"_"+txtime+".blend"


def getFileName():

    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    filename = os.path.splitext(filename)[0]

    return filename


def saveTempPathFile(fpath, fname):

    print(fname)

    finalpath = os.path.join(fpath, fname)
    print("Full path is", os.path.join(fpath, fname))

    bpy.ops.wm.save_as_mainfile(filepath=finalpath, copy=True)

    return finalpath


def saveTempPathFileAs(fpath, fname):

    print(fname)

    finalpath = os.path.join(fpath, fname)
    print("Full path is", os.path.join(fpath, fname))

    bpy.ops.wm.save_as_mainfile(filepath=finalpath, copy=False)

    return finalpath


class SavePreferences(AddonPreferences):
    bl_idname = __name__
    bl_label = "Addonn Prefs"

    tempfolderpath: StringProperty(
        name="Temporary Folder Path",
        subtype='DIR_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our addon")
        layout.prop(self, "tempfolderpath")


class WM_OP_Temporizer(bpy.types.Operator):
    bl_idname = "wm.temporizer"
    bl_label = "Temporizer Save Temporary Versions"

    scene_name: StringProperty(name="Scene Name", default="")

    def execute(self, context):

        scn = context.scene
        user_preferences = context.preferences

        is_copy = False

        addon_prefs = user_preferences.addons[__name__].preferences
        info = ("Path: %s" % (addon_prefs.tempfolderpath))

        print("*******************")

        if not getFileName():

            filename = "TempBlender"
            filename = self.scene_name
            filename = hashedName(filename)
            is_copy = True
            scn.temporizer_issaved = True

        else:

            filename = hashedName(getFileName())

        if not addon_prefs.tempfolderpath:

            if not is_copy:

                saveIt = saveTempPathFile(tempfile.gettempdir(), filename)
            else:
                saveIt = saveTempPathFileAs(tempfile.gettempdir(), filename)

        else:

            if not is_copy:

                saveIt = saveTempPathFile(addon_prefs.tempfolderpath, filename)

            else:
                saveIt = saveTempPathFileAs(
                    addon_prefs.tempfolderpath, filename)

        self.report({'INFO'}, "The file is saved to "+saveIt)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager

        scn = context.scene

        if getFileName():

            print("scene was already saved")

            scn.temporizer_issaved = True
            return self.execute(context)

        if not getFileName():
            return wm.invoke_props_dialog(self)

        return {'FINISHED'}


def menu_draw(self, context):
    self.layout.separator()

    self.layout.operator("wm.temporizer")


classes = (SavePreferences,
           WM_OP_Temporizer,
           )


def register():

    defineSceneProps()

    bl_info['blender'] = getattr(bpy.app, "version")

    bpy.types.TOPBAR_MT_file.append(menu_draw)

    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():

    bpy.types.TOPBAR_MT_file.remove(menu_draw)

    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)
