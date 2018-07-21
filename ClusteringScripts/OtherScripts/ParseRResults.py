import numpy as np
import matplotlib.pyplot as plt
import os
import re
import CATHUtilities as util
import Config as cfg

#structures = ['1c4zA02','1xfjA00','2asfA00','2evvA00','2vxzA01','3bfmA01','3bpkA01','3hisA02','4kp1A01']

# append cluster evaluation to the end of the file

path_to_results = "D:/Dados/cath/clustering_results/"

algorithm = "fcm"

labels = []

for folder in os.listdir(path_to_results):
    current_folder = path_to_results+folder
    for filename in os.listdir(current_folder):
        structure = filename.split('_')[0]
        
        print(filename)
        if "plot_" not in filename and structure in filename and algorithm in filename:
        
            with open(path_to_results+filename,'r') as fp:
                        line = fp.readline()
                        while line:
                            if "$cluster" in line:
                                line = fp.readline()
                                while "[" in line:
                                    line = str(line).rstrip()
                                    values = line.split(" ")
                                    for v in values[2:]:
                                        labels.append(v)
                                    line = fp.readline()

                            line = fp.readline()

for item in labels:
    if "[" in item: 
        labels.remove(item)

print(labels)
       