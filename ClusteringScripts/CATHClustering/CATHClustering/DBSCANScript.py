import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import time as time
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import CATHUtilities as util

st = time.time()

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
# Compute DBSCAN
db = DBSCAN(eps=0.4, min_samples=20).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

# #############################################################################
# Plot result
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=5)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=5)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()



