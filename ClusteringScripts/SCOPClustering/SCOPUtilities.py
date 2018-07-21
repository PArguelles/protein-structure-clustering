import os
import numpy as np
import datetime
from sklearn import metrics
import itertools 
import Config as cfg
import random
from collections import OrderedDict

def readMeasureData(measure1, measure2, structure):
    print("Reading data: "+measure1+" "+measure2+" for "+structure)
    path = 'D:/Dados/scop/scop_tmscore_parsed/'

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

    i = 0

    values = zip(measure1_values,measure2_values)
    dic = dict(itertools.zip_longest(structures, values))

    dic = {k:v for k,v in dic.items() if v is not None}

    dic2 = {}

    while i < 1000:
        key, values = random.choice(list(dic.items()))
        dic2[key] = []
        dic2[key].append(values[0])
        dic2[key].append(values[1])

        i += 1

    dic2 = {k:v for k,v in dic2.items() if v is not None}

    return dic2, measure1_values, measure2_values

# read file with cath classifications and returns result as a dictionary
def readSCOPNames():
    scop_names_path = "D:/Dados/scop/scope/dir.cla.scope.2.07-stable.txt"
    id_map = {}

    with open(scop_names_path) as fp:
        line = fp.readline()
        while line:
            # class, fold, superfamiliy, family
            if '#' not in line:
                pdb_id = str(line).strip().split("\t")[1]
                superfamily = str(line).strip().split("\t")[3].split('.')[2]
                id_map[pdb_id] = superfamily
            line = fp.readline()   
      
    return(id_map)
    
# intersects the keys of both maps in order to extract entries which have
# a CATH classification    
def intersectSCOPKeys(scop_names, measure_data):

    measure_data = {k:v for k,v in measure_data.items() if v is not None}
    scop_names = {k:v for k,v in scop_names.items() if v is not None}
    data = {}
    for pdb_id in scop_names.keys():
        if pdb_id in measure_data.keys():
            data[pdb_id] = []
            data[pdb_id].append(pdb_id)
            data[pdb_id].append(scop_names[pdb_id])
            data[pdb_id].append(measure_data[pdb_id][0])
            data[pdb_id].append(measure_data[pdb_id][1])
            
    return data        

def splitSCOPTuples(data):
    pdb = []
    measure1 = []
    measure2 = []
    true_labels = []

    for pdb_id in data.keys():
        pdb.append(data[pdb_id][0])
        measure1.append(data[pdb_id][2])
        measure2.append(data[pdb_id][3])
        true_labels.append(data[pdb_id][1])   
        
    return pdb, measure1, measure2, true_labels    

def getClassificationsNumber(true_labels):
    unique_labels = set(true_labels)
    return len(unique_labels)

def saveCATHResults(structure, algorithm, parameters, data, measure1, measure2, metrics):
    #date = str(getDate()).replace(':','-')

    data2 = OrderedDict(sorted(data.items(), key=lambda x: x[0]))

    #path = 'D:/Dados/cath/clustering_results/'+structure+'_'+measure1+'_'+measure2+'/'
    path = 'D:/Dados/scop/clustering_results/'+structure+'/'
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path+structure+'_'+measure1+'_'+measure2+'_'+algorithm+'_'+str(parameters), 'w') as file:
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