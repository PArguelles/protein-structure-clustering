import numpy as np
import CATHUtilities as util
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering

def plot_dendrogram(model, **kwargs):

    # Children of hierarchical clustering
    children = model.children_

    # Distances between each pair of children
    # Since we don't have this information, we can use a uniform one for plotting
    distance = np.arange(children.shape[0])

    # The number of observations contained in each cluster level
    no_of_observations = np.arange(2, children.shape[0]+2)

    # Create linkage matrix and then plot the dendrogram
    linkage_matrix = np.column_stack([children, distance, no_of_observations]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

measure1 = 'RMSD'
measure2 = 'MaxSub'
structure = '1c4zA02'

measure_data,_,_ = util.readMeasureData(measure1,measure2,structure)
cath_names = util.readCATHNames()
data = util.intersectKeys(cath_names,measure_data)
_,_,values1,values2,true_labels = util.splitCATHTuples(data)
n_clusters = util.getClassificationsNumber(true_labels)

tmp = list(zip(values1, values2))        
X = np.array(tmp)

model = AgglomerativeClustering(n_clusters=n_clusters)

model = model.fit(X)

plt.title('Hierarchical Clustering Dendrogram')
plot_dendrogram(model, labels=model.labels_)
plt.show()