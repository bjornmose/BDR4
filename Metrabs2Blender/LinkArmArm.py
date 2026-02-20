import bpy
import math
from math import sin, cos, radians
import mathutils
import bmesh
import numpy as np
import os
import sys

#today 2024/11/03

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    print(sys.path)

import BVT

# this next part forces a reload in case you edit the source after you first start the blender session
import importlib
importlib.reload(BVT)

from BVT import *
defaultrigversion = 35
class _Carmlinkoptions:
   def __init__(self) -> None:
       self.linktoes = False
       self.linkhand = True
       self.stiffhand = False
       self.influenceEllbow = 0.75
       self.influenceKnee = 0.75
       self.rigversion = defaultrigversion
    
   def getlinkdict(self):
       if self.rigversion == 27 :
           return dictarmlink2_7
       if self.rigversion == 35 :
           return dictarmlink3_5
       return None
       
       
   
armlinkoptions = _Carmlinkoptions()
'''
#look up info
''' 
   
#joint/target map used for buiding constraints in armature    
joma_simpl = {
        "neck" : "neck_smpl",
        "nose" : "nose_coco",
        "pelv" : "pelv_smpl",
        "htop" : "htop_mpi_inf_3dhp",
        "lsho" : "lsho_smpl",
        "lcla" : "lcla_smpl",
        "lelb" : "lelb_smpl",
        "lwri" : "lwri_smpl",
        "lhip" : "lhip_smpl",
        "lkne" : "lkne_smpl",
        "lank" : "lank_smpl",
        "lhan" : "lhan_smpl",
        "lfoo" : "lank_smpl",
        "ltoe" : "ltoe_smpl",
        "rsho" : "rsho_smpl",
        "rcla" : "rcla_smpl",
        "relb" : "relb_smpl",
        "rwri" : "rwri_smpl",
        "rhip" : "rhip_smpl",
        "rkne" : "rkne_smpl",
        "rank" : "rank_smpl",
        "leye" : "leye_coco",
        "lear" : "lear_coco",
        "reye" : "reye_coco",
        "rear" : "rear_coco",
        "rhan" : "rhan_smpl",
        "rfoo" : "rank_smpl",
        "rtoe" : "rtoe_smpl",
        "bell" : "bell_smpl",
        "spin" : "spin_smpl"
}    
joma_simplOM = {
        "neck" : "neck_smpl",
        "nose" : "nosecoco",
        "pelv" : "pelv_smpl",
        "htop" : "htop_mpi_inf_3dhp",
        "lsho" : "lsho_smpl",
        "lelb" : "lelb_smpl",
        "lwri" : "lwri_smpl",
        "lhip" : "lhip_smpl",
        "lkne" : "lkne_smpl",
        "lank" : "lank_smpl",
        "lhan" : "lhan_smpl",
        "lfoo" : "lank_smpl",
        "ltoe" : "ltoe_smpl",
        "rsho" : "rsho_smpl",
        "relb" : "relb_smpl",
        "rwri" : "rwri_smpl",
        "rhip" : "rhip_smpl",
        "rkne" : "rkne_smpl",
        "rank" : "rank_smpl",
        "leye" : "leye_coco",
        "lear" : "learcoco",
        "reye" : "reyecoco",
        "rear" : "rearcoco",
        "rhan" : "rhan_smpl",
        "rfoo" : "rank_smpl",
        "rtoe" : "rtoe_smpl"
}    
    
joma_picked = {
#joma= {
        "lkne":"lkne",
        "rkne":"rkne",
        "lank":"lank",
        "rank":"rank",
        "ltoe":"ltoe",
        "rtoe":"rtoe",
        "neck":"neck",
        "lsho":"lsho",
        "rsho":"rsho",
        "lelb":"lelb",
        "relb":"relb",
        "lwri":"lwri",
        "rwri":"rwri",
        "lhan":"lhan",
        "rhan":"rhan",
        "htop":"htop_muco",
        "lear":"lear_cmu_panoptic",
        "leye":"leye_sailvos",
        "lhip":"lhip_h36m",
        "nose":"nose_cmu_panoptic",
        "pelv":"pelv_h36m",
        "rear":"rear_cmu_panoptic",
        "reye":"reae_sailvos",
        "rhip":"rhip_h36m",
        "rfoo" : "rank",
        "lfoo" : "lank"

    }
    
