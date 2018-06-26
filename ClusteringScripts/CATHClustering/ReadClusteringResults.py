import numpy as np
import matplotlib.pyplot as plt
import os
import re
import CATHUtilities as util
import Config as cfg

path_to_results = cfg.cath_results

structure = cfg.structure_to_summarize
algorithm = cfg.algorithm_to_summarize

data = []
#todo: rmsd rmsd....
labels = [] 
values = []

counter = 0
reference_value = 0

for folder in os.listdir(path_to_results):
    if structure in folder:
        path_to_results = path_to_results+folder+'/'
        for filename in os.listdir(path_to_results):
            if 'plot_' not in filename and algorithm in filename:
                parsed = filename.split('_')
                measure1 = parsed[1]
                measure2 = parsed[2]
                #label = measure1+' '+measure2+' '+algorithm
                label = measure1+' '+measure2
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
                if 'RMSD_RMSD' in filename:
                    reference_value = counter
                else: counter += 1


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

ref = reference_value+1
#Color matrix
for i,j in the_table._cells:
    if i > 0 and j > -1:
        if i == ref:
            the_table._cells[(i, j)]._text.set_color('black')
        else:    
            if float(the_table._cells[(i, j)]._text.get_text()) > float(the_table._cells[(ref, j)]._text.get_text()):
                the_table._cells[(i, j)]._text.set_color('green')
            if float(the_table._cells[(i, j)]._text.get_text()) == float(the_table._cells[(ref, j)]._text.get_text()):
                the_table._cells[(i, j)]._text.set_color('black')
            if float(the_table._cells[(i, j)]._text.get_text()) < float(the_table._cells[(ref, j)]._text.get_text()):
                the_table._cells[(i, j)]._text.set_color('red')
    
util.saveImage(plt, path_to_results, 'table_'+structure)

plt.title('Algorithm performance: '+algorithm)
plt.show()