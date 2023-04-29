import bpy
import json
import os

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator



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
        "reye_cmu_panoptic",
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


def obj_check_intCP(object,CP):
    i = 0
    try:
        cp=obj['CP']
        i = 1
    except: 
        i = 0
    return i



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
            if obj.animation_data is None:
                obj.animation_data_create()
                obj.animation_data.action = bpy.data.actions.new(name=pre+joint+'Action3D')
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


class push_down_joints_action(bpy.types.Operator):
    bl_idname = "object.push_down_joints_action"
    bl_label = "push_down_joints_action"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        #i = obj_check_intCP(object,"metrabs")
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
            return {'Aborted'}        
            
        for joint in joints:
            obj = bpy.data.objects.get(pre+joint)
            #print('Action3d for', obj)
            if (obj) :
                if obj.animation_data is not None:
                    action = obj.animation_data.action
                    if action is not None:
                        track = obj.animation_data.nla_tracks.new()
                        track.strips.new(action.name, action.frame_range[0], action)
                        obj.animation_data.action = None
              
        
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

def set_importpath(context, filepath, use_some_setting):
    print("Data in ",filepath)
    f = open(filepath, 'r', encoding='utf-8')
    data = f.read()
    f.close()

    # would normally load the data here
    print(data)
    obj = context.active_object
    #obj["inpath"] = filepath
    obj["inpath"] = os.path.dirname(filepath)+'/'


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
            row.operator("operator.findmetabsdata")
            row.operator("object.push_down_joints_action")
            row = layout.row()
            row.prop(obj, '["%s"]' % ("start_frame"),text="start")  
            row = layout.row()
            row.prop(obj, '["%s"]' % ("end_frame"),text="end")  
            row = layout.row()
            row.prop(obj, '["%s"]' % ("incr"),text="step")  
            row = layout.row()
            row.operator("object.import_metrabs_operator")
            row.operator("object.read_metrabs_info")
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
    bpy.utils.register_class(MetrabsPanel)
    bpy.utils.register_class(findMETRABData)
    bpy.utils.register_class(push_down_joints_action)
    print('Import Mertabs register DONE')


def unregister():
    bpy.utils.unregister_class(make_metrabs)
    bpy.utils.unregister_class(read_metrabs_info)
    bpy.utils.unregister_class(import_metrabs)
    bpy.utils.unregister_class(MetrabsPanel)
    bpy.utils.unregister_class(findMETRABData)
    bpy.utils.unregister_class(push_down_joints_action)

if __name__ == "__main__":
    register() 
    
