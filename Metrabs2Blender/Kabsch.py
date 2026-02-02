import bpy

import numpy as np
import mathutils
import math
import os
import sys



dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    print(sys.path)

import BVT

# this next part forces a reload in case you edit the source after you first start the blender session
import importlib
importlib.reload(BVT)




dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    print(sys.path)

# this next part forces a reload in case you edit the source after you first start the blender session
import importlib
importlib.reload(BVT)

from BVT import *

CS_KabschOther = "Kabsch2nd"

def find_camera_b_pose(LA, LB):
    """
    Finds the transformation [R|t] such that LB = R * LA + t.
    LA, LB: (N, 3) arrays of matching 3D points in CamA and CamB frames.
    """
    # 1. Center the point sets
    centroid_A = np.mean(LA, axis=0)
    centroid_B = np.mean(LB, axis=0)
    
    AA = LA - centroid_A
    BB = LB - centroid_B

    # 2. Compute Covariance Matrix H
    H = AA.T @ BB

    # 3. Singular Value Decomposition (SVD)
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    # 4. Handle reflection case (det(R) < 0)
    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = Vt.T @ U.T

    # 5. Translation vector
    t = centroid_B - R @ centroid_A

    return R, t

def objcotrans(obj,cname,IDtarget,influence):
    crc = obj.constraints.get(cname)
    if crc is None:
        target = bpy.data.objects.get(IDtarget)
        if target is None:
            print('MISSING TARGET:',IDtarget)
            return('FAILED')
        crc = obj.constraints.new('COPY_TRANSFORMS')
        crc.name = cname
    if crc : #created or not .. should be here now
        target = bpy.data.objects.get(IDtarget)
        if target is None:
            print('MISSING TARGET:',IDtarget)
            obj.constraints.remove(crc)
            return('FAILED')
        crc.target = target
        crc.influence=influence
    else:
        print('still no object:',cname,IDtarget)
        return('FAILED')
        
    return('FINISHED')





class KabschOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.kabsch_operator"
    bl_label = "Align Kabsch"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]
        except: 
            i = 0
        return i>0
    
    def execute (self,context):
        LA = []
        LB = []
        obj = context.active_object
        name_other = obj[CS_KabschOther]
        for ch in obj.children:
          name = ch.name
          LA.append(ch.location)
          name2=name.replace(obj.name,name_other ,1)
          #print(name,name2)
          c2 = bpy.data.objects.get(name2)
          LB.append(c2.location)
          
        #print(LA)
        #print(LB)
        res = find_camera_b_pose(LA, LB)
        #print(res)
        mat_out = mathutils.Matrix(res[0])
        mat_out.resize_4x4()
        #print(mat_out)
        loc, rot, sca = mat_out.decompose()
        #print(loc, rot, sca)
        rot2=rot.to_euler()
        #obj.rotation_euler = rot2
        #obj.location = res[1]
        
        name3 = 'Akku'+obj.name
        damp = 50.
        obj3 = bpy.data.objects.get(name3 )
        if (obj3 is None):
            obj3 = createEmpty(name3,0.5,'CIRCLE')
        obj3.rotation_euler[0] = obj3.rotation_euler[0] + (rot2[0] - obj3.rotation_euler[0])/damp
        obj3.rotation_euler[1] = obj3.rotation_euler[1] + (rot2[1] - obj3.rotation_euler[1])/damp
        obj3.rotation_euler[2] = obj3.rotation_euler[2] + (rot2[2] - obj3.rotation_euler[2])/damp
        obj3.location[0] = obj3.location[0] + (res[1][0]-obj3.location[0])/damp
        obj3.location[1] = obj3.location[1] + (res[1][1]-obj3.location[1])/damp
        obj3.location[2] = obj3.location[2] + (res[1][2]-obj3.location[2])/damp
        
        
        objcotrans(obj,'Kabsch Transform',name3,1.1)
        
        print(obj3.location,obj3.rotation_euler)
        '''
        obj2 = bpy.data.objects.get(name_other )
        obj2.rotation_euler = rot2
        obj2.location = res[1]
        '''

        '''
        obj2.rotation_euler[0] = rot2[0]
        obj2.rotation_euler[1] = rot2[1]
        obj2.rotation_euler[2] = rot2[2]
        obj2.location[0]= res[1][0]
        obj2.location[1]= res[1][1]
        obj2.location[2]= res[1][2]0
        '''
        return {'FINISHED'}        

class LoopKabschOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.loopkabsch_operator"
    bl_label = "Align Kabsch Loop"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]
        except: 
            i = 0
        return i>0
    
    def execute (self,context):
        start = bpy.context.scene.frame_start
        end = bpy.context.scene.frame_end
        actual = start
        step = 1
        bpy.context.scene.frame_set(actual)
        while (actual < end + step):
            print("actual:",actual)
            bpy.ops.object.kabsch_operator()
            actual += step
        return {'FINISHED'}




class KabschPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Kabsch Panel"
    bl_idname = "OBJECT_PT_Kabsch"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]
        except: 
            i = 0
        return i>0


    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Active object is: " + obj.name,icon='OBJECT_DATA')
        try:
            on = obj[CS_KabschOther]
            row = layout.row()
            row.prop(obj, '["%s"]' % (CS_KabschOther),text=CS_KabschOther)
            o = bpy.data.objects.get(on)
            if ( o ):
             
             row = layout.row()
             row.operator("object.kabsch_operator")

             row = layout.row()
             row.operator("object.loopkabsch_operator")
                
        except:
            row = layout.row()
            row.label("Missing prop "+CS_KabschOther)
            




def register():
    bpy.utils.register_class(KabschOperator)
    bpy.utils.register_class(LoopKabschOperator)
    bpy.utils.register_class(KabschPanel)


def unregister():
    bpy.utils.unregister_class(KabschOperator)
    bpy.utils.unregister_class(LoopKabschOperator)
    bpy.utils.register_class(KabschPanel)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.kabsch_operator()
