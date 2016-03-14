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

bl_info = {"name": "Paint Artist Panel",
           "author": "CDMJ, Spirou4D",
           "version": (1, 0, 6),
           "blender": (2, 76, 0),
           "location": "Toolbar > Misc Tab > Artist Panel",
           "description": "Art Macros.",
           "warning": "Run only in BI now",
           "category": "Paint"}

'''
Modif: 2016-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Modif: 2016-02'01 Patrick optimize the code
'''

import bpy
from bpy.props import *
import os
import math
SEP = os.sep

########################
#      Properties      #
########################

class ArtistPaintPanelPrefs(bpy.types.AddonPreferences):
    """Creates the 3D view > TOOLS > Artist Paint Panel"""
    bl_idname = __name__
    bl_options = {'REGISTER'}

    bpy.types.Scene.Enable_Tab_APP_01 = bpy.props.\
                                        BoolProperty(default=False)
    bpy.types.Scene.CustomAngle = bpy.props.FloatProperty(default=15.0)


    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "CustomAngle",\
                                    text="Custom angle of rotation")

        if context.scene.Enable_Tab_APP_01:
            row = layout.row()
            layout.label(text="– shortcuts _")



#######################
#       UI Tools       #
#######################
#----------------------------------------------Display message
class MessageOperator(bpy.types.Operator):
    bl_idname = "error.message"
    bl_label = "Message"
    type = StringProperty()
    message = StringProperty()

    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=400, height=300)

    def draw(self, context):
        layout = self.layout
        layout.label("WARNING !")
        row = layout.row()
        row.label(self.message)
        row = layout.row()

#-----------------------------The OK button in the error dialog
class OkOperator(bpy.types.Operator):
    bl_idname = "error.ok"
    bl_label = "OK"
    def execute(self, context):
        return {'FINISHED'}



#######################
#       Classes       #
#######################
#-------------------------------------------------reload image
class ImageReload(bpy.types.Operator):
    """Reload Image Last Saved State"""
    bl_description = "Reload canvas's image"
    bl_idname = "artist_paint.reload_saved_state"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            return context.active_object.type == 'MESH'
        return False

    def execute(self, context):
        original_type = context.area.type
        context.area.type = 'IMAGE_EDITOR'

        #return image to last saved state
        bpy.ops.image.reload()
        context.area.type = original_type
        return {'FINISHED'}

#-------------------------------------------------image save
class SaveImage(bpy.types.Operator):
    """Save Image"""
    bl_description = ""
    bl_idname = "artist_paint.save_current"
    bl_label = "Save Image Current"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            return context.active_object.type == 'MESH'
        return False

    def execute(self, context):
        original_type = context.area.type
        context.area.type = 'IMAGE_EDITOR'

        #save as
        bpy.ops.image.save_as()

        context.area.type = original_type
        return {'FINISHED'}


#-------------------------------------------------image save
class SaveIncremImage(bpy.types.Operator):
    """Save Image"""
    bl_description = ""
    bl_idname = "artist_paint.save_increm"
    bl_label = "Save incremential Image Current"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            return context.active_object.type == 'MESH'
        return False

    def execute(self, context):
        original_type = context.area.type
        context.area.type = 'IMAGE_EDITOR'

        #init
        i = 1
        obj = context.active_object
        _obName = obj.name
        filePATH = obj.data.materials[0].texture_slots[0].\
                                            texture.image.filepath
        #//../../../.config/blender/Brushes/13_Tâche_de_café/Cafeina (1).png
        filePATH = (os.path.realpath(filePATH))
        #/.config/blender/Brushes/13_Tâche_de_café/Cafeina (1).png
        _Ext = os.path.splitext(filePATH)[1]
        _tempName = [ _obName + '_' + '{:03d}'.format(i) + _Ext ]

        HOME = os.path.expanduser("~")
        _Dir = HOME+os.path.dirname(filePATH)
        #/home/patrinux/.config/blender/Brushes/13_Tâche_de_café

        #verify the brushname
        l = os.listdir(_Dir)
        brushesName = [ f for f in l if os.path.\
                                isfile(os.path.join(_Dir,f)) ]
        brushesName = sorted(brushesName)
        for x in _tempName:
            for ob in brushesName:
                if ob == _tempName[-1]:
                    i += 1
                    _tempName = _tempName + [_obName + '_' + \
                                    '{:03d}'.format(i) + _Ext]

        #return image to last saved state
        chemin = os.path.join(_Dir,_tempName[-1])
        bpy.ops.image.save_as(filepath = chemin)

        context.area.type = original_type
        return {'FINISHED'}


