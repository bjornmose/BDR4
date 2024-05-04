import bpy
import json
import os
import inspect
import sys
import time

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    print(sys.path)

import BVT

# this next part forces a reload in case you edit the source after you first start the blender session
import importlib
importlib.reload(BVT)

from BVT import *



from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator





joints_coco_19 =  [
        "neck",
        "nose",
        "pelv",
        "lsho",
        "lelb",
        "lwri",
        "lhip",
        "lkne",
        "lank",
        "rsho",
        "relb",
        "rwri",
        "rhip",
        "rkne",
        "rank",
        "leye",
        "lear",
        "reye",
        "rear"
    ]
    
    
joints_mpi_inf_3dhp_28 = [
#bones =  [
        "thor",
        "spi4",
        "spi2",
        "spin",
        "pelv",
        "neck",
        "head",
        "htop",
        "lcla",
        "lsho",
        "lelb",
        "lwri",
        "lhan",
        "rcla",
        "rsho",
        "relb",
        "rwri",
        "rhan",
        "lhip",
        "lkne",
        "lank",
        "lfoo",
        "ltoe",
        "rhip",
        "rkne",
        "rank",
        "rfoo",
        "rtoe"
    ]
      
#   "skeleton": "smpl+head_30",
joints_smpl_head_30 =[
        "pelv_smpl",
        "lhip_smpl",
        "rhip_smpl",
        "bell_smpl",
        "lkne_smpl",
        "rkne_smpl",
        "spin_smpl",
        "lank_smpl",
        "rank_smpl",
        "thor_smpl",
        "ltoe_smpl",
        "rtoe_smpl",
        "neck_smpl",
        "lcla_smpl",
        "rcla_smpl",
        "head_smpl",
        "lsho_smpl",
        "rsho_smpl",
        "lelb_smpl",
        "relb_smpl",
        "lwri_smpl",
        "rwri_smpl",
        "lhan_smpl",
        "rhan_smpl",
        "htop_mpi_inf_3dhp",
        "lear_coco",
        "leye_coco",
        "nose_coco",
        "rear_coco",
        "reye_coco"
    ]
    
# "skeleton": "smpl+head_30OM",
joints_smpl_head_30OM =[
        "pelv_smpl",
        "lhip_smpl",
        "rhip_smpl",
        "bell_smpl",
        "lkne_smpl",
        "rkne_smpl",
        "spin_smpl",
        "lank_smpl",
        "rank_smpl",
        "thor_smpl",
        "ltoe_smpl",
        "rtoe_smpl",
        "neck_smpl",
        "lcla_smpl",
        "rcla_smpl",
        "head_smpl",
        "lsho_smpl",
        "rsho_smpl",
        "lelb_smpl",
        "relb_smpl",
        "lwri_smpl",
        "rwri_smpl",
        "lhan_smpl",
        "rhan_smpl",
        "htop_mpi_inf_3dhp",
        "learcoco",
        "leyecoco",
        "nosecoco",
        "rearcoco",
        "reyecoco"
    ]
    
    
    
    
joints_all= [
        "lhip",
        "rhip",
        "bell",
        "lkne",
        "rkne",
        "spin",
        "lank",
        "rank",
        "thor",
        "ltoe",
        "rtoe",
        "neck",
        "lcla",
        "rcla",
        "head",
        "lsho",
        "rsho",
        "lelb",
        "relb",
        "lwri",
        "rwri",
        "lhan",
        "rhan",
        "pelv",
        "head_h36m",
        "head_muco",
        "head_sailvos",
        "htop_h36m",
        "htop_muco",
        "htop_sailvos",
        "lank_cmu_panoptic",
        "lank_h36m",
        "lank_muco",
        "lank_sailvos",
        "lcla_muco",
        "lear_cmu_panoptic",
        "lear_sailvos",
        "lelb_cmu_panoptic",
        "lelb_h36m",
        "lelb_muco",
        "lelb_sailvos",
        "leye_cmu_panoptic",
        "leye_sailvos",
        "lfin_h36m",
        "lfoo_h36m",
        "lfoo_muco",
        "lhan_muco",
        "lhan_sailvos",
        "lhip_cmu_panoptic",
        "lhip_h36m",
        "lhip_muco",
        "lhip_sailvos",
        "lkne_cmu_panoptic",
        "lkne_h36m",
        "lkne_muco",
        "lkne_sailvos",
        "lsho_cmu_panoptic",
        "lsho_h36m",
        "lsho_muco",
        "lsho_sailvos",
        "lthu_h36m",
        "ltoe_h36m",
        "ltoe_muco",
        "ltoe_sailvos",
        "lwri_cmu_panoptic",
        "lwri_h36m",
        "lwri_muco",
        "lwri_sailvos",
        "neck_cmu_panoptic",
        "neck_h36m",
        "neck_muco",
        "neck_sailvos",
        "nose_cmu_panoptic",
        "nose_sailvos",
        "pelv_cmu_panoptic",
        "pelv_h36m",
        "pelv_muco",
        "pelv_sailvos",
        "rank_cmu_panoptic",
        "rank_h36m",
        "rank_muco",
        "rank_sailvos",
        "rcla_muco",
        "rear_cmu_panoptic",
        "rear_sailvos",
        "relb_cmu_panoptic",
        "relb_h36m",
        "relb_muco",
        "relb_sailvos",
        "reye_cmu_panoptic",
        "reye_sailvos",
        "rfin_h36m",
        "rfoo_h36m",
        "rfoo_muco",
        "rhan_muco",
        "rhan_sailvos",
        "rhip_cmu_panoptic",
        "rhip_h36m",
        "rhip_muco",
        "rhip_sailvos",
        "rkne_cmu_panoptic",
        "rkne_h36m",
        "rkne_muco",
        "rkne_sailvos",
        "rsho_cmu_panoptic",
        "rsho_h36m",
        "rsho_muco",
        "rsho_sailvos",
        "rthu_h36m",
        "rtoe_h36m",
        "rtoe_muco",
        "rtoe_sailvos",
        "rwri_cmu_panoptic",
        "rwri_h36m",
        "rwri_muco",
        "rwri_sailvos",
        "spi2_muco",
        "spi4_muco",
        "spin_h36m",
        "spin_muco",
        "spin_sailvos",
        "thor_muco"
    ]

