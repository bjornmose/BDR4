# BDR4
There are two folders

1. bmmetrabs: Calling METRABS for a sequence of images
1.1 have a python shell with tensorflow installed
<pre><font color="#26A269"><b>jenscave@jenscave-i5</b></font>:<font color="#12488B"><b>~/Documents/BDR_Root/BDR4/bmmetrabs</b></font>$ eval &quot;$(&quot;$HOME/miniconda3/bin/conda&quot; shell.bash hook)&quot; 
(base) <font color="#26A269"><b>jenscave@jenscave-i5</b></font>:<font color="#12488B"><b>~/Documents/BDR_Root/BDR4/bmmetrabs</b></font>$ conda activate tf-py38
(tf-py38) <font color="#26A269"><b>jenscave@jenscave-i5</b></font>:<font color="#12488B"><b>~/Documents/BDR_Root/BDR4/bmmetrabs</b></font>$ 

</pre>
1.2 Edit the file Job_ioV001.py to your needs

1.3 run it

<pre>tf-py38) <font color="#26A269"><b>jenscave@jenscave-i5</b></font>:<font color="#12488B"><b>~/Documents/BDR_Root/BDR4/bmmetrabs</b></font>$ ./Job_ioV001.py 
class __init__ Jobfile e2fjobdefaultMQFOV30.json
found job is {&apos;version&apos;: 3, &apos;max_detections&apos;: 1, &apos;fov_degrees&apos;: 30, &apos;skeleton&apos;: &apos;&apos;, &apos;start&apos;: 1, &apos;end&apos;: 10, &apos;skip&apos;: 1, &apos;viz&apos;: 1, &apos;qual&apos;: 10, &apos;cpu_count&apos;: 3, &apos;create_json&apos;: 1, &apos;inpattern&apos;: &apos;input/default/Image{0:04d}.png&apos;, &apos;outpath&apos;: &apos;output/resdefaultMQFOV30&apos;, &apos;outputpatternjson&apos;: &apos;/Posedata{0:04d}.json&apos;, &apos;outputpatternviz&apos;: &apos;/viz/Image{0:04d}.png&apos;, &apos;outputpatternviz1&apos;: &apos;/viz1/Image{0:04d}.png&apos;, &apos;outputpatternviz2&apos;: &apos;/viz2/Image{0:04d}.png&apos;}
Replace? [y/n] y
Replaced-&gt; e2fjobdefaultMQFOV30.json
New job is {&apos;version&apos;: 3, &apos;max_detections&apos;: 1, &apos;fov_degrees&apos;: 30, &apos;skeleton&apos;: &apos;&apos;, &apos;start&apos;: 1, &apos;end&apos;: 10, &apos;skip&apos;: 1, &apos;viz&apos;: 1, &apos;qual&apos;: 10, &apos;cpu_count&apos;: 3, &apos;create_json&apos;: 1, &apos;inpattern&apos;: &apos;input/default/Image{0:04d}.png&apos;, &apos;outpath&apos;: &apos;output/resdefaultMQFOV30&apos;, &apos;outputpatternjson&apos;: &apos;/Posedata{0:04d}.json&apos;, &apos;outputpatternviz&apos;: &apos;/viz/Image{0:04d}.png&apos;, &apos;outputpatternviz1&apos;: &apos;/viz1/Image{0:04d}.png&apos;, &apos;outputpatternviz2&apos;: &apos;/viz2/Image{0:04d}.png&apos;}
(tf-py38) <font color="#26A269"><b>jenscave@jenscave-i5</b></font>:<font color="#12488B"><b>~/Documents/BDR_Root/BDR4/bmmetrabs</b></font>$ 

</pre>

