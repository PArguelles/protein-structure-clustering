from sklearn.neighbors import NearestNeighbors
import numpy as np
import os
import CATHUtilities as util
from sklearn.neighbors import kneighbors_graph
import matplotlib.pyplot as plt

domain = "1c4zA02"
measure1 = "RMSD"
measure2 = "MaxSub"

measure_data = util.readMeasureData(measure1,measure2,domain)

cath_names = util.readCATHNames()

data = util.intersectKeys(cath_names,measure_data)

pdb_ids,cath_names,values1,values2,true_labels = util.splitCATHTuples(data)

tmp = list(zip(values1, values2))        
X = np.array(tmp)

nbrs = NearestNeighbors(n_neighbors=20, algorithm='ball_tree').fit(X)

distances, indices = nbrs.kneighbors(X)

print("Distances")
print(distances)

print("Indices")
print(indices)

print(nbrs.kneighbors_graph(X).toarray())

#knn_graph = kneighbors_graph(X, 10, include_self=False)

#plt.scatter(X[:, 0], X[:, 1], c=nbrs.labels_,cmap='nipy_spectral')
         

#plt.show()