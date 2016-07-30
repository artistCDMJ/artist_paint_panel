# -*- coding: utf8 -*-
# python
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {"name": "Artist Paint Panel",
           "author": "CDMJ, Spirou4D",
           "version": (2, 00, 0),
           "blender": (2, 77, 0),
           "location": "Toolbar > Misc Tab > Artist Panel",
           "description": "Artist Paint Studio.",
           "warning": "Run only in BI now",
           "category": "Paint"}

'''
Modif: 2016-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Modif: 2016-02'01 Patrick optimize the code
'''

import bpy
from bpy.types import   AddonPreferences,\
                        Menu,\
                        Panel,\
                        UIList,\
                        Operator
from bpy.props import *
import math
import os
SEP = os.sep

MaskMessage = "Name the mask, please..."
CurveMessage = "name the curve, please..."
########################
#      Properties      #
########################
#-------------------------------------------get the addon preferences
def get_addon_preferences():
    #bpy.context.user_preferences.addons["notify_after_render"].preferences['sent_sms']=1
    #Par exemple:
    # addon_prefs = get_addon_preferences()
    # addon_prefs.url_smsservice
    return bpy.context.user_preferences.addons[__name__].preferences

#-------------------------------------------get the main canvas datas
def MainCanvasData(self, context):
    obj = context.active_object
    scene= context.scene

    if scene.artist_paint is not None:      #if main canvas isn't erased
            if len(scene.artist_paint) !=0:
                for main_canvas in scene.artist_paint: #look main canvas name
                    _Ext = (main_canvas.filename)[-4:]
                    canvasName = (main_canvas.filename)[:-4]   #find the name of the maincanvas
                    filePATH = main_canvas.path
                    canvasDimX = main_canvas.dimX
                    canvasDimY =  main_canvas.dimY

    return {canvasName, _Ext, filePATH, canvasDimX, canvasDimY}


def pollAPT(self, context):
    scene = context.scene
    obj =  context.active_object
    empty = scene.maincanvas_is_empty
    main_canvas_name = ""

    if not(empty):
        if scene.artist_paint is not None:
            if len(scene.artist_paint) !=0:
                for main_canvas in scene.artist_paint:
                    main_canvas_name = (main_canvas.filename)[:-4]
    else:
        return False

    if obj is not None:
        return obj.name == main_canvas_name
    else:
        return  False

#------------------------------------------------Create a collection
class SceneCustomCanvas(bpy.types.PropertyGroup):
    filename = bpy.props.StringProperty(name="Test Prop", default="")
    path = bpy.props.StringProperty(name="Test Prop", default='')
    dimX = bpy.props.IntProperty(name="Test Prop", default=0)
    dimY = bpy.props.IntProperty(name="Test Prop", default=0)
bpy.utils.register_class(SceneCustomCanvas)

bpy.types.Scene.artist_paint = \
                    bpy.props.CollectionProperty(type=SceneCustomCanvas)

bpy.types.Scene.Viewmode_toggle = \
                            bpy.props.BoolProperty(default=True)
bpy.types.Scene.UI_is_activated = \
                            bpy.props.BoolProperty(default=False)
bpy.types.Scene.maincanvas_is_empty = \
                            bpy.props.BoolProperty(default=True)
bpy.types.Scene.bordercrop_is_activated = \
                            bpy.props.BoolProperty(default=False)
bpy.types.Scene.guides_are_activated = \
                            bpy.props.BoolProperty(default=False)

#bool property to use constraint rotation
bpy.types.Scene.canvas_in_frame = \
                                bpy.props.BoolProperty(default=False)
#bool property to use with resetrotation
bpy.types.Scene.ArtistPaint_Bool02 = \
                                bpy.props.BoolProperty(default=False)
#bool property to cadenas addon's prefs
bpy.types.Scene.prefs_are_locked = \
                                bpy.props.BoolProperty(default=True)
#bool property to addon's prefs lock
bpy.types.Scene.locking_are_desactived = \
                                bpy.props.BoolProperty(default=False)


#######################
#       UI Tools
#######################
#----------------------------------------------Display message
class MessageOperator(Operator):
    bl_idname = "error.message"
    bl_label = "Warning Message"

    message = StringProperty()
    confirm = StringProperty()

    def check(self, context):
        return True

    def execute(self, context):
        scene = context.scene
        scene.maincanvas_is_deleted = False
        print('INIT')
        return True

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=200, height=300)

    def draw(self, context):
        layout = self.layout
        layout.label("**** WARNING! ****")
        message = "   " + self.message
        line = int(round(float(len(message))/32)) + 1
        n=1
        while (n <= line):
            X = (n-1)*32
            Z = n*32
            content = message[X:Z]
            row = layout.row(align=True)
            row.label(content)
            n += 1
        else:
            print("c'est fini")

        layout.separator()
        row = layout.row(align=True)

        row.operator(self.confirm)

#-----------------------------The OK button in the error dialog
class OkOperator(Operator):
    bl_idname = "error.ok0"
    bl_label = "OK"

    def execute(self, context):
        print('ok')
        return {'FINISHED'}

#-----------------------------The OK button in the error dialog
class OkOperator(Operator):
    bl_idname = "error.ok1"
    bl_label = "OK"

    def execute(self, context):
        scene = context.scene                                #init
        if scene.artist_paint is not None:      #if main canvas isn't erased
            if len(scene.artist_paint) !=0:      #artist_paint isn't empty
                for main_canvas in scene.artist_paint: #look main canvas name
                    canvasName = (main_canvas.filename)[:-4]   #find maincanvas's name
                    _camName = "Camera_" + canvasName  #create canvas's camera name
                for obj in scene.objects:
                    if obj.name == canvasName :      #if mainCanvas Mat exist
                        scene.objects.active = obj
                        break
        else:
            return {'FINISHED'}

        obj = context.active_object             #obj is the mainCanvas
        if obj.mode != 'OBJECT':
            bpy.ops.paint.texture_paint_toggle()     #return in object mode

        bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)
        bpy.ops.object.delete(use_global=True)
        for cam  in bpy.data.objects:
            if cam.name == "Camera_" + canvasName:
                cam.select = True
                context.scene.objects.active = cam
                bpy.ops.object.delete(use_global=True)

        scene.artist_paint.clear()
        scene.maincanvas_is_empty = True

        message = 'The canvas: "' + canvasName + \
                    '" is  removed in memory and deleted with his hierarchy.'
        self.report({'INFO'}, message)

        bpy.ops.artist_paint.load_init()
        return {'FINISHED'}


#######################
#       Classes       #
#######################

#-----------------------------Change to GLSL view mode
class GLSLViewMode(Operator):
    bl_description = "GLSL Mode"
    bl_idname = "artist_paint.glsl"
    bl_label = "GLSL Mode"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        A = context.scene.Viewmode_toggle
        return not A

    def execute(self, context):
        context.scene.game_settings.material_mode = 'GLSL'
        A = context.scene.Viewmode_toggle
        if A == True:
            context.scene.Viewmode_toggle = False
        else:
            context.scene.Viewmode_toggle = True
        return {'FINISHED'}

#-----------------------------Change to MULTITEXTURE view mode
class MTViewMode(Operator):
    bl_description = "Multitexture Mode"
    bl_idname = "artist_paint.multitexture"
    bl_label = "Multi-Texture Mode"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        A = context.scene.Viewmode_toggle
        return A

    def execute(self, context):
        context.scene.game_settings.material_mode = 'MULTITEXTURE'
        A = context.scene.Viewmode_toggle
        if A == True:
            context.scene.Viewmode_toggle = False
        else:
            context.scene.Viewmode_toggle = True
        return {'FINISHED'}


#------------------------------------------------Reset main canvas
class ArtistPaintLoadtInit(Operator):
    bl_idname = "artist_paint.load_init"
    bl_label = "Init Artist Paint Add-on"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):          #Init the Main Canvas object
        scene = context.scene
        init = context.scene.UI_is_activated
        empty = context.scene.maincanvas_is_empty

        if not(empty):
            if scene.artist_paint is not None:
                if len(scene.artist_paint) !=0:
                    main_canvas_0 = scene.artist_paint[0]
                    canvasName = (main_canvas_0.filename)[:-4]

            warning = 'Do you really want to remove "'+ canvasName + \
                    '" from memory and delete all his hierarchy?'
            state = bpy.ops.error.message('INVOKE_DEFAULT',\
                                            message = warning,\
                                            confirm ="error.ok1" )
        else:
            if context.scene.UI_is_activated:
                context.scene.UI_is_activated = False
            else:
                context.scene.UI_is_activated = True
        return {'FINISHED'}


