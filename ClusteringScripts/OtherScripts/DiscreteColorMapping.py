import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import CATHUtilities as util
import Config as cfg

structure = "1c4zA02"

measure1 = "RMSD"
measure2 = 'MaxSub'

path = cfg.cath_results

measure_data = util.readMeasureData(measure1,measure2,structure)
cath_names = util.readCATHNames()
data = util.intersectKeys(cath_names,measure_data)
_,_,values1,values2,true_labels = util.splitCATHTuples(data)

tmp = list(zip(values1, values2))        
X = np.array(tmp)

N = 4 # Number of labels

kmeans = KMeans(n_clusters=N)
kmeans.fit(X)

centroids = kmeans.cluster_centers_
labels = kmeans.labels_


# setup the plot
fig, ax = plt.subplots(1,1, figsize=(6,6))

# define the colormap
cmap = plt.cm.get_cmap('jet')
# extract all colors from the .jet map
cmaplist = [cmap(i) for i in range(cmap.N)]
# create the new map
cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

# define the bins and normalize
bounds = np.linspace(0,N,N+1)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# make the scatter
for i in range(len(X)):
    scat = ax.scatter(X[i][0],X[i][1],c=labels[i],s=20,cmap=cmap,     norm=norm)
# create the colorbar
cb = plt.colorbar(scat, spacing='proportional',ticks=bounds)
cb.set_label('Custom cbar')
ax.set_title('Discrete color mappings')

ax.set_ylim(ymin=0)
ax.set_xlim(xmin=0)

plt.show()
