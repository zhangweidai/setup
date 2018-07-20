import bpy
from utils import *
import material

#clearEverything()

def generateWorld2():
    # get the world
    myWorld = bpy.data.worlds.get("World")
    if myWorld is None:
        myWorld = bpy.data.worlds.new(name="World")

    myWorld.use_nodes = True
    bpy.context.scene.world = myWorld
    
    # get all material nodes
    tree = myWorld.node_tree
    if tree is None:
        myWorld.use_nodes = True
        tree = myWorld.node_tree
        if tree is None:
            print ("no tree")
            return

    nodes = tree.nodes
    links = tree.links

    for n in nodes:
        nodes.remove(n)

    x = 240
    output_node = nodes.new('ShaderNodeOutputWorld')
    output_node.location = (2* x, 0)

    background_node = nodes.new('ShaderNodeBackground')
    background_node.location = (x+50, 0)
    background_node.inputs[1].default_value = 0.7

    rgb_node = nodes.new("ShaderNodeRGBCurve")
    rgb_node.location = (0, 0)
#     rgb_node.mapping.curves[0].points[0].location = (0,0)
    rgb_node.mapping.curves[3].points.new(position = 0.75, value = 0.85)
    rgb_node.mapping.curves[3].points.new(position = 0.25, value = 0.15)

    #red
    rgb_node.mapping.curves[0].points.new(position = 0.5, value = 0.5)
    rgb_node.mapping.curves[0].points.new(position = 0.84, value = 0.70)

    rgb_node.mapping.curves[2].points.new(position = 0.3, value = 0.3)
    rgb_node.mapping.curves[2].points.new(position = 0.75, value = 0.80)

    links.new(background_node.outputs[0], output_node.inputs[0])

    env_node = nodes.new('ShaderNodeTexEnvironment')
    env_node.location = (-1 * x, 0)

    filepath="E:\\Downloads\\dry_field_8k.hdr"
    env_node.image = bpy.data.images.load(filepath)
    links.new(env_node.outputs[0], rgb_node.inputs[1])
    links.new(rgb_node.outputs[0], background_node.inputs[0])

    coord_node = nodes.new("ShaderNodeTexCoord")
    coord_node.location = (-4 * x, 0)

    mapping_node = nodes.new("ShaderNodeMapping")
    mapping_node.location = (-3 * x, 0)

    links.new(mapping_node.outputs[0], env_node.inputs[0])
    links.new(coord_node.outputs[0], mapping_node.inputs[0])
    
    mapping_node.translation[2] = 0.4
    mapping_node.rotation[0] = math.radians(-9.5)
    mapping_node.rotation[1] = math.radians(-5.7)
    mapping_node.rotation[2] = math.radians(-107)

#generateWorld2()

#land = bpy.ops.mesh.landscape_add(subdivision_x=256, subdivision_y=256, mesh_size_x=14, mesh_size_y=18, random_seed=0, noise_offset_y=0, noise_size_x=1.6, noise_size_y=2.3, noise_size=4, noise_type='slick_rock', noise_depth=10, height=4, edge_falloff='2', falloff_x=7, edge_level=0.3, maximum=5, refresh=True)
# land = bpy.ops.mesh.landscape_add(subdivision_x=128, subdivision_y=128, mesh_size_x=14, mesh_size_y=18, random_seed=0, noise_offset_y=0, noise_size_x=1.6, noise_size_y=2.3, noise_size=4, noise_type='slick_rock', noise_depth=10, height=5, edge_falloff='2', falloff_x=7, edge_level=0.3, maximum=5.1, refresh=True)
camera = bpy.data.objects.get("Camera")
#bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(-4.22021, -5.14301, 3.68991), rotation=(1.12279, 6.70124e-007, 0.194665))
camera.data.show_limits = True
camera.data.show_mist = True
camera.location = (4, -11.5, 6)
camera.rotation_euler = (math.radians(67), math.radians(0), math.radians(23))



# ob = bpy.context.active_object
# bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'
# bpy.ops.object.modifier_add(type='SUBSURF')
# bpy.context.object.cycles.use_adaptive_subdivision = True
# bpy.ops.object.editmode_toggle()
# bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
# 
# bpy.ops.object.editmode_toggle()
# 
# mat = material.generateMountainMaterial()
# 
# material.assignM(ob, mat)
# 
# bpy.context.scene.cycles.device = 'GPU'
# bpy.context.scene.view_settings.look = 'Filmic - Base Contrast'
# bpy.context.scene.sequencer_colorspace_settings.name = 'Filmic Log'
# bpy.context.scene.view_settings.view_transform = 'Filmic'
