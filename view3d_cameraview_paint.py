

bl_info = {
    "name": "Add Cameraview Paint",
    "author": "CDMJ",
    "version": (1, 0, 3),
    "blender": (2, 76, 0),
    "location": "",
    "description": "Art Macros.",
    "warning": "",    
    "category": "Paint",
}


import bpy

class CameraviewPaint(bpy.types.Operator):

    bl_idname = "image.cameraview_paint" # must match a operator context, like
                                     # view3d, object or image and cannot have
                                     # more then one '.', if you need something
                                     # that is global use wm.create_brush
                                     # and uncomment from line 24-29
    bl_label = "Cameraview Paint"
    bl_options = { 'REGISTER', 'UNDO' }
    
    
    
    def execute(self, context):
        
        scene = context.scene




    
    
        #toggle texture mode / object mode
        #bpy.ops.paint.texture_paint_toggle()
        #add camera
        bpy.ops.object.camera_add(view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        
        

        bpy.ops.view3d.object_as_camera()
        #bpy.context.object.data.ortho_scale = 2

        bpy.context.object.data.type = 'ORTHO'

        bpy.ops.transform.translate(value=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)



        bpy.context.object.data.show_guide = {'CENTER', 'CENTER_DIAGONAL', 'THIRDS', 'GOLDEN', 'GOLDEN_TRIANGLE_A', 'GOLDEN_TRIANGLE_B', 'HARMONY_TRIANGLE_A', 'HARMONY_TRIANGLE_B'}


        #found on net Atom wrote this simple script
        #import bpy  
  
        image_index = 0

 
        rnd = bpy.data.scenes[0].render  
        rnd.resolution_x, rnd.resolution_y = bpy.data.images[image_index].size[:] 
        
        #bpy.context.object.data.ortho_scale = orthoscale
        
        rndx = rnd.resolution_x
        rndy = rnd.resolution_y
        #orthoscale = ((rndx - rndy)/rndy)+1 
        
        
        if rndx >= rndy:
            orthoscale = ((rndx - rndy)/rndy)+1
            
        elif rndx < rndy:
            orthoscale = 1
        
        
        
        
        
        
        bpy.context.object.data.ortho_scale = orthoscale
        
        
        
        
        return {'FINISHED'} # this is importent, as it tells blender that the
                            # operator is finished.
        
        
def register():
    bpy.utils.register_class(CameraviewPaint)

    
def unregister():
    bpy.utils.unregister_class(CameraviewPaint)

    
if __name__ == "__main__":
    register()
    
