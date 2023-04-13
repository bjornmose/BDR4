import bpy
start = bpy.context.scene.frame_start
end = bpy.context.scene.frame_end
step = 5
actual = start
bpy.context.scene.frame_set(actual)
while (actual < end + step):
 print("actual:",actual)
 bpy.context.scene.frame_set(actual)
 bpy.ops.anim.keyframe_insert()
 actual += step
