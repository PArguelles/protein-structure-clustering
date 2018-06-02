
import GetDiscreteColorMap as cmap
import numpy as np
import matplotlib.pyplot as plt
import os
import time as time

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

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
        
tmp = list(zip(rmsd, maxsub))        
X = np.array(tmp)

dbscan = DBSCAN(eps = 0.1, min_samples = 5)
dbscan.fit(X)

labels = dbscan.labels_


# Black removed and is used for noise instead.

N=13

x = np.random.randn(40)
y = np.random.randn(40)
c = np.random.randint(N, size=40)

    # Edit: don't use the default ('jet') because it makes @mwaskom mad...
plt.scatter(x, y, c=c, s=50, cmap=cmap.discrete_cmap(N, 'hsv'))
#plt.plot([1,2,3,4], [1,2,3,4], markersize=20, c='0F0F0F')

plt.colorbar(ticks=range(N))
plt.clim(-0.5, N - 0.5)
plt.show()