#-------------------------------------------------Load main canvas
class ArtistPaintLoad(Operator):
    bl_description = "Load the main canvas"
    bl_idname = "artist_paint.canvas_load"
    bl_label = ""
    bl_options = {'REGISTER','UNDO'}

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        OBJ = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        filePATH = self.filepath
        fileName = os.path.split(filePATH)[-1]
        fileDIR = os.path.dirname(filePATH)

        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.import_image.to_plane(\
                        files=[{"name":fileName,"name":fileName}],
                        directory=fileDIR,
                        filter_image=True,
                        filter_movie=True,
                        filter_glob="",
                        use_transparency=True,
                        relative=False)
        obj = context.active_object
        select_mat = obj.data.materials[0].texture_slots[0].\
                                            texture.image.size[:]

        main_canvas= bpy.context.scene.artist_paint.add()
        main_canvas.filename = fileName
        main_canvas.path = fileDIR
        main_canvas.dimX = select_mat[0]
        main_canvas.dimY = select_mat[1]
        context.scene.maincanvas_is_empty = False

        for main_canvas in bpy.context.scene.artist_paint:
            print(main_canvas.filename)
            print(main_canvas.path)
            print(str(main_canvas.dimX))
            print(str(main_canvas.dimY))

        #set the cursor snap on object faces
        userpref = context.user_preferences
        userpref.view.use_mouse_depth_cursor = True
        return {'FINISHED'}


#-------------------------------------------------reload image
class ImageReload(Operator):
    """Reload Image Last Saved State"""
    bl_description = "Reload canvas's image"
    bl_idname = "artist_paint.reload_saved_state"
    bl_label = ""
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        A = obj is not None
        if A:
            B = obj.type == 'MESH'
            return B

    def execute(self, context):
        original_type = context.area.type
        context.area.type = 'IMAGE_EDITOR'
        bpy.ops.image.reload()       #return image to last saved state
        context.area.type = original_type
        return {'FINISHED'}

#-------------------------------------------------image save
class SaveImage(Operator):
    """Overwrite Image"""
    bl_description = ""
    bl_idname = "artist_paint.save_current"
    bl_label = "Save Image Current"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        A = obj is not None
        if A:
            B = obj.type == 'MESH'
            return B

    def execute(self, context):
        original_type = context.area.type
        context.area.type = 'IMAGE_EDITOR'
        bpy.ops.image.save_as()                      #save as
        context.area.type = original_type
        return {'FINISHED'}


#-------------------------------------------------image save
class SaveIncremImage(Operator):
    """Save Incremential Images"""
    bl_description = ""
    bl_idname = "artist_paint.save_increm"
    bl_label = "Save incremential Image Current"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        A = obj is not None
        if A:
            B = obj.type == 'MESH'
            return B

    def execute(self, context):
        scene =context.scene
        if scene.artist_paint is not None:      #if main canvas isn't erased
            if len(scene.artist_paint) !=0:
                for main_canvas in scene.artist_paint: #look main canvas name
                    _Ext = (main_canvas.filename)[-4:]
                    canvasName = (main_canvas.filename)[:-4]   #find the name of the maincanvas
                    filePATH = main_canvas.path
                    canvasDimX = main_canvas.dimX
                    canvasDimY =  main_canvas.dimY
                for obj in scene.objects:
                    if obj.name == canvasName :      #if mainCanvas Mat exist
                        scene.objects.active = obj
                        break
        else:
            return {'FINISHED'}
        #init
        obj = context.active_object
        original_type = context.area.type
        context.area.type = 'IMAGE_EDITOR'

        filePATH = os.path.realpath(filePATH)
        #/.config/blender/Brushes/13_Tâche_de_café/Cafeina (1).png

        _tempName = [canvasName + '_001' + _Ext]

        HOME = os.path.expanduser("~")
        if filePATH.find(HOME)!=-1:
            _Dir =  filePATH
        else:
            _Dir = HOME + filePATH

        #verify the brushname
        l = os.listdir(_Dir)
        brushesName = [ f for f in l if os.path.\
                                isfile(os.path.join(_Dir,f)) ]
        brushesName = sorted(brushesName)

        i = 1
        for x in _tempName:
            for ob in brushesName:
                if ob == _tempName[-1]:
                    i += 1
                    _tempName = _tempName + [canvasName + '_' + \
                                    '{:03d}'.format(i) + _Ext]


        #return image to last saved state
        chemin = os.path.join(_Dir,_tempName[-1])
        bpy.ops.image.save_as(filepath = chemin,
                                check_existing=False,
                                relative_path=False)

        context.area.type = original_type
        return {'FINISHED'}


#--------------------------------------------------Create brush
class BrushMakerScene(Operator):
    """Create Brush Scene"""
    bl_description = ""
    bl_idname = "artist_paint.create_brush_scene"
    bl_label = "Create Scene for Image Brush Maker"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        for sc in bpy.data.scenes:
            if sc.name == "Brush":
                return False
        return context.area.type=='VIEW_3D'

    def execute(self, context):
        _name="Brush"
        for sc in bpy.data.scenes:
            if sc.name == "Brush":
                return {'FINISHED'}
        bpy.ops.scene.new(type='NEW') #add new scene & name it 'Brush'
        context.scene.name = _name

        #add lamp and move up 4 units in z
        bpy.ops.object.lamp_add(
                    type = 'POINT',
                    radius = 1,
                    view_align = False,
                    location = (0, 0, 4)
                    )

        #add camera to center and move up 4 units in Z
        bpy.ops.object.camera_add(
                    view_align=False,
                    enter_editmode=False,
                    location=(0, 0, 4),
                    rotation=(0, 0, 0)
                    )

        context.object.name="Tex Camera"      #rename selected camera

        #change scene size to 1K
        _RenderScene = context.scene.render
        _RenderScene.resolution_x=1024
        _RenderScene.resolution_y=1024
        _RenderScene.resolution_percentage = 100

        #save scene size as preset
        bpy.ops.render.preset_add(name = "1K Texture")

        #change to camera view
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                override['area'] = area
                bpy.ops.view3d.viewnumpad(override, type = 'CAMERA')
                break # this will break the loop after the first ran
        return {'FINISHED'}


#-------------------------------------------------Front of CCW15 Rot
class FrontOfCCW(Operator):
    """front of face CCW15 rotate"""
    bl_description = ""
    bl_idname = "artist_paint.frontof_ccw"
    bl_label = "Front Of CCW15 rotation"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = context.mode == 'PAINT_TEXTURE'
            B = obj.type == 'MESH'
            return A and B

    def execute(self, context):
        #init
        paint = bpy.ops.paint
        addon_prefs = get_addon_preferences()
        CustomAngle = math.radians(addon_prefs.customAngle)

        paint.texture_paint_toggle()        #return in object mode
        bpy.ops.transform.rotate(value=-CustomAngle,
                                constraint_orientation='NORMAL')
        paint.texture_paint_toggle()        #return in paint mode
        return {'FINISHED'}


#-------------------------------------------------Front of paint
class FrontOfPaint(Operator):
    """fast front of face view paint"""
    bl_description = ""
    bl_idname = "artist_paint.frontof_paint"
    bl_label = "Front Of Paint"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = context.mode == 'PAINT_TEXTURE'
            B = obj.type == 'MESH'
            return A and B

    def execute(self, context):
        #init
        paint = bpy.ops.paint
        object = bpy.ops.object
        contextObj = context.object

        context.space_data.viewport_shade = 'TEXTURED'  #texture draw
        paint.texture_paint_toggle()
        object.editmode_toggle()
        bpy.ops.view3d.viewnumpad(type='TOP', align_active=True)
        object.editmode_toggle()
        paint.texture_paint_toggle()
        contextObj.data.use_paint_mask = True
        return {'FINISHED'}


#-------------------------------------------------Front of CW15 Rot
class FrontOfCW(Operator):
    """fast front of face CW15 rotate"""
    bl_description = ""
    bl_idname = "artist_paint.frontof_cw"
    bl_label = "Front Of CW15 rotation"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = context.mode == 'PAINT_TEXTURE'
            B = obj.type == 'MESH'
            return A and B

    def execute(self, context):
        #init
        paint = bpy.ops.paint
        addon_prefs = get_addon_preferences()
        CustomAngle = math.radians(addon_prefs.customAngle)

        paint.texture_paint_toggle()        #return in object mode
        bpy.ops.transform.rotate(value=+CustomAngle,
                            constraint_orientation='NORMAL')
        paint.texture_paint_toggle()        #return in paint mode
        return {'FINISHED'}


