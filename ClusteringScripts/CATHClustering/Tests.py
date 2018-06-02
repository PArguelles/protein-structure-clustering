import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
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

print("Reading files")
for filename in os.listdir(path):
    if structure1 in filename:
        with open(path+filename) as fp: 
                #print(filename)
                line = fp.readline()
                index += 1   
                while line:
                    if "MaxSub" in line:
                        for n in line.split():
                            try:
                                maxsub.append(float(n))
                            except ValueError:
                                pass
                        #print(str(index)+": "+line) 
                    if "RMSD" in line:    
                        for n in line.split():
                            try:
                                rmsd.append(float(n))
                            except ValueError:
                                pass
                        #print(str(index)+": "+line) 
                    line = fp.readline()
        
tmp = list(zip(rmsd, maxsub))        
X = np.array(tmp)


# #############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
labels = db.labels_

X = np.c_[X,labels]

N = len(set(labels)) - (1 if -1 in labels else 0)

print(labels)
print(X)
print(N)

tag = np.random.randint(0,N,20)
fig, ax = plt.subplots(1,1, figsize=(6,6))
# define the colormap
cmap = plt.cm.get_cmap('Spectral')
# extract all colors from the .jet map
cmaplist = [cmap(i) for i in range(cmap.N)]
# create the new map
cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

# define the bins and normalize
bounds = np.linspace(0,N,N+1)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# make the scatter
count1 = 0
count2 = 0
index = 0
    ax.scatter(X[:,0],X[:,1],c=labels,s=20,cmap=cmap,norm=norm)
    count1 += 1
#scat = ax.scatter(X[:,0],X[:,1],tag=,s=20,cmap=cmap,norm=norm)
#ax.scatter([1,2],[1,2],s=10,c='k')
# create the colorbar
print(count1)
print(count2)
ax.set_title('Discrete color mappings')
plt.show()

 
