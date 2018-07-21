import AgglomerativeScript as agg
import KMeansScript as km
import SCOPUtilities as util
import numpy as np
import Config as cfg
import time as time

st = time.time()

measures = ['RMSD','GDT-HA','GDT-TS','TM-score','MaxSub']

measures_copy = measures
visited = []
combinations = set()

#structures = ['1iym','1o77','1yd7','2bjg','2j0k','3o88']
structures = ['1yd7','2bjg','2j0k','3o88']

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

        print(structure)
        print(measure1)
        print(measure2)

        measure_data,_,_ = util.readMeasureData(measure1,measure2,structure)
        scop_names = util.readSCOPNames()
        data = util.intersectSCOPKeys(scop_names,measure_data)
        _,values1,values2,true_labels = util.splitSCOPTuples(data)

        agg.agglo(structure, measure1, measure2, values1, values2, data, true_labels)
        km.kmeansFunc(structure, measure1, measure2, values1, values2, data, true_labels)
        current_combo += 1
        
    current_combo = 0
    current_structure += 1    
    
elapsed_time = time.time() - st
print("Total time: %.2fs" % elapsed_time)    