joints_picked= [
        "lkne",
        "rkne",
        "spin",
        "lank",
        "rank",
        "thor",
        "ltoe",
        "rtoe",
        "neck",
        "lcla",
        "rcla",
        "head",
        "lsho",
        "rsho",
        "lelb",
        "relb",
        "lwri",
        "rwri",
        "lhan",
        "rhan",
        "pelv",
        "htop_muco",
        "lear_cmu_panoptic",
        "leye_cmu_panoptic",
        "leye_sailvos",
        "lhip_h36m",
        "nose_cmu_panoptic",
        "pelv_h36m",
        "rear_cmu_panoptic",
        "reye_cmu_panoptic",
        "reye_sailvos",
        "rhip_h36m",
    ]



skel_list ={
    "smpl+head_30OM":joints_smpl_head_30OM,
    "smpl+head_30":joints_smpl_head_30,
    "mpi_inf_3dhp_28":joints_mpi_inf_3dhp_28,
    "coco_19":joints_coco_19,
    "":joints_picked,
    "all":joints_all
    }



def cocoloc(bone,cname,IDtarget,pxname):
    crc = bone.constraints.get('L_'+pxname+cname)
    if crc is None:
        target = bpy.data.objects.get(IDtarget)
        if target is None:
            print('MISSING TARGET:',IDtarget)
            return('FAILED')
        crc = bone.constraints.new('COPY_LOCATION')
        crc.target = target
        crc.name = 'L_'+pxname+cname
    else:
        target = bpy.data.objects.get(IDtarget)
        if target is None:
            print('MISSING TARGET:',IDtarget)
            bone.constraints.remove(crc)
            return('FAILED')
        crc.target = target
        print(bone.name,IDtarget, 'loc_update')
        return('FINISHED')




def readArmatureRestPos(name,jPre,scalediv):
    d_min = 100000.0
    res_arm = None
    pname = 'pose3d' 
    boxes = None
    try: 
        with open(name) as json_file:
            data = json.load(json_file)
    except:
        print('except',name)
        return res_arm
    try:
        gotpose = data[pname]
    except:
        print('no pose')
        return res_arm
    
    p1 = data[pname]
    if (not p1): return res_arm
    aPre = 'Arm_'
    res_arm = create_armature(aPre+jPre,'TestBone')

    bpy.ops.object.mode_set(mode='OBJECT')
    try: #B2.7 style
        bpy.context.scene.objects.active = res_arm
        res_arm.select=True
        bpy.ops.object.mode_set(mode='EDIT')
        bones = bpy.context.active_object.data.edit_bones
    except:
        try: #B3xx style
          print('B3.xx style')
          bpy.context.view_layer.objects.active = res_arm
          res_arm.select_set(True)
          bpy.ops.object.mode_set(mode='EDIT')
          bones = bpy.context.active_object.data.edit_bones
        except Exception as error:
            print('ERROR',error)
            return res_arm

   


    
    for joint in p1:
        jName = joint[0]
        bone = bones.new(jName)
        lx = joint[1] / scalediv
        ly = joint[2] / scalediv
        lz = joint[3] / scalediv
        bone.head = (lx,ly,lz)
        bone.tail = (lx,ly,lz+1.0)
        bone.layers=(True, False , False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                     False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)

        
            
    bpy.ops.object.mode_set(mode='OBJECT')
    if (True):
        for joint in p1:
            jname = joint[0]
            bone = res_arm.pose.bones.get(jname)
            if bone is not None:
                cname = '_'+jname
                IDtarget = jPre+'_'+jname
                cocoloc(bone,cname,IDtarget,jPre)
        res_arm["bakestep"]=1
    return res_arm


