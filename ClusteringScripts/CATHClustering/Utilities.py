import os
import numpy as np

def readMeasureData(measure1, measure2, structure):
    print("Reading data: "+measure1+" "+measure2+" for "+structure)
    #path = "D:/Dados/tmscore_parsed_results/"
    path = "D:/Dados/cath/dompdb_tmscore_parsed/"
    values1 = []
    values2 = []

    for filename in os.listdir(path):
        if structure in filename:
            #print(path+filename)
            with open(path+filename) as fp: 
                    line = fp.readline()
                    while line:
                        if measure1 in line:
                            for n in line.split():
                                try:
                                    values1.append(float(n))
                                except ValueError:
                                    pass
                        if measure2 in line:    
                            for n in line.split():
                                try:
                                    values2.append(float(n))
                                except ValueError:
                                    pass
                        line = fp.readline()
    tmp = list(zip(values1, values2))        
    X = np.array(tmp)
    return X

def readMeasureDataV2(measure1, measure2, structure):
    print("Reading data V2: "+measure1+" "+measure2+" for "+structure)
    #path = "D:/Dados/tmscore_parsed_results/"
    path = "D:/Dados/cath/dompdb_tmscore_parsed/"
    ids = []
    values1 = []
    values2 = []

    for filename in os.listdir(path):
        if structure+"_" in filename:
            #print(path)
            #print(filename)
            structure2 = filename.split('_')[2]
            print(structure2)
            ids.append(str(structure2))
            with open(path+filename) as fp: 
                    line = fp.readline()
                    while line:
                        if measure1 in line:
                            for n in line.split():
                                try:
                                    values1.append(float(n))
                                except ValueError:
                                    pass
                        if measure2 in line:    
                            for n in line.split():
                                try:
                                    values2.append(float(n))
                                except ValueError:
                                    pass
                        line = fp.readline()
    
    tmp = list(zip(ids, values1, values2))        
    X = np.array(tmp)
    print(X)
    return X    

def testClassification():
    cath_names_path = "D:/Dados/cath/cath-classification-data/cath-names.txt"
    id_map = {}

    structure = "1a1vA03" 

    with open(cath_names_path) as fp:
        line = fp.readline()
        while line:
            if structure in line:
                print(line)
            line = fp.readline()   

    print(str(id_map[structure]).split('.')[0])
    print(str(id_map[structure]).split('.')[1])
    print(str(id_map[structure]).split('.')[2])
    print(str(id_map[structure]).split('.')[3])

def getDomainClassificationV2():
    cath_names_path = "D:/Dados/cath/cath-classification-data/cath-names.txt"
    id_map = {}

    structure = "4e6uA02" 

    with open(cath_names_path) as fp:
        line = fp.readline()
        while line:
            if '#' not in line:
                id_map[str(line).split()[1]] = str(line).split()[0]
            line = fp.readline()   

    #print(str(id_map[structure]).split('.')[0])
    #print(str(id_map[structure]).split('.')[1])
    #print(str(id_map[structure]).split('.')[2])
    #print(str(id_map[structure]).split('.')[3])
    return(id_map)

    

