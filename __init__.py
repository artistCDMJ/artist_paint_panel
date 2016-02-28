# -*- coding: utf8 -*-
#
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


bl_info = {
    "name": "Paint Artist Panel",
    "author": "CDMJ,Patrick Depoix ",
    "version": (1, 0, 6),
    "blender": (2, 76, 0),
    "location": "Toolbar > Misc Tab > Artist Panel",
    "description": "Art Macros.",
    "warning": "",
    "category": "Paint",
}

import bpy

'''
Modif: 2016-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Modif: 2016-02'01 Patrick optimize the code
'''



#--------------------------------------------------Create brush
class MacroCreateBrush(bpy.types.Operator):
    """Image Brush Scene Setup Macro"""
     # must match a operator context, like
     # view3d, object or image and cannot have
     # more then one '.', if you need something
     # that is global use wm.create_brush
     # and uncomment from line 24-29
    bl_idname = "image.create_brush"
    bl_label = "Setup Scene for Image Brush Maker"
    bl_options = { 'REGISTER', 'UNDO' }

    '''
    @classmethod
    def poll(self, cls):
    ##################################
    #   A function that controls wether the operator can be accessed
    ##################################
    return context.area.type in {'VIEW3D'. 'IMAGE'}
    '''

    def execute(self, context):

        scene = context.scene

        #add new scene and name it 'Brush'
        bpy.ops.scene.new(type='NEW')
        bpy.context.scene.name = "Brush"

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
        #rename selected camera
        bpy.ops.object.camera_add(
          view_align=False,
          enter_editmode=False,
          location=(0, 0, 4),
          rotation=(0, 0, 0)
        )

        bpy.context.object.name="Tex Camera"

        #change scene size to 1K
        _RenderScene = bpy.context.scene.render
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
                break # this will break the loop after it is first ran
        return {'FINISHED'}


