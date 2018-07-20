import bpy
from utils import *
clearEverything()
bpy.ops.mesh.primitive_plane_add(radius=2, view_align=False, enter_editmode=True);
bpy.ops.mesh.inset(thickness=0.10, depth=0)
bpy.ops.mesh.select_all(action='TOGGLE')


bpy.context.tool_settings.mesh_select_mode = (False, False, True) 

obj = bpy.context.edit_object
me = obj.data
bm = bmesh.from_edit_mesh(me)

# notice in Bmesh polygons are called faces
for count,face in enumerate(bm.faces):
    if count > 2:
        face.select = True
        print ("\n")
        print (face.verts[0].co)
        print (face.verts[1].co)
        print (face.verts[2].co)
        print (face.verts[3].co)
        print ("\n")

bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 2.60358), "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
#     print (dir(face.verts))
 
