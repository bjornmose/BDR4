import bpy
import math
from math import sin, cos, radians
import mathutils
import bmesh
import numpy as np
import os
import sys

#today 2024/02/17

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    print(sys.path)

import BVT

# this next part forces a reload in case you edit the source after you first start the blender session
import importlib
importlib.reload(BVT)

from BVT import *

class _Carmlinkoptions:
   def __init__(self) -> None:
       self.linktoes = True
       self.linkhand = True
       #rigversions = [armlinksto2_7,armlinksto3_5]
       self.rigversion = 27
   
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
    
armlinksto3_5 = {
    "HandIK_R":"hand_ik.R",
    "HandIK_L":"hand_ik.L",
    "FootIK_R":"foot_ik.R",
    "FootIK_L":"foot_ik.L",
    "EllowTargetIK_R":"upper_arm_ik_target.R",
    "EllowTargetIK_L":"upper_arm_ik_target.L",
    "KneeTargetIK_R" :"thigh_ik_target.R",
    "KneeTargetIK_L" :"thigh_ik_target.L",
    "Head":"head"
    }

armlinksto2_7= {
    "HandIK_R":"hand.ik.R",
    "HandIK_L":"hand.ik.L",
    "FootIK_R":"foot.ik.R",
    "FootIK_L":"foot.ik.L",
    "EllowTargetIK_R":"elbow_target.ik.R",
    "EllowTargetIK_L":"elbow_target.ik.L",
    "KneeTargetIK_R" :"knee_target.ik.R",
    "KneeTargetIK_L" :"knee_target.ik.L",
    "Head":"headproxy"
    }
if (armlinkoptions.rigversion == 27):
  armlinksto = armlinksto2_7
else:
  armlinksto = armlinksto3_5
#Library Metrabs Derived Empties 
_lMDE = {
    "kHipRot":"ZD_HipRot",
    "kChestRot":"ZD_ChestRot",
    "kTorso":"ZD_Torso",
    "kTorsoL":"ZD_TorsoL",
    "kTorsoR":"ZD_TorsoR",
    "kHeadRot":"ZD_HeadRot",
    "k11":"ZD_11",
    "k12":"ZD_12",
    "k13":"ZD_13",
    "k14":"ZD_14",
    "kFeetRot":"ZD_FeetRot"
}

def listMDE():
    for mde in _lMDE:
        print(mde,_lMDE[mde])
        

    
    
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


def makehiprot(parent,joma):
    
    pre = parent.name
    ID =pre+_lMDE["kHipRot"]
    #brute force update what ever happend since 
    deleteObject(ID)
    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
        objcoloc(obj,'COL_HipRot_lhip',pre+'_'+joma['lhip'],1.0)
        objcoloc(obj,'COL_HipRot_rhip',pre+'_'+joma['rhip'],0.5)
        objcoTrackTo(obj,'COTT_HipRot_lhip',pre+'_'+joma['lhip'],'TRACK_X','UP_Y',1.0)
        if (armlinkoptions.rigversion == 27):
          objcoLockedTrack(obj,'COLT_HipRot_belly',pre+'_'+joma['bell'],'TRACK_Y','LOCK_X',1.0)
        else:
          objcoLockedTrack(obj,'COLT_HipRot_belly',pre+'_'+joma['bell'],'TRACK_Z','LOCK_X',1.0)

def maketorso(parent,joma):

    pre = parent.name
    ID =pre+_lMDE["kTorso"]
    deleteObject(ID)
    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
    if (obj):
        objcoloc(obj,'COCO_Torso_HipRot',pre+_lMDE["kHipRot"],1.0)
        objcoloc(obj,'COCO_Torso_ChestRot',pre+_lMDE["kChestRot"],0.5)

    ID =pre+_lMDE["kTorsoR"]
    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
    if (obj):
        objcoloc(obj,'COCO_rTorso_rsho',pre+'_'+joma['rsho'],1.0)
        objcoloc(obj,'COCO_rTorso_rhip',pre+'_'+joma['rhip'],0.5)

    ID =pre+_lMDE["kTorsoL"]
    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
    if (obj):
        objcoloc(obj,'COCO_lTorso_rsho',pre+'_'+joma['lsho'],1.0)
        objcoloc(obj,'COCO_lTorso_rhip',pre+'_'+joma['lhip'],0.5)

    ID =pre+_lMDE["kTorso"]
    obj = bpy.data.objects.get(ID)
    if (obj):
        objcoTrackTo(obj,'COTT_Torso_trackL',pre+_lMDE["kTorsoL"],'TRACK_X','UP_Z',1.0)
        objcoTrackTo(obj,'COTT_Torso_trackR',pre+_lMDE["kTorsoR"],'TRACK_NEGATIVE_X','UP_Z',0.5)
        objcoLockedTrack(obj,'COLT_Torso_neck',pre+'_'+joma['neck'],'TRACK_Z','LOCK_X',1.0)

                 