#-------------------------------------------------cameraview paint
class CameraviewPaint(Operator):
    """Create a front-of camera in painting mode"""
    bl_description = ""
    bl_idname = "artist_paint.cameraview_paint"
    bl_label = "Cameraview Paint"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        return pollAPT(self, context)

    def execute(self, context):
        scene = context.scene                     #init
        if scene.artist_paint is not None:      #if main canvas isn't erased
            if len(scene.artist_paint) !=0:
                for main_canvas in scene.artist_paint: #look main canvas name
                    canvasName = (main_canvas.filename)[:-4]   #find the name of the maincanvas
                    _camName = "Camera_" + canvasName
                    canvasDimX = main_canvas.dimX
                    canvasDimY = main_canvas.dimY
                for obj in scene.objects:
                    if obj.name == canvasName :      #if mainCanvas Mat exist
                        scene.objects.active = obj
                        break
        else:
            return {'FINISHED'}

        obj = context.active_object
        context.space_data.viewport_shade = 'TEXTURED'  #texture draw option
        context.object.active_material.use_shadeless = True #shadeless option

        for cam  in bpy.data.objects:
            if cam.name == _camName:
                prefix = 'Already found a camera for this image : '
                bpy.ops.error.message('INVOKE_DEFAULT',
                                    message =  prefix + _camName,
                                    confirm ="error.ok0" )
                return {'FINISHED'}

        bpy.ops.view3d.snap_cursor_to_center()    #Cursor to center of world
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)

        #add camera
        bpy.ops.object.camera_add(view_align=False,\
                        enter_editmode=False,\
                        location=(0, 0, 0),\
                        rotation=(0, 0, 0),\
                        layers=(True, False, False, False, False,\
                                False, False, False, False, False,\
                                False, False, False, False, False,\
                                False, False, False, False, False))

        context.scene.render.resolution_percentage = 100   #ratio full
        context.object.name = _camName                       #name it
        bpy.ops.view3d.object_as_camera()         #switch to camera view

        context.object.data.type = 'ORTHO'      #ortho view 4 cam
        context.object.data.dof_object= obj

        #move cam up in Z by 1 unit
        bpy.ops.transform.translate(value=(0, 0, 1),
                    constraint_axis=(False, False, True),
                    constraint_orientation='GLOBAL',
                    mirror=False,
                    proportional='DISABLED',
                    proportional_edit_falloff='SMOOTH',
                    proportional_size=1)

        #resolution
        rnd = bpy.data.scenes[0].render
        rndx = rnd.resolution_x = canvasDimX
        rndy = rnd.resolution_y = canvasDimY

        #orthoscale
        if rndx >= rndy:
            orthoscale =  rndx / rndy
        else:
            orthoscale = 1
        context.object.data.ortho_scale = orthoscale

        bpy.ops.object.select_all(action='TOGGLE')
        bpy.ops.object.select_all(action='DESELECT')  #init Selection

        #select canvas
        obj.select = True
        context.scene.objects.active = obj
        bpy.ops.paint.texture_paint_toggle()
        scene.game_settings.material_mode = 'GLSL'
        context.space_data.lock_camera = False
        return {'FINISHED'}


#-------------------------------------------------border crop on
class BorderCrop(Operator):
    """Turn on Border Crop in Render Settings"""
    bl_description = "Border Crop ON"
    bl_idname = "artist_paint.border_crop"
    bl_label = ""
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        rs = context.scene.render
        rs.use_border = True
        rs.use_crop_to_border = True
        return {'FINISHED'}


#-------------------------------------------------border crop off
class BorderUnCrop(Operator):
    """Turn off Border Crop in Render Settings"""
    bl_description = "Border Crop OFF"
    bl_idname = "artist_paint.border_uncrop"
    bl_label = ""
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        rs = context.scene.render
        rs.use_border = False
        rs.use_crop_to_border = False
        return {'FINISHED'}


#-------------------------------------------------border crop toggle
class BorderCropToggle(Operator):
    """Set Border Crop in Render Settings"""
    bl_description = "Border Crop On/Off TOGGLE"
    bl_idname = "artist_paint.border_toggle"
    bl_label = ""
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        return pollAPT(self, context)

    def execute(self, context):
        scene = context.scene
        bordercrop_is_activated = scene.bordercrop_is_activated
        rs = context.scene.render

        if not(scene.prefs_are_locked):
            if rs.use_border and rs.use_crop_to_border:
                bpy.ops.artist_paint.border_uncrop()
                bordercrop_is_activated = False
            else:
                bpy.ops.artist_paint.border_crop()
                bordercrop_is_activated = True
        return {'FINISHED'}



#-------------------------------------------------camera guides
class CamGuides(Operator):
    """Turn on Camera Guides"""
    bl_description = "Camera Guides On/Off Toggle"
    bl_idname = "artist_paint.guides_toggle"
    bl_label = ""
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        return pollAPT(self, context)

    def execute(self, context):
        scene = context.scene
        _bool03 = scene.prefs_are_locked

        if scene.artist_paint is not None:      #if main canvas isn't erased
            if len(scene.artist_paint) != 0:
                for main_canvas in scene.artist_paint: #look main canvas name
                    canvasName = (main_canvas.filename)[:-4]   #find the name of the maincanvas
                    _camName = "Camera_" + canvasName
        else:
            return {'FINISHED'}

        for cam in bpy.data.objects :
            if cam.name == _camName:
                if not(_bool03):
                    if not(scene.guides_are_activated): #True = guides not visible
                        cam.data.show_guide = {'CENTER', 'THIRDS', 'CENTER_DIAGONAL'}
                        scene.guides_are_activated = True
                    else:
                        cam.data.show_guide = set() #False = guides visible
                        scene.guides_are_activated = False

        return {'FINISHED'}


#-------------------------------------------------Prefs toogle button
class PrefsLockToggle(Operator):
    """Lock bordercrop & guides preferences in viewport"""
    bl_description = "Prefs lock On/Off TOGGLE"
    bl_idname = "artist_paint.prefs_lock_toggle"
    bl_label = ""
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        return pollAPT(self, context)

    def execute(self, context):
        addon_prefs = get_addon_preferences()
        scene = context.scene
        _bool03 = scene.prefs_are_locked
        bordercrop_is_activated = scene.bordercrop_is_activated
        guides_are_activated = scene.guides_are_activated


        if scene.artist_paint is not None:      #if main canvas isn't erased
            if len(scene.artist_paint) != 0:
                for main_canvas in scene.artist_paint: #look main canvas name
                    canvasName = (main_canvas.filename)[:-4]   #find the name of the maincanvas
                    _camName = "Camera_" + canvasName
        else:
            return {'FINISHED'}


        if addon_prefs.bordercrop:
            bpy.ops.artist_paint.border_crop()
        else:
            bpy.ops.artist_paint.border_uncrop()

        for cam in bpy.data.objects :
            if cam.name == _camName:
                if not(guides_are_activated) and addon_prefs.guides:
                    cam.data.show_guide = {'CENTER', 'THIRDS', 'CENTER_DIAGONAL'}
                    scene.guides_are_activated = True
                else:
                    cam.data.show_guide = set() #False = guides visible
                    scene.guides_are_activated = False

                break

        scene.prefs_are_locked = False if _bool03 else True
        return {'FINISHED'}


