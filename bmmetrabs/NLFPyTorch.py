#!/usr/bin/env python3

import os
import numpy as np
import torch
import torchvision  # Must import this for the model to load without error


home_directory = os.path.expanduser( '~' )
home_models = home_directory+'/sambashare/modelstf2/'
home_data = home_directory+'/sambashare/nlf_data_files/'
num_verts = 52


#   cano_verts = makeFplane(50)
#   cano_joints = np.load(f'{home_data}/canonical_joints/smplh16.npy')
#    cano_verts = np.load(f'{home_data}/canonical_verts/smpl.npy')
marker_names = np.load(f'{home_data}/canonical_verts/MarkerNames{num_verts}.npy')
print(marker_names)
cano_verts = np.load(f'{home_data}/canonical_verts/Markers{num_verts}.npy')
cano_joints = np.load(f'{home_data}/canonical_joints/smpl.npy')
cano_all = np.concatenate([cano_verts, cano_joints], axis=0 )


print('Load Model')
model = torch.jit.load('models/nlf_l_multi.torchscript').cuda().eval()

print('Load Image')
image = torchvision.io.read_image('input/default/Image0001.png').cuda()

print('Run')
with torch.inference_mode(), torch.device('cuda'):

   #pred = model.detect_smpl_batched(frame_batch)
   #cano_all = torch.tensor(np.concatenate([cano_verts, cano_joints], axis=0 ), dtype=torch.float32)
   tcano_all = torch.tensor(cano_all, dtype=torch.float32)
   weights = model.get_weights_for_canonical_points(tcano_all)
   
   pred = model. detect_poses(image,weights)


#convert to CPU numpy ??
print(pred)
p3d = pred['poses3d'][0].numpy(force=True)
#print(p3d)
T1,T2 = torch.split(pred['poses3d'][0], [num_verts,24],dim=-2)

#print('T1',T1)
#print('T2',T2)

vertices = T1.numpy(force=True)
joints   = T2.numpy(force=True)

#swap y z 
poses3d = vertices
poses3d[..., 1], poses3d[..., 2] = poses3d[..., 2], -poses3d[..., 1]
poses3d = joints
poses3d[..., 1], poses3d[..., 2] = poses3d[..., 2], -poses3d[..., 1]

print('vertices',vertices)            
print('joints',joints)            

#print(pred['poses3d'][0][0].numpy(force=True))
#print(pred)

