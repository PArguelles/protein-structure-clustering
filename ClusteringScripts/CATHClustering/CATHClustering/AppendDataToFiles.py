import numpy as np
import matplotlib.pyplot as plt
import os
import re
import CATHUtilities as util
import Config as cfg

#structures = ['1c4zA02','1xfjA00','2asfA00','2evvA00','2vxzA01','3bfmA01','3bpkA01','3hisA02','4kp1A01']

# append cluster evaluation to the end of the file

path_to_results = "D:/Dados/cath/clustering_results/"
path_to_tables = "D:/Dados/cath/dompdb_tmscore_table/table_"

algorithm = "fcm"

labels = []

values1 = []
values2 = []
labels = []

for folder in os.listdir(path_to_results):
    current_folder = path_to_results+folder
    for filename in os.listdir(current_folder):
        # ################################################
        # Go through each file that contains fcm results
        print(filename)
        if "plot" not in filename and algorithm in filename:
            parsed = str(filename).split("_")
            structure = parsed[0]
            measure1 = parsed[1]
            measure2 = parsed[2]
              

print(values1)
print(values2)
print(labels)
