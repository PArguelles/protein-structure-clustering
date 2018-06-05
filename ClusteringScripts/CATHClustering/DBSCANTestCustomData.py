import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import time as time
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

path = "D:/Dados/tmscore_parsed_results/"
structure1 = "140l.ent_"

st = time.time()

# #############################################################################
# Read files
rmsd = []
maxsub = []

index = 0

print("Reading files")
for filename in os.listdir(path):
    if structure1 in filename:
        with open(path+filename) as fp: 
                #print(filename)
                line = fp.readline()
                index += 1   
                while line:
                    if "MaxSub" in line:
                        for n in line.split():
                            try:
                                maxsub.append(float(n))
                            except ValueError:
                                pass
                        #print(str(index)+": "+line) 
                    if "RMSD" in line:    
                        for n in line.split():
                            try:
                                rmsd.append(float(n))
                            except ValueError:
                                pass
                        #print(str(index)+": "+line) 
                    line = fp.readline()
        
tmp = list(zip(rmsd, maxsub))        
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



