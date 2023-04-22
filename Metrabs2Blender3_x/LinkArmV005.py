import bpy
import math
from math import sin, cos, radians
import mathutils
import bmesh
import numpy as np

'''
#look up info
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
'''    
#joint/target map used for buiding constraints in armature    
joma_simpl = {
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
        "leye" : "leyecoco",
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
    
    
joma_list ={
    "smpl+head_30":joma_simpl,
    "":joma_picked,
    }
    
    
    
    
'''    
joints_h36m_17 =['pelv' 'rhip' 'rkne' 'rank' 'lhip' 'lkne' 'lank' 'spin' 'neck' 'head'
 'htop' 'lsho' 'lelb' 'lwri' 'rsho' 'relb' 'rwri']
 
joints_h36m_25 =
 ['rhip' 'rkne' 'rank' 'rfoo' 'rtoe' 'lhip' 'lkne' 'lank' 'lfoo' 'ltoe'
 'spin' 'neck' 'head' 'htop' 'lsho' 'lelb' 'lwri' 'lthu' 'lfin' 'rsho'
 'relb' 'rwri' 'rthu' 'rfin']

joints_mpi_inf_3dhp_28 = ['thor' 'spi4' 'spi2' 'spin' 'pelv' 'neck' 'head' 'htop' 'lcla' 'lsho'
 'lelb' 'lwri' 'lhan' 'rcla' 'rsho' 'relb' 'rwri' 'rhan' 'lhip' 'lkne'
 'lank' 'lfoo' 'ltoe' 'rhip' 'rkne' 'rank' 'rfoo' 'rtoe']
 
joints_mpi_inf_3dhp_17 = ['htop' 'neck' 'rsho' 'relb' 'rwri' 'lsho' 'lelb' 'lwri' 'rhip' 'rkne'
 'rank' 'lhip' 'lkne' 'lank' 'pelv' 'spin' 'head']    
'''



def createEmpty(OName,draw_size,draw_type):
    #print('Create {:}'.format(OName))
    Cobj = bpy.data.objects.new( OName, None )
    ver = bpy.app.version[1]
    ver0 = bpy.app.version[0]
    #print(ver)
    if (ver < 80 and ver0 < 3):
        bpy.context.scene.objects.link( Cobj )
        Cobj.empty_draw_size = draw_size
        Cobj.empty_draw_type = draw_type
        Cobj.show_name=1
    
    if (ver > 79 and ver0 < 3):
        bpy.context.scene.collection.objects.link( Cobj )
        Cobj.empty_display_size = draw_size
        Cobj.empty_display_type = draw_type
        Cobj.show_name=1

    if (ver < 99 and ver0 > 2):
        view_layer = bpy.context.view_layer
        view_layer.active_layer_collection.collection.objects.link( Cobj )
        Cobj.empty_display_size = draw_size
        Cobj.empty_display_type = draw_type
        Cobj.show_name=1

    return Cobj   

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


   

def makehiprot(parent,joma):
    
    pre = parent.name
    ID =pre+"_HipRot"
    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        objcoloc(obj,'COCO_HipRot_lhip',pre+'_'+joma['lhip'],1.0)
        objcoloc(obj,'COCO_HipRot_rhip',pre+'_'+joma['rhip'],0.5)
        obj.parent=parent

        cname = 'COCO_HipRot_track'
        co = obj.constraints.get(cname)
        if co is None:
            co = obj.constraints.new('TRACK_TO')
            ID =pre+'_'+joma['lhip']
            tar = bpy.data.objects.get(ID)
            if tar is None:
                obj.constraints.remove(co)
                return  
            co.target = tar
            co.track_axis="TRACK_X"
            co.up_axis="UP_Y"
            co.name = cname

def maketorso(parent,joma):

    pre = parent.name
    ID =pre+"_Torso"
    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
    if (obj):
        objcoloc(obj,'COCO_Torso_HipRot',pre+'_HipRot',1.0)
        objcoloc(obj,'COCO_Torso_ChestRot',pre+'_ChestRot',0.5)

    ID =pre+"_rTorso"
    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
    if (obj):
        objcoloc(obj,'COCO_rTorso_rsho',pre+'_'+joma['rsho'],1.0)
        objcoloc(obj,'COCO_rTorso_rhip',pre+'_'+joma['rhip'],0.5)

    ID =pre+"_lTorso"
    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
    if (obj):
        objcoloc(obj,'COCO_lTorso_rsho',pre+'_'+joma['lsho'],1.0)
        objcoloc(obj,'COCO_lTorso_rhip',pre+'_'+joma['lhip'],0.5)


    ID =pre+"_Torso"
    obj = bpy.data.objects.get(ID)
    if (obj):
        cname = 'COCO_Torso_trackl'
        co = obj.constraints.get(cname)
        if co is None:
            co = obj.constraints.new('TRACK_TO')
            ID =pre+"_lTorso"
            tar = bpy.data.objects.get(ID)
            if tar is None:
                obj.constraints.remove(co)
                return  
            co.target = tar
            co.track_axis="TRACK_X"
            co.up_axis="UP_Z"
            co.name = cname

    ID =pre+"_Torso"
    obj = bpy.data.objects.get(ID)
    if (obj):
        cname = 'COCO_Torso_trackr'
        co = obj.constraints.get(cname)
        if co is None:
            co = obj.constraints.new('TRACK_TO')
            ID =pre+"_rTorso"
            tar = bpy.data.objects.get(ID)
            if tar is None:
                obj.constraints.remove(co)
                return  
            co.target = tar
            co.track_axis="TRACK_NEGATIVE_X"
            co.up_axis="UP_Z"
            co.name = cname
            co.influence = 0.5
                 
def makechestrot(parent,joma):

    pre = parent.name
    ID =pre+"_ChestRot"
    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
    if (obj):
        objcoloc(obj,'COCO_chestrot_lsho',pre+'_'+joma['lsho'],1.0)
        objcoloc(obj,'COCO_chestrot_rsho',pre+'_'+joma['rsho'],0.5)
        
        cname = 'COCO_ChestTrack'
        co = obj.constraints.get(cname)
        if co is None:
            co = obj.constraints.new('TRACK_TO')
            ID =pre+'_'+joma['lsho']
            tar = bpy.data.objects.get(ID)
            if tar is None:
                obj.constraints.remove(co)
                return  
            co.target = tar
            co.track_axis="TRACK_X"
            co.up_axis="UP_Y"
            co.name = cname
                 
def makeheadrot(parent,joma):

    pre = parent.name
    ID =pre+"_HeadRot"
    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
    if (obj):
        objcoloc(obj,'COCO_HeadRot_lear',pre+'_'+joma['lear'],1.0)
        objcoloc(obj,'COCO_HeadRot_rear',pre+'_'+joma['rear'],0.5)

        cname = 'COCO_HeadTrack'
        co = obj.constraints.get(cname)
        if co is None:
            co = obj.constraints.new('TRACK_TO')
            ID =pre+'_'+joma['nose']
            tar = bpy.data.objects.get(ID)
            if tar is None:
                obj.constraints.remove(co)
                return  
            co.target = tar
            co.track_axis="TRACK_Z"
            co.up_axis="UP_Y"
            co.name = cname

def makefeetrot(parent,joma):

    pre = parent.name
    ID =pre+"_FeetRot"
    obj = bpy.data.objects.get(ID)
    if (not obj):
        obj =createEmpty(ID,0.5,'ARROWS')
        obj.parent=parent
    if (obj):
        
        objcoloc(obj,'COCO_FeetRot_lfoot',pre+'_'+joma['lfoo'],1.0)
        objcoloc(obj,'COCO_FeetRot_rfoot',pre+'_'+joma['rfoo'],0.5)

        cname = 'COCO_FeetTrack'
        co = obj.constraints.get(cname)
        if co is None:
            co = obj.constraints.new('TRACK_TO')
            ID =pre+'_'+joma['lfoo']
            tar = bpy.data.objects.get(ID)
            if tar is None:
                obj.constraints.remove(co)
                return  
            co.target = tar
            co.track_axis="TRACK_Z"
            co.up_axis="UP_Y"
            co.name = cname

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
	


class LinkArmature(bpy.types.Operator):
    """LinkArmatureToSimpl"""
    bl_idname = "object.linkarmature_operator"
    bl_label = "Link to Armature "

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        i = 0
        try:
            i=obj["metrabs"]
        except: 
            i = 0
        return i>0
    
    def cocoloc(self,bone,cname,IDtarget,pxname):
        crc = bone.constraints.get(pxname+cname)
        if crc is None:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                return('FAILED')
            crc = bone.constraints.new('COPY_LOCATION')
            crc.target = target
            crc.name = pxname+cname
        else:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                bone.constraints.remove(crc)
                return('FAILED')
            crc.target = target
            print(bone.name,IDtarget, 'loc_update')
            return('FINISHED')

    def cocorot(self,bone,cname,IDtarget,pxname):
        crc = bone.constraints.get(pxname+cname)
        if crc is None:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                return('FAILED')
            crc = bone.constraints.new('COPY_ROTATION')
            crc.target = target
            crc.name = pxname+cname
        else:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                bone.constraints.remove(crc)
                return('FAILED')
            crc.target = target
            print(bone.name,IDtarget, 'rot_update')
            return('FINISHED')


    def cocoik(self,bone,cname,IDtarget,len,pxname):
        crc = bone.constraints.get(pxname+cname)
        if crc is None:
            target = bpy.data.objects.get(IDtarget)
            if target is None:
                print('MISSING TARGET:',IDtarget)
                return('FAILED')
            crc = bone.constraints.new('IK')
            crc.target = target
            crc.chain_count = len
            crc.name = pxname+cname
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
            
            n_probe = pre+'_'+joma['rwri']
            o_probe = bpy.data.objects.get(n_probe)
            if o_probe is not None:
                makehiprot(obj,joma)
                makechestrot(obj,joma)
                maketorso(obj,joma)
                makeheadrot(obj,joma)
                makefeetrot(obj,joma)
#            pre = obj.name

            bone = self.findbone(arm,"hand.ik.R")
            if bone is not None:
                cname = pre+'_'+joma['rwri']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP)
                cname = pre+'_'+joma['rhan']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoik(bone,cname,IDtarget,1,nameP)

                    
            bone = self.findbone(arm,"hand.ik.L")
            if bone is not None:
                cname = pre+'_'+joma['lwri']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP)
                cname = pre+'_'+joma['lhan']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoik(bone,cname,IDtarget,1,nameP)

            bone = self.findbone(arm,"foot.ik.L")
            if bone is not None:
                cname = pre+'_'+joma['lank']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP)
                cname = pre+'_'+joma['ltoe']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoik(bone,cname,IDtarget,1,nameP)

            bone = self.findbone(arm,"foot.ik.R")
            if bone is not None:
                cname = pre+'_'+joma['rank']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,cname,IDtarget,nameP)
                cname = pre+'_'+joma['rtoe']
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoik(bone,cname,IDtarget,1,nameP)


            bone = self.findbone(arm,"torso")
            if bone is not None:
                cname = pre+'_Torso'
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,'L_'+cname,IDtarget,nameP)
                self.cocorot(bone,'R_'+cname,IDtarget,nameP)
                

            bone = self.findbone(arm,"hips")
            if bone is not None:
                cname =pre+"_HipRot"
                IDtarget ='{:}{:}'.format(nameP,cname)
                target = bpy.data.objects.get(IDtarget)
                self.cocorot(bone,cname,IDtarget,nameP)

                    
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
            
            bone = self.findbone(arm,"chest")
            if bone is not None:
                cname = pre+'_ChestRot'
                IDtarget ='{:}{:}'.format(nameP,cname)
                target = bpy.data.objects.get(IDtarget)
                self.cocoik(bone,cname,IDtarget,1,nameP)

            bone = self.findbone(arm,"root")
            if bone is not None:
                cname = pre+'_FeetRot'
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocoloc(bone,'L'+cname,IDtarget,nameP)
                crc = bone.constraints.get('L'+cname)
                if crc is not None:
                    crc.use_z = 0

                cname = pre+'_Torso'
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocorot(bone,'R'+cname,IDtarget,nameP)
                crc = bone.constraints.get('R'+cname)
                if crc is not None:
                    crc.use_x = 0
                    crc.use_y = 0
                    crc.use_z = 1

            bone = self.findbone(arm,"headproxy")
            if bone is not None:
                cname = pre+'_HeadRot'
                IDtarget ='{:}{:}'.format(nameP,cname)
                self.cocorot(bone,cname,IDtarget,nameP)


            '''

            bone = self.findbone(arm,"chest")
            if bone is not None:
                IDtarget ='{:}{:}'.format(nameP,"_ChestRot")
                target = bpy.data.objects.get(IDtarget)
                if target is not None:
                    cname = '_ChestRot2'
                    crc = bone.constraints.get(nameP+cname)
                    if crc is None:
                        crc = bone.constraints.new('COPY_ROTATION')
                        crc.target = target
                        crc.name = nameP+cname
            '''
        print('LinkArmature.execute done')
        return {'FINISHED'}


class LinkArmPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "LinkArmaturePanel"
    bl_idname = "OBJECT_PT_LACOCO"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

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
            row.operator("object.linkarmature_operator")


"""   
        row = layout.row()
        row.operator("object.pushtweak_operator")
"""    




def register():
    bpy.utils.register_class(LinkArmature)
    bpy.utils.register_class(LinkArmPanel)


def unregister():
    bpy.utils.unregister_class(LinkArmature)
    bpy.utils.unregister_class(LinkArmPanel)
    del theGen

#run from run
if __name__ == "__main__":
    #runit(bpy.context,1)    
    register()
#    makefeetrot() 
    
#run with register flag
else: register() 
print('LinkArmVxx DONE')