#-------------------------------------------Gpencil to Mask in one step
class TraceSelection(Operator):
    """Mesh mask from gpencil lines"""
    bl_idname = "artist_paint.trace_selection"
    bl_label = "Make Mesh Mask from Gpencil's drawing"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = context.mode == 'PAINT_TEXTURE'
            B = obj.type == 'MESH'
            C = False
            GP = bpy.data.grease_pencil
            for lay0 in GP:
                if lay0.name == 'GPencil':
                    if GP['GPencil'].layers.find('GP_Layer')!= -1:
                        C = True
                        break
                break
            return A and B and C

    mask_name = StringProperty(name="Mask name")

    def invoke(self, context, event):
        global MaskMessage
        self.mask_name = MaskMessage
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):
        scene = context.scene
        tool_settings = scene.tool_settings

        objOPS = bpy.ops.object
        gpencilOPS = bpy.ops.gpencil
        paintOPS = bpy.ops.paint
        meshOPS = bpy.ops.mesh
        cvOPS = bpy.ops.curve

        #----------------------------------------------INIT MAIN CANVAS
        if scene.artist_paint is not None:      #if main canvas isn't erased
            if len(scene.artist_paint) !=0:
                for main_canvas in scene.artist_paint: #look main canvas name
                    canvasName = (main_canvas.filename)[:-4]   #find the name of the maincanvas
                    canvasDimX = main_canvas.dimX
                    canvasDimY =  main_canvas.dimY
                for obj in scene.objects:
                    if obj.name == canvasName :      #if mainCanvas Mat exist
                        scene.objects.active = obj
                        break
        else:
            return {'FINISHED'}
        _mkName = self.mask_name

        #----------------------------------------------CONVERT TO CURVE
        obj =  context.active_object             #save the main Canvas
        objRz = obj.rotation_euler[2]

        gpencilOPS.convert(type='CURVE', use_timing_data=True)
        gpencilOPS.data_unlink()
        paintOPS.texture_paint_toggle()          #return object mode
        lrs = []
        for cvP in bpy.data.objects:
            if cvP.name.find('GP_Layer') != -1:
                if cvP.type == "CURVE":
                    lrs.append(cvP)
        cv = lrs[-1]                             #select 'GP_Layer'curve

        scene.objects.active = cv                #active the curve
        cv.name = "msk_"+ _mkName                #name the curve here

        objOPS.editmode_toggle()                 #return in edit mode
        cvOPS.cyclic_toggle()                    #invert normals
        cv.data.dimensions = '2D'                #transform line to face
        objOPS.editmode_toggle()                 #return in Object mode

        #----------------------------------------DUPLICAT-PARENT 2x curves
        context.space_data.layers[19] = True     #layer20 temporary visible
        obj.select = False
        cv.select = True
        objOPS.duplicate_move()
        cvDupli = context.object
        cvDupli.name = 'cvs_' +  _mkName
        #parent curveDupli to Canvas
        cvDupli.select = True
        scene.objects.active = obj               #select the Canvas
        objOPS.parent_set(type='OBJECT',\
                            keep_transform=False)#parent Curve to Canvas
        objOPS.move_to_layer(layers=(False, False, False, False,\
                                False, False, False, False, False,\
                                False, False, False, False, False,\
                                False, False, False, False, False,\
                                True))           #move to layer20
        context.space_data.layers[19] = False    #layer20 stay invisible
        cvDupli.select = False
        #parent curve to Canvas
        cv.select = True
        scene.objects.active = obj               #select the Canvas
        objOPS.parent_set(type='OBJECT',\
                            keep_transform=False)#parent curve to Canvas


        #------------------------------------------------------MESH MASK UV
        scene.objects.active = cv
        objOPS.convert(target='MESH')            #convert to mesh
        
        scene.objects.active = obj               #select the canvas
        #init rotation
        bpy.ops.transform.rotate(value=-objRz,
                                 axis=(0, 0, 1),
                                 constraint_axis=(False, False, True),
                                 constraint_orientation='GLOBAL')

        scene.objects.active = cv                #select the Mask
        objOPS.editmode_toggle()                 #return in edit mode
        meshOPS.select_all(action='TOGGLE')      #select points
        meshOPS.dissolve_faces()                 #dissolve faces
        meshOPS.normals_make_consistent(inside=False)#Normals ouside
        bpy.ops.uv.project_from_view(camera_bounds=True,
                                    correct_aspect=False,
                                    scale_to_bounds=False)#uv cam unwrap
        for mat in bpy.data.materials:           #Material and texture
            if mat.name == canvasName :          #if mainCanvas Mat exist
                cv.data.materials.append(mat)    #add main canvas mat
                paintOPS.add_texture_paint_slot(type='DIFFUSE_COLOR',
                                            name=cv.name,
                                            width=canvasDimX,
                                            height=canvasDimY,
                                            color=(1, 1, 1, 0),
                                            alpha=True,
                                            generated_type='BLANK',
                                            float=False)
                break                            #add a texture
        objOPS.editmode_toggle()                 #return in object mode

        scene.objects.active = obj               #select the Canvas
        #return to rotation state
        bpy.ops.transform.rotate(value=objRz,
                                 axis=(0, 0, 1),
                                 constraint_axis=(False, False, True),
                                 constraint_orientation='GLOBAL')

        #------------------------------------------------------OPTIONS
        scene.objects.active = cv                #return on the mask
        if context.mode != 'PAINT_TEXTURE':
            paintOPS.texture_paint_toggle()          #return in paint mode
        context.object.data.use_paint_mask = True
        tool_settings.image_paint.use_occlude = False
        tool_settings.image_paint.use_backface_culling = False
        tool_settings.image_paint.use_normal_falloff = False
        tool_settings.image_paint.seam_bleed = 0

        return {'FINISHED'}



#-----------------------------------------------Curve Bezier to Poly
class CurvePoly2d(Operator):
    """Curve added and made poly 2d Macro"""
    bl_description = "Create 2D Poly Vector Mask"
    bl_idname = "artist_paint.curve_2dpoly"
    bl_label = "Create 2D Bezier Vector Mask"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        A = pollAPT(self, context)
        B = context.mode == 'PAINT_TEXTURE'
        return A and B

    curve_name = StringProperty(name="Curve name")

    def invoke(self, context, event):
        global MaskMessage
        self.curve_name = CurveMessage
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.active_object            #selected canvas object
        objRz = math.degrees(obj.rotation_euler[2])
        #Operators
        objOPS = bpy.ops.object
        cvOPS = bpy.ops.curve
        paintOPS = bpy.ops.paint

        paintOPS.texture_paint_toggle()         #return object mode
        bpy.ops.view3d.snap_cursor_to_center()  #center the cursor
        cvOPS.primitive_bezier_curve_add(rotation=(0, 0, objRz),
                                layers=(True, False, False, False,
                                 False, False, False, False, False,
                                 False, False, False, False, False,
                                 False, False, False, False, False,
                                 False))        #add curve
        cv = context.object                     #save original curve

        objOPS.editmode_toggle()                #toggle curve edit
        cvOPS.spline_type_set(type= 'POLY')     #change to poly spline
        cv.data.dimensions = '2D'               #change to 2d
        cvOPS.delete(type='VERT')               #delete vertice
        objOPS.editmode_toggle()                #return in  object mode

        context.scene.objects.active = obj      #select mainCanvas
        objOPS.parent_set(type='OBJECT',
                          xmirror=False,
                          keep_transform=False) #parent Mask to canvas

        #Name the curve with "+ Mask.xxx" or "+ Mask"(no mask)
        context.scene.objects.active = cv       #return on the curve
        _cvName = self.curve_name
        cv.name = "cvs_" + _cvName              #name it

        objOPS.editmode_toggle()                #toggle curve edit
        cvOPS.vertex_add()                      #first: add a vertice
        cvOPS.handle_type_set(type='VECTOR')
        context.space_data.show_manipulator = True
        return {'FINISHED'}


