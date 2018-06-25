import matplotlib.pyplot as plt
import numpy as np
import time as time
from sklearn.cluster import KMeans
import CATHUtilities as util
import Config as cfg

def kmeansFunc(n):
    print(n)

    st = time.time()

    algorithm = 'kmeans'

    structure = cfg.structure

    measure1 = cfg.measure1
    measure2 = cfg.measure2

    path = cfg.cath_results

    measure_data = util.readMeasureData(measure1,measure2,structure)
    cath_names = util.readCATHNames()
    data = util.intersectKeys(cath_names,measure_data)
    _,_,values1,values2,true_labels = util.splitCATHTuples(data)

    tmp = list(zip(values1, values2))        
    X = np.array(tmp)

    # #############################################################################
    # Clustering
    kmeans = KMeans(n_clusters=n)
    kmeans.fit(X)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    # #############################################################################
    # Measure performance
    ce = util.clusterEvaluation(X,labels,true_labels)

    # Plot results
    colors = ["r.","g.","b.","y.","c.","m.","gold","violet","sienna","dimgray"]

    for i in range(len(X)):
        plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

    plt.scatter(centroids[:,0], centroids[:,[1]], marker = "x", s=25, linewidths=5, zorder=10)

    # #############################################################################
    # Wrap up results
    util.saveCATHResults(structure, algorithm, n, data, measure1, measure2, ce)
    util.saveImage(plt, path+structure+'/', 'plot_'+structure+'_'+algorithm+'_'+str(n))
    elapsed_time = time.time() - st
    print("Elapsed time: %.2fs" % elapsed_time)

