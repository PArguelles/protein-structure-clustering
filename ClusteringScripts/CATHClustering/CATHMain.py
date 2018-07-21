import AffinityPropScript as ap
import AgglomerativeScript as agg
import KMeansScript as km
import DBSCANScript as dbs
import CATHUtilities as util
import numpy as np
import Config as cfg
import time as time

st = time.time()

measures = ['RMSD','GDT-HA','GDT-TS','TM-score','MaxSub']

measures_copy = measures
visited = []
combinations = set()

structures = ['3bpkA01','3hisA02','4kp1A01']
#'1c4zA02','1xfjA00','2asfA00','2evvA00','2vxzA01',
x = 0
y = 0
while x < len(measures):
    while y < len(measures_copy):
        if measures_copy[y] not in visited:
            line = measures[x]+' '+measures_copy[y]
            combinations.add(line)
        y += 1 
    visited.append(measures[x])      
    x += 1         
    y = 0
    
combinations = list(combinations)

#print(combinations)    

current_combo = 0
current_structure = 0

while current_structure < len(structures):
    structure = structures[current_structure]
    while current_combo < len(combinations):
        parsed = combinations[current_combo].split(' ')
        measure1 = parsed[0]
        measure2 = parsed[1]

        measure_data,_,_ = util.readMeasureData(measure1,measure2,structure)
        cath_names = util.readCATHNames()
        data = util.intersectKeys(cath_names,measure_data)
        _,_,values1,values2,true_labels = util.splitCATHTuples(data)

        agg.agglo(structure, measure1, measure2, values1, values2, data, true_labels)
        
        current_combo += 1
        
    current_combo = 0
    current_structure += 1    
    
elapsed_time = time.time() - st
print("Total time: %.2fs" % elapsed_time)    