#-----------------------------------------------close, mesh and unwrap
class CloseCurveUnwrap(Operator):
    """Close the curve, set to mesh and unwrap"""
    bl_description = "Convert Vector to Mesh"
    bl_idname = "artist_paint.curve_unwrap"
    bl_label = ""
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None and obj.name is not None:
            A = obj.type == 'CURVE'
            B = obj.mode == 'EDIT'
            C = obj.name.find('cvs')!=-1
            return A and B and C
        return False


    def execute(self, context):
        scene = context.scene
        tool_settings = scene.tool_settings
        cv = context.active_object               #the vector curve
        _cvName = cv.name[4:]                    #type "cvs_xxxxxx"
        obj = cv.parent                          #the main canvas
        objRz = obj.rotation_euler[2]            #if mainCanvas rotated

        #Operators
        cvOPS = bpy.ops.curve
        objOPS = bpy.ops.object
        meshOPS = bpy.ops.mesh
        paintOPS = bpy.ops.paint

        #----------------------------------------INIT
        if scene.artist_paint is not None:      #if main canvas isn't erased
            if len(scene.artist_paint) !=0:
                for main_canvas in scene.artist_paint: #look main canvas name
                    canvasName = (main_canvas.filename)[:-4]   #find the name of the maincanvas
                    canvasDimX = main_canvas.dimX
                    canvasDimY = main_canvas.dimY
                    break
        else:
            return {'FINISHED'}

        #----------------------------------------------CURVE
        cvOPS.select_all(action='TOGGLE')        #Init selection
        cvOPS.select_all(action='TOGGLE')        #select points
        cvOPS.cyclic_toggle()                    #close spline 'create faces
        cv.data.dimensions = '2D'                #change the space
        objOPS.editmode_toggle()                 #return to object mode

        #----------------------------------------DUPLICAT-PARENTt 2x curves
        obj.select = False
        cv.select = True
        if cv.layers[0]==False:
            objOPS.move_to_layer(layers=(True, False, False, False,
                                    False, False, False, False, False,
                                    False, False, False, False, False,
                                    False, False, False, False, False,
                                    False))           #move to layer1
        objOPS.duplicate_move()
        cvDupli = context.object

        #parent curveDupli to Canvas
        cv.select = False
        cvDupli.select = True
        scene.objects.active = obj               #select the Canvas
        objOPS.parent_set(type='OBJECT',
                            keep_transform=True)#parent Curve to Canvas
        objOPS.move_to_layer(layers=(False, False, False, False,
                                False, False, False, False, False,
                                False, False, False, False, False,
                                False, False, False, False, False,
                                True))           #move to layer20
        context.space_data.layers[19] = False    #layer20 invisible
        cvDupli.select = False
        #parent curve to Canvas
        cv.select = True
        scene.objects.active = obj               #select the Canvas
        objOPS.parent_set(type='OBJECT',
                            xmirror=False,
                            keep_transform=True)#parent curve to Canvas

        #--------------------------------------------------NEW MESH MASK
        scene.objects.active = cv
        objOPS.convert(target='MESH')            #convert to mesh
        mk = context.object                      #overwrite cv with new mask
        mk.name = "msk_" + _cvName               #name mask with curve name
        scene.objects.active = obj
        #init rotation
        bpy.ops.transform.rotate(value=-objRz,
                                 axis=(0, 0, 1),
                                 constraint_orientation='GLOBAL')

        scene.objects.active = mk
        objOPS.editmode_toggle()                 #mask in edit mode
        meshOPS.select_all(action='TOGGLE')      #select all
        bpy.ops.mesh.edge_face_add()
        meshOPS.normals_make_consistent(inside=False)#Normals outside
        bpy.ops.uv.project_from_view(camera_bounds=True,
                                    correct_aspect=False,
                                    scale_to_bounds=False)#uv cam unwrap

        for mat in bpy.data.materials:
            if mat.name == canvasName :          #if mainCanvas Mat exist
                cv.data.materials.append(mat)    #add main canvas mat
                paintOPS.add_texture_paint_slot(type='DIFFUSE_COLOR',
                                            name=mk.name,
                                            width=canvasDimX,
                                            height=canvasDimY,
                                            color=(1, 1, 1, 0),
                                            alpha=True,
                                            generated_type='BLANK',
                                            float=False)
                break
        objOPS.editmode_toggle()                 #return in object mode

        scene.objects.active = obj               #Select the  maincanvas
        #return to rotation state
        bpy.ops.transform.rotate(value=objRz,
                                 axis=(0, 0, 1),
                                 constraint_orientation='GLOBAL')

        #------------------------------------------------------OPTIONS
        cvDupli.name = "cvs_" + _cvName

        scene.objects.active = mk
        if context.mode != 'PAINT_TEXTURE':
            paintOPS.texture_paint_toggle()      #return in Paint mode
        context.object.data.use_paint_mask = True
        tool_settings.image_paint.use_occlude = False
        tool_settings.image_paint.use_backface_culling = False
        tool_settings.image_paint.use_normal_falloff = False
        tool_settings.image_paint.seam_bleed = 0
        return {'FINISHED'}


#-------------------------------------------Invert all mesh mask
class CurvePolyInvert(Operator):
    """Inverte Mesh Mask in Object mode only"""
    bl_idname = "artist_paint.inverted_mask"
    bl_description = "Inverte curve to Mesh Mask"
    bl_label = "Inverted mesh Mask"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None and obj.name is not None:
            A = obj.type == 'CURVE'
            B = obj.mode == 'EDIT'
            C = obj.name.find('cvs')!=-1
            return A and B and C
        return False

    def execute(self, context):
        scene = context.scene
        tool_settings = scene.tool_settings
        #Operators
        objOPS = bpy.ops.object
        meshOPS = bpy.ops.mesh
        paintOPS = bpy.ops.paint

        #----------------------------------------------------INIT
        if scene.artist_paint is not None:       #if main canvas isn't erased
            if len(scene.artist_paint) !=0:      #look main_canvas data
                for main_canvas in scene.artist_paint:
                    canvasName = (main_canvas.filename)[:-4]
                    canvasDimX = main_canvas.dimX
                    canvasDimY = main_canvas.dimY
                    break
        else:
            return {'FINISHED'}

        #---------------------------------------------------INIT CURVE
        cv = context.active_object               #save active curve
        _cvName = cv.name[4:]                    #Find the genuine name
        mainCanv = cv.parent                     #Select canvas
        objRz = mainCanv.rotation_euler[2]       #if mainCanvas rotated

        #---------------------------------------------------DUPLICATION
        objOPS.editmode_toggle()                 #return in object mode
        objOPS.duplicate_move()                  #duplicate the curve
        cvTemp = context.active_object           #save cvTemp
        cvTemp.select = False                    #deselect cvTemp

        cv.select = False                        #deselect the 'cvs' curve
        mainCanv.select = True
        scene.objects.active = mainCanv          #active the main Canvas
        if mainCanv.mode == 'TEXTURE_PAINT':
            paintOPS.texture_paint_toggle()         #return object mode
        objOPS.duplicate_move()                  #duplicate the main canvas
        objOPS.convert(target='CURVE')           #convert active in curve
        canvTemp = context.active_object         #save canvTemp

        canvTemp.select = True                   #select the canvas curve
        cvTemp.select = True
        scene.objects.active = cvTemp            #active the cvTemp
        objOPS.join()                            #join both curves
        objOPS.convert(target='MESH')            #convert active in mesh
        objInv = context.active_object           #save the new Inverted Mask
        objOPS.move_to_layer(layers=(True, False, False, False,
                                False, False, False, False, False,
                                False, False, False, False, False,
                                False, False, False, False, False,
                                False))           #move to layer0

        #---------------------------------------------------UV PROJECT
        objInv.select = True                     #select the inverted mask
        scene.objects.active = mainCanv          #active the main Canvas
        objOPS.parent_set(type='OBJECT',
                          xmirror=False,
                          keep_transform=True)  #parent: Inverted mask to Canvas

        scene.objects.active = mainCanv          #select again the Canvas
        bpy.ops.transform.rotate(value=-objRz,
                                 axis=(0, 0, 1),
                                 constraint_orientation='GLOBAL')

        scene.objects.active = objInv            #Active the inverted mask
        objInv.name = "inv_" + _cvName           #name the Inverted Mask
        objInv.location[2] = 0.01                #Raise the Z level inv. mask
        objOPS.editmode_toggle()                 #go in edit mode
        bpy.ops.mesh.select_all(action='TOGGLE') #select all vertice
        meshOPS.normals_make_consistent(inside=False)#Normals outside
        bpy.ops.uv.project_from_view(camera_bounds=True,
                                    correct_aspect=False,
                                    scale_to_bounds=True)#uv cam unwrap

        for mat in bpy.data.materials:
            if mat.name == canvasName :          #if mainCanvas Mat exist
                objInv.data.materials.append(mat)    #add mainCanvas mat
                paintOPS.add_texture_paint_slot(type='DIFFUSE_COLOR',
                                            name=objInv.name,
                                            width=canvasDimX,
                                            height=canvasDimY,
                                            color=(1, 1, 1, 0),
                                            alpha=True,
                                            generated_type='BLANK',
                                            float=False)
                break
        objOPS.editmode_toggle()                 #return object mode
        #return to rotation state
        scene.objects.active = mainCanv          #select the Canvas
        bpy.ops.transform.rotate(value=objRz,
                                 axis=(0, 0, 1),
                                 constraint_orientation='GLOBAL')

        #--------------------------------------------------OPTIONS
        scene.objects.active = objInv            #active the Inverted Mask
        if context.mode != 'PAINT_TEXTURE':
            paintOPS.texture_paint_toggle()      #return in Paint mode
        context.object.data.use_paint_mask = True
        tool_settings.image_paint.use_occlude = False
        tool_settings.image_paint.use_backface_culling = False
        tool_settings.image_paint.use_normal_falloff = False
        tool_settings.image_paint.seam_bleed = 0
        return {'FINISHED'}


class SetSymmetryOrigin(Operator):
    """Set Symmetry Origin"""
    bl_idname = "artist_paint.set_symmetry_origin"
    bl_label = "Set Symmetry Origin"
    bl_description = "Move the symetry origin!"

    @classmethod
    def poll(self, context):
        A = pollAPT(self, context)
        B = context.mode == 'PAINT_TEXTURE'
        return A and B

    def execute(self, context):
        paintOPS = bpy.ops.paint
        paintOPS.texture_paint_toggle()                #return in object mode
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        paintOPS.texture_paint_toggle()                #return in paint mode
        return {'FINISHED'}


class ResetOrigin(Operator):
    """"Reset Canvas Origin"""
    bl_idname = "artist_paint.reset_origin"
    bl_label = "Reset Canvas Origin"
    bl_description = "Reset the canvas origin!"

    @classmethod
    def poll(self, context):
        A = pollAPT(self, context)
        B = context.mode == 'PAINT_TEXTURE'
        return A and B

    def execute(self, context):
        paintOPS = bpy.ops.paint
        paintOPS.texture_paint_toggle()                #return in object mode
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        paintOPS.texture_paint_toggle()                #return in paint mode
        return {'FINISHED'}