dictarmlink3_5 = {
    "HandIK_R":"hand_ik.R",
    "HandIK_L":"hand_ik.L",
    "FootIK_R":"foot_ik.R",
    "FootIK_L":"foot_ik.L",
    "EllowTargetIK_R":"upper_arm_ik_target.R",
    "EllowTargetIK_L":"upper_arm_ik_target.L",
    "KneeTargetIK_R" :"thigh_ik_target.R",
    "KneeTargetIK_L" :"thigh_ik_target.L",
    "Shoulder_R": "shoulder.R",
    "Shoulder_L": "shoulder.L",
    "Head":"head",
    "Neck":"neck",
    "Root":"root",
    "Torso":"torso",
    "Chest":"chest",
    "Hips":"hips",
    "ForearmR":"DEF-forearm.R.001",
    "ForearmL":"DEF-forearm.L.001"
    }

dictarmlink2_7= {
    "HandIK_R":"hand.ik.R",
    "HandIK_L":"hand.ik.L",
    "FootIK_R":"foot.ik.R",
    "FootIK_L":"foot.ik.L",
    "EllowTargetIK_R":"elbow_target.ik.R",
    "EllowTargetIK_L":"elbow_target.ik.L",
    "KneeTargetIK_R" :"knee_target.ik.R",
    "KneeTargetIK_L" :"knee_target.ik.L",
    "Shoulder_R": "shoulder.R",
    "Shoulder_L": "shoulder.L",
    "Head":"headproxy",
    "Neck":"neck",
    "Root":"root",
    "Torso":"torso",
    "Chest":"chest",
    "Hips":"hips",
    "ForearmR":"DEF-forearm.02.R",
    "ForearmL":"DEF-forearm.02.L"
    }



#Dictionary Metrabs Derived Bones
_dMDB = {
    "kHipRot": {"name":"ZD_HipRot","tail":[0.,0.,1.],"parent":""},
    "kChestRot":{"name":"ZD_ChestRot","tail":[0.,0.,1.]},
    "kTorso":{"name":"ZD_Torso","tail":[0.,0.,1.]},
    "kTorsoR":{"name":"ZD_TorsoR","tail":[0.,1.,0.]},
    "kTorsoL":{"name":"ZD_TorsoL","tail":[0.,1.,0.]},
    "kHeadRot":{"name":"ZD_HeadRot","tail":[0.,1.,0.]},
    "kHips":{"name":"ZD_Hips","tail":[-1.,0.,0.],"parent":"kTorso"},
#    "kChest":{"name":"ZD_Chest","tail":[1.,0.,0.],"parent":"kTorso"},
    "kChest":{"name":"ZD_Chest","tail":[1.,0.,0.],"parent":"kChestRot"},
    "kTorsoLoc":{"name":"ZD_TorsoLoc","tail":[0.,1.,0.],"parent":"kTorso"},
    "kKneeR":{"name":"ZD_KneeR","tail":[0.,1.,0.],"parent":"rkne"},
    "kKneeL":{"name":"ZD_KneeL","tail":[0.,1.,0.],"parent":"lkne"}
}

# get the name of a _dMDB bone
def _nMDB(key):
    return (_dMDB[key]["name"])
    
    
joma_list ={
    "smpl+head_30":joma_simpl,
    "smpl+head_30OM":joma_simplOM,
    "":joma_picked,
    }
    


def objcoloc(obj,cname,IDtarget,influence):
    crc = obj.constraints.get(cname)
    if crc is None:
        target = bpy.data.objects.get(IDtarget)
        if target is None:
            print('MISSING TARGET:',IDtarget)
            return('FAILED')
        crc = obj.constraints.new('COPY_LOCATION')
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

