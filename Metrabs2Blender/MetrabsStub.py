import sys
import os
import bpy

blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

import ImportMetrabsjsonB27_B3Test2D
import ArmatureBasic
import CloneMotionPanel
import LinkArmV004work


import importlib
importlib.reload(ImportMetrabsjsonB27_B3Test2D)
importlib.reload(ArmatureBasic)
importlib.reload(CloneMotionPanel)
importlib.reload(LinkArmV004work)
#ImportMetrabsjsonB27_B3Test2D.main() 

