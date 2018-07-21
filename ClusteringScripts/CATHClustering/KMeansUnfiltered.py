import os
import CATHUtilities as util
import AffinityPropScript as ap
import KMeansScript as km
import DBSCANScript as dbs
import AgglomerativeScript as agg
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import Config as cfg
import numpy as np
from sklearn.cluster import DBSCAN

def kmeansFunc():

    algorithm = 'kmeans'

    measure1 = 'RMSD'
    measure2 = 'MaxSub'
    structure = '1c4zA02'

    measure_data, v1, v2 = util.readMeasureData(measure1,measure2,structure)
    cath_names = util.readCATHNames()
    data = util.intersectKeys(cath_names,measure_data)
    _,_,values1,values2,true_labels = util.splitCATHTuples(data)

    path = cfg.cath_results

    tmp = list(zip(v1, v2))        
    X = np.array(tmp)

    for n in (3,40,80,101):
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
            #ce = util.clusterEvaluation(X,labels,true_labels)

            # Plot results
            colors = ["r.","g.","b.","y.","c.","m.","r.","g.","b.","y."]

            plt.xlabel(measure1)
            plt.ylabel(measure2)
            plt.title("K-means: "+str(n)+" clusters")

            for i in range(len(X)):
                plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

            plt.scatter(centroids[:,0], centroids[:,[1]], marker = "x", s=25, linewidths=5, zorder=10)

            plt.show()

            # #############################################################################
            # Wrap up results
            #util.saveCATHResults(structure, algorithm, n, data, measure1, measure2, ce)
            #util.saveImage(plt, path+structure+'/', 'plot_'+structure+'_'+measure1+'_'+measure2+'_'+algorithm+'_'+str(n))
        except Exception:
            pass    

kmeansFunc()

