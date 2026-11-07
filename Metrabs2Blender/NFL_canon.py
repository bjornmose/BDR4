import bpy

import numpy as np
import mathutils
import math
import os
import sys
'''
author: bjornmose
date: 7/nov/2026
copyright: MIT
purpose: visualize the 3D canonical locations NFL 
(https://github.com/isarandi/nlf) was trained to
read the lincece !!!

future: easy tool to define a custom target set eg. hip_left/right .. 
may be use kabsch for traslation rotation for subsets
'''

version = 0


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

def main():
    cs_canoroot = 'Cano_Root'
    _CR = bpy.data.objects.get(cs_canoroot)
    if ( not _CR):
        _CR = createEmpty(cs_canoroot,1.0,'SPHERE')

    cano_verts = np.load(f'{home_data}/canonical_verts/smpl.npy')
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


if __name__ == "__main__":
    main() 
else:
    main() 

