import bpy
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.delete(use_global=True)
bpy.ops.surface.primitive_nurbs_surface_surface_add(view_align=False, enter_editmode=False, location=(-2.70894, 0.876662, 0.95013), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.ops.object.editmode_toggle()
bpy.ops.transform.translate(value=(0, 0, -4.70668), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True, use_accurate=False)