#--------------------------------------------------Shaderless
class CanvasShadeless(bpy.types.Operator):
    """Canvas made shadeless Macro"""
     # must match a operator context, like
     # view3d, object or image and cannot have
     # more then one '.', if you need something
     # that is global use wm.create_brush
     # and uncomment from line 24-29
    bl_idname = "image.canvas_shadeless"
    bl_label = "Canvas Shadeless"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):
        scene = context.scene

        #texture draw mode
        bpy.context.space_data.viewport_shade = 'TEXTURED'

        #shadeless material
        bpy.context.object.active_material.use_shadeless = True

        #change to local view and centerview
        bpy.ops.view3d.localview()

        #change to Texture Paint
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#--------------------------------------------------flip  horiz. macro
class CanvasHoriz(bpy.types.Operator):
    """Canvas Flip Horizontal Macro"""
     # must match a operator context, like
     # view3d, object or image and cannot have
     # more then one '.', if you need something
     # that is global use wm.create_brush
     # and uncomment from line 24-29
    bl_idname = "image.canvas_horizontal"
    bl_label = "Canvas horiz"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):

        scene = context.scene

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #flip canvas horizontal
        bpy.ops.transform.resize(value=(-1, 1, 1), \
        constraint_axis=(True, False, False), \
        constraint_orientation='GLOBAL', \
        mirror=False, proportional='DISABLED', \
        proportional_edit_falloff='SMOOTH', \
        proportional_size=1)

        #toggle object to texture
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#--------------------------------------------------flip vertical macro
class CanvasVertical(bpy.types.Operator):
    """Canvas Flip Vertical Macro"""
     # must match a operator context, like
     # view3d, object or image and cannot have
     # more then one '.', if you need something
     # that is global use wm.create_brush
     # and uncomment from line 24-29
    bl_idname = "image.canvas_vertical"
    bl_label = "Canvas Vertical"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):

        scene = context.scene

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #flip canvas horizontal
        bpy.ops.transform.resize(value=(1, -1, 1), \
        constraint_axis=(False, True, False), \
        constraint_orientation='GLOBAL', \
        mirror=False, \
        proportional='DISABLED', \
        proportional_edit_falloff='SMOOTH', \
        proportional_size=1)

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------ccw15
class RotateCanvasCCW15(bpy.types.Operator):
    """Image Rotate CounterClockwise 15 Macro"""
     # must match a operator context, like
     # view3d, object or image and cannot have
     # more then one '.', if you need something
     # that is global use wm.create_brush
     # and uncomment from line 24-29
    bl_idname = "image.rotate_ccw_15"
    bl_label = "Canvas Rotate CounterClockwise 15"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):

        scene = context.scene

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 15 degrees left
        bpy.ops.transform.rotate(value=0.261799, \
        axis=(0, 0, 1), \
        constraint_axis=(False, False, True), \
        constraint_orientation='GLOBAL', \
        mirror=False, \
        proportional='DISABLED', \
        proportional_edit_falloff='SMOOTH', \
        proportional_size=1)

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------cw15
class RotateCanvasCW15(bpy.types.Operator):
    """Image Rotate Clockwise 15 Macro"""
     # must match a operator context, like
     # view3d, object or image and cannot have
     # more then one '.', if you need something
     # that is global use wm.create_brush
     # and uncomment from line 24-29
    bl_idname = "image.rotate_cw_15"
    bl_label = "Canvas Rotate Clockwise 15"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):

        scene = context.scene

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 15 degrees left
        bpy.ops.transform.rotate(value=-0.261799, \
        axis=(0, 0, 1), \
        constraint_axis=(False, False, True), \
        constraint_orientation='GLOBAL', \
        mirror=False, \
        proportional='DISABLED', \
        proportional_edit_falloff='SMOOTH', \
        proportional_size=1)

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------ccw 90
class RotateCanvasCCW(bpy.types.Operator):
    """Image Rotate CounterClockwise 90 Macro"""
     # must match a operator context, like
     # view3d, object or image and cannot have
     # more then one '.', if you need something
     # that is global use wm.create_brush
     # and uncomment from line 24-29
    bl_idname = "image.rotate_ccw_90"
    bl_label = "Canvas Rotate CounterClockwise 90"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):

        scene = context.scene

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 90 degrees left
        bpy.ops.transform.rotate(value=1.5708, \
        axis=(0, 0, 1), \
        constraint_axis=(False, False, True), \
        constraint_orientation='GLOBAL', \
        mirror=False, \
        proportional='DISABLED', \
        proportional_edit_falloff='SMOOTH', \
        proportional_size=1)

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------cw 90
class RotateCanvasCW(bpy.types.Operator):
    """Image Rotate Clockwise 90 Macro"""
     # must match a operator context, like
     # view3d, object or image and cannot have
     # more then one '.', if you need something
     # that is global use wm.create_brush
     # and uncomment from line 24-29
    bl_idname = "image.rotate_cw_90"
    bl_label = "Canvas Rotate Clockwise 90"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):

        scene = context.scene

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 90 degrees left
        bpy.ops.transform.rotate(value=-1.5708, \
        axis=(0, 0, 1), \
        constraint_axis=(False, False, True), \
        constraint_orientation='GLOBAL', \
        mirror=False, \
        proportional='DISABLED', \
        proportional_edit_falloff='SMOOTH', \
        proportional_size=1)

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------reload image
class ImageReload(bpy.types.Operator):
    """Reload Image Last Saved State"""
    bl_idname = "image.reload_saved_state"
    bl_label = "Reload Image Save Point"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):
        scene = context.scene
        original_type = bpy.context.area.type
        bpy.context.area.type = 'IMAGE_EDITOR'

        #return image to last saved state
        bpy.ops.image.reload()
        bpy.context.area.type = original_type
        return {'FINISHED'}


#-------------------------------------------------image rotation reset
class CanvasResetrot(bpy.types.Operator):
    """Canvas Rotation Reset Macro"""
     # must match a operator context, like
     # view3d, object or image and cannot have
     # more then one '.', if you need something
     # that is global use wm.create_brush
     # and uncomment from line 24-29
    bl_idname = "image.canvas_resetrot"
    bl_label = "Canvas Reset Rotation"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):
        scene = context.scene

        #reset canvas rotation
        bpy.ops.object.rotation_clear()
        return {'FINISHED'}


