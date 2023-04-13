import bpy
import json
import os


clearout = 1
scale = 100

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
        "reye_sailvos",
        "rhip_h36m",
    ]



skel_list ={
    "smpl+head_30":joints_smpl_head_30,
    "mpi_inf_3dhp_28":joints_mpi_inf_3dhp_28,
    "coco_19":joints_coco_19,
    "":joints_picked,
    "all":joints_all
    }



    
'''    
joints_h36m_17 =['pelv' 'rhip' 'rkne' 'rank' 'lhip' 'lkne' 'lank' 'spin' 'neck' 'head'
 'htop' 'lsho' 'lelb' 'lwri' 'rsho' 'relb' 'rwri']
 
joints_h36m_25 =
 ['rhip' 'rkne' 'rank' 'rfoo' 'rtoe' 'lhip' 'lkne' 'lank' 'lfoo' 'ltoe'
 'spin' 'neck' 'head' 'htop' 'lsho' 'lelb' 'lwri' 'lthu' 'lfin' 'rsho'
 'relb' 'rwri' 'rthu' 'rfin']
 
joints_mpi_inf_3dhp_17 = ['htop' 'neck' 'rsho' 'relb' 'rwri' 'lsho' 'lelb' 'lwri' 'rhip' 'rkne'
 'rank' 'lhip' 'lkne' 'lank' 'pelv' 'spin' 'head']    
'''    


#body_25
#bones = ['Nose','Neck','RShoulder','RElbow','RWrist','LShoulder','LElbow','LWrist','MidHip','RHip','RKnee','RAnkle','LHip','LKnee','LAnkle','REye','LEye','REar','LEar']

#COCO
#bones = ['Nose','Neck','RShoulder','RElbow','RWrist','LShoulder','LElbow','LWrist','RHip','RKnee','RAnkle','LHip','LKnee','LAnkle','REye','LEye','REar','LEar']

#bones =['pelv_smpl', 'lhip_smpl', 'rhip_smpl', 'bell_smpl', 'lkne_smpl', 'rkne_smpl', 'spin_smpl', 'lank_smpl', 'rank_smpl', 'thor_smpl', 'ltoe_smpl', 'rtoe_smpl',
#    'neck_smpl', 'lcla_smpl', 'rcla_smpl', 'head_smpl', 'lsho_smpl', 'rsho_smpl','lelb_smpl', 'relb_smpl', 'lwri_smpl', 'rwri_smpl' ,'lhan_smpl' ,'rhan_smpl', 'htop_mpi_inf_3dhp' ,'learcoco' ,'leyecoco', 'nosecoco' ,'rearcoco','reyecoco']

#bones =['pelv_smpl', 'lhip_smpl', 'rhip_smpl', 'lkne_smpl', 'rkne_smpl', 'spin_smpl', 'lank_smpl', 'rank_smpl', 'thor_smpl', 'ltoe_smpl', 'rtoe_smpl']








def createEmpty(OName,draw_size,draw_type):
    #print('Create {:}'.format(OName))
    Cobj = bpy.data.objects.new( OName, None )
    ver = bpy.app.version[1]
    #print(ver)
    if (ver < 80):
        bpy.context.scene.objects.link( Cobj )
        Cobj.empty_draw_size = draw_size
        Cobj.empty_draw_type = draw_type
        Cobj.show_name=1
    
    if (ver > 79):
        bpy.context.scene.collection.objects.link( Cobj )
        Cobj.empty_display_size = draw_size
        Cobj.empty_display_type = draw_type
        Cobj.show_name=1

    return Cobj   

'''
#deprecated remove me
def makeempties(parent):
    for bone in bones:
        obj = bpy.data.objects.get(bone)
        if ( not obj):
            obj = createEmpty(bone,0.5,'ARROWS')
            obj.parent = parent
'''

def makejoints(parent,joints,pre):
    for joint in joints:
        objname = pre + joint
        obj = bpy.data.objects.get(objname)
        if ( not obj):
            obj = createEmpty(objname,0.5,'ARROWS')
            obj.parent = parent
    