#--------------------------------------------------Create brush
class BrushMakerScene(bpy.types.Operator):
    """Create Brush Scene"""
    bl_description = ""
    bl_idname = "artist_paint.create_brush_scene"
    bl_label = "Create Scene for Image Brush Maker"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        #A sub-function that controls the use of the class
        notBScene = True
        for sc in bpy.data.scenes:
            if sc.name == "Brush":
                notBScene = False
        return context.area.type=='VIEW_3D'and notBScene


    def execute(self, context):
        _name="Brush"
        for sc in bpy.data.scenes:
            if sc.name == "Brush":
                return {'FINISHED'}

        #add new scene and name it 'Brush'
        bpy.ops.scene.new(type='NEW')
        context.scene.name = _name

        #add lamp and move up 4 units in z
        # you can sort elements like this if the code
        # is gettings long
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

        #rename selected camera
        context.object.name="Tex Camera"

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


#--------------------------------------------------Shaderless
class CanvasShadeless(bpy.types.Operator):
    """Canvas made shadeless Macro"""
    bl_description = ""
    bl_idname = "artist_paint.canvas_shadeless"
    bl_label = "Canvas Shadeless"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            return context.active_object.type == 'MESH'
        return False

    def execute(self, context):
        #texture draw mode
        context.space_data.viewport_shade = 'TEXTURED'

        #shadeless material
        context.object.active_material.use_shadeless = True

        #change to local view
        bpy.ops.view3d.localview()

        #change to Texture Paint
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------cameraview paint
class CameraviewPaint(bpy.types.Operator):
    """Create a front-of camera in painting mode"""
    bl_description = ""
    bl_idname = "artist_paint.cameraview_paint"
    bl_label = "Cameraview Paint"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            return context.active_object.type == 'MESH'
        return False

    def execute(self, context):
        #init
        obj = context.active_object
        _obName = obj.name
        _camName = "Camera_" + _obName
        #http://blender.stackexchange.com/users/660/mutant-bob
        select_mat = obj.data.materials[0].texture_slots[0].\
                                            texture.image.size[:]

        for cam  in bpy.data.objects:
            if cam.name == _camName:
                prefix = 'Already found a camera for this image : '
                bpy.ops.error.message('INVOKE_DEFAULT',
                                        type = "Error",
                                    message =  prefix + _camName )
                return {'FINISHED'}

        #Cursor to center of world
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)

        #toggle on/off textpaint
        if obj and (obj.mode == 'TEXTURE_PAINT'):
            bpy.ops.paint.texture_paint_toggle()

        #add camera
        bpy.ops.object.camera_add(view_align=False,
                        enter_editmode=False,
                        location=(0, 0, 0),
                        rotation=(0, 0, 0),
                        layers=(True, False, False, False, False,
                                False, False, False, False, False,
                                False, False, False, False, False,
                                False, False, False, False, False))

        #ratio full
        context.scene.render.resolution_percentage = 100

        #name it
        context.object.name = _camName

        #switch to camera view
        bpy.ops.view3d.object_as_camera()

        #ortho view on current camera
        context.object.data.type = 'ORTHO'
        context.object.data.dof_object= obj

        #move cam up in Z by 1 unit
        bpy.ops.transform.translate(value=(0, 0, 1),
                    constraint_axis=(False, False, True),
                    constraint_orientation='GLOBAL',
                    mirror=False,
                    proportional='DISABLED',
                    proportional_edit_falloff='SMOOTH',
                    proportional_size=1)

        #switch on composition guides for use in cameraview paint
        context.object.data.show_guide = {'CENTER',
                            'CENTER_DIAGONAL', 'THIRDS', 'GOLDEN',
                            'GOLDEN_TRIANGLE_A', 'GOLDEN_TRIANGLE_B',
                            'HARMONY_TRIANGLE_A', 'HARMONY_TRIANGLE_B'
                            }

        #resolution
        rnd = bpy.data.scenes[0].render
        rndx = rnd.resolution_x = select_mat[0]
        rndy = rnd.resolution_y = select_mat[1]

        #orthoscale = ((rndx - rndy)/rndy)+1
        if rndx >= rndy:
            orthoscale = ((rndx - rndy)/rndy)+1
        elif rndx < rndy:
            orthoscale = 1
        context.object.data.ortho_scale = orthoscale

        #Init Selection
        bpy.ops.object.select_all(action='TOGGLE')
        bpy.ops.object.select_all(action='DESELECT')

        #select plane
        ob = bpy.data.objects[_obName]
        ob.select = True
        context.scene.objects.active = ob

        #selection to texpaint toggle
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------Gpencil to Mask in one step
class TraceSelection(bpy.types.Operator):
    """Convert gpencil to CURVE"""
    bl_idname = "artist_paint.trace_selection"
    bl_label = "Setup Mirror Canvas"
    bl_options = {'REGISTER', 'UNDO'}
    '''
    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            return context.active_object.type == 'MESH'
        return False
    '''
    def execute(self, context):
        scene = context.scene
        tool_settings = scene.tool_settings
        obj = context.object                 #select canvas object
        objProp = bpy.ops.object

        bpy.ops.gpencil.convert(type='CURVE', use_timing_data=True)
        bpy.ops.gpencil.data_unlink()

        bpy.ops.paint.texture_paint_toggle()    #return object mode
        objProp.select_by_type(type = 'CURVE')
        lrs = []
        for lay in bpy.data.objects:
            if lay.name.find('GP_Layer') != -1:
                lrs.append(lay)
        cv = lrs[-1]
        context.scene.objects.active = cv
        objProp.origin_set(type='ORIGIN_GEOMETRY')

        objProp.editmode_toggle()                 #return edit mode
        cvProp = bpy.ops.curve
        cvProp.cyclic_toggle()     #return curve object mode
        cv.data.dimensions = '2D'

        objProp.editmode_toggle()               #return object mode
        objProp.convert(target='MESH')

        objProp.editmode_toggle()                 #return edit mode
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.dissolve_faces()
        bpy.ops.uv.project_from_view(camera_bounds=True,
                                        correct_aspect=False,
                                        scale_to_bounds=False)
        #Add a material+texture diffuse
        mat = bpy.data.materials.new("default")
        cv.data.materials.append(mat)
        cv.active_material.use_shadeless = True

        #select canvas
        obj.select = True
        context.scene.objects.active = obj

        #layer parent to canvas
        bpy.ops.object.parent_set(type='OBJECT',
                                    xmirror=False,
                                    keep_transform=False)

        objProp.editmode_toggle()               #return object mode
        bpy.ops.paint.texture_paint_toggle()     #return paint mode
        tool_settings.image_paint.use_occlude = False
        tool_settings.image_paint.use_backface_culling = False
        tool_settings.image_paint.use_normal_falloff = False
        tool_settings.image_paint.seam_bleed = 0
        return {'FINISHED'}

