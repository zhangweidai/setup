import bpy
import math
import random
import bmesh
import material
import numpy as np
from utils import *

bpy.context.scene.frame_end = 80
clearEverything()
material.generateWood()

def main():
    xloc = 0
    yloc = 0
    zloc = 0
    radi = .45
    count = 7
    radi_diff = .30
    spacing = radi + radi_diff + .5
    
    linkRot = (math.radians(0), math.radians(90), math.radians(0))
    added = bpy.ops.mesh.primitive_torus_add(major_radius=radi, minor_radius = radi - radi_diff, rotation = linkRot, location=(xloc, yloc, zloc))
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.mass = 2
    bpy.context.object.rigid_body.collision_shape = 'MESH'
    bpy.context.object.name = "FirstLink"
    
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='DESELECT')
        
    # force edge selection mode
    bpy.context.tool_settings.mesh_select_mode = (False, False, True) 
    
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    
    # notice in Bmesh polygons are called faces
    for face in bm.faces:
        if face.verts[0].co[0] < 0:
            face.select = True
    bpy.ops.transform.translate(value=(0, 0, 0.60), constraint_axis=(False, False, True))
    
    bpy.ops.object.editmode_toggle()
    # ctrl shift alt c
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.duplicate()
    bpy.ops.transform.translate(value=(0, 0, 1), constraint_axis=(False, False, True))
    linkRot = (math.radians(0), math.radians(90), math.radians(90))
    bpy.context.object.rotation_euler = linkRot;
    
    bpy.ops.object.select_all(action='SELECT')
    for i in range(1,count):
        bpy.ops.object.duplicate()
        bpy.ops.transform.translate(value=(0, 0, 0.70 * 2.70), constraint_axis=(False, False, True))
    
    obs = bpy.data.objects
    sobs = bpy.context.scene.objects
    active = bpy.context.scene.objects.active
    linkCount = len(bpy.data.objects)
    lastLink = bpy.data.objects[linkCount-1]
    lastLink.name = "LastLink"
    lastLink.rigid_body.enabled = False
    
    bpy.ops.object.select_all(action='DESELECT')
    sobs.active = sobs["FirstLink"]
    
    #active.select = True
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.primitive_uv_sphere_add(size=1.8, view_align=False, enter_editmode=False, location=(0, 0, -1.5))
    bpy.ops.object.editmode_toggle()
    bpy.context.object.rigid_body.mass = 10
    view3d = get_3d_view()
    view3d.pivot_point='CURSOR'
    view3d.cursor_location = lastLink.location
    bpy.ops.object.select_all(action='SELECT')
    override = get_override( 'VIEW_3D', 'WINDOW')
    bpy.ops.transform.rotate(override, value=1.5, axis=(1,0,0))     

    bpy.ops.mesh.primitive_cube_add(radius = 0.9, view_align=False, enter_editmode=False, location=(-4,-9,-4))

    ob = bpy.context.active_object
    material.assignM(ob, bpy.data.materials.get("BSDF_Wood"))

    bpy.context.object.name = "Block"
    bpy.ops.object.modifier_add(type='ARRAY')
    bpy.context.object.modifiers["Array"].count = 5
    bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 1.1
    bpy.ops.object.modifier_add(type='ARRAY')
    bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
    bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 1.1
    bpy.context.object.modifiers["Array.001"].count = 5
    bpy.ops.object.modifier_add(type='ARRAY')
    bpy.context.object.modifiers["Array.002"].relative_offset_displace[0] = 0
    bpy.context.object.modifiers["Array.002"].relative_offset_displace[1] = 0
    bpy.context.object.modifiers["Array.002"].relative_offset_displace[2] = 1.1
    bpy.context.object.modifiers["Array.002"].count = 4
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.mass = 0.20

    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array")
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array.002")
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array.001")

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
# 
    plane = bpy.ops.mesh.primitive_plane_add(radius=17, view_align=False, enter_editmode=False, location=(-0,-14,-5))
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.enabled = False
    bpy.context.scene.rigidbody_world.time_scale = 3

#     bpy.ops.node.add_node(use_transform=True, type="ShaderNodeBsdfPrincipled")
#     bpy.ops.node.add_node(use_transform=True, type="ShaderNodeTexImage")
#     bpy.context.space_data.viewport_shade = 'MATERIAL'
#     bpy.ops.node.add_node(use_transform=True, type="ShaderNodeTexCoord")

#     distance = get_distance_between("FirstLink", "LastLink")
#     print (distance)
#     distance = get_distance_between("FirstLink", "Block")
#     print (distance)
  
main()
