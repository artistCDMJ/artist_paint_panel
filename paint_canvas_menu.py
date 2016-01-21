bl_info = {
    "name": "Canvas Menu",
    "author": "CDMJ",
    "version": (1, 0),
    "blender": (2, 76, 0),
    "location": "",
    "description": "shortcut menu for Artist Panel addon",
    "warning": "",
    "wiki_url": "",
    "category": "Paint",
        }




import bpy

class canvasMenu(bpy.types.Menu):
    bl_label = "Canvas Menu"
    bl_idname = "view3D.canvas_menu"
    
    def draw(self, context):        
        layout = self.layout
        
        layout.operator("image.canvas_horizontal")
        layout.operator("image.canvas_vertical")
        layout.operator("image.rotate_ccw_15")
        layout.operator("image.rotate_cw_15")
        layout.operator("image.rotate_ccw_90")
        layout.operator("image.rotate_cw_90")
        layout.operator("image.canvas_resetrot")
        
def register():
    bpy.utils.register_class(canvasMenu)
    #bpy.ops.wm.call_menu(name=canvasMenu.bl_idname)
    
def unregister():
    bpy.utils.unregister_class(canvasMenu)
    
if __name__ == "__main__":
    register()
    
        
        
