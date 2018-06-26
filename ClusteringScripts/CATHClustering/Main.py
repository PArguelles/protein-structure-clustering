import AffinityPropScript as ap
import KMeansScript as km
import DBSCANScript as dbs
import Config as cfg
import CATHUtilities as util
import numpy as np

#aff = [ap.affinityProp()]
#kmeans = [km.kmeansFunc(2),km.kmeansFunc(4),km.kmeansFunc(6)]
#dbscan = [dbs.dbscanFunc()]

measures = ['GDT-HA','GDT-TS','MaxSub','RMSD','TM-score']
measures_copy = measures
visited = []
combinations = set()

x = 0
y = 0
while x < len(measures):
    while y < len(measures_copy):
        if measures_copy[y] not in visited:
            line = measures[x]+' '+measures_copy[y]
            print(line)
            combinations.add(line)
        y += 1 
    visited.append(measures[x])      
    x += 1         
    y = 0
    
combinations = list(combinations)

print(combinations)    

current_combo = 0
while current_combo < len(combinations):
    parsed = combinations[current_combo].split(' ')
    cfg.measure1 = parsed[0]
    cfg.measure2 = parsed[1]

    kmeans_limit = 10
    i = 2
    interval = 4
    while i < kmeans_limit:
        km.kmeansFunc(i)
        i += interval
    i = 0

    #ap.affinityProp()
    current_combo += 1
    