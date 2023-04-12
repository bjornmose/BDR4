#!/usr/bin/env python3
import resource
import gc
import os
import json
from os.path import exists

import tensorflow as tf

#say where the files come from
def inpattern():
    return 'Cris26leave/Image{0:04d}.png'

#just say where the output goes
def outpath():
    return 'fileresCr26leave/'

def outputpatternjson():
    return outpath() + 'Posedata{0:04d}.json'

def outputpatternviz():
    return outpath() + 'Image{0:04d}.png'



def main():
    frame_start= 3416
    frame_end = 3634
    frame_skip= 1
     
    viz = 2
    qual = 0
    cpu_count = 10
    fov_degrees = 55
    
    create_json = 1 # enum 0 dont 1 skip existing 2 overwrite
#    skeleton = 'smpl+head_30'
#    skeleton = 'coco_19'
#    skeleton = 'h36m_17'
#    skeleton = 'h36m_25'
#    skeleton = 'mpi_inf_3dhp_17'
    skeleton = 'mpi_inf_3dhp_28'

    print('Start', frame_start, 'End', frame_end, 'Skip',frame_skip)	
    #inpattern ='inputimages/Image{0:04d}.png'
    with open(outpath()+'jobinfo.json', 'w') as ji:
        jdata = {}
        jdata['skeleton'] = skeleton 
        jdata['start'] = frame_start
        jdata['end'] = frame_end
        jdata['inpattren'] = inpattern()
        json.dump(jdata, ji, ensure_ascii=False, indent=4)
        ji.close()	
        

    #see if image exists
    probename=inpattern().format(frame_start)
    if not exists(probename):
      print('no input leaving')
      return
    tf.config.threading.set_intra_op_parallelism_threads(cpu_count)
    if qual < 1 : model = tf.saved_model.load('./models/metrabs_mob3l_y4t')
    else:
      if qual < 20 : model = tf.saved_model.load('./models/metrabs_eff2s_y4')
      else:
        if qual < 50 :
          model = tf.saved_model.load('./models/metrabs_eff2l_y4')
        else:
          model = tf.saved_model.load('./models/metrabs_eff2l_y4_360')
      
    print('end load\n')	
    with open('debugoutput.txt', 'w') as f:

    
     for i in range ( frame_start , frame_end , frame_skip):
      if jsonexists(i) : 
         if create_json < 2:
           print('skip',i)
           continue
      name=inpattern().format(i)
      print('in->',name)
      image = tf.image.decode_jpeg(tf.io.read_file(name))
      #no mem leak until here
      pred = model.detect_poses(image, default_fov_degrees=fov_degrees, skeleton=skeleton, max_detections=1)
      #wild guess leak is in the line above
      pred = tf.nest.map_structure(lambda x: x.numpy(), pred)  # convert tensors to numpy arrays
#      print(pred['boxes'], pred['poses3d'], pred['poses2d'])
#      print(pred['poses3d'], file=f)
      
      joint_names = model.per_skeleton_joint_names[skeleton].numpy().astype(str)
      joint_edges = model.per_skeleton_joint_edges[skeleton].numpy()   
      if viz == 1 :visualize_3dtofile(image.numpy(), pred, joint_names, joint_edges,i)
      if viz == 2 :visualize_tofile(image.numpy(), pred, joint_names, joint_edges,i)
      if i == 1 : print(skeleton,joint_names,file=f)
      if create_json > 0 :
        p3d = pred['poses3d']
        pose2json(skeleton,p3d,joint_names,i)
      print('Frame Loop ', i, ' maxrss: ', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, file=f)
      print('Frame Loop ', i, ' maxrss: ', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
      print('garbage collect')
      gc.collect()

    # Read the docs to learn how to
    # - supply your own bounding boxes
    # - perform multi-image (batched) prediction
    # - supply the intrinsic and extrinsic camera calibration matrices
    # - select the skeleton convention (COCO, H36M, SMPL...)
    # etc.

def jsonexists(frame):
     name=outputpatternjson().format(frame)
     file_exists = exists(name)
     return(file_exists)

def pose2json(skeleton,p3d,joint_names,frame):
    name=outputpatternjson().format(frame)
    print('<-out',name)
    with open(name, 'w', encoding='utf-8') as jf:
        jdata = {}
        jdata['skeleton'] = skeleton 
        jdata['joints'] = []
        jdata['pose3d'] = []
        
        for joint in joint_names:
          jdata['joints'].append(joint.astype(str))
          if len(p3d) > 0 :         	
             for ppose,joint, in zip(p3d[0],joint_names):
               jdata['pose3d'].append([joint.astype(str), ppose[0].astype(float) ,ppose[1].astype(float) , ppose[2].astype(float)])
        json.dump(jdata, jf, ensure_ascii=False, indent=4)
        jf.close()


def download_model(model_type):
    server_prefix = 'https://omnomnom.vision.rwth-aachen.de/data/metrabs'
    model_zippath = tf.keras.utils.get_file(
        origin=f'{server_prefix}/{model_type}_20211019.zip',
        extract=True, cache_subdir='models')
    model_path = os.path.join(os.path.dirname(model_zippath), model_type)
    return model_path


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


def visualize_tofile(image, pred, joint_names, joint_edges,i):
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
    poses3d[..., 1], poses3d[..., 2] = poses3d[..., 2], -poses3d[..., 1]
    for pose3d, pose2d in zip(poses3d, poses2d):
        for i_start, i_end in joint_edges:
            image_ax.plot(*zip(pose2d[i_start], pose2d[i_end]), marker='o', markersize=2)
        image_ax.scatter(*pose2d.T, s=2)
        

 
    fig.tight_layout()
    name=outputpatternviz().format(i)
    print(name)
    fig.savefig(name, dpi=200) 
#    plt.show()


def visualize_3dtofile(image, pred, joint_names, joint_edges,frame):
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
    name=outputpatternviz().format(frame)
    print(name)
    fig.savefig(name, dpi=200) 


 
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


if __name__ == '__main__':
    main()
    
    
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
    
    
