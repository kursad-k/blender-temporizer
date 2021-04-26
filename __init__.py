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


#import bpy
#import os
#import tempfile

#filename = bpy.path.basename(bpy.context.blend_data.filepath)
#fname = os.path.splitext(filename)[0]
#tempfolder = tempfile.ettempdir()
#finalpath = os.path.join(tempfolder, fname)
#bpy.ops.wm.save_as_mainfile(filepath=finalpath, copy=True)


import os

import bpy
import os
import glob
import time
import tempfile
from bpy.props import *
#from bpy_extras.io_utils import ExportHelper

from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty


APIVER = str(bpy.app.version[0])+str(bpy.app.version[1])


def defineSceneProps():
    # bpy.types.Scene.ezlattice_object = StringProperty(name="Object2Operate",
    #                                     description="Object to be operated on",
    #                                     default="")
    bpy.types.Scene.temporizer_issaved = BoolProperty(name="Untitled",
                                        description="Is it saved before",
                                        default=False)

def removeSceneProps():
    # bpy.types.Scene.ezlattice_object = StringProperty(name="Object2Operate",
    #                                     description="Object to be operated on",
    #                                     default="")
    del bpy.context.scene.temporizer_issaved



def hashedName(fname):

    txtime=str(time.time()).split(".")[0]

    txtime= time.strftime("%d%m%Y_%H%M_%S")

    return fname+"_"+txtime+".blend"

def getFileName():

    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    filename = os.path.splitext(filename)[0]

    return filename

def saveTempPathFile(fpath,fname):

    #This function saves the scene based on the path settings in the addon setting

    print(fname)

    finalpath=os.path.join(fpath,fname)
    print("Full path is",os.path.join(fpath,fname))

    bpy.ops.wm.save_as_mainfile(filepath=finalpath, copy=True)

    return finalpath

def saveTempPathFileAs(fpath,fname):

    #This function saves the scene based on the path settings in the addon setting

    print(fname)

    finalpath=os.path.join(fpath,fname)
    print("Full path is",os.path.join(fpath,fname))

    bpy.ops.wm.save_as_mainfile(filepath=finalpath, copy=False)

    return finalpath

class SavePreferences(AddonPreferences):
    bl_idname = __name__
    bl_label = "Addonn Prefs"

    tempfolderpath : StringProperty(
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


    scene_name:StringProperty(name="Scene Name", default="")

    def execute(self,context):

        #PREFERENCES
        # if APIVER=="279":
        #     user_preferences=context.user_preferences

        scn=context.scene
        user_preferences=context.preferences

        is_copy=False

        addon_prefs = user_preferences.addons[__name__].preferences
        info = ("Path: %s" % (addon_prefs.tempfolderpath))
        #PREFERENCES

        #DEBUG
        print("*******************")

        if not getFileName():
            #We do not have a  file name
            #self.report({'INFO'},"The scene has no file name")
            filename="TempBlender"
            filename=self.scene_name
            filename=hashedName(filename)
            is_copy=True
            scn.temporizer_issaved=True


        else:
            #We have a file name
            #filename=getFileName()
            filename=hashedName(getFileName())


            # self.report({'INFO'},"The scene has a filename  ->"+filename)

        #saveIt=saveTempFile(hashedName(filename))

        if not addon_prefs.tempfolderpath:
            #We have no path settings, we save to the system's temp folder

            if not is_copy:
                #saveIt=saveTempPathFile(tempfile.gettempdir(),hashedName(filename))
                saveIt=saveTempPathFile(tempfile.gettempdir(),filename)
            else:
                saveIt=saveTempPathFileAs(tempfile.gettempdir(),filename)

            # self.report({'INFO'}, "Addon path setting is empty, saving to " + tempfile.gettempdir())
#
        else:
            #we have a path set in the settings

            if not is_copy:
                #saveIt=saveTempPathFile(addon_prefs.tempfolderpath,hashedName(filename))
                saveIt=saveTempPathFile(addon_prefs.tempfolderpath,filename)

            else:
                saveIt=saveTempPathFileAs(addon_prefs.tempfolderpath,filename)
            # self.report({'INFO'}, "Addon path is set, saving to " + saveIt)

        # self.report({'INFO'}, "The file name is " + filename)
        self.report({'INFO'}, "The file is saved to "+saveIt)

        return {'FINISHED'}




    def invoke( self, context, event ):
        wm = context.window_manager

        scn=context.scene

        # if scn.temporizer_issaved or getFileName():
        if getFileName():
            # return wm.invoke_props_dialog( self )
            # return {'PASS_THROUGH'}
            #return {'RUNNING_MODAL'}
            print("scene was already saved")

            #return {'EXEC_DEFAULT'}
            scn.temporizer_issaved=True
            return self.execute(context)

        # if not scn.temporizer_issaved and  not getFileName():
        if  not getFileName():
            return wm.invoke_props_dialog( self )
            #context.window_manager.invoke_search_popup(self)
            #return {'RUNNING_MODAL'}

            # return
        return {'FINISHED'}


def menu_draw(self, context):
    self.layout.separator()
    # self.layout.operator(WM_OP_Temporizer.bl_idname, WM_OP_Temporizer.bl_label, icon='ZOOMIN')
    self.layout.operator("wm.temporizer")



classes = (SavePreferences,
        WM_OP_Temporizer,
        )

def register():

    defineSceneProps()

    bl_info['blender'] = getattr(bpy.app, "version")
    # bpy.types.INFO_MT_file.append(menu_draw)

    # if APIVER == "279":
    #     bpy.types.INFO_MT_file.append(menu_draw)

    # if APIVER == "280":
    bpy.types.TOPBAR_MT_file.append(menu_draw)

    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():

    # if APIVER == "279":
    #     bpy.types.INFO_MT_file.remove(menu_draw)

    # if APIVER == "280":
    bpy.types.TOPBAR_MT_file.remove(menu_draw)

    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    #removeSceneProps()
    #
    # if 'TempFolder' in globals():
#         del TempFolder



# register, unregister = bpy.utils.register_classes_factory(classes)


# if __name__ == "__main__":
#     register()
