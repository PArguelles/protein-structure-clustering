from sklearn.cluster import AffinityPropagation
from sklearn import metrics
import numpy as np
import os
import CATHUtilities as util

domain = "1c4zA02"
measure1 = "RMSD"
measure2 = "MaxSub"

measure_data = util.readMeasureData(measure1,measure2,domain)

cath_names = util.readCATHNames()

data = util.intersectKeys(cath_names,measure_data)

pdb_ids,cath_names,values1,values2,true_labels = util.splitCATHTuples(data)

tmp = list(zip(values1, values2))        
X = np.array(tmp)

# #############################################################################
# Compute Affinity Propagation
af = AffinityPropagation().fit(X)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)

# #############################################################################
# Plot result
import matplotlib.pyplot as plt
from itertools import cycle

plt.close('all')
plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    class_members = labels == k
    cluster_center = X[cluster_centers_indices[k]]
    plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=5)
    for x in X[class_members]:
        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()