#-----------------------------------------------Inverted Mask after init masking
class CurvePolyinvert(bpy.types.Operator):
    """Canvas Flip Horizontal Macro"""
    bl_idname = "artist_paint.inverted_mask" # must match a operator
    bl_label = "Inverted Mask"
    bl_options = { 'REGISTER', 'UNDO' }
    
    @classmethod
    def poll(self, context):
        if context.active_object:
            return context.active_object.type == 'MESH'
        else:
            return False
    
    def execute(self, context):
        
        scene = context.scene

        bpy.ops.object.select_by_type(type = 'MESH')
        #dup
        bpy.ops.object.duplicate_move()
        bpy.ops.object.convert(target='CURVE')
        bpy.context.object.data.dimensions = '2D'
        bpy.ops.object.join()
        bpy.ops.object.convert(target='MESH')        
        #toggle edit mode
        bpy.ops.object.editmode_toggle()        
        #selct all faces
        bpy.ops.mesh.select_all(action='TOGGLE')        
        #dissolve faces       
        
        #uv unwrap from camera view        
        bpy.ops.uv.project_from_view(camera_bounds=True, correct_aspect=True, scale_to_bounds=False)
        
        bpy.ops.object.editmode_toggle()
    
        bpy.ops.paint.texture_paint_toggle()

        
        return {'FINISHED'}


