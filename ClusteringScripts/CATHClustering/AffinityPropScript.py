import matplotlib.pyplot as plt
import numpy as np
import time as time
import CATHUtilities as util
from sklearn.cluster import AffinityPropagation
from itertools import cycle
import Config as cfg

def affinityProp():

    st = time.time()

    algorithm = 'afp'

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
    # Compute Affinity Propagation
    af = AffinityPropagation().fit(X)
    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_
    n_clusters_ = len(cluster_centers_indices)

    # #############################################################################
    # Measure performance
    ce = util.clusterEvaluation(X,labels,true_labels)

    # #############################################################################
    # Plot result
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

    # #############################################################################
    # Wrap up results
    n = 'none'
    util.saveCATHResults(structure, algorithm, n, data, measure1, measure2, ce)
    util.saveImage(plt, path+structure+'/', 'plot_'+structure+'_'+cfg.measure1+'_'+cfg.measure2+'_'+algorithm+'_'+str(n))
    

    elapsed_time = time.time() - st
    print("Elapsed time: %.2fs" % elapsed_time)