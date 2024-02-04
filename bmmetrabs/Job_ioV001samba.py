#!/usr/bin/env python3
import resource
import gc
import os
import json
import sys
from os.path import exists
#licence GPL
#author bjornmose
#today 2024_01_31
version = 4

##############################################
# configuration start
##############################################

# choose skeleton
#skeleton = ''
skeleton = 'smpl+head_30'
# skeleton = 'coco_19'
# skeleton = 'h36m_17'
# skeleton = 'h36m_25'
# skeleton = 'mpi_inf_3dhp_17'
#skeleton = 'mpi_inf_3dhp_28'


# I/O Path
datapath = 'BlueLeg'
#outpathdeko
outpathdeko = ''
# absolute path homebased
usehome = True
datapathpre = '/sambashare/MetarbsData/'
filetemplate = '/Image{0:04d}.png'


#fov_degrees = 30
fov_degrees = 55
#fov_degrees = 75
#fov_degrees = 100

#'quality' v: v<1 lowest v<20 medium v<50 good else above  https://istvansarandi.com/dozens/ model  >199 >215 >225
#old !! return other joints 
#qual = 10
#qual = 25
#qual = 55
#New with unified joinz
#qual = 200
qual = 220
#qual = 230
#models picked by chance
'''
    EfficientNetV2-S, 256 px: hub.load('https://bit.ly/metrabs_s_256')
    EfficientNetV2-S, 384 px: hub.load('https://bit.ly/metrabs_s')
    EfficientNetV2-L, 384 px: hub.load('https://bit.ly/metrabs_l')
    EfficientNetV2-XL, 384 px: hub.load('https://bit.ly/metrabs_xl')
'''    
#qual = 400
qual = 401
#qual = 402
#qual = 403
#qual = 404
#qual = 405
modellist = {
	400:'',
	401:'metrabs_eff2s_y4_384px_800k_28ds',
	402:'metrabs_eff2s_y4_256px_1600k_28ds',
	403:'metrabs_eff2l_y4_384px_800k_28ds',
	404:'metrabs_eff2xl_y4_384px_800k_28ds',
	405:''
}
tfmodelname = ''
#use modellist
if (qual > 399):
	tfmodelname = modellist[qual]


#framerange
frame_start = 1
frame_end = 30000 # 7000
skip = 1

#
max_detections=1

#result as images 
viz = 2 # enum 0, none 1, 3D Plot 2, 2D ovelay clipped 3, 3D 2D aside 
#result as data
create_json = 1  # enum 0, dont 1, skip existing 2, overwrite
add_2d_json = 0 
cpu_count = 3


##############################################
# configuration end
##############################################

#adust pathes

# set appenix
txt="{}fov{}m{}".format(skeleton,fov_degrees,qual)
resdetail = txt+outpathdeko
respath = datapath + resdetail

jobfilename = 'e2fjob'+datapath+resdetail+'.json'
#use relative (local) path by default
inpath ='input/' + datapath
outpath ='output/res' + respath
#override to absolute path in users home
if (usehome):
	home_directory = os.path.expanduser( '~' )
	inpath = home_directory+datapathpre+'input/' + datapath
	outpath =home_directory+datapathpre+'output/res' + respath


inpattern = inpath + filetemplate



# create default file
if (0):
	datapath = 'default'
	# set appenix
	respath = datapath
	inpath = 'input/' + datapath
	outpath = 'output/res' + respath
	frame_start = 1
	frame_end = 10
	jobfilename = 'e2fjob'+datapath+'.json'
	create_json = 2  # enum 0 dont 1 skip existing 2 overwrite
	fov_degrees = 90
	qual = 15  # enum 0 lowest 19 meduim 49 good above 100 best
	cpu_count = 1
	viz  = 1
	skip = 1


        

class Job_io:
    @classmethod
    def __init__(self,name = jobfilename):
        print('class __init__ Jobfile', name)
        self._myname = name

    @classmethod
    def myname(self):
    	#print('func myname smn',self._myname)
    	return self._myname

    @classmethod
    def make_job_input(self):
        with open(self.myname(), 'w') as ji:
            jdata = {}
            jdata['version'] = version
            jdata['max_detections'] = max_detections
            jdata['fov_degrees'] = fov_degrees
            jdata['skeleton'] = skeleton
            jdata['start'] = frame_start
            jdata['end'] = frame_end
            jdata['skip'] = skip
            jdata['viz'] = viz
            jdata['qual'] = qual
            jdata['modelname'] = tfmodelname
            jdata['cpu_count'] = cpu_count
            jdata['create_json'] = create_json
            jdata['add_2d_json'] = add_2d_json
            jdata['inpattern'] = inpattern
            jdata['outpath'] = outpath
            jdata['outputpatternjson'] = '/Posedata{0:04d}.json'
            jdata['outputpatternviz'] = '/viz/Image{0:04d}.png'
            jdata['outputpatternviz1'] = '/viz1/Image{0:04d}.png'
            jdata['outputpatternviz2'] = '/viz2/Image{0:04d}.png'
            json.dump(jdata, ji, ensure_ascii=False, indent=4)
            ji.close()

    @classmethod           	
    def read_job_input(self):
        try: 
            with open(self.myname()) as json_file:
                jdata = json.load(json_file)
                return jdata
        except:
            print('read_job_input()->except',self.myname())
            return None

    
def main():

    # total arguments
    #n = len(sys.argv)
    #print("Total arguments passed:", n)
    # Arguments passed
    #print("\nName of Python script:", sys.argv[0])
    #print("\nArguments passed:", end = " ")
    #for i in range(1, n):
    	#print(sys.argv[i], end = " ")

    jobio = Job_io()
    #jobio = Job_io('something_else.json')
    
    res = jobio.read_job_input()
    if (res == None):
        jobio.make_job_input()
        print(jobio.myname(),'created' )
        res = jobio.read_job_input()
        print ('The job is',res)

    else :
        print ('found job is',res)
        answ = input('Replace? [y/n] ')
        if len(answ)>0:
            if answ[0] ==  'y':
                jobio.make_job_input()
                print('Replaced->',jobio.myname())
                res = jobio.read_job_input()
                print ('New job is',res)
            else:
                if answ[0] ==  'n':
                    print('no changes')
                else:
                    print(answ)
                    print('so what?')
        	
        


if __name__ == '__main__':
    main()