def objcoLockedTrack(obj,cname,IDtarget,track_axis,lock_axis,influence):
    crc = obj.constraints.get(cname)
    if crc is None:
        target = bpy.data.objects.get(IDtarget)
        if target is None:
            print('MISSING TARGET:',IDtarget)
            return('FAILED')
        crc = obj.constraints.new('LOCKED_TRACK')
        crc.name = cname
    if crc : #created or not .. should be here now
        target = bpy.data.objects.get(IDtarget)
        crc.target = target
        crc.track_axis=track_axis
        crc.lock_axis=lock_axis
        crc.influence=influence
    return('FINISHED')

def objcoTrackTo(obj,cname,IDtarget,track_axis,up_axis,influence):
    crc = obj.constraints.get(cname)
    if crc is None:
        target = bpy.data.objects.get(IDtarget)
        if target is None:
            print('MISSING TARGET:',IDtarget)
            return('FAILED')
        crc = obj.constraints.new('TRACK_TO')
        crc.name = cname
    if crc : #created or not .. should be here now
        target = bpy.data.objects.get(IDtarget)
        crc.target = target
        crc.track_axis=track_axis
        crc.up_axis=up_axis
        crc.influence=influence
    return('FINISHED')


def _clear_ArmatureConstraints(arm):
    print('_clear_ArmatureConstraints')
    for bone in arm.pose.bones:
        for co in bone.constraints:
            try:
                _ta = co.target 
            except:
                continue # no property target
            if _ta is None:
                bone.constraints.remove(co) 
    print('_clear_ArmatureConstraints Done')
	
def _Tar_clear_ArmatureConstraints(arm,pat):
    print('_Tar_clear_ArmatureConstraints')
    for bone in arm.pose.bones:
        for co in bone.constraints:
            try:
                _ta = co.target 
            except:
                continue # no property target
            if _ta is None:                
                bone.constraints.remove(co)
            else: 
                _na = co.name 
                if (_na.find(pat) > -1):
                    bone.constraints.remove(co)
                    print('remove',_na,'from',bone.name)
    print('_Tar_clear_ArmatureConstraints Done')

class UnLinkArmature2A(bpy.types.Operator):
    """UnLinkArmatureToSimpl"""
    bl_idname = "object.unlinka2armature_operator"
    bl_label = "Detach A2Armature "

    @classmethod
    def poll(cls, context):

        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]
        except: 
            i = 0
        return i>0
    
    def execute(self,context):
        obj = context.active_object
        #nameP = obj.name
        nameP = ''
        try:
            a=obj["~armature"]
        except: 
            obj["~armature"] = '*None*'
        nameA = obj["~armature"]
        arm = bpy.data.objects.get(nameA)
        print(nameA,' is:',arm)
        pre = obj.name
        _Tar_clear_ArmatureConstraints(arm,pre)
        return {'FINISHED'}

def coboneloc(bone,cname,target,IDbone,influence):
        lcname = 'L_'+cname
        crc = bone.constraints.get(lcname)
        if crc is None:
            crc = bone.constraints.new('COPY_LOCATION')
            crc.target = target
            crc.subtarget = IDbone
            crc.name = lcname
            crc.influence = influence
        else:
            crc.target = target
            crc.subtarget = IDbone
            crc.influence = influence
            return('FINISHED')

def coboneIK(bone,cname,target,IDbone,len,influence):
        lcname = 'IK_'+cname
        crc = bone.constraints.get(lcname)
        if crc is None:
            crc = bone.constraints.new('IK')
            crc.target = target
            crc.subtarget = IDbone
            crc.name = lcname
            crc.chain_count = len
            crc.influence = influence
        else:
            crc.target = target
            crc.subtarget = IDbone
            crc.chain_count = len
            crc.influence = influence
            return('FINISHED')


def cobonerot(bone,cname,target,IDbone,use_x,use_y,use_z,influence):
        lcname = 'R_'+cname
        crc = bone.constraints.get(lcname)
        if crc is None:
            crc = bone.constraints.new('COPY_ROTATION')
            crc.target = target
            crc.subtarget = IDbone
            crc.name = lcname
            crc.use_x = use_x
            crc.use_y = use_y
            crc.use_z = use_z
            crc.influence = influence
        else:
            crc.target = target
            crc.subtarget = IDbone
            crc.use_x = use_x
            crc.use_y = use_y
            crc.use_z = use_z
            crc.influence = influence
            return('FINISHED')

