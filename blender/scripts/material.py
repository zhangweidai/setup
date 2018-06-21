import bpy
import math

for image in bpy.data.images:
    if not image.users:
        bpy.data.images.remove(image)

def assignM(ob, mat):
    # Assign it to object
    if ob.data.materials:
        # assign to 1st material slot
        ob.data.materials[0] = mat
    else:
        # no slots
        ob.data.materials.append(mat)

rock = 0 # detailed
rock = 1 # rock
rock = 2 # rough

def principledHelper(nodes, x, shift, links, rock):

    principled = nodes.new("ShaderNodeBsdfPrincipled")
    principled.location = (x*2, (x*2) + shift)

    image_node = nodes.new('ShaderNodeTexImage')
    filepath = ""
    if rock == 0:
        filepath="C:\\Users\\Peter\\Documents\\textures\\TexturesCom_SnowDetail_1024_albedo.tif"
    elif rock == 1:
        filepath="C:\\Users\\Peter\\Documents\\textures\\TexturesCom_RockSharp0092_23_seamless_S.jpg"
    elif rock == 2:
        filepath="C:\\Users\\Peter\\Documents\\textures\\TexturesCom_SnowRough_1024_albedo.tif"
    image_node.image = bpy.data.images.load(filepath)
    contrast_node = nodes.new("ShaderNodeBrightContrast")

    if rock == 1:
        contrast_node.location = (x, (x*3) + shift)
        image_node.location = (0, (x*3) + shift)
        contrast_node.inputs[1].default_value = -0.05
    elif rock == 0 or rock  == 2:
        contrast_node.location = (x, (x*4) + shift)
        image_node.location = (0, (x*5) + shift)
        contrast_node.inputs[1].default_value = 0.1

    links.new(image_node.outputs[0], contrast_node.inputs[0])
    links.new(contrast_node.outputs[0], principled.inputs[0])

    coord_node2 = nodes.new("ShaderNodeTexCoord")
    coord_node2.location = (-3 * x, (2*x) + shift)

    mapping_node2 = nodes.new("ShaderNodeMapping")
    mapping_node2.location = (-2 * x, (2*x) + shift )
    if rock == 2:
        mapping_node2.scale[0] = 50
        mapping_node2.scale[1] = 22
    else:
        mapping_node2.scale[0] = 30
        mapping_node2.scale[1] = 25

    links.new(mapping_node2.outputs[0], image_node.inputs[0])
    links.new(coord_node2.outputs[0], mapping_node2.inputs[0])

    # for snow
    if rock == 0 or rock == 2:
        imageR_node = nodes.new('ShaderNodeTexImage')
        imageR_node.location = (0, (x*4) + shift)
        if rock == 0:
            filepath="C:\\Users\\Peter\\Documents\\textures\\TexturesCom_SnowDetail_1024_roughness.tif"
        else:
            filepath="C:\\Users\\Peter\\Documents\\textures\\TexturesCom_SnowRough_1024_roughness.tif"
        imageR_node.image = bpy.data.images.load(filepath)

        links.new(imageR_node.outputs[0], principled.inputs[7])
        links.new(mapping_node2.outputs[0], imageR_node.inputs[0])

        imageS_node = nodes.new('ShaderNodeTexImage')
        imageS_node.location = (0, (x*3) + shift)
        if rock == 0:
            filepath="C:\\Users\\Peter\\Documents\\textures\\TexturesCom_SnowDetail_1024_specular.tif"
        else:
            filepath="C:\\Users\\Peter\\Documents\\textures\\TexturesCom_SnowDetail_1024_specular.tif"
        imageS_node.image = bpy.data.images.load(filepath)

        links.new(imageR_node.outputs[0], principled.inputs[7])
        links.new(mapping_node2.outputs[0], imageR_node.inputs[0])
        links.new(mapping_node2.outputs[0], imageS_node.inputs[0])
        links.new(imageS_node.outputs[0], principled.inputs[5])
    
        imageH_node = nodes.new('ShaderNodeTexImage')
        imageH_node.location = (-1*(x/2), (x*2) + shift)
        if rock == 0:
            filepath="C:\\Users\\Peter\\Documents\\textures\\TexturesCom_SnowPlain_1024_height.tif"
        else:
            filepath="C:\\Users\\Peter\\Documents\\textures\\TexturesCom_SnowRough_1024_height.tif"

        imageH_node.image = bpy.data.images.load(filepath)
        links.new(mapping_node2.outputs[0], imageH_node.inputs[0])


    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (x, (2*x+ shift))
    if rock == 2:
        bump_node.inputs[0].default_value = 0.4
    else:
        bump_node.inputs[0].default_value = 0.3

    ramp_node = None
    if rock == 1:
        ramp_node = nodes.new("ShaderNodeValToRGB")
        ramp_node.location = (x/2, (x) + shift)
        ramp_node.color_ramp.elements.new(position=.10)
        ramp_node.color_ramp.elements[1].color = (0,0,0,1)
        ramp_node.color_ramp.elements[2].position = .5
        bump_node.inputs[0].default_value = 0.5
        bump_node.inputs[1].default_value = 0.7
        links.new(ramp_node.outputs[0], bump_node.inputs[2])
        links.new(image_node.outputs[0], ramp_node.inputs[0])

        rough_node = nodes.new("ShaderNodeBrightContrast")
        rough_node.location = (x, (x*2.5) + shift)
        rough_node.inputs[1].default_value = 0.2
        rough_node.inputs[2].default_value = -0.3
        links.new(image_node.outputs[0], rough_node.inputs[0])
        links.new(rough_node.outputs[0], principled.inputs[7])

    elif rock == 0 or rock == 2:
        links.new(imageH_node.outputs[0], bump_node.inputs[2])
        links.new(mapping_node2.outputs[0], imageH_node.inputs[0])

    links.new(bump_node.outputs[0], principled.inputs[17])


    return principled



