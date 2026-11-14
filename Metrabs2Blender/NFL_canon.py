import bpy

import numpy as np
import mathutils
import math
import os
import sys
'''
author: bjornmose
date: 8/nov/2026
copyright: MIT
purpose: visualize the 3D canonical locations NFL 
(https://github.com/isarandi/nlf) was trained to
read the lincece !!!

as far as i dived into it:
    NLF gets a bunch of input 3d vectors
    mangles trough field build up by the input image
    and spits out the resulting 3d vectors 
    dirac speaking it looks like this
    vector_out = |NLF_Operator|image_in><vector_in|
    

past: 8/nov/20226
    added a list of markers
    a bunch of named empties to be dragged in place
    read / write markers to files
    all i need for now :)
    
future: easy tool to define a custom target set eg. hip_left/right .. 

todo : 
    handle pirvate collections
    adjustabel path for input/output on UI   

may be use kabsch for traslation rotation for subsets
'''

version = 1


dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    print(sys.path)

import BVT

# this next part forces a reload in case you edit the source after you first start the blender session
import importlib
importlib.reload(BVT)

from BVT import *



#define path to models based on home
home_directory = os.path.expanduser( '~' )

home_data = home_directory+'/sambashare/nlf_data_files/'

scale = 1.

markers = [
    'HeadTop',
    'HeadBase',
    'Nose',
    'Ear_R',
    'Ear_L',
    'Neck',
    'Clav_R',
    'Clav_L',
    'Sho_R',
    'Sho_L',
    'Nip_R',
    'Nip_L',
    'Chest_R',
    'Chest_L',
    'Chest_B',
    'Chest_F',
    'Hip_R',
    'Hip_L',
    'Hip_B',
    'Hip_F',
    'Hip_C',
    'Belly_R',
    'Belly_L',
    'Belly_B',
    'Belly_F',
    'Ellb_R',
    'Ellb_L',
    'EllbT_R',
    'EllbT_L',
    'Wrist_R',
    'Wrist_L',
    'WristT_R',
    'WristT_L',
    'Palm_R',
    'Palm_L',
    'Knee_R',
    'Knee_L',
    'KneeT_R',
    'KneeT_L',
    'Ank_R',
    'Ank_L',
    'Toe_R',
    'Toe_L',
    'Thigh_RO',
    'Thigh_RF',
    'Thigh_RI',
    'Thigh_RB',
    'Thigh_LO',
    'Thigh_LF',
    'Thigh_LI',
    'Thigh_LB',
    
    
    'Root'
    ]


def makeCano():
    cs_canoroot = 'Cano_Root'
    _CR = bpy.data.objects.get(cs_canoroot)
    if ( not _CR):
        _CR = createEmpty(cs_canoroot,1.0,'CUBE')

    cano_verts = np.load(f'{home_data}/canonical_verts/smpl.npy')
#    cano_verts = makeFplane(50)
    print(cano_verts)
    n = 0
    for vert in cano_verts:
        objname = 'ca{0:}'.format(n)
        obj = bpy.data.objects.get(objname)
        if ( not obj):
            obj = createEmpty(objname,0.005,'SPHERE')
            obj.parent = _CR
            obj.show_name = False
        obj.location[0] = vert[0]*scale
        obj.location[1] = vert[1]*scale
        obj.location[2] = vert[2]*scale
        n = n+1

        #print(vert)
        
def makeFplane(nv):
    res = []
    for nx in range(nv):
        for ny in range(nv):
            res.append([2*nx/nv-1.,2*ny/nv-1.,0])
    return res

def makeMarkers():
    cs_markersroot = 'Markers'
    _CR = bpy.data.objects.get(cs_markersroot)
    if ( not _CR):
        _CR = createEmpty(cs_markersroot,1.0,'CUBE')

    for vert in markers:
        objname = vert
        obj = bpy.data.objects.get(objname)
        if ( not obj):
            obj = createEmpty(objname,0.01,'SPHERE')
            obj.parent = _CR
            obj.show_name = True
            
def dumpMarkers():
    out = []
    l = len(markers)
    opath_m = f'{home_data}/canonical_verts/Markers{l}.npy'
    opath_mn = f'{home_data}/canonical_verts/MarkerNames{l}.npy'
    for vert in markers:
        obj = bpy.data.objects.get(vert)
        if (obj):
            out.append([obj.location[0],obj.location[1],obj.location[2]])
    np.save(opath_m, out, allow_pickle=True)
    np.save(opath_mn, markers, allow_pickle=True)
    print(out)
            
def readMarkers(inpath_m ):
    locs = np.load(inpath_m)
    for rmark,vert in zip(locs,markers):
        obj = bpy.data.objects.get(vert)
        if (obj):
            obj.location[0] = rmark[0]
            obj.location[1] = rmark[1]
            obj.location[2] = rmark[2]
            
            
class op_makecano(bpy.types.Operator):
    bl_idname = "object.make_cano_operator"
    bl_label = "Make cano"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (True)
    
    def execute (self,context):
        obj = context.active_object
        makeCano() 
        return {'FINISHED'}        

class op_makemarkers(bpy.types.Operator):
    bl_idname = "object.makemarkers_operator"
    bl_label = "Make Markers"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (True)
    
    def execute (self,context):
        obj = context.active_object
        makeMarkers() 
        return {'FINISHED'}        

class op_dumpmarkers(bpy.types.Operator):
    bl_idname = "object.dumpmarkers_operator"
    bl_label = "Write Markers"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (True)
    
    def execute (self,context):
        obj = context.active_object
        dumpMarkers() 
        return {'FINISHED'}        

class op_readmarkers(bpy.types.Operator):
    bl_idname = "object.readmarkers_operator"
    bl_label = "Read Markers"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (True)
    
    def execute (self,context):
        obj = context.active_object
        file = f'{home_data}/canonical_verts/Markers.npy'
        readMarkers(file) 
        return {'FINISHED'}        
            
            
            
            
            
class NLFCanonPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "NLF_Panel"
    bl_idname = "OBJECT_PT_METRABS"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (True)


    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        row = layout.row()
        row.operator("object.dumpmarkers_operator")
        row.operator("object.readmarkers_operator")

        row = layout.row()
        row.operator("object.make_cano_operator")
        row.operator("object.makemarkers_operator")

            #row.prop(obj, '["%s"]' % ("tof"),text="filter")  
            #row.prop(obj, '["%s"]' % ("inpath"),text="path")
            #row = layout.row()
            #row.prop(obj, '["%s"]' % ("domirr"),text="mirror")

            
            
            
def register():
    bpy.utils.register_class(NLFCanonPanel)
    bpy.utils.register_class(op_makecano)
    bpy.utils.register_class(op_makemarkers)
    bpy.utils.register_class(op_dumpmarkers)
    bpy.utils.register_class(op_readmarkers)


def unregister():
    bpy.utils.unregister_class(NLFCanonPanel)
    bpy.utils.unregister_class(op_makecano)
    bpy.utils.unregister_class(op_makemarkers)
    bpy.utils.unregister_class(op_dumpmarkers)
    bpy.utils.unregister_class(op_readmarkers)
    

    


if __name__ == "__main__":
    register() 
    #makemarkers()
    #MakeCano() 
else:
    register() 

    #main() 

