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
from bpy.types import   AddonPreferences,\
                        Menu,\
                        Panel,\
                        UIList,\
                        Operator
from bpy.props import *
import math
import os
SEP = os.sep


########################
#      Properties      #
########################

class ArtistPaintPanelPrefs(AddonPreferences):
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
#       UI Tools       #WARNING = not used actually!
#######################
#----------------------------------------------Display message
class MessageOperator(Operator):
    bl_idname = "error.message"
    bl_label = "Message"

    message = StringProperty()

    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400, height=300)

    def draw(self, context):
        layout = self.layout
        layout.label("WARNING !")
        row = layout.row(align=True)
        row.label(self.message)
        layout.separator()


#######################
#       Classes       #
#######################
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
        return obj is not None and context.active_object.type == 'MESH'

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
        return obj is not None and context.active_object.type == 'MESH'

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
        return obj is not None and context.active_object.type == 'MESH'

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
class BrushMakerScene(Operator):
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


#------------------------------------------------------Shaderless
class CanvasShadeless(Operator):
    """Canvas made shadeless Macro"""
    bl_description = ""
    bl_idname = "artist_paint.canvas_shadeless"
    bl_label = "Canvas Shadeless"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        return obj is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        context.space_data.viewport_shade = 'TEXTURED'  #texture draw
        context.object.active_material.use_shadeless = True #shadeless
        #bpy.ops.view3d.localview()             #change to local view
        bpy.ops.paint.texture_paint_toggle()   #change to Texture Paint
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
        obj =  context.active_object
        return obj is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        #init
        obj = context.active_object
        _obName = obj.name
        _camName = "Camera_" + _obName

        context.space_data.viewport_shade = 'TEXTURED'  #texture draw
        context.object.active_material.use_shadeless = True #shadeless
        #bpy.ops.view3d.localview()             #change to local view
        bpy.ops.paint.texture_paint_toggle()   #change to Texture Paint

        #http://blender.stackexchange.com/users/660/mutant-bob
        select_mat = obj.data.materials[0].texture_slots[0].\
                                            texture.image.size[:]

        for cam  in bpy.data.objects:
            if cam.name == _camName:
                prefix = 'Already found a camera for this image : '
                bpy.ops.error.message('INVOKE_DEFAULT',
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
class TraceSelection(Operator):
    """Convert gpencil to mesh"""
    bl_idname = "artist_paint.trace_selection"
    bl_label = "Make Mesh Mask from Gpencil's drawing"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        return obj is not None and context.active_object.type == 'MESH'

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
        objProp.origin_set(type='ORIGIN_GEOMETRY') #origine to geometry

        objProp.editmode_toggle()             #return curve edit mode
        cvProp = bpy.ops.curve
        cvProp.cyclic_toggle()                   #inverte the spline
        cv.data.dimensions = '2D'

        objProp.editmode_toggle()               #return object mode
        objProp.convert(target='MESH')

        objProp.editmode_toggle()                 #return edit mode
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.dissolve_faces()
        bpy.ops.uv.project_from_view(camera_bounds=True,
                                        correct_aspect=False,
                                        scale_to_bounds=False)

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


#-----------------------------------------------Curve Bezier to Poly
class CurvePoly2d(Operator):
    """Curve added and made poly 2d Macro"""
    bl_description = "Create 2D Poly Vector Mask"
    bl_idname = "artist_paint.curve_2dpoly"
    bl_label = "Create 2D Bezier Vector Mask"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = obj.mode == 'TEXTURE_PAINT'
            B = obj.type == 'MESH'
            return A and B

    def execute(self, context):
        obj = context.object                   #selected canvas object
        objProp = bpy.ops.object

        bpy.ops.paint.texture_paint_toggle()    #return object mode
        bpy.ops.view3d.snap_cursor_to_center()    #center the cursor
        bpy.ops.curve.primitive_bezier_curve_add()      #add curve
        cv = context.object
        cvProp = bpy.ops.curve
        cv.layers[0]                  #place the curve on the layer 1
        bpy.ops.object.editmode_toggle()            #toggle curve edit
        cvProp.spline_type_set(type= 'POLY') #change to poly spline
        bpy.context.object.data.dimensions = '2D'     #change to 2d
        cvProp.delete(type='VERT')
        objProp.editmode_toggle()            #toggle object mode

        context.scene.objects.active = obj      #layer parent to canvas
        bpy.ops.object.parent_set(type='OBJECT',
                                    xmirror=False,
                                    keep_transform=False)
        context.scene.objects.active = cv
        cv.name = "Mask"
        objProp.editmode_toggle()                 #toggle curve edit
        cvProp.vertex_add()
        cvProp.handle_type_set(type='VECTOR')
        context.space_data.show_manipulator = False
        return {'FINISHED'}


#-----------------------------------------------close, mesh and unwrap
class CloseCurveunwrap(Operator):
    """Close the curve, set to mesh and unwrap"""
    bl_description = "Convert Vector to Mesh"
    bl_idname = "artist_paint.curve_unwrap"
    bl_label = ""
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        if obj is not None:
            A = obj.mode == 'EDIT'
            B = obj.type == 'CURVE'
            return A and B

    def execute(self, context):
        cv = context.object           #In curve edit, the vector curve
        _cvName = cv.name
        cvProp = bpy.ops.curve
        objProp = bpy.ops.object

        cvProp.select_all(action='TOGGLE')        #Init selection
        cvProp.select_all(action='TOGGLE')        #select points
        cvProp.cyclic_toggle()                    #close spline
        cv.data.dimensions = '2D'
        objProp.editmode_toggle()               #toggle object mode
        objProp.convert(target='MESH')            #convert to mesh
        obj = context.object
        objProp.editmode_toggle()                 #toggle edit mode
        bpy.ops.mesh.select_all(action='TOGGLE')     #select all
        bpy.ops.mesh.normals_make_consistent(inside=False)#Normals ouside
        bpy.ops.uv.project_from_view(correct_aspect=False)#uv cam unwrap
        objProp.editmode_toggle()               #toggle object mode
        obj.name = "+ " + _cvName              #name the new mask

        bpy.ops.paint.texture_paint_toggle()    #return in paint mode
        #ici add the material TO DO!
        context.scene.objects.active = obj.parent      #Mask parent to canvas
        return {'FINISHED'}


#-------------------------------------------Invert all mesh mask
class CurvePolyinvert(Operator):
    """Inverte Mesh Mask in Object mode only"""
    bl_idname = "artist_paint.inverted_mask"
    bl_description = "Inverte Mesh Mask in Object mode only"
    bl_label = "Inverte Mesh Mask"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.object
        if obj is not None:
            A = obj.mode=='TEXTURE_PAINT'
            B = obj.type == 'MESH'
            return A and B

    #Canvas selected &Actived mask  must be selected together
    def execute(self, context):
        objA = bpy.context.object                  #Active Mask
        objS = objA.parent                        #Select canvas
        objProp = bpy.ops.object

        bpy.ops.paint.texture_paint_toggle()        #toggle object mode
        objS.select = True                         #Select the canvas
        context.scene.objects.active = objA         #active the mask

        objProp.duplicate_move()               #duplicate mesh objects
        objProp.join()                     #join active & selected mesh
        objProp.convert(target='CURVE')       #convert active in curve
        mk = context.active_object            #cv the new result curve
        objProp.editmode_toggle()                 #toggle curve edit
        mk.data.dimensions = '2D'             #set to 2D = create face
        objProp.editmode_toggle()              #toggle curve mode
        objProp.convert(target='MESH')        #convert active in mesh

        objProp.editmode_toggle()                  #toggle edit mode
        bpy.ops.mesh.select_all(action='TOGGLE')      #deselect all
        bpy.ops.uv.project_from_view(scale_to_bounds=False)#uv cam unwrap
        objProp.editmode_toggle()                #return object mode

        mk.select = True                           #select canvas
        context.scene.objects.active = objS      #Mask parent to canvas
        bpy.ops.object.parent_set()
        context.scene.objects.active = mk      #Active the Inverted Mask
        mk.name = "- " + objA.name[1:]
        mk.location[2] = 0.01              #Raise the mask in Z level

        bpy.ops.paint.texture_paint_toggle()     #return Paint  mode
        #ici add the material TO DO!
        context.scene.objects.active = objS      #Mask parent to canvas
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
        return obj is not None and context.active_object.type == 'MESH'

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
        return obj is not None and context.active_object.type == 'MESH'

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
        return obj is not None and context.active_object.type == 'MESH'

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
class RotateCanvasCW15(Operator):
    """Image Rotate Clockwise 15 Macro"""
    bl_description = "Rotate from prefs. custom angle, default=15°."
    bl_idname = "artist_paint.rotate_cw_15"
    bl_label = "Canvas Rotate Clockwise 15°"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        return obj is not None and context.active_object.type == 'MESH'

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
class RotateCanvasCCW(Operator):
    """Image Rotate CounterClockwise 90 Macro"""
    bl_idname = "artist_paint.rotate_ccw_90"
    bl_label = "Canvas Rotate CounterClockwise 90"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        return obj is not None and context.active_object.type == 'MESH'

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
class RotateCanvasCW(Operator):
    """Image Rotate Clockwise 90 Macro"""
    bl_idname = "artist_paint.rotate_cw_90"
    bl_label = "Canvas Rotate Clockwise 90"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        return obj is not None and context.active_object.type == 'MESH'

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
class CanvasResetrot(Operator):
    """Canvas Rotation Reset Macro"""
    bl_idname = "artist_paint.canvas_resetrot"
    bl_label = "Canvas Reset Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj =  context.active_object
        return obj is not None and context.active_object.type == 'MESH'

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
class ArtistPanel(Panel):
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
                    text = "Import Canvas", icon = 'IMAGE_COL')
        row.operator("artist_paint.reload_saved_state",
                     icon = 'LOAD_FACTORY')

        row = col.row(align = True)
        row.operator("artist_paint.save_current",
                    text = "Save/Overwrite", icon = 'IMAGEFILE')
        row.operator("artist_paint.save_increm",
                    text = "Incremental Save", icon = 'SAVE_COPY')
        col.operator("render.opengl", \
                    text = "Snapshot", icon = 'RENDER_STILL')

        box = layout.box()                             #MACRO
        col = box.column(align = True)
        col.label(text="Special Macros")
        col.operator("artist_paint.create_brush_scene",
                text="Create Brush Maker Scene",
                icon='OUTLINER_OB_CAMERA')
        col.separator()
        col.operator("artist_paint.cameraview_paint",
                    text = "Add Shaderless Painting Camera",
                    icon = 'RENDER_REGION')

        box = layout.box()
        col = box.column(align = True)
        col.label(text="Object Masking Tools") #OBJECTS MASKING TOOLS
        col.operator("artist_paint.trace_selection",
                    text = "Mesh Mask from Gpencil",
                    icon = 'OUTLINER_OB_MESH')

        col.separator() #empty line

        row = col.row(align = True)
        row.operator("artist_paint.curve_2dpoly",
                    text = "Make Vector Mask",
                    icon = 'PARTICLE_POINT')
        row.operator("artist_paint.curve_unwrap",
                    text = "",
                    icon = 'OUTLINER_OB_MESH')

        col.separator() #empty line

        col.operator("artist_paint.inverted_mask",
                    text = "Mesh Mask Inversion",
                    icon = 'MOD_TRIANGULATE')

        col.separator() #empty line

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


        box = layout.box()

        col = box.column(align = True)          #CANVAS FRAME CONSTRAINT
        col.prop(context.scene, "ArtistPaint_Bool01" ,
                                    text="Canvas Frame Constraint")
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