def makechestrot(parent,joma):

    pre = parent.name
    ID =pre+_lMDE["kChestRot"]
    #brute force update what ever happend since 
    deleteObject(ID)

    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
        objcoloc(obj,'COCO_chestrot_lcla',pre+'_'+joma['lcla'],1.0)
        objcoloc(obj,'COCO_chestrot_rcla',pre+'_'+joma['rcla'],0.5)
        objcoTrackTo(obj,'COTT_chestrot_lcla',pre+'_'+joma['lcla'],'TRACK_X','UP_Y',1.0)
        if (armlinkoptions.rigversion == 27):
          objcoLockedTrack(obj,'COLT_chestrot_spin',pre+'_'+joma['spin'],'TRACK_NEGATIVE_Y','LOCK_X',1.0)
        else:
          objcoLockedTrack(obj,'COLT_chestrot_spin',pre+'_'+joma['spin'],'TRACK_NEGATIVE_Z','LOCK_X',1.0)
                 
def makeheadrot(parent,joma):

    pre = parent.name
    ID =pre+_lMDE["kHeadRot"]
    deleteObject(ID)

    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
    if (obj):
        objcoloc(obj,'COCO_HeadRot_lear',pre+'_'+joma['lear'],1.0)
        objcoloc(obj,'COCO_HeadRot_rear',pre+'_'+joma['rear'],0.5)
        objcoTrackTo(obj,'COTT_HeadRot_nose',pre+'_'+joma['nose'],'TRACK_Z','UP_Y',1.0)
        #objcoLockedTrack(obj,'COLT_HeadRot_htop',pre+'_'+joma['htop'],'TRACK_Y','LOCK_Z',1.0)
        objcoLockedTrack(obj,'COLT_HeadRot_lear',pre+'_'+joma['lear'],'TRACK_X','LOCK_Z',1.0)

def makefeetrot(parent,joma):

    pre = parent.name
    ID =pre+_lMDE["kFeetRot"]
    deleteObject(ID)

    
    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
    if (obj):        
        objcoloc(obj,'COCO_FeetRot_lfoot',pre+'_'+joma['lfoo'],1.0)
        objcoloc(obj,'COCO_FeetRot_rfoot',pre+'_'+joma['rfoo'],0.5)
        objcoTrackTo(obj,'COTT_FeetRot_lfoo',pre+'_'+joma['lfoo'],'TRACK_Z','UP_Y',1.0)

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
        print('CleanUp:')
        if(False):
         for mde in _lMDE:
            deleteObject(pre+_lMDE[mde])
        else:
         print('keep _lMDE for inspection')

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

def cobonerot(bone,cname,target,IDbone,influence):
        lcname = 'L_'+cname
        crc = bone.constraints.get(lcname)
        if crc is None:
            crc = bone.constraints.new('COPY_ROTATION')
            crc.target = target
            crc.subtarget = IDbone
            crc.name = lcname
            crc.influence = influence
        else:
            crc.target = target
            crc.subtarget = IDbone
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
        