#-------------------------------------------------cameraview paint
class CameraviewPaint(bpy.types.Operator):
     # must match a operator context, like
     # view3d, object or image and cannot have
     # more then one '.', if you need something
     # that is global use wm.create_brush
     # and uncomment from line 24-29
    bl_idname = "image.cameraview_paint"
    bl_label = "Cameraview Paint"
    bl_options = { 'REGISTER', 'UNDO' }



    def execute(self, context):

        scene = context.scene

        #toggle on/off textpaint

        obj = context.active_object

        if obj:
            mode = obj.mode
            # aslkjdaslkdjasdas
            if mode == 'TEXTURE_PAINT':
                bpy.ops.paint.texture_paint_toggle()

        #save selected plane by rename
        bpy.context.object.name = "canvas"
        #variable to get image texture dimensions -
        #thanks to Mutant Bob
        #http://blender.stackexchange.com/users/660/mutant-bob

        select_mat = bpy.context.active_object.data.materials[0].\
        texture_slots[0].texture.image.size[:]

        #add camera
        bpy.ops.object.camera_add(view_align=False, \
        enter_editmode=False, \
        location=(0, 0, 0), \
        rotation=(0, 0, 0), \
        layers=(True, False, False, False, False, False, False, False, \
        False, False, False, False, False, False, False, False, False, \
        False, False, False))

        #ratio full
        bpy.context.scene.render.resolution_percentage = 100

        #name it
        bpy.context.object.name = "Canvas View Paint"

        #switch to camera view
        bpy.ops.view3d.object_as_camera()

        #ortho view on current camera
        bpy.context.object.data.type = 'ORTHO'

        #move cam up in Z by 1 unit
        bpy.ops.transform.translate(value=(0, 0, 1), \
        constraint_axis=(False, False, True), \
        constraint_orientation='GLOBAL', \
        mirror=False, \
        proportional='DISABLED', \
        proportional_edit_falloff='SMOOTH', \
        proportional_size=1)

        #switch on composition guides for use in cameraview paint
        bpy.context.object.data.show_guide = {'CENTER', \
        'CENTER_DIAGONAL', 'THIRDS', 'GOLDEN', 'GOLDEN_TRIANGLE_A', \
        'GOLDEN_TRIANGLE_B', 'HARMONY_TRIANGLE_A', 'HARMONY_TRIANGLE_B'
        }

        #found on net Atom wrote this simple script
        #image_index = 0
        rnd = bpy.data.scenes[0].render
        rnd.resolution_x, rnd.resolution_y = select_mat

        #bpy.context.object.data.ortho_scale = orthoscale
        rndx = rnd.resolution_x
        rndy = rnd.resolution_y

        #orthoscale = ((rndx - rndy)/rndy)+1
        if rndx >= rndy:
            orthoscale = ((rndx - rndy)/rndy)+1
        elif rndx < rndy:
            orthoscale = 1
        bpy.context.object.data.ortho_scale = orthoscale
        bpy.context.selectable_objects

        #deselect camera
        bpy.ops.object.select_all(action='TOGGLE')

        #select plane
        bpy.ops.object.select_all(action='DESELECT')
        ob = bpy.data.objects["canvas"]
        ob.select = True
        bpy.context.scene.objects.active = ob

        #selection to texpaint toggle
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------image save
class SaveImage(bpy.types.Operator):
    """Save Image"""
    bl_idname = "image.save_current"
    bl_label = "Save Image Current"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):

        scene = context.scene
        original_type = bpy.context.area.type
        bpy.context.area.type = 'IMAGE_EDITOR'

        #return image to last saved state
        bpy.ops.image.save()
        bpy.context.area.type = original_type
        return {'FINISHED'}

#--------------------------------------------------Curve Bezier to Poly
class CurvePoly2d(bpy.types.Operator):
    """Curve added and made poly 2d Macro"""
     
    bl_idname = "object.curve_2dpoly"
    bl_label = "Curve 2D Poly"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):
        scene = context.scene

        #add curve
        bpy.ops.curve.primitive_bezier_curve_add(radius=1, view_align=False, enter_editmode=True, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

        
        #change to lpoly spline
        bpy.ops.curve.spline_type_set(type= 'POLY')

        #change to 2d
        bpy.context.object.data.dimensions = '2D'

        return {'FINISHED'}

#------------------------------------------------------close, mesh and unwrap
class CloseCurveunwrap(bpy.types.Operator):
    """Close the curve, set to mesh and unwrap"""
    
    bl_idname = "object.curve_unwrap"
    bl_label = "Close and Unwrap"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):
        scene =  context.scene
        
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
        bpy.ops.uv.project_from_view(camera_bounds=True, correct_aspect=False, scale_to_bounds=False)
        
        #tex paint toggle
        bpy.ops.object.editmode_toggle()
        bpy.ops.paint.texture_paint_toggle()
        
        return {'FINISHED'}




