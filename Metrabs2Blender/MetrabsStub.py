import sys
import os
import bpy

'''
to avoid multiple diverging copies inside blend files rather import modules
also for using external editors
'''

'''
for reasons a script in Blender does not see the local path of the blend
make it visible
'''

blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

import ImportMetrabsjsonB27_B3_3
import ArmatureBasic
import CloneMotionPanel
import LinkArmSimpl

'''
the cache may hold older copies
HINT run this script manually to find errors on you new edit
'''
import importlib
importlib.reload(ImportMetrabsjsonB27_B3_3)
importlib.reload(ArmatureBasic)
importlib.reload(CloneMotionPanel)
importlib.reload(LinkArmSimpl)

