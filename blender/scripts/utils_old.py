import bpy
import math
import random
import bmesh
import numpy as np
import utils

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

#copyToClipBoard()
