import matplotlib.pyplot as plt
import numpy as np
import time as time
import CASP12Utilities as util

from sklearn.cluster import KMeans

def kmeansFunc(structure, measure1, measure2, values1, values2):

    algorithm = 'km'
    
    path = "D:/Dados/casp12/clustering_results/"

    tmp = list(zip(values1, values2))        
    X = np.array(tmp)

    print(X)

    for n in (3, 4, 5, 6, 7, 8):
        try:
            # #############################################################################
            # Clustering
            print("K-Means: "+str(n))
            kmeans = KMeans(n_clusters=n)
            kmeans.fit(X)

            centroids = kmeans.cluster_centers_
            labels = kmeans.labels_

            # #############################################################################
            # Measure performance
            ce = util.clusterEvaluationNoLabels(X,labels)

            # Plot results
            colors = ["r.","g.","b.","y.","c.","m.","r.","g.","b.","y."]

            plt.xlabel(measure1)
            plt.ylabel(measure2)
            
            plt.title("K-means: "+str(n)+" clusters")

            for i in range(len(X)):
                plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

            plt.scatter(centroids[:,0], centroids[:,[1]], marker = "x", s=25, linewidths=5, zorder=10)

            # #############################################################################
            # Wrap up results
            util.saveCASPResults(structure, algorithm, n, measure1, measure2, ce)
            util.saveImage(plt, path+structure+'/', 'plot_'+structure+'_'+measure1+'_'+measure2+'_'+algorithm+'_'+str(n))
        except Exception:
            pass    