##############################################################  panel
class ArtistPanel(bpy.types.Panel):
    """A custom panel in the viewport toolbar"""
    bl_label = "Artist Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Artist Macros"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Image State")
        row = layout.row()
        row.operator("import_image.to_plane", \
        text = "Image to plane", icon = 'IMAGE_COL')
        row = layout.row()
        row.operator("image.canvas_shadeless", \
        text = "Shadeless Canvas", icon = 'FORCE_TEXTURE')
        row = layout.row()
        row.operator("image.reload_saved_state", \
        text = "Reload Image", icon = 'LOAD_FACTORY')
        row = layout.row()
        row.operator("image.save_current", \
        text = "Save Image", icon = 'IMAGEFILE')
        row = layout.row()
        row.label(text="Flip")
        row = layout.row()
        row.operator("image.canvas_horizontal", \
        text = "Canvas Flip Horizontal", icon = 'ARROW_LEFTRIGHT')
        row = layout.row()
        row.operator("image.canvas_vertical", \
        text = "Canvas Flip Vertical", icon = 'FILE_PARENT')
        row = layout.row()
        row.label(text="Special Macros")        
        row = layout.row()
        row.operator("image.cameraview_paint", \
        text = "Camera View Paint", icon = 'RENDER_REGION')
        row = layout.row()
        row.operator("render.opengl", \
        text = "OpenGL Render", icon = 'RENDER_STILL')
        row = layout.row()
        row.operator("image.create_brush", \
        text = "Brush Maker Scene", icon = 'OUTLINER_OB_CAMERA')
        row = layout.row()
        row.operator("object.curve_2dpoly", \
        text = "2D Mask Maker", icon = 'PARTICLE_POINT')
        row = layout.row()
        row.operator("object.curve_unwrap", \
        text = "Close Mask & Unwrap", icon = 'CURVE_NCIRCLE')



        row = layout.row()
        row.label(text="Rotation")
        row = layout.row()
        row.operator("image.rotate_ccw_15", \
        text = "Rotate 15 CCW", icon = 'MAN_ROT')
        row = layout.row()
        row.operator("image.rotate_cw_15", \
        text = "Rotate 15 CW", icon = 'MAN_ROT')
        row = layout.row()
        row.operator("image.rotate_ccw_90", \
        text = "Rotate 90 CCW", icon = 'MAN_ROT')
        row = layout.row()
        row.operator("image.rotate_cw_90", \
        text = "Rotate 90 CW", icon = 'MAN_ROT')
        row = layout.row()
        row.operator("image.canvas_resetrot", \
        text = "Reset Rotation", icon = 'CANCEL')



def register():
    bpy.utils.register_class(SaveImage)
    bpy.utils.register_class(ArtistPanel)
    bpy.utils.register_class(MacroCreateBrush)
    bpy.utils.register_class(CanvasShadeless)
    bpy.utils.register_class(CanvasHoriz)
    bpy.utils.register_class(CanvasVertical)
    bpy.utils.register_class(RotateCanvasCCW15)
    bpy.utils.register_class(RotateCanvasCW15)
    bpy.utils.register_class(RotateCanvasCCW)
    bpy.utils.register_class(RotateCanvasCW)
    bpy.utils.register_class(ImageReload)
    bpy.utils.register_class(CanvasResetrot)
    bpy.utils.register_class(CameraviewPaint)
    bpy.utils.register_class(CurvePoly2d)
    bpy.utils.register_class(CloseCurveunwrap)

def unregister():
    bpy.utils.unregister_class(CameraviewPaint)
    bpy.utils.unregister_class(SaveImage)
    bpy.utils.unregister_class(CanvasResetrot)
    bpy.utils.unregister_class(ImageReload)
    bpy.utils.unregister_class(RotateCanvasCW)
    bpy.utils.unregister_class(RotateCanvasCCW)
    bpy.utils.unregister_class(RotateCanvasCW15)
    bpy.utils.unregister_class(RotateCanvasCCW15)
    bpy.utils.unregister_class(CanvasVertical)
    bpy.utils.unregister_class(CanvasHoriz)
    bpy.utils.unregister_class(CanvasShadeless)
    bpy.utils.unregister_class(MacroCreateBrush)
    bpy.utils.unregister_class(ArtistPanel)
    bpy.utils.unregister_class(CurvePoly2d)
    bpy.utils.unregister_class(CloseCurveunwrap)
    

if __name__ == "__main__":
    register()
