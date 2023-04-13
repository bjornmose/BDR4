# BDR4
There are two folders

## 1. bmmetrabs: Calling METRABS for a sequence of images
### 1.1 have a python shell with tensorflow installed
'''
jenscave@jenscave-i5:~/Documents/BDR_Root/BDR4/bmmetrabs$ eval "$("$HOME/miniconda3/bin/conda" shell.bash hook)" 
(base) jenscave@jenscave-i5:~/Documents/BDR_Root/BDR4/bmmetrabs$ conda activate tf-py38
'''

### 1.2 Edit the file Job_ioV001.py to your needs

1.3 run it
'''
(tf-py38) jenscave@jenscave-i5:~/Documents/BDR_Root/BDR4/bmmetrabs$ ./Job_ioV001.py 
class __init__ Jobfile e2fjobdefaultMQFOV30.json
found job is {'version': 3, 'max_detections': 1, 'fov_degrees': 30, 'skeleton': '', 'start': 1, 'end': 10, 'skip': 1, 'viz': 1, 'qual': 10, 'cpu_count': 3, 'create_json': 1, 'inpattern': 'input/default/Image{0:04d}.png', 'outpath': 'output/resdefaultMQFOV30', 'outputpatternjson': '/Posedata{0:04d}.json', 'outputpatternviz': '/viz/Image{0:04d}.png', 'outputpatternviz1': '/viz1/Image{0:04d}.png', 'outputpatternviz2': '/viz2/Image{0:04d}.png'}
Replace? [y/n] y
Replaced-> e2fjobdefaultMQFOV30.json
New job is {'version': 3, 'max_detections': 1, 'fov_degrees': 30, 'skeleton': '', 'start': 1, 'end': 10, 'skip': 1, 'viz': 1, 'qual': 10, 'cpu_count': 3, 'create_json': 1, 'inpattern': 'input/default/Image{0:04d}.png', 'outpath': 'output/resdefaultMQFOV30', 'outputpatternjson': '/Posedata{0:04d}.json', 'outputpatternviz': '/viz/Image{0:04d}.png', 'outputpatternviz1': '/viz1/Image{0:04d}.png', 'outputpatternviz2': '/viz2/Image{0:04d}.png'}

'''

### 1.4 run the job

'''
(tf-py38) jenscave@jenscave-i5:~/Documents/BDR_Root/BDR4/bmmetrabs$ ./evaltofiles.py 
###e2f#######################################################
 START 
^^^e2f^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Name of Python script: ./evaltofiles.py
Argument List:
len(_cl) 1
class __init__ Jobfile e2fjobdefaultMQFOV30.json
{'version': 3, 'max_detections': 1, 'fov_degrees': 30, 'skeleton': '', 'start': 1, 'end': 10, 'skip': 1, 'viz': 1, 'qual': 10, 'cpu_count': 3, 'create_json': 1, 'inpattern': 'input/default/Image{0:04d}.png', 'outpath': 'output/resdefaultMQFOV30', 'outputpatternjson': '/Posedata{0:04d}.json', 'outputpatternviz': '/viz/Image{0:04d}.png', 'outputpatternviz1': '/viz1/Image{0:04d}.png', 'outputpatternviz2': '/viz2/Image{0:04d}.png'}
Start 1 End 10 Skip 1
inpattern input/default/Image{0:04d}.png outpath output/resdefaultMQFOV30 json output/resdefaultMQFOV30/Posedata{0:04d}.json viz output/resdefaultMQFOV30/viz/Image{0:04d}.png
###e2f#######################################################
 load model :) 
^^^e2f^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
'''
Wait.. 

loading takes a while

....







2. Metrabs2Blender Cropping results in Blender
