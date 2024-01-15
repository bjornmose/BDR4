import bpy



def _clonemotion():
    start = bpy.context.scene.frame_start
    end = bpy.context.scene.frame_end
    obj = bpy.context.active_object
    step = obj["bakestep"]
    actual = start
    bpy.context.scene.frame_set(actual)
    while (actual < end + step):
     print("actual:",actual)
     bpy.context.scene.frame_set(actual)
     bpy.ops.anim.keyframe_insert()
     actual += step
     
class op_CloneMotion(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.clone_motion"
    bl_label = "Bake"
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        i = 0
        try:
            i=obj["bakestep"]
        except: 
            i = 0
        return (i > 0)

    def execute(self, context):
        _clonemotion()
        return {'FINISHED'}

     
     
class CloneMotionPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "ClonePanel"
    bl_idname = "OBJECT_PT_CloneMotion"
    '''
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    '''
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    

    def draw(self, context):
        layout = self.layout

        obj = context.object

        obj = context.active_object
        i = 0
        try:
            i=obj["bakestep"]                            
        except: 
            i = 0

        if(i ==0): 
            row = layout.row()
        else:
            row = layout.row()
            row.prop(obj, '["%s"]' % ("bakestep"),text="Step")
            row.operator("object.clone_motion")

def register():
    bpy.utils.register_class(op_CloneMotion)
    bpy.utils.register_class(CloneMotionPanel)
    print('register CloneMotionxxx Done')


def unregister():
    bpy.utils.unregister_class(op_CloneMotion)
    bpy.utils.unregister_class(CloneMotionPanel)
    print('unregister CloneMotionxxx Done')

#run from run
if __name__ == "__main__":
    #runit(bpy.context,1)    
    register()
    print('ConeMotionxx DONE')
#    makefeetrot() 
    
#run with register flag
else: 
    register() 