def makejoints(parent,joints,pre):
    for joint in joints:
        objname = pre + joint
        obj = bpy.data.objects.get(objname)
        if ( not obj):
            obj = createEmpty(objname,0.1,'SPHERE')
            obj.parent = parent
    
def readMetrabsJoints(name,pat):
    res =[]
    print('Filter:',pat)
    try: 
        with open(name) as json_file:
            data = json.load(json_file)
            joints = data['joints']
            for jo in joints:
                #print('Filter',pat,jo)
                if pat in jo:
              	   res.append(jo)  
    except:
        print('except',name)
        return (None)
    return(res)




def readmetrabs(name,frame,box,jPre,sf):
    d_min = 100000.0
    res_box = box
    pname = 'pose3d' 
    boxes = None
    try: 
        with open(name) as json_file:
            data = json.load(json_file)
    except:
        print('except',name)
        return res_box
    '''
    try:
        failmsg = data['fail']
        return res_box
    except:
        pass
        #print('no fail')
    '''
    try:
        gotpose = data[pname]
    except:
        print('no pose')
        return res_box
    try:
        boxes = data['boxes']
    except:
        print('no boxes')
    if (boxes):
        #print('DO BOXES')                
        l =len(boxes)
        if l>0:
          xb = boxes[0][0]
          yb = boxes[0][1]
          res_box = [xb,yb]
          d_min = (xb - box[0])*(xb - box[0]) +(yb - box[1])*(yb - box[1]) 
        for nb in range(1,l):
            xn = boxes[nb][0]
            yn = boxes[nb][1]
            dn = (xn - box[0])*(xn - box[0]) +(yn - box[1])*(yn - box[1])
            print('dn',dn,'d_min',d_min)
            if dn < d_min:
                res_box = [xn,yn]
                d_min = dn
                pname='pose3d{0:d}'.format(nb+1)
                print(res_box,pname)        
    
    p1 = data[pname]
    if (not p1): return res_box
    missmatch = 0
    for joint in p1:
        jName = jPre + joint[0]
        #print(jName)
        obj = bpy.data.objects.get(jName)
        if (obj):
            lx = joint[1] / sf
            ly = joint[2] / sf
            lz = joint[3] / sf
            fcu_x = obj.animation_data.action.fcurves[0]
            fcu_y = obj.animation_data.action.fcurves[1]
            fcu_z = obj.animation_data.action.fcurves[2]
            fcu_x.keyframe_points.insert(frame,lx,options={'NEEDED','FAST'})
            fcu_y.keyframe_points.insert(frame,ly,options={'NEEDED','FAST'})
            fcu_z.keyframe_points.insert(frame,lz,options={'NEEDED','FAST'})
        else:
            missmatch += 1
            #print('joint missmatch',jName)
    #print('Joints UnUsed:',100*missmatch/len(p1),'%')
    return res_box


