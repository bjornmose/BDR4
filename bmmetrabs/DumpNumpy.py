#!/usr/bin/env python3
import numpy as np

# Replace 'path_to_your_file.pkl' with the actual path to your PKL file
#file_path = '/home/jenscave/sambashare/nlf_data_files/skeleton_types_huge8.pkl'
#file_path = '/home/jenscave/sambashare/nlf_data_files/canonical_nodes3.npy'
#file_path = '/home/jenscave/Documents/Bdr_Root/NLF_Extra/SMPL_N/posedirs.npy'
file_path = '/home/jenscave/sambashare/nlf_data_files/canonical_verts/smpl.npy'

data = np.load(file_path)

# Now 'data' contains the deserialized Python object
print(data)
print(len(data))

