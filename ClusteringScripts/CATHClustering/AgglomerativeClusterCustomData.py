import time
import matplotlib.pyplot as plt
import numpy as np
import os

from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph

path = "D:/Dados/tmscore_parsed_results/"
structure1 = "140l.ent_"

rmsd = []
tmscore = []
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
        
tmp = list(zip(rmsd, maxsub))        
X = np.array(tmp)

print(X)
# Create a graph capturing local connectivity. Larger number of neighbors
# will give more homogeneous clusters to the cost of computation
# time. A very large number of neighbors gives more evenly distributed
# cluster sizes, but may not impose the local manifold structure of
# the data
knn_graph = kneighbors_graph(X, 10, include_self=False)

for connectivity in (None, knn_graph):
    for n_clusters in (10, 3):
        plt.figure(figsize=(10, 4))
        for index, linkage in enumerate(('average', 'complete', 'ward')):
            plt.subplot(1, 3, index + 1)
            model = AgglomerativeClustering(linkage=linkage,
                                            connectivity=connectivity,
                                            n_clusters=n_clusters)
            t0 = time.time()
            model.fit(X)
            elapsed_time = time.time() - t0
            plt.scatter(X[:, 0], X[:, 1], c=model.labels_,
                        cmap='nipy_spectral')
            plt.title('linkage=%s (time %.2fs)' % (linkage, elapsed_time),
                      fontdict=dict(verticalalignment='top'))

            plt.axis('on')

            plt.subplots_adjust(bottom=0, top=.89, wspace=0,
                                left=0, right=1)
            plt.suptitle('n_cluster=%i, connectivity=%r' %
                         (n_clusters, connectivity is not None), size=17)

plt.show()