import os
import numpy as np
import datetime
from sklearn import metrics
from collections import OrderedDict

def getDate():
    date = datetime.datetime.now()
    return date

def readMeasureData(measure1, measure2, structure):
    print("Reading data V3: "+measure1+" "+measure2+" for "+structure)
    path = "D:/Dados/cath/dompdb_tmscore_parsed/"
    
    dic = {}

    for filename in os.listdir(path):
        if structure+"_" in filename:
            structure2 = filename.split('_')[2]
            dic[str(structure2)] = []
            with open(path+filename) as fp: 
                    line = fp.readline()
                    while line:
                        if measure1 in line:
                            for n in line.split():
                                try:
                                    dic[str(structure2)].append(float(n))
                                except ValueError:
                                    pass
                        if measure2 in line:    
                            for n in line.split():
                                try:
                                    dic[str(structure2)].append(float(n))
                                except ValueError:
                                    pass
                        line = fp.readline()
    #print(dic)
    print(len(dic))
    return dic

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

    print(len(data))
    return data        

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
        true_labels.append(data[pdb_id][1][0])   

    return pdb, cath, measure1, measure2, true_labels    

def saveCATHResults(data, measure1, measure2):
    date = str(getDate()).replace(':','.')

    data2 = OrderedDict(sorted(data.items(), key=lambda x: x[0]))

    with open('D:/Dados/'+date+'_test.txt', 'w') as file:
        file.write('# ####################################################\n')
        file.write('# Performance: \n')
        file.write('Homogeneity: \n')
        file.write('Completeness: \n')
        file.write('V-measure: \n')
        file.write('Adjusted Rand Index: \n')
        file.write('Adjusted Mutual Information: \n')
        file.write('Silhouette coefficient: \n')
        file.write('# ####################################################\n')
        file.write('# pdb | cath | '+str(measure1).upper+' | '+str(measure2).upper+' | label | truth\n')
        for value in data2.values():
            file.write('{}\n'.format(value))

def clusterEvaluation(X, labels, labels_true):
    homogeneity = metrics.homogeneity_score(labels_true, labels)
    completeness = metrics.completeness_score(labels_true, labels)
    v_measure = metrics.v_measure_score(labels_true, labels)
    ari = metrics.adjusted_rand_score(labels_true, labels)
    ami = metrics.adjusted_mutual_info_score(labels_true, labels)
    silhouette = metrics.silhouette_score(X, labels, metric='sqeuclidean')
    print("Homogeneity: %0.3f" % homogeneity)
    print("Completeness: %0.3f" % completeness)
    print("V-measure: %0.3f" % v_measure)
    print("Adjusted Rand Index: %0.3f" % ari)
    print("Adjusted Mutual Information: %0.3f" % ami)
    print("Silhouette Coefficient: %0.3f" % silhouette)
                