def createbones(arm,bnames):
    print('createbones',bnames)
    bpy.ops.object.mode_set(mode='OBJECT')
    try: #B2.7 style
        bpy.context.scene.objects.active = arm
        arm.select=True
        bpy.ops.object.mode_set(mode='EDIT')
        bones = bpy.context.active_object.data.edit_bones
    except:
        try: #B3xx style
          print('B2.7 failed')
          bpy.context.scene.objects.active = arm
          arm.select_set(True)
          bpy.ops.object.mode_set(mode='EDIT')
          bones = bpy.context.active_object.data.edit_bones
        except:
            print('ERROR')
            return(1)
    lx = 0.
    for bname in bnames:
        bone = arm.pose.bones.get(bname)
        if bone is None:
           lx += 0.5
           bone = bones.new(bname)
           bone.head = (lx,0.,0.)
           bone.tail = (lx,0.,1.)
             
    bpy.ops.object.mode_set(mode='OBJECT')
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
            MDEbones = []
            homearm = obj
            for mde in _lMDE:
              print(mde,_lMDE[mde])
              MDEbones.append(_lMDE[mde])
            print(MDEbones)
            createbones(homearm,MDEbones)
            '''build constraints for helpers'''
            bone = self.findbone(homearm,_lMDE["kTorsoR"])
            if bone is not None:
                subtarget = joma['rsho']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,1.0)
                subtarget = joma['rhip']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,homearm,subtarget,0.5)
            

            
            if(False):
             n_probe = pre+'_'+joma['rwri']
             o_probe = bpy.data.objects.get(n_probe)
             if o_probe is not None:
                makehiprot(obj,joma)
                makechestrot(obj,joma)
                maketorso(obj,joma)
                makeheadrot(obj,joma)

            bone = self.findbone(arm,armlinksto["HandIK_R"])
            if bone is not None:
                subtarget = joma['rwri']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,1.0)
                if (armlinkoptions.linkhand):
                    subtarget = joma['relb']
                    cname = pre+'_'+subtarget
                    if (armlinkoptions.rigversion == 27):
                      cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_NEGATIVE_Y','LOCK_Z',1.0)

            bone = self.findbone(arm,armlinksto["HandIK_L"])
            if bone is not None:
                subtarget = joma['lwri']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,1.0)
                if (armlinkoptions.linkhand):
                    subtarget = joma['lelb']
                    cname = pre+'_'+subtarget
                    if (armlinkoptions.rigversion == 27):
                      cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_NEGATIVE_Y','LOCK_Z',1.0)

            subtarget = joma['relb']   
            bone = self.findbone(arm,armlinksto["EllowTargetIK_R"])
            cname = pre+'_'+subtarget
            if bone is not None:
                coboneloc(bone,cname,obj,subtarget,1.0)

            subtarget = joma['lelb']   
            bone = self.findbone(arm,armlinksto["EllowTargetIK_L"])
            cname = pre+'_'+subtarget
            if bone is not None:
                coboneloc(bone,cname,obj,subtarget,1.0)

            bone = self.findbone(arm,armlinksto["FootIK_R"])
            if bone is not None:
                subtarget = joma['rank']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,1.0)
                if (armlinkoptions.linkhand):
                    subtarget = joma['rtoe']
                    cname = pre+'_'+subtarget
                    if (armlinkoptions.rigversion == 27):
                      cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_Y','LOCK_X',1.0)

            bone = self.findbone(arm,armlinksto["FootIK_L"])
            if bone is not None:
                subtarget = joma['lank']
                cname = pre+'_'+subtarget
                coboneloc(bone,cname,obj,subtarget,1.0)
                if (armlinkoptions.linkhand):
                    subtarget = joma['ltoe']
                    cname = pre+'_'+subtarget
                    if (armlinkoptions.rigversion == 27):
                      cobonelockedtrack(bone,cname,obj,subtarget,'TRACK_Y','LOCK_X',1.0)


            print('DebugStop done')
            return {'FINISHED'}
            

            bone = self.findbone(arm,armlinksto["FootIK_L"])
            if bone is not None:
                cname = pre+'_'+joma['lank']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,1.0)
                if (armlinkoptions.linktoes):
                  cname = pre+'_'+joma['ltoe']
                  IDtarget ='{:}{:}'.format(nameP,cname)
                  if (armlinkoptions.rigversion == 27):
                    self.cocolockedtrack(bone,cname,IDtarget,nameP,'TRACK_Y','LOCK_X')

            bone = self.findbone(arm,armlinksto["FootIK_R"])
            if bone is not None:
                cname = pre+'_'+joma['rank']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,1.0)
                if (armlinkoptions.linktoes):
                  cname = pre+'_'+joma['rtoe']
                  IDtarget ='{:}{:}'.format(nameP,cname)
                  if (armlinkoptions.rigversion == 27):
                    self.cocolockedtrack(bone,cname,IDtarget,nameP,'TRACK_Y','LOCK_X')

            bone = self.findbone(arm,armlinksto["EllowTargetIK_R"])
            if bone is not None:
                cname = pre+'_'+joma['relb']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,1.0)

            bone = self.findbone(arm,armlinksto["EllowTargetIK_L"])
            if bone is not None:
                cname = pre+'_'+joma['lelb']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,1.0)

            bone = self.findbone(arm,armlinksto["KneeTargetIK_R"])
            if bone is not None:
                cname = pre+'_'+joma['rkne']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,1.0)

            bone = self.findbone(arm,armlinksto["KneeTargetIK_L"])
            if bone is not None:
                cname = pre+'_'+joma['lkne']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,1.0)

            bone = self.findbone(arm,"torso")
            if bone is not None:
                cname = pre+_lMDE['kChestRot']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,1.0)
                cname = pre+_lMDE['kHipRot']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,0.5)
                cname = pre+'_'+joma['bell']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,1.0)
                cname = pre+_lMDE['kTorso']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocorot(bone,cname,IDtarget,nameP)
                

            bone = self.findbone(arm,"hips")
            if bone is not None:
                cname =pre+_lMDE['kChestRot']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,1.0)
                cname = pre+_lMDE['kHipRot']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,0.5)
                self.cocorot(bone,cname,IDtarget,nameP)
                cname = pre+'_'+joma['bell']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,1.0)

            bone = self.findbone(arm,"chest")
            if bone is not None:
                cname =pre+_lMDE['kChestRot']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,1.0)
                self.cocorot(bone,cname,IDtarget,nameP)
                
                cname = pre+_lMDE['kHipRot']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,0.5)

                    
            '''
                    
            bone = self.findbone(arm,"head")
            if bone is not None:
                cname = 'Oszhead'
                IDtarget ='{:}{:}'.format(nameP,cname)
                target = bpy.data.objects.get(IDtarget)
                self.cocoik(bone,cname,IDtarget,1,nameP)
            '''

            bone = self.findbone(arm,"shoulder.L")
            if bone is not None:
                cname = pre+'_'+joma['lsho']
                IDtarget ='{:}{:}'.format(nameP,cname)
                target = bpy.data.objects.get(IDtarget)
                self.cocoik(bone,cname,IDtarget,1,nameP)

            bone = self.findbone(arm,"shoulder.R")
            if bone is not None:
                cname = pre+'_'+joma['rsho']
                IDtarget ='{:}{:}'.format(nameP,cname)
                target = bpy.data.objects.get(IDtarget)
                self.cocoik(bone,cname,IDtarget,1,nameP)
            
            bone = self.findbone(arm,"root")
            if bone is not None:

                #cname = pre+'_FeetRot'
                cname = pre+_lMDE['kTorso']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP,1.0)
                crc = bone.constraints.get('L_'+cname)
                if crc is not None:
                    crc.use_z = 0

                cname = pre+_lMDE['kTorso']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocorot(bone,cname,IDtarget,nameP)
                crc = bone.constraints.get('R_'+cname)
                if crc is not None:
                    crc.use_x = 0
                    crc.use_y = 0
                    crc.use_z = 1

            bone = self.findbone(arm,armlinksto["Head"])
            if bone is not None:
                cname = pre+_lMDE['kHeadRot']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocorot(bone,cname,IDtarget,nameP)
                #cname = pre+'_'+joma['htop']
                #IDtarget ='{:}{:}'.format(nameP,cname)
                #target = bpy.data.objects.get(IDtarget)
                #self.cocoik(bone,cname,IDtarget,1,nameP)
        print('LinkArmature.execute done')
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
            except: 
                pass
            row = layout.row()
            row.operator("object.linka2armature_operator")
            row.operator("object.unlinka2armature_operator")

"""   
        row = layout.row()
        row.operator("object.pushtweak_operator")
"""    




def register():
    bpy.utils.register_class(LinkArmature2A)
    bpy.utils.register_class(UnLinkArmature2A)
    bpy.utils.register_class(LinkArm2ArmPanel)
    print('register LinkA2ArmVxxx Done')


def unregister():
    bpy.utils.unregister_class(LinkArmature2A)
    bpy.utils.unregister_class(UnLinkArmature2A)
    bpy.utils.unregister_class(LinkArm2ArmPanel)
    del theGen

#run from run
if __name__ == "__main__":
    #runit(bpy.context,1)    
    register()
    listMDE()
    print('LinkA2ArmVxx DONE')
#    makefeetrot() 
    
#run with register flag
else: 
    register() 
