#!/usr/bin/env python3
#evaltofiles.py vers: J
import resource
import gc
import os
import sys
import json
from os.path import exists
from os import remove
from Job_ioV001 import Job_io


import tensorflow as tf


msgbarstart = '###e2f#######################################################\n'
msgbarend   = '\n^^^e2f^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'


def main(jobname):
    #set default values
    max_blowup= 1.1
    frame_start= 1
    frame_end = 10
    frame_skip= 1
    qual = 0 # 0 lowest 19 meduim 49 good above 100 best
    cpu_count = 3
    fov_degrees = 55
    viz = 0
    max_detections=1
    create_json = 1 # enum 0 dont 1 skip existing 2 overwrite
    outpath = 'output/fileres'
    inpattern = 'input/metrabsimg/image{0:04d}.png'
    outputpatternjson = outpath + '/Posedata{0:04d}.json'
    outputpatternviz = outpath + '/viz/Image{0:04d}.png'
    outputpatternviz1 = outpath + '/viz1/Image{0:04d}.png'
    outputpatternviz2 = outpath + '/viz2/Image{0:04d}.png'
    skeleton = 'smpl+head_30'
#    skeleton = 'coco_19'
#    skeleton = 'h36m_17'
#    skeleton = 'h36m_25'
#    skeleton = 'mpi_inf_3dhp_17'
#    skeleton = 'mpi_inf_3dhp_28'
    if jobname == None: 
        joi = Job_io()
        #use the name known by class Job_io()
    else:
        joi = Job_io(jobname)

    inpt = joi.read_job_input()
    if inpt != None:
        print(inpt)
        viz = inpt['viz']
        qual = inpt['qual']
        frame_start = inpt['start']
        frame_end = inpt['end']
        frame_skip = inpt['skip']
        outpath = inpt['outpath']
        inpattern = inpt['inpattern'] 
        outputpatternjson = outpath + inpt['outputpatternjson'] 
        outputpatternviz =  outpath + inpt['outputpatternviz']
        skeleton = inpt['skeleton']
        try:
            version = inpt['version']
        except:
            print(msgbarstart,'no_Vesion --> deprcated file',msgbarend)
            version = 0
        if version > 0:
            create_json = inpt['create_json']
        if version > 1:
            cpu_count = inpt['cpu_count']
            fov_degrees = inpt['fov_degrees']
            max_detections = inpt['max_detections'] 
        if version > 2:
            outputpatternviz1 =  outpath + inpt['outputpatternviz1']
            outputpatternviz2 =  outpath + inpt['outputpatternviz2']

            
    else:
        print(msgbarstart,'job not found: ->',joi.myname(),'<- *using defaults*',msgbarend)


    if create_json > 0:
        name = outputpatternjson.format(42)+'.txt'
        try:
            with open(name, 'w') as probe:
                print('Path looks good',file=probe)
                probe.close()
                os.remove(name)
        except:
            print(msgbarstart,'can not write:',name,msgbarend)
            return
        
        
    if viz > 0:
        name = outputpatternviz.format(42)+'.txt'
        try:
            with open(name, 'w') as probe:
                print('Path looks good',file=probe)
                probe.close()
                os.remove(name)
        except:
            print(msgbarstart,'can not write:',name,msgbarend)
            return

    if viz > 2:
        name = outputpatternviz2.format(42)+'.txt'
        try:
            with open(name, 'w') as probe:
                print('Path looks good',file=probe)
                probe.close()
                os.remove(name)
        except:
            print(msgbarstart,'can not write:',name,msgbarend)
            return


    

    
         
     
    if qual < 1 : 
        _modelname = './models/metrabs_mob3l_y4t'
    else: 
        if qual < 20 : 
            _modelname = './models/metrabs_eff2s_y4'
        else:
            if qual< 50 : 
                _modelname = './models/metrabs_eff2l_y4'