# generateWood()
def generateMountainMaterial():
    mat = bpy.data.materials.get("Mat")
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name="Mat")
    
    mat.cycles.displacement_method = 'TRUE'
    
    mat.use_nodes = True
    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links
    
    for n in nodes:
        nodes.remove(n)
    
    x = 280
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (x*6, 3*x)
    
#     diffuse_node = nodes.new('ShaderNodeBsdfDiffuse')
#     diffuse_node.location = (0, x)
#     links.new(diffuse_node.outputs[0], output_node.inputs[0])
        
    image_node = nodes.new('ShaderNodeTexImage')
    image_node.location = (-1 * x, 0)
    filepath="E:\\mt\\rockdp.jpg"
    image_node.image = bpy.data.images.load(filepath)
    
    mult_node = nodes.new("ShaderNodeMath")
    mult_node.location = (0, -1 * x)
    mult_node.operation = 'MULTIPLY'
    mult_node.inputs[1].default_value = 1.4


    sub_node = nodes.new("ShaderNodeMath")
    sub_node.operation = 'SUBTRACT'
    sub_node.location = (x, -1 * x)
        
    links.new(image_node.outputs[0], mult_node.inputs[0])
    links.new(mult_node.outputs[0], sub_node.inputs[0])
    
    mapping_node = nodes.new("ShaderNodeMapping")
    mapping_node.location = (-3 * x, 0)
    links.new(mapping_node.outputs[0], image_node.inputs[0])
    
    mapping_node.scale[0] = 28
    mapping_node.scale[1] = 25
    
    coord_node = nodes.new("ShaderNodeTexCoord")
    coord_node.location = (-4 * x, 0)
    links.new(coord_node.outputs[0], mapping_node.inputs[0])

    geom_node = nodes.new("ShaderNodeNewGeometry")
    geom_node.location = (-4 * x, x)

    vmath_node = nodes.new("ShaderNodeVectorMath")
    vmath_node.location = (-3 * x, x)
    vmath_node.operation = 'AVERAGE'

    cxyz_node = nodes.new("ShaderNodeCombineXYZ")
    cxyz_node.inputs[0].default_value = 0.1
    cxyz_node.inputs[1].default_value = 0.1
    cxyz_node.inputs[2].default_value = -0.1
    cxyz_node.location = (-4 * x, x * 2)

    sxyz_node = nodes.new("ShaderNodeSeparateXYZ")
    sxyz_node.location = (-2 * x, x)

    links.new(geom_node.outputs[1], vmath_node.inputs[1])
    links.new(cxyz_node.outputs[0], vmath_node.inputs[0])
    links.new(vmath_node.outputs[0], sxyz_node.inputs[0])

    ramp_node = nodes.new("ShaderNodeValToRGB")
    ramp_node.location = (-1 * x, x)
    ramp_node.color_ramp.elements.new(position=.58)
    ramp_node.color_ramp.elements[1].color = (0,0,0,1)
    ramp_node.color_ramp.elements[2].position = .66
    ramp_node.color_ramp.interpolation = 'CONSTANT'
    links.new(sxyz_node.outputs[2], ramp_node.inputs[0])

    ramp_node2 = nodes.new("ShaderNodeValToRGB")
    ramp_node2.location = (-1 * x, x*2)
    ramp_node2.color_ramp.elements.new(position=.40)
    ramp_node2.color_ramp.elements[1].color = (0,0,0,1)
    ramp_node2.color_ramp.elements[2].position = .52
    ramp_node2.color_ramp.interpolation = 'CONSTANT'
    links.new(sxyz_node.outputs[2], ramp_node2.inputs[0])

    ramp_node3 = nodes.new("ShaderNodeValToRGB")
    ramp_node3.location = (-1 * x, x*3)
    ramp_node3.color_ramp.elements.new(position=.6)
    ramp_node3.color_ramp.elements[1].color = (0,0,0,1)
    ramp_node3.color_ramp.elements[2].position = .8
    ramp_node3.color_ramp.interpolation = 'EASE'
    links.new(sxyz_node.outputs[2], ramp_node3.inputs[0])



    colorMixRgb_node = nodes.new("ShaderNodeMixRGB")
    colorMixRgb_node.location = (x*2, 0)
    colorMixRgb_node.blend_type = 'MULTIPLY'
    colorMixRgb_node.inputs[0].default_value = 1
    links.new(colorMixRgb_node.outputs[0], output_node.inputs[2])

    links.new(sub_node.outputs[0], colorMixRgb_node.inputs[1])

    invert_node = nodes.new("ShaderNodeInvert")
    invert_node.location = (x,0)
    links.new(ramp_node.outputs[0], invert_node.inputs[1])
    links.new(invert_node.outputs[0], colorMixRgb_node.inputs[2])

    principled1 = principledHelper(nodes, x, 1700, links, 0)
    principled2 = principledHelper(nodes, x, 800, links, 1)
    principled3 = principledHelper(nodes, x, 3100, links, 2)

    mixShader_node = nodes.new("ShaderNodeMixShader")
    mixShader_node.location = (x*4, 3*x)
    links.new(principled1.outputs[0], mixShader_node.inputs[1])
    links.new(principled2.outputs[0], mixShader_node.inputs[2])

    invert_node2 = nodes.new("ShaderNodeInvert")
    invert_node2.location = (x,x)
    links.new(invert_node2.outputs[0], mixShader_node.inputs[0])
    links.new(ramp_node2.outputs[0], invert_node2.inputs[1])

    invert_node3 = nodes.new("ShaderNodeInvert")
    invert_node3.location = (x,x*2)
    links.new(ramp_node3.outputs[0], invert_node3.inputs[1])

    colorMixRgb_node2 = nodes.new("ShaderNodeMixRGB")
    colorMixRgb_node2.location = (x*3, x)
    colorMixRgb_node2.blend_type = 'MULTIPLY'
    colorMixRgb_node2.inputs[0].default_value = 1
    links.new(invert_node3.outputs[0], colorMixRgb_node2.inputs[1])
    links.new(ramp_node2.outputs[0], colorMixRgb_node2.inputs[2])

    mixShader_node2 = nodes.new("ShaderNodeMixShader")
    mixShader_node2.location = (x*5, 4*x)
    links.new(principled3.outputs[0], mixShader_node2.inputs[2])
    links.new(mixShader_node.outputs[0], mixShader_node2.inputs[1])
    links.new(colorMixRgb_node2.outputs[0], mixShader_node2.inputs[0])
    links.new(mixShader_node2.outputs[0], output_node.inputs[0])