#-----------------------------------------------Curve Bezier to Poly
class CurvePoly2d(bpy.types.Operator):
    """Curve added and made poly 2d Macro"""
    bl_description = "Create Bezier2Poly Curve"
    bl_idname = "artist_paint.curve_2dpoly"
    bl_label = "Curve 2D Poly"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):
        #add curve
        bpy.ops.curve.primitive_bezier_curve_add(radius=1,
                                    view_align=False,
                                    enter_editmode=True,
                                    layers=(True, False, False,
                                    False, False, False, False,
                                    False, False, False, False,
                                    False, False, False, False,
                                    False, False, False, False,
                                    False))
        #change to poly spline
        bpy.ops.curve.spline_type_set(type= 'POLY')
        #change to 2d
        bpy.context.object.data.dimensions = '2D'
        return {'FINISHED'}


#-----------------------------------------------close, mesh and unwrap
class CloseCurveunwrap(bpy.types.Operator):
    """Close the curve, set to mesh and unwrap"""
    bl_description = "Close, mesh and unwrap"
    bl_idname = "artist_paint.curve_unwrap"
    bl_label = "Close and Unwrap"
    bl_options = { 'REGISTER', 'UNDO' }

    def execute(self, context):
        #deselect and select points
        bpy.ops.curve.select_all(action='TOGGLE')
        bpy.ops.curve.select_all(action='TOGGLE')

        #close curve
        bpy.ops.curve.cyclic_toggle()

        #toggle object mode
        bpy.ops.object.editmode_toggle()

        #convert to mesh
        bpy.ops.object.convert(target='MESH')

        #toggle edit mode
        bpy.ops.object.editmode_toggle()

        #select all
        bpy.ops.mesh.select_all(action='TOGGLE')

        #uv unwrap inside camera view
        bpy.ops.uv.project_from_view(camera_bounds=True,
                                    correct_aspect=False,
                                    scale_to_bounds=False)

        #tex paint toggle
        bpy.ops.object.editmode_toggle()
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#--------------------------------------------------flip  horiz. macro
class CanvasHoriz(bpy.types.Operator):
    """Canvas Flip Horizontal Macro"""
    bl_idname = "artist_paint.canvas_horizontal"
    bl_label = "Canvas horiz"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object:
            return context.active_object.type == 'MESH'
        return False

    def execute(self, context):

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        # Horizontal mirror
        bpy.ops.transform.mirror(constraint_axis=(True, False, False))

        #toggle object to texture
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#--------------------------------------------------flip vertical macro
class CanvasVertical(bpy.types.Operator):
    """Canvas Flip Vertical Macro"""
    bl_idname = "artist_paint.canvas_vertical"
    bl_label = "Canvas Vertical"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            return context.active_object.type == 'MESH'
        return False

    def execute(self, context):
        #toggle texture mode/object mode
        bpy.ops.paint.texture_paint_toggle()

        # Vertical mirror
        bpy.ops.transform.mirror(constraint_axis=(False, True, False))

        #toggle texture mode/object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------ccw15
