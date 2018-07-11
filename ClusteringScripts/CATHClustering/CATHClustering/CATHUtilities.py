import os
import numpy as np
import datetime
from sklearn import metrics
import itertools 
from collections import OrderedDict
import Config as cfg

def getDate():
    date = datetime.datetime.now()
    return date

def readMeasureData(measure1, measure2, structure):
    print("Reading data: "+measure1+" "+measure2+" for "+structure)
    path = cfg.cath_alignments

    measure1_values = []
    measure2_values = []
    structures = []

    for filename in os.listdir(path):
        if structure+"_" in filename:
            structure2 = filename.split('_')[2]
            structures.append(structure2)
            print(filename)
            with open(path+filename) as fp: 
                    line = fp.readline()
                    while line:
                        if measure1 in line:
                            #print(line)
                            for n in line.split():
                                try:                                   
                                    measure1_values.append(float(n))
                                except ValueError:
                                    pass
                        if measure2 in line:  
                            #print(line)  
                            for n in line.split():
                                try:                                   
                                    measure2_values.append(float(n))
                                except ValueError:
                                    pass
                        line = fp.readline()

    dic = {}
    values = zip(measure1_values,measure2_values)
    dic = dict(itertools.zip_longest(structures, values))

    return dic, measure1_values, measure2_values

# read file with cath classifications and returns result as a dictionary
def readCATHNames():
    cath_names_path = "D:/Dados/cath/cath-classification-data/cath-names.txt"
    id_map = {}

    with open(cath_names_path) as fp:
        line = fp.readline()
        while line:
            if '#' not in line:
                id_map[str(line).split()[1]] = str(line).split()[0]
            line = fp.readline()   

    return(id_map)
    
# intersects the keys of both maps in order to extract entries which have
# a CATH classification    
def intersectKeys(cath_names, measure_data):
    data = {}
    for pdb_id in cath_names.keys():
        if pdb_id in measure_data.keys():
            data[pdb_id] = []
            data[pdb_id].append(pdb_id)
            data[pdb_id].append(cath_names[pdb_id])
            data[pdb_id].append(measure_data[pdb_id][0])
            data[pdb_id].append(measure_data[pdb_id][1])
            data[pdb_id].append(cath_names[pdb_id][0][0])

    return data        

# splits the intersected dictionary into lists
def splitCATHTuples(data):
    pdb = []
    cath = []
    measure1 = []
    measure2 = []
    true_labels = []

    for pdb_id in data.keys():
        pdb.append(data[pdb_id][0])
        cath.append(data[pdb_id][1])
        measure1.append(data[pdb_id][2])
        measure2.append(data[pdb_id][3])
        true_labels.append(str(data[pdb_id][1].split('.')[3]))   

    return pdb, cath, measure1, measure2, true_labels    

def getClassificationsNumber(true_labels):
    unique_labels = set(true_labels)
    return len(unique_labels)

def saveCATHResults(structure, algorithm, parameters, data, measure1, measure2, metrics):
    #date = str(getDate()).replace(':','-')

    data2 = OrderedDict(sorted(data.items(), key=lambda x: x[0]))

    #path = 'D:/Dados/cath/clustering_results/'+structure+'_'+measure1+'_'+measure2+'/'
    path = cfg.cath_results+structure+'/'
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path+structure+'_'+measure1+'_'+measure2+'_'+algorithm+'_'+str(parameters)+'.txt', 'w') as file:
        file.write('# ####################################################\n')
        file.write('Structure: '+structure+'\n')
        file.write('\n')
        file.write('# ####################################################\n')
        file.write('Algorithm: '+algorithm+'\n')
        file.write('\n')
        file.write('# ####################################################\n')
        file.write('Parameters: '+str(parameters).replace('_',' ')+'\n')
        file.write('\n')
        file.write('# ####################################################\n')
        file.write('Measures: '+measure1+' '+measure2+'\n')
        file.write('\n')
        file.write('# ####################################################\n')
        file.write('# Cluster evaluation: \n')
        file.write('Homogeneity: %0.3f \n' % metrics[0])
        file.write('Completeness: %0.3f \n' % metrics[1])
        file.write('V-measure: %0.3f \n' % metrics[2])
        file.write('Adjusted Rand Index: %0.3f \n' % metrics[3])
        file.write('Adjusted Mutual Information: %0.3f \n' % metrics[4])
        file.write('Silhouette coefficient: %0.3f \n' % metrics[5])
        file.write('\n')
        file.write('# ####################################################\n')
        file.write('# pdb | cath | '+measure1+' | '+measure2+' | label\n')
        for value in data2.values():
            file.write('{}\n'.format(value))

def clusterEvaluation(X, labels, labels_true):
    values = []
    homogeneity = metrics.homogeneity_score(labels_true, labels)
    completeness = metrics.completeness_score(labels_true, labels)
    v_measure = metrics.v_measure_score(labels_true, labels)
    ari = metrics.adjusted_rand_score(labels_true, labels)
    ami = metrics.adjusted_mutual_info_score(labels_true, labels)
    silhouette = metrics.silhouette_score(X, labels, metric='sqeuclidean')
    values.append(homogeneity)
    values.append(completeness)
    values.append(v_measure)
    values.append(ari)
    values.append(ami)
    values.append(silhouette)
    return values
                
def saveImage(plt, path, name):
    plt.savefig(path+name+'.png',bbox_inches='tight')
    plt.clf() # Clear figure
    plt.cla() # Clear axis
    plt.close() # Close a figure window