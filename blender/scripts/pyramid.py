import bpy
import utils

utils.clearEverything()
directions = list()
directions.append("y,232")
directions.append("x,162") # wall in front of me
directions.append("y,83")
directions.append("x,-5")
directions.append("y,-78")
directions.append("x,-157")
directions.append("y,124") # bed wall
directions.append("x,79")
directions.append("y,24")
directions.append("x,-5")
directions.append("y,-19")
directions.append("x,-74")
directions.append("y,91")
directions.append("x,36")
directions.append("y,-40")
directions.append("x,38")
directions.append("y,-2")
directions.append("x,5")
directions.append("y,7")
directions.append("x,-33")
directions.append("y,40")
directions.append("x,95")
directions.append("y,-92")
directions.append("x,-26")
directions.append("y,-5")
directions.append("x,50")
directions.append("y,-14")
directions.append("x,5")
directions.append("y,7")
directions.append("x,5")
directions.append("y,5")
directions.append("x,-5")
directions.append("y,12")
directions.append("x,-23")
directions.append("y,91") # bathroom mirror
directions.append("x,57")
directions.append("y,-103")
directions.append("x,-3")
directions.append("y,-5")
directions.append("x,40") # hall
directions.append("y,5")
directions.append("x,-3")
directions.append("y,27")
directions.append("x,-28")
directions.append("y,78")
directions.append("x,28")
directions.append("y,-5")
directions.append("x,5")
directions.append("y,5")
directions.append("x,116") # room back wall
directions.append("y,-105")
directions.append("x,-88")
directions.append("y,-5")
directions.append("x,88")

directions.append("y,-78")
directions.append("x,-83")
directions.append("y,40")
directions.append("x,-72") # hall corner
directions.append("y,-47") # hall
directions.append("x,5")
directions.append("y,5")
directions.append("x,8")
directions.append("y,5")
directions.append("x,-7")
directions.append("y,33")
directions.append("x,62") # closet back wall
directions.append("y,-37")
directions.append("x,-8")
directions.append("y,-5")
directions.append("x,88")
directions.append("y,-44")
directions.append("x,38")
directions.append("y,-36")
directions.append("x,-38")
directions.append("x,-30,y,-30")
directions.append("x,-101")
directions.append("x,-12,y,12")
directions.append("y,70")
directions.append("x,-5")
directions.append("y,-71")
directions.append("x,15,y,-15")
directions.append("x,105")
directions.append("x,30,y,30")
directions.append("x,37")
directions.append("y,-50")
directions.append("x,18")
directions.append("y,-31")
directions.append("x,26,y,-7")
directions.append("y,-67")
directions.append("x,-26,y,-7")
directions.append("y,-31")
directions.append("x,-181")
# 
# directions.append("x,3")
# directions.append("y,-14.5")
# directions.append("x,5")
# directions.append("y,2")
# directions.append("x,0.5")
# directions.append("y,2.5")
# directions.append("x,20.5") # undon
# directions.append("y,-30.5") # undon
# directions.append("x,-45.5") # undon
# directions.append("y,9.5") # undon
# directions.append("x,100")
# directions.append("y,-100")
# directions.append("x,100")
# directions.append("y,200")
# directions.append("x,-200")
# directions.append("y,-100")

scale = 10.00;

currentX = 0.0
currentY = 0.0
currentZ = 0.0
startvert = (currentX, currentY, currentZ)
verts = list()
verts.append(startvert)
faces = list()
maintyple = tuple()
for r,adir in enumerate(directions):
    maintyple = maintyple + (r,)
    tokens = adir.split(",")

    direct = tokens[0]
    howmuch = float(tokens[1])/scale

    other = ""
    howmuch2 = 0 
    if len(tokens) == 4:
        other = tokens[2]
        howmuch2 = float(tokens[3])/scale

    if other == "x":
        currentX = currentX + howmuch2
    if other == "y":
        currentY = currentY + howmuch2

    if "x" == direct:
        currentX = currentX + howmuch
    if "y" == direct:
        currentY = currentY + howmuch
#     if direct == "z":
#         currentZ = currentZ + howmuch

    currentVert = (currentX, currentY, 0)
    verts.append(currentVert)

faces.append(maintyple)
bpy.ops.object.text_add(view_align=False, enter_editmode=False, location=currentVert)
ob=bpy.context.object
ob.data.body = "({})".format(currentVert)

 
#Define vertices, faces, edges
# verts = [(0,0,0),(0,5,0),(5,5,0),(5,0,0),(2.5,2.5,4.5)]
# faces = [(0,1,2,3), (0,4,1), (1,4,2), (2,4,3), (3,4,0)]
 
#Define mesh and object
mesh = bpy.data.meshes.new("Floor")
object = bpy.data.objects.new("Floor", mesh)
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)

# sizex = 50
# sizey = 54
# origin = -1
# verts = [(origin,origin,0), (origin,sizey,0), (sizex,sizey,0), (sizex,origin,0)]
# faces = [(0,1,2,3)]
# mesh2 = bpy.data.meshes.new("Floor2")
# object = bpy.data.objects.new("Floor2", mesh2)
# object.location = bpy.context.scene.cursor_location
# bpy.context.scene.objects.link(object)
# mesh2.from_pydata(verts,[],faces)
# mesh2.update(calc_edges=True)

