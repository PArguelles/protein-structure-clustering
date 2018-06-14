import matplotlib.pyplot as plt
import os
import numpy as np
import time as time
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans
from sklearn import metrics
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
# Clustering
kmeans = KMeans(n_clusters=6)
kmeans.fit(X)

centroids = kmeans.cluster_centers_
labels = kmeans.labels_

print(centroids)
print(labels)

# #############################################################################
# Measure performance
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))
print("Calinski-Harabaz score: %0.3f" % metrics.calinski_harabaz_score(X, labels))
#print("ARS: %0.3f" % metrics.adjusted_rand_score(labels_true, labels) )
# #############################################################################

# Plot results
colors = ["r.","g.","b.","y.","c.","m."]

for i in range(len(X)):
    #print("coordinate:",X[i], "label:", labels[i])
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

plt.scatter(centroids[:,0], centroids[:,[1]], marker = "x", s=150, linewidths=5, zorder=10)
plt.show()

# #############################################################################
# Wrap up results
elapsed_time = time.time() - st
print("Elapsed time: %.2fs" % elapsed_time)
print(X)