1.4 run the job
<pre>(tf-py38) <font color="#26A269"><b>jenscave@jenscave-i5</b></font>:<font color="#12488B"><b>~/Documents/BDR_Root/BDR4/bmmetrabs</b></font>$ ./Job_ioV001.py 
class __init__ Jobfile e2fjobdefaultMQFOV30.json
found job is {&apos;version&apos;: 3, &apos;max_detections&apos;: 1, &apos;fov_degrees&apos;: 30, &apos;skeleton&apos;: &apos;&apos;, &apos;start&apos;: 1, &apos;end&apos;: 10, &apos;skip&apos;: 1, &apos;viz&apos;: 1, &apos;qual&apos;: 10, &apos;cpu_count&apos;: 3, &apos;create_json&apos;: 1, &apos;inpattern&apos;: &apos;input/default/Image{0:04d}.png&apos;, &apos;outpath&apos;: &apos;output/resdefaultMQFOV30&apos;, &apos;outputpatternjson&apos;: &apos;/Posedata{0:04d}.json&apos;, &apos;outputpatternviz&apos;: &apos;/viz/Image{0:04d}.png&apos;, &apos;outputpatternviz1&apos;: &apos;/viz1/Image{0:04d}.png&apos;, &apos;outputpatternviz2&apos;: &apos;/viz2/Image{0:04d}.png&apos;}
Replace? [y/n] y
Replaced-&gt; e2fjobdefaultMQFOV30.json
New job is {&apos;version&apos;: 3, &apos;max_detections&apos;: 1, &apos;fov_degrees&apos;: 30, &apos;skeleton&apos;: &apos;&apos;, &apos;start&apos;: 1, &apos;end&apos;: 10, &apos;skip&apos;: 1, &apos;viz&apos;: 1, &apos;qual&apos;: 10, &apos;cpu_count&apos;: 3, &apos;create_json&apos;: 1, &apos;inpattern&apos;: &apos;input/default/Image{0:04d}.png&apos;, &apos;outpath&apos;: &apos;output/resdefaultMQFOV30&apos;, &apos;outputpatternjson&apos;: &apos;/Posedata{0:04d}.json&apos;, &apos;outputpatternviz&apos;: &apos;/viz/Image{0:04d}.png&apos;, &apos;outputpatternviz1&apos;: &apos;/viz1/Image{0:04d}.png&apos;, &apos;outputpatternviz2&apos;: &apos;/viz2/Image{0:04d}.png&apos;}
(tf-py38) <font color="#26A269"><b>jenscave@jenscave-i5</b></font>:<font color="#12488B"><b>~/Documents/BDR_Root/BDR4/bmmetrabs</b></font>$ ./evaltofiles.py 
###e2f#######################################################
 START 
^^^e2f^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Name of Python script: ./evaltofiles.py
Argument List:
len(_cl) 1
class __init__ Jobfile e2fjobdefaultMQFOV30.json
{&apos;version&apos;: 3, &apos;max_detections&apos;: 1, &apos;fov_degrees&apos;: 30, &apos;skeleton&apos;: &apos;&apos;, &apos;start&apos;: 1, &apos;end&apos;: 10, &apos;skip&apos;: 1, &apos;viz&apos;: 1, &apos;qual&apos;: 10, &apos;cpu_count&apos;: 3, &apos;create_json&apos;: 1, &apos;inpattern&apos;: &apos;input/default/Image{0:04d}.png&apos;, &apos;outpath&apos;: &apos;output/resdefaultMQFOV30&apos;, &apos;outputpatternjson&apos;: &apos;/Posedata{0:04d}.json&apos;, &apos;outputpatternviz&apos;: &apos;/viz/Image{0:04d}.png&apos;, &apos;outputpatternviz1&apos;: &apos;/viz1/Image{0:04d}.png&apos;, &apos;outputpatternviz2&apos;: &apos;/viz2/Image{0:04d}.png&apos;}
Start 1 End 10 Skip 1
inpattern input/default/Image{0:04d}.png outpath output/resdefaultMQFOV30 json output/resdefaultMQFOV30/Posedata{0:04d}.json viz output/resdefaultMQFOV30/viz/Image{0:04d}.png
###e2f#######################################################
 load model :) 
^^^e2f^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
</pre>

Wait.. 

loading takes a while

....







2. Metrabs2Blender Cropping results in Blender