''' 
kind of man in the middle aproach
collect a 3D track: (time[frame] location(x.y,z)) for each METRABS joint
the place to apply fiters
'''
class C_rawMeterasData():
    def __init__(self) -> None:
        self.myData = {}
        self.firstframe = 1000
        self.lastframe = -1000
        self.channels = {}
        self.joints = []
        pass

    def addframe(self,name,frame):
        pname = 'pose3d' 
        try: 
            with open(name) as json_file:
                data = json.load(json_file)
                boxes = data['boxes'] # at least on box must be there
                self.myData[frame] = data[pname] #quick and dirty .. no box selction
                self.joints = data['joints']
                if self.firstframe > frame : self.firstframe = frame
                if self.lastframe < frame : self.lastframe = frame
        except:
            print('except',name)
        return
    
    def extract_all(self):
        for ch in self.joints:
            print('Extracting',ch)
            chdata = self.extract_channel(ch)
            self.channels[ch] = chdata
            #print('\n****xx***',ch,chdata,) // ok that works

    def extract_channel(self,chname):
        channel = {}
        for frame in range (self.firstframe,self.lastframe+1):
            try:
              f = self.myData[frame]
              for joint in f:
                chn = joint[0]
                if chn == chname:
                  x = joint[1]
                  y = joint[2]
                  z = joint[3]
              channel[frame] = (x,y,z)
            except: 
                pass
            channel[frame] = (x,y,z)
        return channel
    
    def inject_action(self,obj,chdata,sf):
        fcu_x = obj.animation_data.action.fcurves[0]
        fcu_y = obj.animation_data.action.fcurves[1]
        fcu_z = obj.animation_data.action.fcurves[2]
        for frame in range (self.firstframe,self.lastframe+1):
          try:  
            loc = chdata[frame] 
            lx = loc[0]/ sf
            ly = loc[1]/ sf
            lz = loc[2]/ sf
            fcu_x.keyframe_points.insert(frame,lx,options={'NEEDED','FAST'})
            fcu_y.keyframe_points.insert(frame,ly,options={'NEEDED','FAST'})
            fcu_z.keyframe_points.insert(frame,lz,options={'NEEDED','FAST'})
          except (KeyError):
            pass  
        
    def redavg(self,chdata,w):
        res = {}
        lx = ly = lz = 0
        n = 0
        for frame in range (self.firstframe,self.lastframe+1):
          try:  
            loc = chdata[frame] 
            lx += loc[0]
            ly += loc[1]
            lz += loc[2]            
            n  += 1
          except (KeyError):
            pass 
          if ( (n > 0) and  (frame % w ) == 0):
              res[frame] = (lx/n,ly/n,lz/n)
              n = 0
              lx = ly = lz = 0
        return res

    def redmedian(self,chdata,incr,w):
        res = {}
        for step in range (self.firstframe,self.lastframe+1,incr):
          lx = []
          ly = []
          lz = []
          for frame in range(1,w+1):
              try:  
                loc = chdata[step+frame - w//2] 
                lx.append(loc[0])
                ly.append(loc[1])
                lz.append(loc[2])            
              except (KeyError):
                pass 
        
          lx.sort()
          ly.sort()
          lz.sort()
          l = len(lx)
          if l > 0:
            res[step] = (lx[l//2],ly[l//2],lz[l//2])
        return res

    def redfilter(self,chdata,filter,w):
        res = {}
        fl = len (filter)
        for step in range (self.firstframe,self.lastframe+1,w):
          lx = 0
          ly = 0
          lz = 0
          k = 0
          for n in range(0,fl):
              try:  
                loc = chdata[step+n - fl//2] 
                lx += filter[n] * loc[0]
                ly += filter[n] * loc[1]
                lz += filter[n] * loc[2]     
                k  += filter[n]
              except (KeyError):
                pass 
          res[step] = (lx/k,ly/k,lz/k)
        
        return res
        
        
    
    def _dump(self):
        print(self.myData)
        return



def readmetrabs2D(name,frame,box,jPre,rx,ry,sf):
    d_min = 100000.0
    res_box = box
    pname = 'pose2d' 
    boxes = None
    try: 
        with open(name) as json_file:
            data = json.load(json_file)
    except:
        print('except',name)
        return res_box
    '''
    try:
        failmsg = data['fail']
        return res_box
    except:
        pass
        #print('no fail')
    '''
    try:
        gotpose = data[pname]
    except:
        print('no pose')
        return res_box
    try:
        boxes = data['boxes']
    except:
        print('no boxes')
    if (boxes):
        print('DO BOXES')                
        l =len(boxes)
        if l>0:
          xb = boxes[0][0]
          yb = boxes[0][1]
          res_box = [xb,yb]
          d_min = (xb - box[0])*(xb - box[0]) +(yb - box[1])*(yb - box[1]) 
        for nb in range(1,l):
            xn = boxes[nb][0]
            yn = boxes[nb][1]
            dn = (xn - box[0])*(xn - box[0]) +(yn - box[1])*(yn - box[1])
            print('dn',dn,'d_min',d_min)
            if dn < d_min:
                res_box = [xn,yn]
                d_min = dn
                pname='pose2d{0:d}'.format(nb+1)
                print(pname)        
    
    p1 = data[pname]
    if (not p1): return res_box
    missmatch = 0
    _rx=bpy.data.scenes[0].render.resolution_x
    _ry=bpy.data.scenes[0].render.resolution_y
    for joint in p1:
        jName = jPre + joint[0]
        #print(jName)
        obj = bpy.data.objects.get(jName)
        if (obj):
            lx = (joint[1]-rx/2) / sf 
            lz = (-joint[2]+ry/2) / sf
            #lz = joint[3] / sf
            ly = 0
            fcu_x = obj.animation_data.action.fcurves[0]
            fcu_y = obj.animation_data.action.fcurves[1]
            fcu_z = obj.animation_data.action.fcurves[2]
            fcu_x.keyframe_points.insert(frame,lx,options={'NEEDED','FAST'})
            fcu_y.keyframe_points.insert(frame,ly,options={'NEEDED','FAST'})
            fcu_z.keyframe_points.insert(frame,lz,options={'NEEDED','FAST'})
        else:
            missmatch += 1
            #print('joint missmatch',jName)
    print('Joints UnUsed:',100*missmatch/len(p1),'%')
    return res_box        

#More advanced animation, editing animation curves, building an spiral.
def makeactions_2d():
    for bone in bones:
        obj = bpy.data.objects.get(bone)
        print(obj)
        if (obj) :
            obj.animation_data_create()
            obj.animation_data.action = bpy.data.actions.new(name=bone+'Action')
            fcu_x = obj.animation_data.action.fcurves.new(data_path="location", index=0)
            fcu_y = obj.animation_data.action.fcurves.new(data_path="location", index=1)
            #fcu_z = obj.animation_data.action.fcurves.new(data_path="location", index=2)

def makeactions_3d(joints,pre):
    n_reused = 0
    n_created = 0
    for joint in joints:
        obj = bpy.data.objects.get(pre+joint)
        if (obj) :
            if obj.animation_data is None:
                obj.animation_data_create()
            if obj.animation_data.action is None: 
                n_created += 1
                obj.animation_data.action = bpy.data.actions.new(name=pre+joint+'3D')
                fcu_x = obj.animation_data.action.fcurves.new(data_path="location", index=0)
                fcu_y = obj.animation_data.action.fcurves.new(data_path="location", index=1)
                fcu_z = obj.animation_data.action.fcurves.new(data_path="location", index=2)
            else:
                #print('continue / replace ',obj.animation_data.action.name )
                n_reused += 1
    print('makeactions_3d continue',n_reused,'of',len(joints))
    return [n_reused,n_created,len(joints)]
                
def completeObjectProperties(obj):
    try:
        T=obj["infile"]
    except: 
        obj["infile"] = '/Posedata'

    try:
        T=obj["inpath"]
    except: 
        obj["inpath"] = '*none*'

    try:
        T=obj["start_frame"]
    except: 
        obj["start_frame"] = 1

    try:
        T=obj["end_frame"]
    except: 
        obj["end_frame"]   = 5

    try:
        T=obj["incr"] 
    except:
        obj["incr"]   = 1
    try:
        T=obj["scaledidvisor"] 
    except:
        obj["scaledidvisor"]   = 100
    try:
        T=obj["ZBA"] 
    except:
        obj["ZBA"]   = 1
    obj["metrabs"] = 1  
    try:
        tof=obj["tof"] 
    except:
        obj["tof"]=3
        tof=3
    try:
        frw=obj["frw"] 
    except:
        frw=100
        obj["frw"]=frw
        
      
                
                
class read_metrabs_info(bpy.types.Operator):
    """print info file"""
    bl_idname = "object.read_metrabs_info"
    bl_label = "read_metrabs_job"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]
        except: 
            i = 0
        try:
            p=obj["inpath"]
            p += "jobinfo.json"
            #print(p)
            if p != None:
                if os.path.exists(p):
                    i=1
                else: i =0
        except:
                i = 0
        
        return i>0


    def execute(self, context):
        obj = context.active_object
        name = obj['inpath']+"jobinfo.json"
        print('******read jobinfo.json *******')
        print(name)
        with open(name) as json_file:
            data = json.load(json_file)
            print(data)
            res = data['skeleton']
            obj['skeleton'] = res
            print('skeleton=',res,'.')
            j = skel_list[res]
            print('***joints imported****')
            print(j)
            res = data['start']
            obj['start_frame'] = res
            res = data['end']
            obj['end_frame'] = res

        return {'FINISHED'}

'''
pretty much pointless that way removed from UI 
'''
class push_down_joints_action(bpy.types.Operator):
    bl_idname = "object.push_down_joints_action"
    bl_label = "push_down_joints_action"

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
        obj = context.active_object
        pre = obj.name + '_'
        try:
            res = obj['skeleton']
            joints = skel_list[res]
        except:
            print('missing joint list')
            return {'CANCELLED'}
            
        for joint in joints:
            obj = bpy.data.objects.get(pre+joint)
            if (obj) :
                if obj.animation_data is not None:
                    action = obj.animation_data.action
                    if action is not None:
                        #print('push down Action', obj.name)
                        track = obj.animation_data.nla_tracks.new()
                        stript = track.strips.new(action.name, action.frame_range[0], action)
                        obj.animation_data.action = None
              
        
        return {'FINISHED'}        
    

class delete_childen_actions(bpy.types.Operator):
    bl_idname = "object.delete_children_actions"
    bl_label = "delete_children_actions"

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
        obj = context.active_object
        for ch in obj.children:
          if ch.animation_data is not None:
            ch.animation_data.action = None
        return {'FINISHED'}        

class delete_childen(bpy.types.Operator):
    bl_idname = "mtr.delete_children"
    bl_label = "delete_children"

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
        obj = context.active_object
        for ch in obj.children:
          deleteObject(ch.name)
        return {'FINISHED'}        


class _ETA():
    def __init__(self,items):
      try:
        self.starttick =time.monotonic_ns()
      except:
        self.starttick =time.monotonic()*1000000000.      
      self.curtick = self.starttick 
      self.prevtick = self.curtick  
      self.items =items
      self.itemsdone =0
      self.tpifs=0.
      self.tpifloating=0.
      self.slopefs=0.
      self.slopefloating=0.
      self.timelefs=0.
      self.timeelapsed=0
      self.timeleftfloating=0.
      
    
    #@classmethod
    def ticknow(self,itdone,plen):
     prevtpifs = self.tpifs
     prevtpifloating = self.tpifloating
     self.prevtick = self.curtick
     self.itemsdone = itdone 
     try:
       ticknow = time.monotonic_ns()
     except:
       ticknow = time.monotonic()*1000000000.
     self.curtick = ticknow 
     self.timeelapsed = (ticknow - self.starttick)
     self.tpifs = self.timeelapsed / itdone
     #we need to have previos values
     if (itdone > 1):
       self.tpifloating=((self.curtick-self.prevtick)+plen*self.tpifloating) /(plen+1)
       self.slopefs = ((self.tpifs - prevtpifs) + plen*self.slopefs) /(plen+1)
       self.slopefloating= ((self.tpifloating-prevtpifloating) + plen*self.slopefloating) /(plen+1)
       self.timeleftfloating = self.tpifloating * (self.items - self.itemsdone)
       self.timelefs = self.tpifs * (self.items - self.itemsdone)
     
     
    def gettpifs(self):
      return(self.tpifs/1000000)

    def gettotal(self):
      total = (self.curtick - self.starttick)
      return(total/1000000000)

    def timeleftfloating_sec(self):
      tl = self.timeleftfloating/1000000000
      return(tl) 
      
    def guesttotal(self):
      tt = (self.timeelapsed + self.timeleftfloating)/1000000000 
      return(tt)

    def guesttotalslopefs(self):
      tpi = self.tpifs + self.slopefs * (self.items - self.itemsdone)
      tt = (self.timeelapsed + tpi * (self.items - self.itemsdone))/1000000000
      return(tt)

    def guesttotalslopefloating(self):
      tpi = self.tpifloating+ self.slopefloating * (self.items - self.itemsdone)
      tt = (self.timeelapsed + tpi * (self.items - self.itemsdone))/1000000000
      return(tt)

    def guestleft(self):
      tpi = self.tpifs + self.slopefs * (self.items - self.itemsdone)
      tl = (tpi * (self.items - self.itemsdone))/1000000000
      return(tl) 

    def guestleftfloating(self):
      tpi = self.tpifloating+ self.slopefloating * (self.items - self.itemsdone)
      tl = (tpi * (self.items - self.itemsdone))/1000000000
      return(tl) 


    
def progbar(pv,blen):
  bar = ''
  for i in range(0,blen):    
    if (i < pv*blen/100):
      bar = bar+'X'
    else:
      bar = bar+'_'
  return bar
  

class import_metrabs(bpy.types.Operator):
    bl_idname = "object.import_metrabs_operator"
    bl_label = "Import metrabs data"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]
        except: 
            i = 0
        try:
            p=obj["inpath"]
            #print(p)
            if p != None:
                if os.path.exists(p):
                    i=1
                else: i =0
        except: 
            i = 0

        return i>0
    
    def execute (self,context):
        obj = context.active_object
        print('importMetrabsJson----------------Start' ) 
        '''
        try:
            res = obj['skeleton']
            joints = skel_list[res]
            print('Object defined joints')
        except:
            print('## Manual joints ## in ',__file__,'line:',inspect.currentframe().f_lineno)
            joints = joints_coco_19
#           joints = joints_smpl_head_30 
#            joints = joints_mpi_inf_3dhp_28
        '''
        completeObjectProperties(obj)
        sf = obj["scaledidvisor"]
        tof=obj["tof"] 
        frw=obj["frw"] 
        zba=obj["ZBA"]

        pre = obj.name + '_'
        file = obj['inpath']+obj["infile"] 
        start_frame = obj["start_frame"]
        incr = obj["incr"]
        end_frame = obj["end_frame"] + incr
        print(file,start_frame,end_frame,incr)
        # read the joints from data 
        Name='{0:}{1:04d}.json'.format(file,start_frame)
        #When we have all here set a filter with label _XXXX to pick up only one skeleton/joint model 
        pat= ''
        #pat= '_smpl'
        #pat= '_coco'
        #pat= '__h36m'
        #pat= '_gpa'
        #pat= '_aspset'
        #pat= '_smplx'
        #pat= '_3doh'
        #pat= '_3dpeople'
        #pat= '_bmlmovi'
        #pat= '_mads'
        #pat= '_umpm'
        #pat= '_bmhad'
        #pat= '_totcap'
        #pat= '_jta'
        #pat= '_ikea'
        #pat= '_human4d'
        #pat= '_ghum'
        #pat= '_kinectv2'
        #pat= ''
        
        joints = readMetrabsJoints(Name,pat)
        print('joints from data')
        print(joints)

        makejoints(obj,joints,pre) 
        makeactions_3d_res = makeactions_3d(joints,pre)
        box = [0.0,0.0]
            
          
        ETA = _ETA(end_frame-start_frame)
        TheFilterCass = C_rawMeterasData()

        #read all frames from source
        for i in range (start_frame ,end_frame):
            Name='{0:}{1:04d}.json'.format(file,i)
            if zba > 0:
              TheFilterCass.addframe(Name,i-start_frame)
              #box=readmetrabs(Name,i - start_frame,box,pre,sf)
            else:
              TheFilterCass.addframe(Name,i)
              #box=readmetrabs(Name,i,box,pre,sf)
            progress =  (i-start_frame) * 100/(end_frame-start_frame)
            txt = "{0:06d}:{1:06d} {2:}".format(i,end_frame,progbar(progress,30)) 
            print(txt, end="\r") 

        print('First',TheFilterCass.firstframe,'Last',TheFilterCass.lastframe)
        TheFilterCass.extract_all()
        for ch in TheFilterCass.joints:
            jName = pre + ch
            obj = bpy.data.objects.get(jName)
            chdata = TheFilterCass.channels[ch]
            #apply filter here +++     
            #calculated filters
            avfilter = []
            fw = int (incr * frw / 100)      
            for i in range (0 ,fw+1):
                avfilter.append(1.0)

            
            
            if (incr > 0):
                if tof == 1:
                      print('->AverageFilter->Action',ch)
                      res = TheFilterCass.redavg(chdata,incr)
                elif tof == 2:
                      print("->MedianFilter(w={0:03d})->Action {1:} ".format(fw,ch) )
                      #print(txt)
                      res = TheFilterCass.redmedian(chdata,incr,fw)
                elif tof == 3:
                      print('->KernelFilter5->Action',ch)
                      filter = [1.0,2.0,6.0,2.0,1.0]
                      res = TheFilterCass.redfilter(chdata,filter,incr)
                elif tof == 4:
                      print("->AverageFilter(w={0:03d})->Action {1:} ".format(fw,ch) )
                      res = TheFilterCass.redfilter(chdata,avfilter,incr)
                else:
                      print('->KernelFilter3->Action',ch)
                      filter = [1.0,4.0,1.0]
                      res = TheFilterCass.redfilter(chdata,filter,incr)
            
                #apply filter here ----
                TheFilterCass.inject_action(obj,res,sf)
            else:
                print('->Raw->Action',ch)
                TheFilterCass.inject_action(obj,chdata,sf)
                


        if zba > 0:
            bpy.context.scene.frame_start = 0
            bpy.context.scene.frame_end = end_frame-start_frame
        else:
            bpy.context.scene.frame_start = start_frame
            bpy.context.scene.frame_end = end_frame


        print(txt)
        print('updated',makeactions_3d_res[0],'created',makeactions_3d_res[1],'of',makeactions_3d_res[2],'actions')
        print('importMetrabsJson----------------End' )
        return {'FINISHED'}        
    
    
    
class import_metrabs2D(bpy.types.Operator):
    bl_idname = "object.import_metrabs2d_operator"
    bl_label = "Import metrabs 2d data"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]
        except: 
            i = 0
        try:
            p=obj["inpath"]
            #print(p)
            if p != None:
                if os.path.exists(p):
                    i=1
                else: i =0
        except: 
            i = 0

        return i>0
    
    def execute (self,context):
        obj = context.active_object
        print('importMetrabsJson----------------Start' ) 
        try:
            res = obj['skeleton']
            joints = skel_list[res]
            print('Object defined joints')
        except:
            print('## Manual joints ## in ',__file__,'line:',inspect.currentframe().f_lineno)
            joints = joints_coco_19
#           joints = joints_smpl_head_30 
#            joints = joints_mpi_inf_3dhp_28
        print(joints)
        pre = obj.name + '_'
        makejoints(obj,joints,pre) 
        makeactions_3d_res = makeactions_3d(joints,pre)
        file = obj['inpath']+obj["infile"] 
        start_frame = obj["start_frame"]
        incr = obj["incr"]
        end_frame = obj["end_frame"] + incr
        print(file,start_frame,end_frame,incr)
        box = [0.0,0.0]
        try:
          sf = obj["scaledidvisor"]
        except:
          sf = 100
          obj["scaledidvisor"] = sf
        rx=bpy.data.scenes[0].render.resolution_x
        ry=bpy.data.scenes[0].render.resolution_y
        for i in range (start_frame ,end_frame,incr):
            Name='{0:}{1:04d}.json'.format(file,i)
            bpy.context.scene.frame_set(i)
            print(Name)
            box=readmetrabs2D(Name,i,box,pre,rx,ry,sf) 
            print(box)
        print('updated',makeactions_3d_res[0],'created',makeactions_3d_res[1],'of',makeactions_3d_res[2],'actions')
        print('importMetrabsJson----------------End' )
        return {'FINISHED'}        

    

class make_metrabs(bpy.types.Operator):
    bl_idname = "object.make_metrabs_operator"
    bl_label = "Make metrabs root"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]
        except: 
            i = 0
        return (i == 0)
    
    def execute (self,context):
        obj = context.active_object
        completeObjectProperties(obj)
        obj["metrabs"] = 1  
        obj["~armature"] = '*none*'  

        
        #
        #clear = lambda: os.system('clear')
        #clear()
