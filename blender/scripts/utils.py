import bpy
import math
import random
import bmesh
import numpy as np

from importlib import *
# imp.reload(module)

mainPath = "C:\\Users\Peter\AppData\Roaming\Blender Foundation\Blender\\2.79\scripts\\addons\Dynamat\dynamats"
dynaPath = "C:\\Users\Peter\AppData\Roaming\Blender Foundation\Blender\\2.79\scripts\\addons\Dynamat\dynamats"
texturesPath = "C:\\Users\\Peter\\Documents\\Textures"
# bpy.ops.mesh.primitive_plane_add(radius=2, view_align=False, enter_editmode=True);
# verts = [(0,0,0),(0,5,0),(5,5,0),(5,0,0),(2.5,2.5,4.5)]
# faces = [(0,1,2,3), (0,4,1), (1,4,2), (2,4,3), (3,4,0)]
# mesh = bpy.data.meshes.new("Floor")
# object = bpy.data.objects.new("Floor", mesh)
# object.location = bpy.context.scene.cursor_location
# bpy.context.scene.objects.link(object)
# mesh.from_pydata(verts,[],faces)
# mesh.update(calc_edges=True)

def clearEverthing():
    try:
        bpy.ops.object.mode_set(mode = 'OBJECT')
    except:
        pass
    bpy.context.scene.cursor_location = (0,0,0)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

whatmsg = None
sobs = bpy.context.scene.objects
def debugMsg(msg):
    print ("msg")
    print (msg)
    sobs = bpy.context.scene.objects
    if not "debugText" in sobs:
        msg = bpy.ops.object.text_add(view_align=False, enter_editmode=False, location=(-15,15,0))
        bpy.context.object.name = "debugText"
    sobs["debugText"].data.body = str(msg)

def printCursorLocation():
    debugMsg(bpy.context.scene.cursor_location)


printfMsg = None
def printf(msg, start = False, done = False):
    global printfMsg

    if not isinstance(msg, str):
        msg = str(msg)

    if start:
        printfMsg = msg + "\n"
    else:
        printfMsg = printfMsg + "\n" + msg

    if done:
        debugMsg(printfMsg)

def start(msg = "Start"):
    printf(msg, start = True, done = True)

def end(msg = "End"):
    printf(msg, done = True)


def nomod(coord):
    return (coord[0], coord[1], coord[2])

def mod(coord, dire = "z"):
    xmod = 0
    ymod = 0
    zmod = 0
    if dire == "x":
        xmod = .1
    elif dire == "y":
        ymod = .1
    elif dire == "z":
        zmod = .1
    return (coord[0] + xmod, coord[1] + ymod, coord[2] + zmod)

def stats(obdata):
#     obdata = bpy.context.object.data
#     print('Vertices:')
#     for v in obdata.vertices:
#         print('{}. {} {} {}'.format(v.index, v.co.x, v.co.y, v.co.z))
#     
#     print('Edges:')
#     for e in obdata.edges:
#         print('{}. {} {}'.format(e.index, e.vertices[0], e.vertices[1]))
    
    printf('Faces:', start = True, done = True)

    for f in obdata.polygons:
#         printf('{}. '.format(f.index))
        for e in f.edge_keys:
#             printf('{}'.format(e))
            p1 = e[0]
            p2 = e[1]
            v1 = obdata.vertices[p1].co
            v2 = obdata.vertices[p2].co
#             printf('point {} : {} '.format(p1, v1))
#             printf('point {} : {} '.format(p2, v2))
#             cube = bpy.ops.mesh.primitive_cube_add(radius=.2, view_align=True, enter_editmode=False, location=v1)
#             cube = bpy.ops.mesh.primitive_cube_add(radius=.2, view_align=True, enter_editmode=False, location=v2)

            maintyple = tuple()
            maintyple = maintyple + (p1,)
            maintyple = maintyple + (p2,)

            verts = list()
            verts.append(nomod(v1))
            verts.append(mod(v1))
            verts.append(mod(v2))
            verts.append(nomod(v2))
            faces = [(0,1,2,3)]
            printf(str(verts))
#             faces = list()
#             faces.append(maintyple)


            mesh = bpy.data.meshes.new("Floor")
            object = bpy.data.objects.new("Floor", mesh)
            object.location = bpy.context.scene.cursor_location
            bpy.context.scene.objects.link(object)
            mesh.from_pydata(verts,[],faces)
            mesh.update(calc_edges=True)

#         for v in f.vertices:
#             print('{} '.format(v), end='')
    printf('', done = True)

def contained():
    bpy.context.scene.tool_settings.use_mesh_automerge = True
    
    clearEverthing()
    bpy.ops.mesh.primitive_plane_add(radius=2, view_align=False, enter_editmode=False);
    bpy.context.object.name = "added_plane"

    b = bpy.context.object.data
    stats(b)

# contained()


def floorplan(mesh, dist):
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, dist), "constraint_axis":(False, False, False)})

def get_distance_between(obj1, obj2):
    sobs = bpy.context.scene.objects
    p1 = np.array(sobs[obj1].location)
    p2 = np.array(sobs[obj2].location)
    squared_dist = np.sum(p1**2 + p2**2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist

def get_random_color():
    ''' generate rgb using a list comprehension '''
    r, g, b = [random.random() for i in range(3)]
    return (r, g, b)

def clearEverything():
    try:
        bpy.ops.object.mode_set(mode = 'OBJECT')
    except:
        pass
    bpy.context.scene.cursor_location = (0,0,0)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def get_override(area_type, region_type):
    for area in bpy.context.screen.areas: 
        if area.type == area_type:             
            for region in area.regions:                 
                if region.type == region_type:                    
                    override = {'area': area, 'region': region} 
                    return override
    #error message if the area or region wasn't found
    raise RuntimeError("Wasn't able to find", region_type," in area ", area_type,
                        "\n Make sure it's open while executing script.")

def area_of_type(type_name):
    for area in bpy.context.screen.areas:
        if area.type == type_name:
            return area

def get_3d_view():
    return area_of_type('VIEW_3D').spaces[0]

import os
def copyToClipBoard():
    file = open("testfile.txt","w") 
    file.write("bpy.context.active_object.location = ({}, {}, {})\n".format(
                bpy.context.active_object.location[0], 
                bpy.context.active_object.location[1], 
                bpy.context.active_object.location[2]))
    file.write("bpy.context.active_object.rotation_euler = ({}, {}, {})".format(
                bpy.context.active_object.rotation_euler[0], 
                bpy.context.active_object.rotation_euler[1], 
                bpy.context.active_object.rotation_euler[2]))

    file.close() 
    os.system("type testfile.txt | clip")

print ("hllo world")
# C.object.location
def getbm():
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    return b
    
C = bpy.context
D = bpy.data
S = D.scenes['Scene']

def getfaces():
    return getbm().faces

def well():
    # active face bm.faces.active
    bm = getbm()
    print (bm.faces.active.normal)
#    for face in bm.faces:
#        print (face)

#copyToClipBoard()
