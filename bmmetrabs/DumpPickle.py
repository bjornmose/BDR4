#!/usr/bin/env python3
import pickle

# Replace 'path_to_your_file.pkl' with the actual path to your PKL file
#file_path = '/home/jenscave/sambashare/nlf_data_files/skeleton_types_huge8.pkl'
#file_path = '/home/jenscave/sambashare/nlf_data_files/joint_info_866.pkl'
file_path = '/home/jenscave/Downloads/basicmodel_neutral_lbs_10_207_0_v1.1.0.pkl'

# Open the file in binary mode and load the data
with open(file_path, 'rb') as file:
    data = pickle.load(file)
#data = pickle.load(file_path)

# Now 'data' contains the deserialized Python object
print(data)

