import matplotlib.pyplot as plt
import os
import numpy as np
import time as time
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans
from sklearn import metrics

def readData():
    path = "D:/Dados/tmscore_parsed_results/"
    structure1 = "140l.ent_"
    rmsd = []
    maxsub = []

    index = 0

    for filename in os.listdir(path):
        if structure1 in filename:
            with open(path+filename) as fp: 
                    print(filename)
                    line = fp.readline()
                    index += 1   
                    while line:
                        if "MaxSub" in line:
                            for n in line.split():
                                try:
                                    maxsub.append(float(n))
                                except ValueError:
                                    pass
                            print(str(index)+": "+line) 
                        if "RMSD" in line:    
                            for n in line.split():
                                try:
                                    rmsd.append(float(n))
                                except ValueError:
                                    pass
                            print(str(index)+": "+line) 
                        line = fp.readline()
    tmp = list(zip(rmsd, maxsub))        
    X = np.array(tmp)
    return X

def getDomainClassification():
    cath_names_path = "D:/Dados/cath/cath-classification-data/cath-names.txt"
    id_map = {}

    structure = "4gv5A00" 

    with open(cath_names_path) as fp:
        line = fp.readline()
        while line:
            if '#' not in line:
                id_map[str(line).split()[1]] = str(line).split()[0]
            line = fp.readline()   

    print(str(id_map[structure]).split('.')[0])
    print(str(id_map[structure]).split('.')[1])
    print(str(id_map[structure]).split('.')[2])
    print(str(id_map[structure]).split('.')[3])
