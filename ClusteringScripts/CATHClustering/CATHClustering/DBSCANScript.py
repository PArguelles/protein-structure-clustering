import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time as time
from sklearn.cluster import DBSCAN
import CATHUtilities as util
import Config as cfg

def dbscanFunc(structure, measure1, measure2, values1, values2, data, true_labels):

    algorithm = 'dbs'

    path = cfg.cath_results

    tmp = list(zip(values1, values2))        
    X = np.array(tmp)
                       
    # #############################################################################
    # Compute DBSCAN
    #0.6 1, 
    eps = 0.6 
    min_samples = 2
    db = DBSCAN(eps=0.6, min_samples=2).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    # #############################################################################
    # Measure performance
    ce = util.clusterEvaluation(X,labels,true_labels)

    # #############################################################################
    # Plot result
        
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
    #plt.show()

    # #############################################################################
    # Wrap up results
    n = str(eps)+'_'+str(min_samples)
    util.saveCATHResults(structure, algorithm, n, data, measure1, measure2, ce)
    util.saveImage(plt, path+structure+'/', 'plot_'+structure+'_'+measure1+'_'+measure2+'_'+algorithm+'_'+str(n))