def cobonetrackto(bone,cname,target,IDbone,track_axis,up_axis,influence):
        lcname = 'TT_'+cname
        crc = bone.constraints.get(lcname)
        if crc is None:
            crc = bone.constraints.new('TRACK_TO')
            crc.target = target
            crc.subtarget = IDbone
            crc.name = lcname
            crc.track_axis = track_axis
            crc.up_axis = up_axis
            crc.influence = influence
        else:
            crc.target = target
            crc.subtarget = IDbone
            crc.track_axis = track_axis
            crc.up_axis = up_axis
            crc.influence = influence
            return('FINISHED')


def cobonelockedtrack(bone,cname,target,IDbone,track_axis,lock_axis,influence):
        lcname = 'LT_'+cname
        crc = bone.constraints.get(lcname)
        if crc is None:
            crc = bone.constraints.new('LOCKED_TRACK')
            crc.target = target
            crc.subtarget = IDbone
            crc.name = lcname
            crc.track_axis=track_axis
            crc.lock_axis=lock_axis
            crc.influence = influence
        else:
            crc.target = target
            crc.subtarget = IDbone
            crc.track_axis=track_axis
            crc.lock_axis=lock_axis
            crc.influence = influence
            return('FINISHED')
        
def createbones_ex(arm,dicbones,joma):
    print('dicbones',dicbones)
    bpy.ops.object.mode_set(mode='OBJECT')
    try: #B2.7 style
        bpy.context.scene.objects.active = arm
        arm.select=True
        bpy.ops.object.mode_set(mode='EDIT')
        bones = bpy.context.active_object.data.edit_bones
    except:
        try: #B3xx style
          print('B2.7 failed')
          bpy.context.view_layer.objects.active = arm
          arm.select_set(True)
          bpy.ops.object.mode_set(mode='EDIT')
          bones = bpy.context.active_object.data.edit_bones
        except Exception as error:
         print('ERROR',error)
         return(1)
    cs_MTRCollection = "MTR_Helper"
    col = arm.data.collections.get(cs_MTRCollection)
    if col is None:
        col = arm.data.collections.new(cs_MTRCollection)

        
    lx = 0.
    for key in dicbones:
        item = dicbones[key]
        t = item["tail"]
        bname = item["name"]
        bp = None
        try:
            pname = item["parent"]
            if pname:
                try:
                  bp = bones[_nMDB(pname)]
                except:
                  bp = bones[joma[pname]]
        except:
            pass
        bone = arm.pose.bones.get(bname)
        if bone is None:
           lx += 1.5
           bone = bones.new(bname)
           if bp is None:
               bone.head = (lx,0.,0.)
               bone.tail = (lx+t[0],t[1],t[2])
           else:
               h = bp.head
               bone.head = (h[0],h[1],h[2])
               bone.tail = (h[0]+t[0],h[1]+t[1],h[2]+t[2])
               bone.parent = bp
        
        
           bone.parent = bp
           try:#fails in 4.x
               bone.layers=(False, True , False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
           except:
               col.assign(bone)
               pass
        
           
             
    bpy.ops.object.mode_set(mode='OBJECT')
    try:
      bpy.data.armatures[arm.name].layers[1] = True
    except:
      pass
    return (0)



class LinkArmature2A(bpy.types.Operator):
    """LinkArmatureToSimpl"""
    bl_idname = "object.linka2armature_operator"
    bl_label = "Link to A2Armature "

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]
        except: 
            i = 0
        return i>0

    
    def cocoloc(self,bone,cname,IDtarget,pxname,influence):
        crc = bone.constraints.get('L_'+pxname+cname)
        if crc is None:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                return('FAILED')
            crc = bone.constraints.new('COPY_LOCATION')
            crc.target = target
            crc.name = 'L_'+pxname+cname
            crc.influence = influence
        else:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                bone.constraints.remove(crc)
                return('FAILED')
            crc.target = target
            crc.influence = influence
            print(bone.name,IDtarget, 'loc_update')
            return('FINISHED')

    def cocorot(self,bone,cname,IDtarget,pxname):
        crc = bone.constraints.get('R_'+pxname+cname)
        if crc is None:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                return('FAILED')
            crc = bone.constraints.new('COPY_ROTATION')
            crc.target = target
            crc.name = 'R_'+pxname+cname
        else:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                bone.constraints.remove(crc)
                return('FAILED')
            crc.target = target
            print(bone.name,IDtarget, 'rot_update')
            return('FINISHED')

    def cocolockedtrack(self,bone,cname,IDtarget,pxname,track_axis,lock_axis):
        crc = bone.constraints.get('LT_'+pxname+cname)
        if crc is None:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                return('FAILED')
            crc = bone.constraints.new('LOCKED_TRACK')
            crc.target = target
            crc.track_axis=track_axis
            crc.lock_axis=lock_axis
            crc.name = 'LT_'+pxname+cname
        else:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                bone.constraints.remove(crc)
                return('FAILED')
            crc.target = target
            crc.track_axis=track_axis
            crc.lock_axis=lock_axis
            print(bone.name,IDtarget, 'LOCKED_TRACK_update')
            return('FINISHED')


    def cocoik(self,bone,cname,IDtarget,len,pxname):
        crc = bone.constraints.get('I_'+pxname+cname)
        if crc is None:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                return('FAILED')
            crc = bone.constraints.new('IK')
            crc.target = target
            crc.chain_count = len
            crc.name = 'I_'+pxname+cname
        else:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                bone.constraints.remove(crc)
                return('FAILED')
            crc.target = target
            print(bone.name,IDtarget, 'ik_update')
            return('FINISHED')
 
            
    def findbone(self,arm,name):
            bone = arm.pose.bones.get(name)
            if bone is None:
                print(name)
                print('not in:',arm)
                print('!!!!!!!')    
            return(bone)
    

                                      
    def execute(self,context):
        obj = context.active_object
        #nameP = obj.name
        nameP = ''
        try:
            a=obj["~armature"]
        except: 
            obj["~armature"] = '*None*'
        nameA = obj["~armature"]
        arm = bpy.data.objects.get(nameA)
        print(nameA,' is:',arm)
        pre = obj.name
        if(arm is not None):
            arm['bakestep']=1
            _clear_ArmatureConstraints(arm)
            armlinkoptions.rigversion = arm['RV']
            armlinksto = armlinkoptions.getlinkdict()

        # see if 'rwri' element of jome is there
        '''
        n_probe = pre+'_'+joma['rwri']
        o_probe = bpy.data.objects.get(n_probe)
        if o_probe is None:
            print("Missing",n_probe,"leaving 4 Now")
            return {'FINISHED'}
        '''
        try:
            res = obj['skeleton']
            joma = joma_list[res]
            print('Object defined joma')
        except:
            joma = joma_list['']

        
        if arm is not None:
            '''create helper bones'''
            homearm = obj
            createbones_ex(homearm,_dMDB,joma)
            '''build constraints for helpers'''
            '''ktorso'''
            bone = self.findbone(homearm,_nMDB("kTorsoR"))
            if bone is not None:
                subtarget = joma['rsho']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,1.0)
                subtarget = joma['rhip']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,0.5)
            
            bone = self.findbone(homearm,_nMDB("kTorsoL"))
            if bone is not None:
                subtarget = joma['lsho']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,1.0)
                subtarget = joma['lhip']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,0.5)

            bone = self.findbone(homearm,_nMDB("kTorso"))
            if bone is not None:
                '''position'''
                subtarget = _nMDB("kTorsoR")
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,1.0)
                subtarget = _nMDB("kTorsoL")
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,0.5)
                '''rotation'''
                subtarget = _nMDB("kTorsoL")
                cname = pre+'_'+subtarget
                cobonetrackto(bone,cname,obj,subtarget,'TRACK_X','UP_Z',1.0)

            '''kHipRot'''
            bone = self.findbone(homearm,_nMDB("kHipRot"))
            if bone is not None:
                subtarget = joma['rhip']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,1.0)
                subtarget = joma['lhip']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,0.5)
                cobonetrackto(bone,cname,obj,subtarget,'TRACK_X','UP_Z',1.0)
                subtarget = joma['bell']
                cname = pre+'_'+subtarget
                if (armlinkoptions.rigversion == 27):
                  cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_Y','LOCK_X',1.0)
                else:
                  cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_Z','LOCK_X',1.0)

            '''kChestRot'''
            bone = self.findbone(homearm,_nMDB("kChestRot"))
            if bone is not None:
                subtarget = joma['rcla']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,1.0)
                subtarget = joma['lcla']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,0.5)
                cobonetrackto(bone,cname,obj,subtarget,'TRACK_X','UP_Y',1.0)
                subtarget = joma['spin']
                cname = pre+'_'+subtarget
                if (armlinkoptions.rigversion == 27):
                  cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_NEGATIVE_Y','LOCK_X',1.0)
                else:
                  cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_NEGATIVE_Z','LOCK_X',1.0)

            '''kHeadRot'''
            bone = self.findbone(homearm,_nMDB("kHeadRot"))
            if bone is not None:
                subtarget = joma['rear']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,1.0)
                subtarget = joma['lear']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,0.5)
                subtarget = joma['nose']
                cname = pre+'_'+subtarget
                cobonetrackto(bone,cname,obj,subtarget,'TRACK_Z','UP_Y',1.0)
                subtarget = joma['lear']
                cname = pre+'_'+subtarget
                cobonelockedtrack(bone,cname,homearm,subtarget,'TRACK_X','LOCK_Z',1)

            '''Knee rotation'''
            bone = self.findbone(homearm,joma['rkne'])
            if bone is not None:
                subtarget = _nMDB("kTorso")
                cname = pre+'_'+subtarget
                cobonerot(bone,cname,homearm,subtarget,1,1,1,1.0)
            bone = self.findbone(homearm,joma['lkne'])
            if bone is not None:
                subtarget = _nMDB("kTorso")
                cname = pre+'_'+subtarget
                cobonerot(bone,cname,homearm,subtarget,1,1,1,1.0)


            '''helpers done'''
            

            bone = self.findbone(arm,armlinksto["HandIK_R"])
            if bone is not None:
                subtarget = joma['rwri']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,1.0)
                # not really happy with either option play with it and bring better solution 

                if (armlinkoptions.stiffhand): #deps circle
                    subtarget = armlinksto["ForearmR"]
                    cname = pre+'_'+subtarget
                    cobonerot(bone,cname,arm,subtarget,1,1,1,1.0)
        
                if (armlinkoptions.linkhand):
                    subtarget = joma['relb']
                    cname = pre+'_'+subtarget
                    if (armlinkoptions.rigversion == 27):
                      cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_NEGATIVE_Y','LOCK_Z',1.0)
                    else: #fix me 
                      #coboneIK(bone,cname,obj,subtarget,1,1.0)
                      cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_NEGATIVE_Y','LOCK_X',1.0)

            bone = self.findbone(arm,armlinksto["HandIK_L"])
            if bone is not None:
                subtarget = joma['lwri']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,1.0)
                #see hand right
                if (armlinkoptions.stiffhand): #deps circle
                    subtarget = armlinksto["ForearmL"]
                    cname = pre+'_'+subtarget
                    cobonerot(bone,cname,arm,subtarget,1,1,1,1.0)

                if (armlinkoptions.linkhand):
                    subtarget = joma['lelb']
                    cname = pre+'_'+subtarget
                    if (armlinkoptions.rigversion == 27):
                      cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_NEGATIVE_Y','LOCK_Z',1.0)
                    else: # fix me
                      #coboneIK(bone,cname,obj,subtarget,1,1.0)
                      cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_NEGATIVE_Y','LOCK_X',1.0)
                    

            subtarget = joma['relb']   
            bone = self.findbone(arm,armlinksto["EllowTargetIK_R"])
            cname = pre+'_'+subtarget
            if bone is not None:
                coboneloc(bone,cname,obj,subtarget,armlinkoptions.influenceEllbow)

            subtarget = joma['lelb']   
            bone = self.findbone(arm,armlinksto["EllowTargetIK_L"])
            cname = pre+'_'+subtarget
            if bone is not None:
                coboneloc(bone,cname,obj,subtarget,armlinkoptions.influenceEllbow)

            bone = self.findbone(arm,armlinksto["FootIK_R"])
            if bone is not None:
                subtarget = joma['rank']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,1.0)
                if (armlinkoptions.linktoes):
                    subtarget = joma['rtoe']
                    cname = pre+'_'+subtarget
                    if (armlinkoptions.rigversion == 27):
                      cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_Y','LOCK_X',1.0)
                    else:
                      cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_NEGATIVE_Y','LOCK_X',1.0)

            bone = self.findbone(arm,armlinksto["FootIK_L"])
            if bone is not None:
                subtarget = joma['lank']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,1.0)
                if (armlinkoptions.linktoes):
                    subtarget = joma['ltoe']
                    cname = pre+'_'+subtarget
                    if (armlinkoptions.rigversion == 27):
                      cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_Y','LOCK_X',1.0)
                    else:
                      cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_NEGATIVE_Y','LOCK_X',1.0)

            bone = self.findbone(arm,armlinksto["KneeTargetIK_R"])
            cname = pre+'_'+subtarget
            if bone is not None:
                subtarget =  _nMDB("kKneeR")
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,armlinkoptions.influenceKnee)

            bone = self.findbone(arm,armlinksto["KneeTargetIK_L"])
            if bone is not None:
                subtarget =  _nMDB("kKneeL")
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,armlinkoptions.influenceKnee)

            bone = self.findbone(arm,armlinksto["Shoulder_R"])
            if bone is not None:
                subtarget = joma['rcla']   
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,1.0)
                subtarget = joma['lcla']   
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,0.5)

                subtarget = joma['rsho']   
                cname = pre+'_'+subtarget
                coboneIK(bone,cname,obj,subtarget,1,1.0)

            bone = self.findbone(arm,armlinksto["Shoulder_L"])
            if bone is not None:
                subtarget = joma['lcla']   
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,1.0)
                subtarget = joma['rcla']   
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,0.5)

                subtarget = joma['lsho']   
                cname = pre+'_'+subtarget
                coboneIK(bone,cname,obj,subtarget,1,1.0)

            
            bone = self.findbone(arm,armlinksto["Root"])
            if bone is not None:
                subtarget = _nMDB("kTorso")
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,1.0)
                cobonerot(bone,cname,obj,subtarget,0,0,1,1.0)

            bone = self.findbone(arm,armlinksto["Torso"])    
            if bone is not None:
                if (armlinkoptions.rigversion == 27):
                    subtarget = _nMDB("kChestRot")
                    cname = pre+'_'+subtarget
                    coboneloc(bone,cname,obj,subtarget,1.0)
                    subtarget = _nMDB("kHipRot")
                    cname = pre+'_'+subtarget
                    coboneloc(bone,cname,obj,subtarget,0.5)
                else:
                    subtarget = _nMDB("kTorsoLoc")
                    cname = pre+'_'+subtarget
                    coboneloc(bone,cname,obj,subtarget,1.0)
                subtarget = _nMDB("kTorso")
                cname = pre+'_'+subtarget
                cobonerot(bone,cname,obj,subtarget,1,1,1,1.0)

            bone = self.findbone(arm,armlinksto["Chest"])
            if bone is not None:
                if (armlinkoptions.rigversion == 27):
                    subtarget = _nMDB("kChestRot")
                    cname = pre+'_'+subtarget
                    coboneloc(bone,cname,obj,subtarget,1.0)
                    cobonerot(bone,cname,obj,subtarget,1,1,1,1.0)
                    subtarget = _nMDB("kHipRot")
                    cname = pre+'_'+subtarget
                    coboneloc(bone,cname,obj,subtarget,0.5)
                else:
                    subtarget = _nMDB("kChest")
                    cname = pre+'_'+subtarget
                    coboneloc(bone,cname,obj,subtarget,1.0)
                subtarget = _nMDB("kChestRot")
                cname = pre+'_'+subtarget
                cobonerot(bone,cname,obj,subtarget,1,1,1,1.0)
                    

            bone = self.findbone(arm,armlinksto["Hips"])
            if bone is not None:
                if (armlinkoptions.rigversion == 27):
                    subtarget = _nMDB("kChestRot")
                    cname = pre+'_'+subtarget
                    coboneloc(bone,cname,obj,subtarget,1.0)
                    subtarget = _nMDB("kHipRot")
                    cname = pre+'_'+subtarget
                    coboneloc(bone,cname,obj,subtarget,0.5)
                else:
                    subtarget = _nMDB("kHips")
                    cname = pre+'_'+subtarget
                    coboneloc(bone,cname,obj,subtarget,1.0)
                subtarget = _nMDB("kHipRot")
                cname = pre+'_'+subtarget
                cobonerot(bone,cname,obj,subtarget,1,1,1,1.0)

            bone = self.findbone(arm,armlinksto["Neck"])
            if bone is not None:
                subtarget = joma['neck']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,1.0)
                subtarget = joma['nose']
                cname = pre+'_'+subtarget
                coboneIK(bone,cname,obj,subtarget,1,0.2)




            bone = self.findbone(arm,armlinksto["Head"])
            if bone is not None:
                subtarget = _nMDB("kHeadRot")
                cname = pre+'_'+subtarget
                cobonerot(bone,cname,obj,subtarget,1,1,1,1.0)
        else:
            print('no arm')
        print('LinkArmature2A.execute done')
        return {'FINISHED'}

