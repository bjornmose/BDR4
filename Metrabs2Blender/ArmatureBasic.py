import bpy


def _putz_All_ArmatureConstraints(arm):
    print('_putz_ALL_ArmatureConstraints')
    for bone in arm.pose.bones:
        for co in bone.constraints:
          print('bone:',bone.name,'CO:',co.name)
          bone.constraints.remove(co) 
    print('_putz_ALL_ArmatureConstraints Done')


def _putz_Targetless_ArmatureConstraints(arm):
    print('_putz_ArmatureConstraints')
    for bone in arm.pose.bones:
        for co in bone.constraints:
            try:
                _ta = co.target 
            except:
                continue # no property target
            if _ta is None:
                print('bone:',bone.name,'CO:',co.name)
                bone.constraints.remove(co) 
    print('_putz_Targetless_ArmatureConstraints Done')
	
def _ListTargetless_ArmatureConstraints(arm):
    print('_list_lost_target_ArmatureConstraints')
    count = 0
    for bone in arm.pose.bones:
        for co in bone.constraints:
            try:
                _ta = co.target 
            except:
                continue # no property target
            if _ta is None:
            	print('bone:',bone.name,'CO:',co.name)
            	count += 1
    print('_list_lost_target_ArmatureConstraints Done' ,count)
	

class PutzAllArmature(bpy.types.Operator):
    bl_idname = "object.putzallarmature_operator"
    bl_label = "Remove ALL Bone Constraints"

    def execute(self,context):
        obj = context.active_object
        _putz_All_ArmatureConstraints(obj)
        return {'FINISHED'}


class PutzArmature(bpy.types.Operator):
    bl_idname = "object.putzarmature_operator"
    bl_label = "Remove Lost Targets Bone Constraints"

    def execute(self,context):
        obj = context.active_object
        _putz_Targetless_ArmatureConstraints(obj)
        return {'FINISHED'}
        
class ListLostTargetsArmature(bpy.types.Operator):
    bl_idname = "object.listlosttargetsarmature_operator"
    bl_label = "List Lost Targets Bone Constraints"

    def execute(self,context):
        obj = context.active_object
        _ListTargetless_ArmatureConstraints(obj)
        return {'FINISHED'}



class PutzArmPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "ArmPutz"
    bl_idname = "OBJECT_PT_ARMPRUTZ"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
#    bl_context = "unsinn"
    @classmethod
    def poll(self, context):
        obj = context.active_object
        probe = obj.pose
        if (probe is not None): 
            return 1
        return 0

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("object.putzarmature_operator")
        row = layout.row()
        row.operator("object.listlosttargetsarmature_operator")
        row = layout.row()
        row.operator("object.putzallarmature_operator")






def register():
    bpy.utils.register_class(ListLostTargetsArmature)
    bpy.utils.register_class(PutzAllArmature)
    bpy.utils.register_class(PutzArmature)
    bpy.utils.register_class(PutzArmPanel)


def unregister():
    bpy.utils.unregister_class(ListLostTargetsArmature)
    bpy.utils.unregister_class(PutzAllArmature)
    bpy.utils.unregister_class(PutzArmature)
    bpy.utils.unregister_class(PutzArmPanel)

#run from run
if __name__ == "__main__":
    register()
    
#run with register flag
else: register() 
print('PutzArmVxx DONE')
