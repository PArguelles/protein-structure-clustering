import matplotlib.pyplot as plt
import os
import numpy as np
import time as time
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans
from sklearn import metrics

path = "D:/Dados/tmscore_parsed_results/"
structure1 = "140l.ent_"

st = time.time()

# #############################################################################
# Read files
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
        
# #############################################################################
# Pre-process data
print(rmsd)
#rmsd = scale(rmsd)
print(rmsd)

tmp = list(zip(rmsd, maxsub))        
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
    print("coordinate:",X[i], "label:", labels[i])
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

plt.scatter(centroids[:,0], centroids[:,[1]], marker = "x", s=150, linewidths=5, zorder=10)
plt.show()

# #############################################################################
# Wrap up results
elapsed_time = time.time() - st
print("Elapsed time: %.2fs" % elapsed_time)
print(X)
