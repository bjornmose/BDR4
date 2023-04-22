# BDR4

Some work I did to crop the fruit of :

https://github.com/isarandi/metrabs [1]

in my little blender world on an lunix machine

There are three folders
## 1. bmmetrabs: Calling METRABS for a sequence of images
## 2. Metrabs2Blender Cropping results in Blender
## 3. Metrabs2Blender3_x Cropping results in Blender

## 1. bmmetrabs: Calling METRABS for a sequence of images
### 1.1 have a python shell with tensorflow installed
to get there see [1]

works fine without using the GPU
Want you GPU to run? -> Follow ulysses in TensorFlowGPUHack.txt

``
jenscave@jenscave-i5:~/Documents/BDR_Root/BDR4/bmmetrabs$ eval "$("$HOME/miniconda3/bin/conda" shell.bash hook)" 
(base) jenscave@jenscave-i5:~/Documents/BDR_Root/BDR4/bmmetrabs$ conda activate tf-py38
``
### 1.2 Edit the file Job_ioV001.py to your needs

### 1.3 run it
```
(tf-py38) jenscave@jenscave-i5:~/Documents/BDR_Root/BDR4/bmmetrabs$ ./Job_ioV001.py 
class __init__ Jobfile e2fjobdefaultMQFOV30.json
found job is {'version': 3, 'max_detections': 1, 'fov_degrees': 30, 'skeleton': '', 'start': 1, 'end': 10, 'skip': 1, 'viz': 1, 'qual': 10, 'cpu_count': 3, 'create_json': 1, 'inpattern': 'input/default/Image{0:04d}.png', 'outpath': 'output/resdefaultMQFOV30', 'outputpatternjson': '/Posedata{0:04d}.json', 'outputpatternviz': '/viz/Image{0:04d}.png', 'outputpatternviz1': '/viz1/Image{0:04d}.png', 'outputpatternviz2': '/viz2/Image{0:04d}.png'}
Replace? [y/n] y
Replaced-> e2fjobdefaultMQFOV30.json
New job is {'version': 3, 'max_detections': 1, 'fov_degrees': 30, 'skeleton': '', 'start': 1, 'end': 10, 'skip': 1, 'viz': 1, 'qual': 10, 'cpu_count': 3, 'create_json': 1, 'inpattern': 'input/default/Image{0:04d}.png', 'outpath': 'output/resdefaultMQFOV30', 'outputpatternjson': '/Posedata{0:04d}.json', 'outputpatternviz': '/viz/Image{0:04d}.png', 'outputpatternviz1': '/viz1/Image{0:04d}.png', 'outputpatternviz2': '/viz2/Image{0:04d}.png'}

```

NOTE: the destination folders must be there ... otherwise evaltofiles.py will complain! 
NOTE: the models folders is empty  ! see text in the folder. For now my choices are:

```

    if qual < 1 : 
        _modelname = './models/metrabs_mob3l_y4t'
    else: 
        if qual < 20 : 
            _modelname = './models/metrabs_eff2s_y4'
        else:
            if qual< 50 : 
                _modelname = './models/metrabs_eff2l_y4'
            else :
                _modelname = './models/metrabs_eff2l_y4_360'
```


### 1.4 run the job
```
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
```
Wait.. 

loading takes a while .. with loads of TF output

.... 1rst result
```
<-out output/resdefaultMQFOV30/Posedata0001.json
output/resdefaultMQFOV30/viz/Image0001.png

....
```
finally you may see
```
Frame Loop  9  maxrss:  5864248
###e2f#######################################################
 DONE :) 
^^^e2f^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
....
### 1.5 Results
There should be a bunch of JSON files in the destination folder:
```
jenscave@jenscave-i5:~/Documents/BDR_Root/BDR4/bmmetrabs/output/resdefaultMQFOV30$ ls
jobinfo.json       Posedata0002.json  Posedata0004.json  Posedata0006.json  Posedata0008.json  viz
Posedata0001.json  Posedata0003.json  Posedata0005.json  Posedata0007.json  Posedata0009.json
```
The optional viz folder holds images visualizing the results. The Posedata files hold the data to go on.
At this point you are free to go where ever you want. Data is JSON and can be imported by any tool of your choice.



## 2. Metrabs2Blender Cropping results in Blender 2.79a
However I decided to proceed with blender.
Blender files are 2.79 

## 3. Metrabs2Blender3_x Cropping results in Blender 3.x (3.2, 3.5 where tested here)
However I decided to proceed with blender.
Blender files are 3.5 
*.py files should work for 2.79 - 3.5 however I did not understand in which collecion(s) the empties are created any why



### Reading data to a bunch of 'empies'
Once the script 'ImportMetrabsjsonV004.py' ran in blender the object panel will have a button 'Make metrabs root' 
This will generate some 'custom properties' and some new items in the objects 'Metrabs' panel.
Once you have set the path variable there to the 'destination' folder it will enable the job reading and the importing button.
The script 'job reading' will evaluate the file 'jobinfo' and some of the object properties will be adjusted to read the data.
The script behind the import botton will do its very best to build a bunch of empties with actions attached. 

### Link to armature
So now we have a cloud of empties moving .. how to make my charater move?
Tricky but possible using constraints .. to be continued
Best 4 now LinkArmV004.py in MetrabsDemoLink.blend (2.79)
Best 4 now LinkArmV005.py in no file yet (3.x) would expect to work in MetrabsDemoLink.blend (2.79) loaded in 3.x


## on uTube

https://www.youtube.com/watch?v=yiU9tS6l2VU
https://www.youtube.com/watch?v=VgyKScXE33I
https://www.youtube.com/watch?v=r_s-iVQXNf0