class RotateCanvasCCW15(bpy.types.Operator):
    """Image Rotate CounterClockwise 15 Macro"""
    bl_description = "Rotate from prefs. custom angle, default=15°."
    bl_idname = "artist_paint.rotate_ccw_15"
    bl_label = "Canvas Rotate CounterClockwise 15°"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            return context.active_object.type == 'MESH'
        return False


    def execute(self, context):
        _customAngle = math.radians(context.scene.CustomAngle)
        _bool01 = context.scene.ArtistPaint_Bool01
        #init
        obj = context.active_object
        _obName = obj.name
        _camName = "Camera_" + _obName

        #toggle texture mode/object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 15 degrees left
        bpy.ops.transform.rotate(value=_customAngle,
                        axis=(0, 0, 1),
                        constraint_axis=(False, False, True))
        if _bool01 == True:
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
class RotateCanvasCW15(bpy.types.Operator):
    """Image Rotate Clockwise 15 Macro"""
    bl_description = "Rotate from prefs. custom angle, default=15°."
    bl_idname = "artist_paint.rotate_cw_15"
    bl_label = "Canvas Rotate Clockwise 15°"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            return context.active_object.type == 'MESH'
        return False

    def execute(self, context):
        _customAngle = math.radians(context.scene.CustomAngle)
        _bool01 = context.scene.ArtistPaint_Bool01
        #init
        obj = context.active_object
        _obName = obj.name
        _camName = "Camera_" + _obName

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 15 degrees left
        bpy.ops.transform.rotate(value=-(_customAngle),
                axis=(0, 0, 1),
                constraint_axis=(False, False, True))
        if _bool01 ==True:
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
class RotateCanvasCCW(bpy.types.Operator):
    """Image Rotate CounterClockwise 90 Macro"""
    bl_idname = "artist_paint.rotate_ccw_90"
    bl_label = "Canvas Rotate CounterClockwise 90"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            return context.active_object.type == 'MESH'
        return False

    def execute(self, context):
        _bool01 = context.scene.ArtistPaint_Bool01
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
class RotateCanvasCW(bpy.types.Operator):
    """Image Rotate Clockwise 90 Macro"""
    bl_idname = "artist_paint.rotate_cw_90"
    bl_label = "Canvas Rotate Clockwise 90"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            return context.active_object.type == 'MESH'
        return False

    def execute(self, context):
        _bool01 = context.scene.ArtistPaint_Bool01
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
class CanvasResetrot(bpy.types.Operator):
    """Canvas Rotation Reset Macro"""
    bl_idname = "artist_paint.canvas_resetrot"
    bl_label = "Canvas Reset Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            return context.active_object.type == 'MESH'
        return False

    def execute(self, context):
        #init
        obj = context.active_object
        _obName = obj.name
        _camName = "Camera_" + _obName
        #http://blender.stackexchange.com/users/660/mutant-bob
        #(988, 761) X select_mat[0] Y select_mat[1]
        select_mat = obj.data.materials[0].texture_slots[0].\
                                            texture.image.size[:]

        if select_mat[0] >= select_mat[1]:
            camRatio = select_mat[0]/select_mat[1]
        else:
            camRatio = select_mat[1]/select_mat[0]

        #resolution
        rnd = context.scene.render
        rnd.resolution_x= select_mat[0]
        rnd.resolution_y= select_mat[1]

        #reset canvas rotation
        bpy.ops.object.rotation_clear()
        bpy.ops.view3d.camera_to_view_selected()

        for cam  in bpy.data.objects:
            if cam.name == _camName:
                cam.select = True
                context.scene.objects.active = cam
        context.object.data.ortho_scale = camRatio

        #activate on composition guides
        context.object.data.show_guide = {'CENTER',
                    'CENTER_DIAGONAL', 'THIRDS', 'GOLDEN',
                    'GOLDEN_TRIANGLE_A', 'GOLDEN_TRIANGLE_B',
                    'HARMONY_TRIANGLE_A', 'HARMONY_TRIANGLE_B'}

        bpy.ops.object.select_all(action='DESELECT')
        ob = bpy.data.objects[_obName]
        ob.select = True
        context.scene.objects.active = ob
        return {'FINISHED'}