#     links.new(invert_node3.outputs[0], mixShader_node.inputs[0])



generateMountainMaterial()
# mat = bpy.data.materials.get("Mat")


def generateWorld():
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


def generateWood():
    # Get material
    mat = bpy.data.materials.get("BSDF_Wood")
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name="BSDF_Wood")
    
    mat.use_nodes = True
    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links
    
    for n in nodes:
        nodes.remove(n)
    
    x = 240
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (x*2, 0)
    # Add a diffuse shader and set its location:    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (0, 0)
    
    links.new(bsdf_node.outputs[0], output_node.inputs[0])
    
    image_node = nodes.new('ShaderNodeTexImage')
    image_node.location = (-1 * x, 0)
    filepath="E:\\Downloads\\WoodPlanksWorn19\\WoodPlanksWorn19\\6K\\WoodPlanksWorn19_COL_VAR1_6K.jpg"
    image_node.image = bpy.data.images.load(filepath)
    image_node.projection = 'BOX'
    
    links.new(image_node.outputs[0], bsdf_node.inputs[0])
    
    coord_node = nodes.new("ShaderNodeTexCoord")
    coord_node.location = (-2 * x, 0)
    
    links.new(coord_node.outputs[0], image_node.inputs[0])


#     bpy.ops.image.open(filepath="E:\\Downloads\\dry_field_8k.hdr", directory="E:\\Downloads\\", files=[{"name":"dry_field_8k.hdr", "name":"dry_field_8k.hdr"}], relative_path=True, show_multiview=False)

#generateWorld()