#new models 2023 
#picked from
#https://istvansarandi.com/dozens/
    if qual > 199 :
    	_modelname = './models/metrabs_eff2s_y4_256px_1600k_28ds'
    	if qual > 215:
    		_modelname = './models/metrabs_eff2s_y4_384px_800k_28ds'
    	if qual > 225:    	
    		_modelname = './models/metrabs_eff2l_y4_384px_800k_28ds'


    print('Start', frame_start, 'End', frame_end, 'Skip',frame_skip)    
    print('inpattern', inpattern, 'outpath', outpath, 'json',outputpatternjson,'viz',outputpatternviz)  
    with open(outpath+'/jobinfo.json', 'w') as ji:
        jdata = {}
        jdata['skeleton'] = skeleton 
        jdata['start'] = frame_start
        jdata['end'] = frame_end
        jdata['inpattern'] = inpattern
        jdata['modelname'] = _modelname
        jdata['max_detections'] = max_detections
        jdata['fov_degrees'] = fov_degrees
        json.dump(jdata, ji, ensure_ascii=False, indent=4)
        ji.close()  

    #see if image exists
    probename=inpattern.format(frame_start)
    if not exists(probename):
      print(msgbarstart,'no input:',probename,'STOP',msgbarend)
      return
    tf.config.threading.set_intra_op_parallelism_threads(cpu_count)

    print(msgbarstart,'load model :)',_modelname,msgbarend)
    model = tf.saved_model.load(_modelname)
    memstart = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss    
    print(msgbarstart,'model loaded:)',msgbarend)
    with open('debugoutput.txt', 'w') as f:

    
     for i in range ( frame_start , frame_end , frame_skip):
      if jsonexists(i,outputpatternjson) : 
         if create_json < 2:
           print('skip',i)
           continue
      _name=inpattern.format(i)
      progress = 100.0 * (i - frame_start)/(frame_end-frame_start)
      print('in->',_name,'max_detections',max_detections,'progress',progress)
      doimage(model,i,inpattern,fov_degrees,skeleton,max_detections,viz,create_json,outputpatternviz,outputpatternviz1,outputpatternviz2,outputpatternjson)
      gc.collect()
      memnow = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
      memratio = (memnow - memstart) / memstart
      print('Blowup:',memratio,'Max',max_blowup)
      if (memratio > max_blowup) :
      	print(msgbarstart+'Blowup limit at',i,progress,'%',msgbarend)
      	return
      print('Frame Loop ', i, ' maxrss: ', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(msgbarstart,'DONE :)',msgbarend)
    

    # Read the docs to learn how to
    # - supply your own bounding boxes
    # - perform multi-image (batched) prediction
    # - supply the intrinsic and extrinsic camera calibration matrices
    # - select the skeleton convention (COCO, H36M, SMPL...)
    # etc.
    
def doimage(model,i,inpattern,fov_degrees,skeleton,max_detections,viz,create_json,outputpatternviz,outputpatternviz1,outputpatternviz2,outputpatternjson):
	name=inpattern.format(i)
	image = tf.image.decode_jpeg(tf.io.read_file(name))
	try:
		pred = model.detect_poses(image, default_fov_degrees=fov_degrees, skeleton=skeleton, max_detections=max_detections)
	except:
		print(msgbarstart)
		print('detect_poses bailed out','max_detections',max_detections)
	if max_detections > 1:
		print('retry with 1')
		try:
			print(msgbarstart)
			pred = model.detect_poses(image, default_fov_degrees=fov_degrees, skeleton=skeleton, max_detections=1)
		except:
			print('did not work',file=f)
			fail2json(i,outputpatternjson)
			return
	pred = tf.nest.map_structure(lambda x: x.numpy(), pred)  # convert tensors to numpy arrays
	joint_names = model.per_skeleton_joint_names[skeleton].numpy().astype(str)	
	joint_edges = model.per_skeleton_joint_edges[skeleton].numpy()
	rearrange(pred)   
	if create_json > 0 :
		p3d = pred['poses3d']
		boxes = pred['boxes']
		pose2json(skeleton,p3d,boxes,joint_names,i,outputpatternjson)
	if viz == 1 :visualize_3dtofile(image.numpy(), pred, joint_names, joint_edges,i,outputpatternviz)
	if viz == 2 :visualize_tofile(image.numpy(), pred, joint_names, joint_edges,i,outputpatternviz)
	if viz == 3 :
		visualize_tofile(image.numpy(), pred, joint_names, joint_edges,i,outputpatternviz1)
		visualize_3dOtofile(image.numpy(), pred, joint_names, joint_edges,i,outputpatternviz2)
		visualize_3dtofile(image.numpy(), pred, joint_names, joint_edges,i,outputpatternviz)


	

def jsonexists(frame,pat):
     name=pat.format(frame)
     file_exists = exists(name)
     return(file_exists)

def fail2json(frame,pat):
    name=pat.format(frame)
    with open(name, 'w', encoding='utf-8') as jf:
        jdata = {}
        jdata['fail'] = []
        json.dump(jdata, jf, ensure_ascii=False, indent=4)
        jf.close()


def pose2json(skeleton,p3d,boxes,joint_names,frame,pat):
    name=pat.format(frame)
    print('<-out',name)
    with open(name, 'w', encoding='utf-8') as jf:
        jdata = {}
        jdata['boxes'] = []
        jdata['skeleton'] = skeleton 
        jdata['joints'] = []
        jdata['pose3d'] = []
        jdata['pose3d1'] = []
        jdata['pose3d2'] = []
        for x, y, w, h in boxes[:, :4]:
          jdata['boxes'].append([x.astype(float),y.astype(float)])
          
        for joint in joint_names:
          jdata['joints'].append(joint.astype(str))
          if len(p3d) > 0 :             
             for ppose,joint, in zip(p3d[0],joint_names):
               jdata['pose3d'].append([joint.astype(str), ppose[0].astype(float) ,ppose[1].astype(float) , ppose[2].astype(float)])
          if len(p3d) > 1 :             
             for ppose,joint, in zip(p3d[1],joint_names):
               jdata['pose3d1'].append([joint.astype(str), ppose[0].astype(float) ,ppose[1].astype(float) , ppose[2].astype(float)])
          if len(p3d) > 2 :             
             for ppose,joint, in zip(p3d[2],joint_names):
               jdata['pose3d2'].append([joint.astype(str), ppose[0].astype(float) ,ppose[1].astype(float) , ppose[2].astype(float)])
        json.dump(jdata, jf, ensure_ascii=False, indent=4)
        jf.close()


def download_model(model_type):
    server_prefix = 'https://omnomnom.vision.rwth-aachen.de/data/metrabs'
    model_zippath = tf.keras.utils.get_file(
        origin=f'{server_prefix}/{model_type}_20211019.zip',
        extract=True, cache_subdir='models')
    model_path = os.path.join(os.path.dirname(model_zippath), model_type)
    return model_path


def rearrange(pred):
    poses3d = pred['poses3d']
    poses3d[..., 1], poses3d[..., 2] = poses3d[..., 2], -poses3d[..., 1]
	   


def visualize(image, pred, joint_names, joint_edges):
    try:
        visualize_poseviz(image, pred, joint_names, joint_edges)
    except ImportError:
        print(
            'Install PoseViz from https://github.com/isarandi/poseviz to get a nicer 3D'
            'visualization.')
        visualize_matplotlib(image, pred, joint_names, joint_edges)


def visualize_poseviz(image, pred, joint_names, joint_edges):
    # Install PoseViz from https://github.com/isarandi/poseviz
    import poseviz
    camera = poseviz.Camera.from_fov(55, image.shape)
    viz = poseviz.PoseViz(joint_names, joint_edges)
    viz.update(frame=image, boxes=pred['boxes'], poses=pred['poses3d'], camera=camera)


def visualize_tofile(image, pred, joint_names, joint_edges,i,pat):
    detections, poses3d, poses2d = pred['boxes'], pred['poses3d'], pred['poses2d']

    import matplotlib.pyplot as plt
    # noinspection PyUnresolvedReferences
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.patches import Rectangle
    plt.switch_backend('TkAgg')

    fig = plt.figure(figsize=(7, 5))
    image_ax = fig.add_subplot(1, 1, 1)
    image_ax.imshow(image)
    for x, y, w, h in detections[:, :4]:
        image_ax.add_patch(Rectangle((x, y), w, h, fill=False))
        
    # Matplotlib plots the Z axis as vertical, but our poses have Y as the vertical axis.
    # Therefore, we do a 90° rotation around the X axis:
    #poses3d[..., 1], poses3d[..., 2] = poses3d[..., 2], -poses3d[..., 1]
    for pose3d, pose2d in zip(poses3d, poses2d):
        for i_start, i_end in joint_edges:
            image_ax.plot(*zip(pose2d[i_start], pose2d[i_end]), marker='o', markersize=2)
        image_ax.scatter(*pose2d.T, s=2)
        

 
    fig.tight_layout()
    name=pat.format(i)
    print('<--',name)
    fig.savefig(name, dpi=200) 
    plt.close()
#    plt.show()


def visualize_3dtofile(image, pred, joint_names, joint_edges,frame,pat):
    detections, poses3d, poses2d = pred['boxes'], pred['poses3d'], pred['poses2d']

    import matplotlib.pyplot as plt
    # noinspection PyUnresolvedReferences
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.patches import Rectangle
    plt.switch_backend('TkAgg')

    fig = plt.figure(figsize=(10, 5.2))
    image_ax = fig.add_subplot(1, 2, 1)
    image_ax.imshow(image)
    for x, y, w, h in detections[:, :4]:
        image_ax.add_patch(Rectangle((x, y), w, h, fill=False))

    pose_ax = fig.add_subplot(1, 2, 2, projection='3d')
    pose_ax.view_init(5, -85)
    pose_ax.set_xlim3d(-1500, 1500)
    pose_ax.set_zlim3d(-1500, 1500)
    pose_ax.set_ylim3d(0, 3000)
    pose_ax.set_box_aspect((1, 1, 1))

    # Matplotlib plots the Z axis as vertical, but our poses have Y as the vertical axis.
    # Therefore, we do a 90° rotation around the X axis:
    #poses3d[..., 1], poses3d[..., 2] = poses3d[..., 2], -poses3d[..., 1]
    for pose3d, pose2d in zip(poses3d, poses2d):
        for i_start, i_end in joint_edges:
            image_ax.plot(*zip(pose2d[i_start], pose2d[i_end]), marker='o', markersize=2)
            pose_ax.plot(*zip(pose3d[i_start], pose3d[i_end]), marker='o', markersize=2)
        image_ax.scatter(*pose2d.T, s=2)
        pose_ax.scatter(*pose3d.T, s=2)

    fig.tight_layout()
    name=pat.format(frame)
    print(name)
    fig.savefig(name, dpi=200)
    plt.close() 

def visualize_3dOtofile(image, pred, joint_names, joint_edges,frame,pat):
    detections, poses3d, poses2d = pred['boxes'], pred['poses3d'], pred['poses2d']

    import matplotlib.pyplot as plt
    # noinspection PyUnresolvedReferences
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.patches import Rectangle
    plt.switch_backend('TkAgg')

    fig = plt.figure(figsize=(10, 5.2))

    pose_ax = fig.add_subplot(1, 1, 1, projection='3d')
    pose_ax.view_init(5, -85)
    pose_ax.set_xlim3d(-1500, 1500)
    pose_ax.set_zlim3d(-1500, 1500)
    pose_ax.set_ylim3d(0, 3000)
    pose_ax.set_box_aspect((1, 1, 1))

    # Matplotlib plots the Z axis as vertical, but our poses have Y as the vertical axis.
    # Therefore, we do a 90° rotation around the X axis:
    # poses3d[..., 1], poses3d[..., 2] = poses3d[..., 2], -poses3d[..., 1]
    # not needed if 3D only
    for pose3d in poses3d:
        for i_start, i_end in joint_edges:
            pose_ax.plot(*zip(pose3d[i_start], pose3d[i_end]), marker='o', markersize=2)
        pose_ax.scatter(*pose3d.T, s=2)

    fig.tight_layout()
    name=pat.format(frame)
    print(name)
    fig.savefig(name, dpi=200) 
    plt.close()

 
def visualize_matplotlib(image, pred, joint_names, joint_edges):
    detections, poses3d, poses2d = pred['boxes'], pred['poses3d'], pred['poses2d']

    import matplotlib.pyplot as plt
    # noinspection PyUnresolvedReferences
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.patches import Rectangle
    plt.switch_backend('TkAgg')

    fig = plt.figure(figsize=(10, 5.2))
    image_ax = fig.add_subplot(1, 2, 1)
    image_ax.imshow(image)
    for x, y, w, h in detections[:, :4]:
        image_ax.add_patch(Rectangle((x, y), w, h, fill=False))

    pose_ax = fig.add_subplot(1, 2, 2, projection='3d')
    pose_ax.view_init(5, -85)
    pose_ax.set_xlim3d(-1500, 1500)
    pose_ax.set_zlim3d(-1500, 1500)
    pose_ax.set_ylim3d(0, 3000)
    pose_ax.set_box_aspect((1, 1, 1))

    # Matplotlib plots the Z axis as vertical, but our poses have Y as the vertical axis.
    # Therefore, we do a 90° rotation around the X axis:
    poses3d[..., 1], poses3d[..., 2] = poses3d[..., 2], -poses3d[..., 1]
    for pose3d, pose2d in zip(poses3d, poses2d):
        for i_start, i_end in joint_edges:
            image_ax.plot(*zip(pose2d[i_start], pose2d[i_end]), marker='o', markersize=2)
            pose_ax.plot(*zip(pose3d[i_start], pose3d[i_end]), marker='o', markersize=2)
        image_ax.scatter(*pose2d.T, s=2)
        pose_ax.scatter(*pose3d.T, s=2)

    fig.tight_layout()
    plt.show()
    plt.close()

def readCL():
    # total arguments
    n = len(sys.argv)
    # Arguments passed
    print("\nName of Python script:", sys.argv[0])
    print("Argument List:")
    for i in range(1, n):
            print(i,sys.argv[i])
    return sys.argv



if __name__ == '__main__':
    print(msgbarstart,'START',msgbarend)
    _cl = readCL()
    n = len(_cl)
    print('len(_cl)',n)
    if n > 1 :
        jobname = _cl[1]
        print(msgbarstart,'JobName:',jobname,msgbarend)
        main(jobname)
    else:
        main(None)
        '''
        probe = 'e2fjobdefault.json'
        if exists(probe):
            print(msgbarstart,'Found:',probe,msgbarend)
            main(probe)
        else:main(None)
        '''
            
    
    
#    Our models support several different skeleton conventions out of the box. Specify one of the
#    following strings as the ```skeleton``` argument to the prediction functions.
'''
- ```smpl_24```: SMPL body model
- ```coco_19```: COCO joints including pelvis at the midpoint of the hips and neck at the midpoint
  of the shoulders as in CMU-Panoptic.
- ```h36m_17```: Most common Human3.6M joint convention
- ```h36m_25```: Extended Human3.6M joint set
- ```mpi_inf_3dhp_17```: MPI-INF-3DHP main joints (same as the MuPoTS joints)
- ```mpi_inf_3dhp_28```: full MPI-INF-3DHP joint set
- ```smpl+head_30```: SMPL joints plus face keypoints from COCO and the head top from MPI-INF-3DHP (
  recommended for visualization as SMPL_24 has no face keypoints).
- (empty string): All the joints that the model was trained on.
'''
    
    