def readmetrabs(name,frame,box,jPre):
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
                pname='pose3d{0:d}'.format(nb+1)
                print(pname)        
    
    p1 = data[pname]
    if (not p1): return res_box
    missmatch = 0
    for joint in p1:
        jName = jPre + joint[0]
        #print(jName)
        obj = bpy.data.objects.get(jName)
        if (obj):
            lx = joint[1] / scale
            ly = joint[2] / scale
            lz = joint[3] / scale
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
    for joint in joints:
        obj = bpy.data.objects.get(pre+joint)
        #print('Action3d for', obj)
        if (obj) :
            obj.animation_data_create()
            obj.animation_data.action = bpy.data.actions.new(name=joint+'Action')
            fcu_x = obj.animation_data.action.fcurves.new(data_path="location", index=0)
            fcu_y = obj.animation_data.action.fcurves.new(data_path="location", index=1)
            fcu_z = obj.animation_data.action.fcurves.new(data_path="location", index=2)

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
        name = obj['inpath']+"/jobinfo.json"
        print(name)
        with open(name) as json_file:
            data = json.load(json_file)
            print(data)
            res = data['skeleton']
            obj['skeleton'] = res
            j = skel_list[res]
            print(j)
            res = data['start']
            obj['start_frame'] = res
            res = data['end']
            obj['end_frame'] = res

        return {'FINISHED'}



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
        if (clearout == 1) :
            clear = lambda: os.system('clear')
            clear()
        print('importMetrabsJson----------------Start' ) 
        try:
            res = obj['skeleton']
            joints = skel_list[res]
            print('Object defined joints')
        except:
            joints = joints_coco_19
#           joints = joints_smpl_head_30 
#            joints = joints_mpi_inf_3dhp_28
            print('Manual joints')
        print(joints)
        pre = obj.name + '_'
        makejoints(obj,joints,pre) 
        makeactions_3d(joints,pre)
        file = obj['inpath']+obj["infile"] 
        start_frame = obj["start_frame"]
        incr = obj["incr"]
        end_frame = obj["end_frame"] + incr
        print(file,start_frame,end_frame,incr)
        box = [0.0,0.0]
        for i in range (start_frame ,end_frame,incr):
            Name='{0:}{1:04d}.json'.format(file,i)
            bpy.context.scene.frame_set(i)
            print(Name)
            box=readmetrabs(Name,i,box,pre) 
            print(box)
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
        obj["metrabs"] = 1  
        
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




class MetrabsPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Metrabs"
    bl_idname = "OBJECT_PT_METRABS"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

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
            row.prop(obj, '["%s"]' % ("inpath"),text="path")  
            row = layout.row()
            row.prop(obj, '["%s"]' % ("start_frame"),text="start")  
            row = layout.row()
            row.prop(obj, '["%s"]' % ("end_frame"),text="end")  
            row = layout.row()
            row.prop(obj, '["%s"]' % ("incr"),text="step")  
            #row = layout.row()
            #row.prop(obj, '["%s"]' % ("jobinfo"),text="jobinfo")  
            row = layout.row()
            row.operator("object.import_metrabs_operator")
            row.operator("object.read_metrabs_info")


"""   
        row = layout.row()
        row.operator("object.pushtweak_operator")
"""    




def register():
    bpy.utils.register_class(make_metrabs)
    bpy.utils.register_class(read_metrabs_info)
    bpy.utils.register_class(import_metrabs)
    bpy.utils.register_class(MetrabsPanel)
    print('Import Mertabs register DONE')


def unregister():
    bpy.utils.unregister_class(make_metrabs)
    bpy.utils.unregister_class(read_metrabs_info)
    bpy.utils.unregister_class(import_metrabs)
    bpy.utils.unregister_class(MetrabsPanel)

#run from run
if __name__ == "__main__":
    #runit(bpy.context,1)    
    register() 
    
#run with register flag
else: register() 