#--------------------------------------------------flip  horiz. macro
class CanvasHoriz(Operator):
    """Canvas Flip Horizontal Macro"""
    bl_idname = "artist_paint.canvas_horizontal"
    bl_label = "Canvas horiz"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = context.active_object.type == 'MESH'
            B = pollAPT(self, context)
            return A and B

    def execute(self, context):
        bpy.ops.paint.texture_paint_toggle()     #toggle Object mode

        # Horizontal mirror
        bpy.ops.transform.mirror(constraint_axis=(True, False, False))

        bpy.ops.paint.texture_paint_toggle()     #return Paint mode
        return {'FINISHED'}


#--------------------------------------------------flip vertical macro
class CanvasVertical(Operator):
    """Canvas Flip Vertical Macro"""
    bl_idname = "artist_paint.canvas_vertical"
    bl_label = "Canvas Vertical"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = context.active_object.type == 'MESH'
            B = pollAPT(self, context)
            return A and B

    def execute(self, context):
        bpy.ops.paint.texture_paint_toggle()    #toggle Object mode

        # Vertical mirror
        bpy.ops.transform.mirror(constraint_axis=(False, True, False))

        bpy.ops.paint.texture_paint_toggle()    #toggle Paint mode
        return {'FINISHED'}


#-------------------------------------------------ccw15
class RotateCanvasCCW15(Operator):
    """Image Rotate CounterClockwise 15 Macro"""
    bl_description = "Rotate from prefs. custom angle, default=15°."
    bl_idname = "artist_paint.rotate_ccw_15"
    bl_label = "Canvas Rotate CounterClockwise 15°"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = context.active_object.type == 'MESH'
            B = pollAPT(self, context)
            return A and B

    def execute(self, context):
        scene = context.scene
        addon_prefs = get_addon_preferences()
        guides_are_activated =  scene.guides_are_activated
        CustomAngle = math.radians(addon_prefs.customAngle)
        _bool01 = scene.canvas_in_frame
        _bool02 = scene.ArtistPaint_Bool02
        _bool03 = scene.prefs_are_locked
        _bool04 = scene.locking_are_desactived

        #init
        obj = context.active_object
        _obName = obj.name
        _camName = "Camera_" + _obName

        if guides_are_activated:             #remove guides
            if scene.prefs_are_locked:     #prefs locked
                scene.prefs_are_locked = False #desactivate the lock
                scene.locking_are_desactived = True  #prefs_was_locked
            bpy.ops.artist_paint.guides_toggle()
            scene.ArtistPaint_Bool02 = True #rotation sans guide

        #toggle texture mode/object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 15 degrees left
        bpy.ops.transform.rotate(value=CustomAngle,
                        axis=(0, 0, 1),
                        constraint_axis=(False, False, True))

        if _bool01 == True:                     #option Frame contraint
            bpy.ops.view3d.camera_to_view_selected()

        for cam  in bpy.data.objects:
            if cam.name == _camName:
                cam.select = True
                context.scene.objects.active = cam


        bpy.ops.object.select_all(action='DESELECT')
        ob = bpy.data.objects[_obName]
        ob.select = True
        context.scene.objects.active = ob

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------cw15
class RotateCanvasCW15(Operator):
    """Image Rotate Clockwise 15 Macro"""
    bl_description = "Rotate from prefs. custom angle, default=15°."
    bl_idname = "artist_paint.rotate_cw_15"
    bl_label = "Canvas Rotate Clockwise 15°"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = context.active_object.type == 'MESH'
            B = pollAPT(self, context)
            return A and B

    def execute(self, context):
        scene = context.scene
        addon_prefs = get_addon_preferences()
        guides_are_activated =  scene.guides_are_activated
        CustomAngle = math.radians(addon_prefs.customAngle)
        _bool01 = context.scene.canvas_in_frame
        _bool02 = context.scene.ArtistPaint_Bool02

        #init
        obj = context.active_object
        _obName = obj.name
        _camName = "Camera_" + _obName

        if guides_are_activated:             #remove guides
            if scene.prefs_are_locked:     #prefs locked
                scene.prefs_are_locked = False #desactivate the lock
                scene.locking_are_desactived = True  #prefs_was_locked
            bpy.ops.artist_paint.guides_toggle()
            scene.ArtistPaint_Bool02 = True #rotation sans guide

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 15 degrees left
        bpy.ops.transform.rotate(value=-(CustomAngle),
                                axis=(0, 0, 1),
                                constraint_axis=(False, False, True))

        if _bool01 ==True:                     #option Frame contraint
            bpy.ops.view3d.camera_to_view_selected()

        for cam  in bpy.data.objects:
            if cam.name == _camName:
                cam.select = True
                context.scene.objects.active = cam

        bpy.ops.object.select_all(action='DESELECT')
        ob = bpy.data.objects[_obName]
        ob.select = True
        context.scene.objects.active = ob

        #toggle texture mode/object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------ccw 90
class RotateCanvasCCW(Operator):
    """Image Rotate CounterClockwise 90 Macro"""
    bl_idname = "artist_paint.rotate_ccw_90"
    bl_label = "Canvas Rotate CounterClockwise 90"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = context.active_object.type == 'MESH'
            B = pollAPT(self, context)
            return A and B

    def execute(self, context):
        _bool01 = context.scene.canvas_in_frame
        #init
        obj = context.active_object
        _obName = obj.name
        _camName = "Camera_" + _obName
        #http://blender.stackexchange.com/users/660/mutant-bob
        select_mat = obj.data.materials[0].texture_slots[0].\
                                            texture.image.size[:]
        if select_mat[0] >= select_mat[1]:
            camRatio = select_mat[0]/select_mat[1]
        else:
            camRatio = select_mat[1]/select_mat[0]
        #(988, 761) X select_mat[0] Y select_mat[1]

        #resolution
        rnd = context.scene.render
        if rnd.resolution_x==select_mat[0]:
            rnd.resolution_x= select_mat[1]
            rnd.resolution_y= select_mat[0]
        elif rnd.resolution_x==select_mat[1]:
            rnd.resolution_x= select_mat[0]
            rnd.resolution_y= select_mat[1]

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 90 degrees left
        bpy.ops.transform.rotate(value=1.5708,
                                axis=(0, 0, 1),
                                constraint_axis=(False, False, True),
                                constraint_orientation='GLOBAL',
                                mirror=False,
                                proportional='DISABLED',
                                proportional_edit_falloff='SMOOTH',
                                proportional_size=1)
        if _bool01 == True:
            bpy.ops.view3d.camera_to_view_selected()

        #Init Selection
        bpy.ops.object.select_all(action='TOGGLE')
        bpy.ops.object.select_all(action='DESELECT')

        #select plane
        ob = bpy.data.objects[_obName]
        ob.select = True
        context.scene.objects.active = ob

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------cw 90
class RotateCanvasCW(Operator):
    """Image Rotate Clockwise 90 Macro"""
    bl_idname = "artist_paint.rotate_cw_90"
    bl_label = "Canvas Rotate Clockwise 90"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = context.active_object.type == 'MESH'
            B = pollAPT(self, context)
            return A and B

    def execute(self, context):
        _bool01 = context.scene.canvas_in_frame
        #init
        obj = context.active_object
        _obName = obj.name
        _camName = "Camera_" + _obName
        #http://blender.stackexchange.com/users/660/mutant-bob
        select_mat = obj.data.materials[0].texture_slots[0].\
                                            texture.image.size[:]

        if select_mat[0] >= select_mat[1]:
            camRatio = select_mat[0]/select_mat[1]
        else:
            camRatio = select_mat[1]/select_mat[0]
        #(988, 761) X select_mat[0] Y select_mat[1]

        #resolution
        rnd = context.scene.render
        if rnd.resolution_x==select_mat[0]:
            rnd.resolution_x= select_mat[1]
            rnd.resolution_y= select_mat[0]
        elif rnd.resolution_x==select_mat[1]:
            rnd.resolution_x= select_mat[0]
            rnd.resolution_y= select_mat[1]

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 90 degrees left
        bpy.ops.transform.rotate(value=-1.5708,
                    axis=(0, 0, 1),
                    constraint_axis=(False, False, True),
                    constraint_orientation='GLOBAL',
                    mirror=False,
                    proportional='DISABLED',
                    proportional_edit_falloff='SMOOTH',
                    proportional_size=1)

        if _bool01 == True:
            bpy.ops.view3d.camera_to_view_selected()

        #Init Selection
        bpy.ops.object.select_all(action='TOGGLE')
        bpy.ops.object.select_all(action='DESELECT')

        #select plane
        ob = bpy.data.objects[_obName]
        ob.select = True
        context.scene.objects.active = ob

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------image rotation reset
class CanvasResetrot(Operator):
    """Canvas Rotation Reset Macro"""
    bl_idname = "artist_paint.canvas_resetrot"
    bl_label = "Canvas Reset Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = context.active_object.type == 'MESH'
            B = pollAPT(self, context)
            return A and B

    def execute(self, context):
        scene = context.scene                             #init
        tool_settings = scene.tool_settings
        _bool2 = context.scene.ArtistPaint_Bool02

        if scene.artist_paint is not None:      #if main canvas isn't erased
            if len(scene.artist_paint) !=0:
                for main_canvas in scene.artist_paint: #look main canvas name
                    canvasName = (main_canvas.filename)[:-4]   #find the name of the maincanvas
                    _camName = "Camera_" + canvasName
                    canvasDimX = main_canvas.dimX
                    canvasDimY =  main_canvas.dimY
                for obj in scene.objects:
                    if obj.name == canvasName :      #if mainCanvas Mat exist
                        scene.objects.active = obj
                        break
        else:
            return {'FINISHED'}

        #changing
        obj = context.active_object
        if canvasDimX >= canvasDimY:
            camRatio = canvasDimX/canvasDimY
        else:
            camRatio = 1

        #resolution
        rnd = context.scene.render
        rnd.resolution_x= canvasDimX
        rnd.resolution_y= canvasDimY

        #reset canvas rotation
        bpy.ops.object.rotation_clear()
        bpy.ops.view3d.camera_to_view_selected()

        for cam  in bpy.data.objects:
            if cam.name == _camName:
                cam.select = True
                scene.objects.active = cam
        context.object.data.ortho_scale = camRatio

        bpy.ops.object.select_all(action='DESELECT')
        obj.select = True
        context.scene.objects.active = obj

        if _bool2 == True:                         #if rotation
            bpy.ops.artist_paint.guides_toggle()    #add guides
            scene.ArtistPaint_Bool02 = False   #init the rotation state

        if scene.locking_are_desactived:          #prefs_was_locked
            bpy.ops.artist_paint.prefs_lock_toggle()    #lock the prefs
            scene.locking_are_desactived = False #init the locking state
        return {'FINISHED'}

