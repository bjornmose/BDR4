#!/usr/bin/env python3
import resource
import gc
import os
import json
import sys
from os.path import exists

version = 3

# choose skeleton
#skeleton = ''
#skeleton = 'smpl+head_30'
# skeleton = 'coco_19'
# skeleton = 'h36m_17'
# skeleton = 'h36m_25'
# skeleton = 'mpi_inf_3dhp_17'
skeleton = 'mpi_inf_3dhp_28'


# set other parameters here
datapath = 'Cris26'
fov_degrees = 55
qual = 230  # v: v<1 lowest v<20 medium v<50 good else above  https://istvansarandi.com/dozens/ model  >199 >215 >225
txt="fov{}m{}".format(fov_degrees,qual) 
txt=skeleton+txt
resdetail = ''+txt
frame_start = 730
frame_end = 2800  # 7000

max_detections=1
create_json = 1  # enum 0 dont 1 skip existing 2 overwrite
cpu_count = 3
viz = 2
skip = 1
#adust pathes

# set appenix
respath = datapath + resdetail
jobfilename = 'e2fjob'+datapath+resdetail+'.json'

inpath = 'input/' + datapath
outpath = 'output/res' + respath

inpattern = inpath +'/Image{0:04d}.png'
#inpattern = inpath +'/image{0:04d}.png'



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
            jdata['cpu_count'] = cpu_count
            jdata['create_json'] = create_json
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