##############################################################  panel
class ArtistPanel(bpy.types.Panel):
    """A custom panel in the viewport toolbar"""
    bl_label = "Artist Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "BlenderPaint 2D"

    bpy.types.Scene.ArtistPaint_Bool01 = bpy.props.\
                                        BoolProperty(default=False)

    @classmethod
    def poll(self, cls):
        return bpy.context.scene.render.engine == 'BLENDER_RENDER'

    def draw(self, context):
        _strAngle = str(context.scene.CustomAngle)
        layout = self.layout
        toolsettings = context.tool_settings
        ipaint = context.tool_settings.image_paint

        box = layout.box()

        box.label(text="Image State")                #IMAGE STATE
        col = box.column(align = True)
        row = col.row(align = True)
        row.operator("import_image.to_plane",
                    text = "Import Img. as canvas", icon = 'IMAGE_COL')
        row.operator("artist_paint.reload_saved_state",
                     icon = 'LOAD_FACTORY')

        row = col.row(align = True)
        row.operator("artist_paint.save_current",
                    text = "Save/Overwrite", icon = 'IMAGEFILE')
        row.operator("artist_paint.save_increm",
                    text = "Incremental Save", icon = 'SAVE_COPY')
        col.operator("render.opengl", \
                    text = "OpenGL Render", icon = 'RENDER_STILL')

        col.label(text='') #empty line
        col.operator("artist_paint.create_brush_scene",
                text="Create Brush Maker Scene",
                icon='OUTLINER_OB_CAMERA')


        box = layout.box()                             #MACRO
        col = box.column(align = True)
        col.label(text="Special Macros")
        row = col.row(align = True)
        row.operator("artist_paint.canvas_shadeless",
                    text = "Shadeless Canvas", icon = 'FORCE_TEXTURE')
        row.operator("artist_paint.cameraview_paint",
                    text = "Add Painting Camera",
                    icon = 'RENDER_REGION')


        box = layout.box()
        col = box.column(align = True)
        col.label(text="Object Masking Tools") #OBJECTS MASKING TOOLS
        col.operator("artist_paint.trace_selection",
                    text = "Mask from Gpencil",
                    icon = 'CURVE_BEZCIRCLE')
        col.operator("artist_paint.inverted_mask",
                    text = "Mask Inversion",
                    icon = 'MOD_TRIANGULATE')

        col.separator() # empty line

        row = col.row(align = True)
        row.operator("artist_paint.curve_2dpoly",
                    text = "A. 2D Mask Maker",
                    icon = 'PARTICLE_POINT')
        row.operator("artist_paint.curve_unwrap",
                    text = "B. Close Mask & Unwrap",
                    icon = 'CURVE_NCIRCLE')


        col.separator() # empty line

        col.prop(ipaint, "use_stencil_layer", text="Stencil Mask")
        if ipaint.use_stencil_layer == True:
            cel = box.column(align = True)
            cel.template_ID(ipaint, "stencil_image")
            cel.operator("image.new", text="New").\
                                        gen_context = 'PAINT_STENCIL'
            row = cel.row(align = True)
            row.prop(ipaint, "stencil_color", text="")
            row.prop(ipaint, "invert_stencil",
                        text="Invert the mask", icon='IMAGE_ALPHA')


        box = layout.box()

        col = box.column(align = True)          #CANVAS FRAME CONTRAINT
        col.prop(context.scene, "ArtistPaint_Bool01" ,
                                    text="Canvas Frame Contraint")
        col.label(text="Mirror")                      #MIRROR FLIP
        row = col.row(align = True)
        row.operator("artist_paint.canvas_horizontal",
                    text="Canvas Flip Horizontal",
                    icon='ARROW_LEFTRIGHT')
        row.operator("artist_paint.canvas_vertical",
                    text = "Canvas Flip Vertical",
                    icon = 'FILE_PARENT')


        row = col.row(align = True)                    #ROTATION
        row.label(text="Rotation")
        row = col.row(align = True)
        buttName_1 = "Rotate " +_strAngle+"° CCW"
        buttName_2 = "-"+buttName_1
        row.operator("artist_paint.rotate_ccw_15",
                    text = buttName_1, icon = 'TRIA_LEFT')
        row.operator("artist_paint.rotate_cw_15",
                    text = buttName_2, icon = 'TRIA_RIGHT')

        row = col.row(align = True)
        row.operator("artist_paint.rotate_ccw_90",
                    text = "Rotate 90° CCW", icon = 'PREV_KEYFRAME')
        row.operator("artist_paint.rotate_cw_90",
                    text = "Rotate 90° CW", icon = 'NEXT_KEYFRAME')

        col.operator("artist_paint.canvas_resetrot",
                    text = "Reset Rotation", icon = 'CANCEL')



def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