class makeRigVersion(bpy.types.Operator):
    """UnLinkArmatureToSimpl"""
    bl_idname = "metrabs.makerigversion"
    bl_label = "RegisterRigVersion"

    def execute(self,context):
        obj = context.active_object
        arm = bpy.data.objects.get(obj["~armature"])
        arm["RV"] = defaultrigversion
        #no need to create here -- however nice to see them b4 they get linked
        if (1):
          createbones_ex(obj,_dMDB)

        return {'FINISHED'}



class LinkArm2ArmPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "LinkA2APanel"
    bl_idname = "OBJECT_PT_LA2ACOCO"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]
            po=obj.pose
            if po is None:
             i=0  
        except: 
            i = 0
        return i>0


    def draw(self, context):
        layout = self.layout

        obj = context.object

        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]                            
        except: 
            i = 0

        if(i ==0): 
            row = layout.row()
        else:
            try:
                a=obj["~armature"]
                if a is not None:
                    row = layout.row()
                    row.prop(obj, '["%s"]' % ("~armature"),text="Armature")
                    arm = bpy.data.objects.get(a)
                    if arm is not None: 
                      try:
                        arm["RV"]
                        row.prop(arm, '["%s"]' % ("RV"),text="RigVersion")
                        row = layout.row()
                        row.operator(LinkArmature2A.bl_idname)
                        row.operator(UnLinkArmature2A.bl_idname)
                      except:
                        row.operator(makeRigVersion.bl_idname)
        
            except: 
                pass

"""   
        row = layout.row()
        row.operator("object.pushtweak_operator")
"""    




def register():
    bpy.utils.register_class(LinkArmature2A)
    bpy.utils.register_class(UnLinkArmature2A)
    bpy.utils.register_class(LinkArm2ArmPanel)
    bpy.utils.register_class(makeRigVersion)
    print('register LinkA2ArmVxxx Done')


def unregister():
    bpy.utils.unregister_class(LinkArmature2A)
    bpy.utils.unregister_class(UnLinkArmature2A)
    bpy.utils.unregister_class(LinkArm2ArmPanel)
    bpy.utils.unregister_class(makeRigVersion)
    del theGen

#run from run
if __name__ == "__main__":
    #runit(bpy.context,1)    
    register()
    print('LinkA2ArmVxx DONE')
#    makefeetrot() 
    
#run with register flag
else: 
    register() 
