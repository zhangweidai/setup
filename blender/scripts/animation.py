# prepare a (scene)
import bpy
import math
scn = bpy.context.scene
scn.frame_start = 1
scn.frame_end = 101

# move to frame 17
bpy.context.scene.frame_set(frame=17)

# create an object
bpy.ops.object.add(type='MESH')
newObject = bpy.context.object
newObject.name = "MyTriangle"

newMesh = newObject.data
x, y, z = 0, 0, 0
width, depth, height = 1, 1, 0.5
newVerts = [(x,y,z), (x+width,y,z), (x+width,y+depth,z), (x,y+depth,z),
           (x,y,z+height), (x+width,y,z+height), (x+width,y+depth,z+height),
           (x,y+depth,z+height)]
newEdges = []       # creating vertices and faces is sufficient.
newFaces = [(0,1,2,3), (2,3,7,6), (4,5,6,7), (0,3,7,4), (1,2,6,5), (0,1,5,4)]
newMesh.from_pydata(newVerts, newEdges, newFaces)
newMesh.update()

# select the created object
bpy.data.objects['MyTriangle'].select = True

# do something with the object. A rotation, in this case
bpy.ops.transform.rotate(value=(-0.5*math.pi), axis=(-1, 0, 0))

# create keyframe
bpy.ops.anim.keyframe_insert_menu(type='Rotation')


