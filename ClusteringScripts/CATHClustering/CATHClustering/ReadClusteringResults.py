import numpy as np
import matplotlib.pyplot as plt
import os
import re
import CATHUtilities as util
import Config as cfg

path_to_results = cfg.cath_results

structure = cfg.structure

algorithm = cfg.algorithm_to_summarize

data = []
#todo: rmsd rmsd....
labels = [] 
values = []

for folder in os.listdir(path_to_results):
    if structure in folder:
        path_to_results = path_to_results+folder+'/'
        for filename in os.listdir(path_to_results):
            if 'plot_' not in filename:
                parsed = filename.split('_')
                measure1 = parsed[1]
                measure2 = parsed[2]
                label = measure1+''+measure2
                labels.append(label)
                with open(path_to_results+filename,'r') as fp:
                    line = fp.readline()
                    while line:
                        if 'Cluster evaluation' in line:
                            i = 0
                            while i < 6:
                                line = fp.readline()
                                num = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)]
                                values.append(num[0])
                                i += 1
                                print(line)   
                        line = fp.readline()
                    data.append(values)
                    values = []  


print(measure1)
print(measure2)
print(data)
print(labels)

columns = ('Homogeneity', 'Completeness', 'V-measure', 'ARI', 'AMI', 'Silhouette')
rows = labels

plt.axis('off')

# Add a table at the bottom of the axes
the_table = plt.table(cellText=data,
                      rowLabels=rows,
                      rowColours=None,
                      colLabels=columns,
                      cellLoc='center',
                      loc='center')

util.saveImage(plt, path_to_results, 'plot_table_'+structure)

plt.show()