#        print('MetrabsJson----------------Start' )     
#        joints = joints_coco_19
#        joints = joints_smpl_head_30
#        joints = joints_mpi_inf_3dhp_28 
#        print(joints)
#        makejoints(obj,joints) 
#        makeactions_3d(joints);
#        print('MetrabsJson----------------End' )
        return {'FINISHED'}        

def set_importpath(context, filepath, use_some_setting):
    print("Data in ",filepath)
    obj = context.active_object
    completeObjectProperties(obj)
    obj["inpath"] = os.path.dirname(filepath)+'/'
    try:
        f = open(filepath, 'r', encoding='utf-8')
        data = f.read()
        print(data)
        f.close()
    except:
        print('Failed to open',filepath)
        
    try:
        with open(filepath) as json_file:
            data = json.load(json_file)
            res = data['skeleton']
            obj['skeleton'] = res
            try:
                j = skel_list[res]
                print('skeleton:',res,'OK')
            except:
                print('***skeleton ? ****')
            res = data['start']
            obj['start_frame'] = res
            res = data['end']
            obj['end_frame'] = res
            print('automacik DONE')
    except:
        print('automacik failed')
    return {'FINISHED'}


class findMETRABData(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "operator.findmetabsdata"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Find Data"

    # ImportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob = StringProperty(
            default="*.json",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting = BoolProperty(
            name="Example Boolean",
            description="Example Tooltip",
            default=True,
            )

    type = EnumProperty(
            name="Example Enum",
            description="Choose between two items",
            items=(('OPT_A', "First Option", "Description one"),
                   ('OPT_B', "Second Option", "Description two")),
            default='OPT_A',
            )

    def execute(self, context):
        return set_importpath(context, self.filepath, self.use_setting)
    
    
class op_CreateArmature(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.create_armature"
    bl_label = "Create Armature"
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]
        except: 
            i = 0
        return (i > 0)

    def execute(self, context):
        print('op_CreateArmature--------Start' ) 
        obj = context.active_object
         
        try:
            rFrame = obj['start_frame']
        except:
            rFrame = 1
        aName = obj.name
        
        file = obj['inpath']+obj["infile"] 
        box = [0.0,0.0]
        path='{0:}{1:04d}.json'.format(file,rFrame)
        print(self.bl_idname,path)
        scalediv = obj["scaledidvisor"]
        arm_obj=readArmatureRestPos(path,aName,scalediv)
        arm_obj['skeleton'] = obj['skeleton']
        arm_obj["metrabs"] = 2
        try:
          arm_obj["~armature"] = obj["~armature"]
        except:
          arm_obj["~armature"] = "*none*"   
        obj["~armature"] = arm_obj.name
        print('op_CreateArmaturet-----------End' ) 
        return {'FINISHED'}



class MetrabsPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Metrabs"
    bl_idname = "OBJECT_PT_METRABS"
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
        return (i in [0,1])


    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]                            
        except: 
            i = 0
        if(i ==0): 
            row = layout.row()
            row.operator("object.make_metrabs_operator")
        else:
            row = layout.row()
            row.operator("operator.findmetabsdata")
            row.operator("object.read_metrabs_info")
            row.operator("object.import_metrabs_operator")
            row = layout.row()
            row.prop(obj, '["%s"]' % ("start_frame"),text="start")  
            row.prop(obj, '["%s"]' % ("end_frame"),text="end")  
            row.prop(obj, '["%s"]' % ("incr"),text="step")  
            row = layout.row()
            row.prop(obj, '["%s"]' % ("scaledidvisor"),text="ScaleDiv")  
            row.prop(obj, '["%s"]' % ("tof"),text="filter")  
            row.prop(obj, '["%s"]' % ("frw"),text="frw")  
            #row.operator("object.delete_joints_action")
            #row.operator("object.push_down_joints_action")
            if len(obj.children): 
              row = layout.row()
              row.operator(delete_childen.bl_idname)
              row.operator(delete_childen_actions.bl_idname)
              row = layout.row()
              row.operator(op_CreateArmature.bl_idname)
            row = layout.row()
            row.prop(obj, '["%s"]' % ("inpath"),text="path")  