#########################################################experimental operations

class ReprojectMask(bpy.types.Operator):
    """Reproject Mask"""
    bl_idname = "artist_paint.reproject_mask" 
                                     
     
    bl_label = "Reproject Mask by View"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        bpy.ops.object.editmode_toggle() #toggle edit mode
        bpy.ops.uv.project_from_view(camera_bounds=True, correct_aspect=False, scale_to_bounds=False) #project from view
        bpy.ops.object.editmode_toggle() #toggle back from edit mode
        bpy.ops.object.convert(target='MESH')#in obj mode, convert to mesh for correction on Artist Panel Vector Masks/Gpencil Masks

        bpy.ops.paint.texture_paint_toggle() #toggle texpaint
        return {'FINISHED'}
    
#next operator
class SolidfyDifference(bpy.types.Operator):
    """Solidify and Difference Mask"""
    bl_idname = "artist_paint.solidfy_difference"
    bl_label = "Add Solidy and Difference Bool"
    bl_options = { 'REGISTER','UNDO' }
    
    def execute(self, context):
        scene = context.scene
                
        
        #new code
        sel = bpy.context.selected_objects
        act = bpy.context.scene.objects.active
        
        for obj in sel:
            context.scene.objects.active = obj#set active to selected
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.dissolve_faces()#to get a clean single face for paint projection
            bpy.ops.object.editmode_toggle()

            bpy.ops.object.modifier_add(type='SOLIDIFY')#set soldifiy for bool
            bpy.context.object.modifiers["Solidify"].thickness = 0.3#thicker than active
            bpy.ops.transform.translate(value=(0, 0, 0.01), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)#attempt to only move bool brush up in Z
            
            context.scene.objects.active = act#reset active 
            
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.dissolve_faces()
            bpy.ops.object.editmode_toggle()

            
            bpy.ops.object.modifier_add(type='SOLIDIFY')#basic soldify for boolean
            bpy.ops.transform.translate(value=(0, 0, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)#to move active 0 in Z
                
            
            bpy.ops.btool.boolean_diff()#call booltool
                
            
            return {'FINISHED'}           

        
        #user moves parent and then adjusts child
        #user calls reproject while in obj mode which returns mask to texpaint
        
#next operator
class SolidfyUnion(bpy.types.Operator):
    """Solidify and Union Mask"""
    bl_idname = "artist_paint.solidfy_union"
    bl_label = "Add Solidy and Union Bool"
    bl_options = { 'REGISTER','UNDO' }
    
    def execute(self, context):
        scene = context.scene
                
        
        #new code
        sel = bpy.context.selected_objects
        act = bpy.context.scene.objects.active
        
        for obj in sel:
            context.scene.objects.active = obj#set active to selected
            
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.dissolve_faces()#to get a single face for paint projection
            bpy.ops.object.editmode_toggle()
            
            bpy.ops.object.modifier_add(type='SOLIDIFY')#set soldifiy for bool
            bpy.context.object.modifiers["Solidify"].thickness = 0.3#thicker than active
            #bpy.ops.transform.translate(value=(0, 0, 0.01), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)#attempt to only move bool brush up in Z
            
            context.scene.objects.active = act#reset active 
            
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.dissolve_faces()
            bpy.ops.object.editmode_toggle()
            
            bpy.ops.object.modifier_add(type='SOLIDIFY')#basic soldify for boolean
            bpy.context.object.modifiers["Solidify"].thickness = 0.3#thicker than active
            #bpy.ops.transform.translate(value=(0, 0, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)#to move active 0 in Z
                
            
            bpy.ops.btool.boolean_union()#call booltool
                
            
            return {'FINISHED'}           

        
        #user moves parent and then adjusts child
        #user calls reproject while in obj mode which returns mask to texpaint
        
        
#next operator
class RemoveMods(bpy.types.Operator):
    """Remove Modifiers"""
    bl_idname = "artist_paint.remove_modifiers"
    bl_label = "Remove Modifiers"
    bl_options = { 'REGISTER','UNDO' }
    
    def execute(self, context):
        scene = context.scene
                
        
        #new code
        context = bpy.context
        scene = context.scene
        obj = context.object

        # get a reference to the current obj.data
        old_mesh = obj.data

        # settings for to_mesh
        apply_modifiers = False
        settings = 'PREVIEW'
        new_mesh = obj.to_mesh(scene, apply_modifiers, settings)

        # object will still have modifiers, remove them
        obj.modifiers.clear()

        # assign the new mesh to obj.data 
        obj.data = new_mesh

        # remove the old mesh from the .blend
        bpy.data.meshes.remove(old_mesh)
        bpy.context.object.draw_type = 'TEXTURED'

        
                
            
        return {'FINISHED'}



##############################################################  panel
class ArtistPanel(Panel):
    bl_label = "Artist Paint Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Artist Paint 2D"


    @classmethod
    def poll(self, cls):
        return bpy.context.scene.render.engine == 'BLENDER_RENDER'

    def draw_header(self, context):
        if context.scene.UI_is_activated:
            pic = 'FILE_TICK'
        else:
            pic = 'X_VEC'
        self.layout.operator("artist_paint.load_init", text = "",
                                                    icon = pic)

    def draw(self, context):
        scene = context.scene
        rs = scene.render
        addon_prefs = get_addon_preferences()
        buttName_1 = str(addon_prefs.customAngle) +"°"
        buttName_2 = str(addon_prefs.customAngle) +"°"


        #layout.active
        layout = self.layout
        layout.active = layout.enabled = scene.UI_is_activated

        #change variables with prefs
        #------------------------------------------
        empty = scene.maincanvas_is_empty
        bordercrop_is_activated = scene.bordercrop_is_activated
        guides_are_activated =  scene.guides_are_activated
        PAL = scene.prefs_are_locked

        GAA = BIA = False
        if scene.artist_paint is not None:      #if main canvas isn't erased
            if len(scene.artist_paint) != 0:
                for main_canvas in scene.artist_paint: #look main canvas name
                    canvasName = (main_canvas.filename)[:-4]   #find the name of the maincanvas
                    _camName = "Camera_" + canvasName
                for cam in bpy.data.objects :
                    if cam.name == _camName:
                        if cam.data.show_guide == set(): #True = guides not visible
                            GAA = False
                        else:
                            GAA = True
                if rs.use_border or rs.use_crop_to_border:
                    BIA = True
                else:
                    BIA = False

        if PAL:
            BIA = addon_prefs.bordercrop
            GAA = addon_prefs.guides

        toolsettings = context.tool_settings
        ipaint = toolsettings.image_paint

        box = layout.box()
        col = box.column(align = True)
        row = col.row(align = True)
        row1 = row.split(align=True)
        row1.label(text="Image State")                #IMAGE STATE
        row2 = row.split(align=True)
        row2.operator("artist_paint.multitexture",
                    text='', icon="RENDERLAYERS")
        row2.operator("artist_paint.glsl",
                    text='', icon="RADIO")
        row2.scale_x = 1.00

        col.separator()
        row = col.row(align = True)
        row.operator("artist_paint.canvas_load",
                    text = "Import canvas", icon = 'IMAGE_COL')
        row.operator("artist_paint.reload_saved_state",
                                        icon = 'LOAD_FACTORY')

        row = col.row(align = True)
        row.operator("artist_paint.save_current",
                    text = "Save/Overwrite", icon = 'IMAGEFILE')
        row.operator("artist_paint.save_increm",
                    text = "Incremental Save", icon = 'SAVE_COPY')
        col.operator("render.opengl",
                    text = "Snapshot", icon = 'RENDER_STILL')

        box = layout.box()                             #MACRO
        col = box.column(align = True)
        col.label(text="Special Macros")               #?
        col.operator("artist_paint.create_brush_scene",
                text="Create Brush Maker Scene",
                icon='OUTLINER_OB_CAMERA')

        row = col.row(align = True)
        row1 = row.split(align=True)
        row1.operator("artist_paint.frontof_ccw",
                text="-"+buttName_1, icon = 'TRIA_LEFT')
        row1.scale_x = 0.40
        row2 = row.split(align=True)
        row2.operator("artist_paint.frontof_paint",
                text = "View Align 3D",
                icon = 'ERROR')
        row3 = row.split(align=True)
        row3.operator("artist_paint.frontof_cw",
                 text= "+"+buttName_2, icon = 'TRIA_RIGHT')
        row3.scale_x = 0.40
        col.label('')

        col =layout.column(align = True)
        col.separator()
        row = col.row(align = True)
        row1 = row.split(align=True)
        row1.label(text="Canvas Cam. Setup")         #INIT
        row2 = row.split(align=True)
        row2.operator("artist_paint.cameraview_paint",
                    text = "Camera",
                    icon = 'RENDER_REGION')
        row3 = row.split(align=True)

        Icon = 'CLIPUV_DEHLT' if BIA else 'BORDER_RECT'
        row3.operator("artist_paint.border_toggle",
                    text = "",
                    icon = Icon)

        Icun = 'CLIPUV_DEHLT' if GAA else 'MOD_LATTICE'
        row3.operator("artist_paint.guides_toggle",
                    text = "",
                    icon = Icun)

        Ican = 'LOCKED' if PAL else 'UNLOCKED'
        row3.operator("artist_paint.prefs_lock_toggle",
                    text = "",
                    icon = Ican)
        row3.scale_x = 1.60

        col.separator()
        box = layout.box()
        col = box.column(align = True)
        col.label(text="Canvas Masks Tools")       #OBJECTS MASKING TOOLS
        col.operator("artist_paint.trace_selection",
                    text = "Mesh Mask from Gpencil",
                    icon = 'OUTLINER_OB_MESH')

        col.separator()

        col.operator("artist_paint.curve_2dpoly",
                    text = "Make Vector Contour",
                    icon = 'PARTICLE_POINT')

        row = col.row(align = True)
        row.operator("artist_paint.curve_unwrap",
                    text = "To Mesh Mask",
                    icon = 'OUTLINER_OB_MESH')
        row.operator("artist_paint.inverted_mask",
                    text = "To Inverted Mesh Mask",
                    icon = 'MOD_TRIANGULATE')

        col.separator()

        row = col.row(align = True)
        col.prop(ipaint, "use_stencil_layer", text="Stencil Mask")
        if ipaint.use_stencil_layer == True:
            cel = box.column(align = True)
            cel.template_ID(ipaint, "stencil_image")
            cel.operator("image.new", text="New").\
                                        gen_context = 'PAINT_STENCIL'
            row = cel.row(align = True)
            row.prop(ipaint, "stencil_color", text="")
            row.prop(ipaint, "invert_stencil",
                        text="Invert the mask",
                        icon='IMAGE_ALPHA')
    
        col.separator()
    
        box = layout.box()                        #BOOL MASK AND REUSE
        col = box.column(align = True)
        row = col.row(align = True)
        row1 = row.split(align=True)
        row1.label(text="Bool")
        row1.scale_x = 0.50
        row.separator()
        row2 = row.split(align=True)
        row2.operator("artist_paint.solidfy_difference", text="Difference", icon = 'ROTACTIVE')
        row2.operator("artist_paint.solidfy_union", text="Union", icon = 'ROTATECOLLECTION')
        row2.scale_x = 1.00
        row.separator()
        row3 = row.split(align=True)
        row3.operator("artist_paint.reproject_mask",
                    text="Reproject", icon = 'NODE_SEL')
        row4 = row.split(align=True)
        row4.operator("artist_paint.remove_modifiers",
                    text="", icon='RECOVER_LAST')


        box = layout.box()                        #CANVAS FRAME CONSTRAINT
        col = box.column(align = True)
        row = col.row(align = True)
        row1 = row.split(align=True)
        row1.label(text="Mirror")
        row1.scale_x = 0.50
        row.separator()
        row2 = row.split(align=True)
        row2.prop(ipaint, "use_symmetry_x", text="Horizontal", toggle=True)
        row2.prop(ipaint, "use_symmetry_y", text="Vertical", toggle=True)
        row2.scale_x = 1.00
        row.separator()
        row3 = row.split(align=True)
        row3.operator("artist_paint.set_symmetry_origin",
                    text="New", icon='VIEW3D_VEC')
        row4 = row.split(align=True)
        row4.operator("artist_paint.reset_origin",
                    text="", icon='RECOVER_AUTO')



        col.separator()
        row = col.row(align = True)                     #FLIP
        row.operator("artist_paint.canvas_horizontal",
                    text="Canvas Flip Horizontal",
                    icon='ARROW_LEFTRIGHT')
        row.operator("artist_paint.canvas_vertical",
                    text = "Canvas Flip Vertical",
                    icon = 'FILE_PARENT')


        row = col.row(align = True)                    #ROTATION
        row.label(text="Rotation")
        row.prop(context.scene, "canvas_in_frame" ,
                                    text="Frame Constraint")
        row.enabled = pollAPT(self, context)
        row = col.row(align = True)

        row.operator("artist_paint.rotate_ccw_15",
                    text = "Rotate -" + buttName_1, icon = 'TRIA_LEFT')
        row.operator("artist_paint.rotate_cw_15",
                    text = "Rotate +" + buttName_2, icon = 'TRIA_RIGHT')

        row = col.row(align = True)
        row.operator("artist_paint.rotate_ccw_90",
                    text = "Rotate 90° CCW", icon = 'PREV_KEYFRAME')
        row.operator("artist_paint.rotate_cw_90",
                    text = "Rotate 90° CW", icon = 'NEXT_KEYFRAME')

        col.operator("artist_paint.canvas_resetrot",
                    text = "Reset Rotation", icon = 'CANCEL')


def update_panel(self, context):
    #author: Thks mano-wii
    try:
        bpy.utils.unregister_class(ArtistPanel)
    except:
        pass
    ArtistPanel.bl_category = context.user_preferences.addons[__name__].preferences.category
    bpy.utils.register_class(ArtistPanel)

#-----------------------------------------------Preferences of add-on
class ArtistPaintPanelPrefs(AddonPreferences):
    """Creates the 3D view > TOOLS > Artist Paint Panel"""
    bl_idname = __name__

    enable_Tab_APP_01 = bpy.props.BoolProperty(
            name = "Defaults",
            default=False)

    bordercrop = bpy.props.BoolProperty(
            name = "Bordercrop",
            default=False)

    guides = bpy.props.BoolProperty(
            name="Guides",
            default=False)

    customAngle = bpy.props.FloatProperty(
            name="Angle of rotation",
            default=15.00,
            min=1)

    category = bpy.props.StringProperty(
            name="Category",
            description="Choose a name for the category of the panel",
            default="Artist Paint 2D",
            update=update_panel)

    def check(context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "enable_Tab_APP_01", icon="QUESTION")
        if self.enable_Tab_APP_01:
            row = layout.row()
            row.prop(self,"bordercrop")
            row.prop(self,"guides")
            row.prop(self, "customAngle")
            row = layout.row(align=True)
            row.label(text="Panel's location (category): ")
            row.prop(self, "category", text="")


def register():
    bpy.utils.register_class(ArtistPaintPanelPrefs)
    bpy.utils.register_module(__name__)
    update_panel(None, bpy.context)

def unregister():
    bpy.utils.unregister_class(ArtistPaintPanelPrefs)
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
