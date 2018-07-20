import material
import bpy
ob = bpy.context.active_object

material.assignM(ob, bpy.data.materials.get("BSDF_Wood"))