"""   
        row = layout.row()
        row.operator("object.pushtweak_operator")
"""    




def register():
    bpy.utils.register_class(make_metrabs)
    bpy.utils.register_class(read_metrabs_info)
    bpy.utils.register_class(import_metrabs)
    bpy.utils.register_class(import_metrabs2D)
    bpy.utils.register_class(MetrabsPanel)
    bpy.utils.register_class(findMETRABData)
    #bpy.utils.register_class(push_down_joints_action)
    bpy.utils.register_class(delete_childen_actions)
    bpy.utils.register_class(delete_childen)
    bpy.utils.register_class(op_CreateArmature)
    print('Import Mertabs register DONE')


def unregister():
    bpy.utils.unregister_class(make_metrabs)
    bpy.utils.unregister_class(read_metrabs_info)
    bpy.utils.unregister_class(import_metrabs)
    bpy.utils.unregister_class(import_metrabs2D)
    bpy.utils.unregister_class(MetrabsPanel)
    bpy.utils.unregister_class(findMETRABData)
    #bpy.utils.unregister_class(push_down_joints_action)
    bpy.utils.register_class(delete_childen_actions)
    bpy.utils.register_class(delete_childen)
    bpy.utils.unregister_class(op_CreateArmature)
    
def main():
    register()

if __name__ == "__main__":
    #createArmature()
    register() 
else:
    register() 
    
    
