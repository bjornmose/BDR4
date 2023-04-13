# BDR4
Some work I did to crop the fruit of :

https://github.com/isarandi/metrabs [1]

in my little blender world on an lunix machine

There are two folders
## 1. bmmetrabs: Calling METRABS for a sequence of images
## 2. Metrabs2Blender Cropping results in Blender

## 1. bmmetrabs: Calling METRABS for a sequence of images
### 1.1 have a python shell with tensorflow installed
to get there see [1]
'''
jenscave@jenscave-i5:~/Documents/BDR_Root/BDR4/bmmetrabs$ eval "$("$HOME/miniconda3/bin/conda" shell.bash hook)" 
(base) jenscave@jenscave-i5:~/Documents/BDR_Root/BDR4/bmmetrabs$ conda activate tf-py38
'''

### 1.2 Edit the file Job_ioV001.py to your needs

### 1.3 run it
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
### 1.5 Results
There should be a bunch of JSON files in the destination folder:
```
jenscave@jenscave-i5:~/Documents/BDR_Root/BDR4/bmmetrabs/output/resdefaultMQFOV30$ ls
jobinfo.json       Posedata0002.json  Posedata0004.json  Posedata0006.json  Posedata0008.json  viz
Posedata0001.json  Posedata0003.json  Posedata0005.json  Posedata0007.json  Posedata0009.json
```



## 2. Metrabs2Blender Cropping results in Blender
Blender files are 2.79 but should work with 3.x too
