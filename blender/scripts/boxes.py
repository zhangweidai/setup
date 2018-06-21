import bpy
import math
import random

def get_random_color():
    ''' generate rgb using a list comprehension '''
    r, g, b = [random.random() for i in range(3)]
    return (r, g, b)

def clearEverthing():
    try:
        bpy.ops.object.mode_set(mode = 'OBJECT')
    except:
        pass
    bpy.context.scene.cursor_location = (0,0,0)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def Main():
    clearEverthing()

    radi = 1
    spacing = 3.3
    count = 6
    prod = (count * radi * spacing)  + radi
    xshift = (prod / 2.0)
    yshift = (count * radi * spacing) / 2.0

    furthestX = 0    
    furthestY = 0    
    furthestZ = 0    

    for x in range(0, count):
        for y in range(0, count):
            for z in range(0, 1):
                xloc = x * (radi * spacing)
                yloc = y * (radi * spacing)
                zloc = z * (radi * spacing) 

                if xloc > furthestX:
                    furthestX = xloc
                if yloc > furthestY:
                    furthestY = yloc

                resized = (random.random() * 10) + 0.1
                cube = bpy.ops.mesh.primitive_cube_add(radius=radi, view_align=True, enter_editmode=False, location=(xloc, yloc, zloc))

                ob = bpy.context.object

                activeObject = bpy.context.active_object #Set active object to variable
                resized = (random.random() * 4) + 2.1
                activeObject.dimensions[2] = resized


                if resized > furthestZ:
                    furthestZ = resized

                bpy.ops.transform.translate(value=(0, 0, (resized/2)), 
                        constraint_axis=(False, False, True), 
                        constraint_orientation='GLOBAL', 
                        mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)


                mat = bpy.data.materials.new(name="MaterialName") #set new material to variable
                activeObject.data.materials.append(mat) #add the material to the object
                bpy.context.object.active_material.diffuse_color = get_random_color()
    
    center = (furthestX/2, furthestY/2, 0)
    bpy.ops.mesh.primitive_plane_add(radius=furthestX, view_align=False, enter_editmode=False, location=center)
    
    centerC = (furthestX/2, furthestY/2,furthestZ + 1)
    centerE = (furthestX/2, furthestY/2,furthestZ - 1)

    # add a path
    bpy.ops.curve.primitive_bezier_circle_add(radius=15, view_align=False, enter_editmode=False, location=centerC)
    bpy.context.object.name = "CameraPath"

    # add Focus point
    bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False, location=centerE)
    bpy.context.object.name = "FocusPoint"

    cameraLoc = (15, 25, furthestZ + 2)
    cameraRot = (math.radians(-125), math.radians(180), math.radians(-50))

    # add Lamp
    bpy.ops.object.lamp_add(type='SUN', radius=1, view_align=False, location=cameraLoc, rotation= cameraRot)
    bpy.context.object.data.energy = 5.38
    bpy.context.object.name = "Lamp"
    bpy.ops.object.constraint_add(type='TRACK_TO')
    bpy.context.object.constraints["Track To"].target = bpy.data.objects["FocusPoint"]
    bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
    bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'
    
    # add Camera
    bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=cameraLoc, rotation=cameraRot)
    bpy.ops.object.constraint_add(type='TRACK_TO')
    bpy.context.object.constraints["Track To"].target = bpy.data.objects["FocusPoint"]
    bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
    bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'

    bpy.ops.object.select_all(action='DESELECT')
    cameraObj = bpy.data.objects['Camera']
    path = bpy.data.objects['CameraPath']
    lamp = bpy.data.objects['Lamp']
    path.select = True
    lamp.select = True
    cameraObj.select = True
    bpy.context.scene.objects.active = path
#     camPathObj.parent = cameraObj
#     cameraObj.parent_set(type='FOLLOW')
    bpy.ops.object.parent_set(type='FOLLOW')
    

#     bpy.context.scene.objects.active = camPathObj
#     bpy.ops.object.editmode_toggle()
#     bpy.ops.curve.select_all(action='DESELECT')
# 
#     # iterate over points of the curve's first spline
#     bpy.context.object.data.splines.active.bezier_points[0].select_control_point = True
    #bpy.ops.view3d.snap_cursor_to_selected()
    

Main()
