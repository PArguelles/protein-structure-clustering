import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

N = 15 # Number of labels

# setup the plot
fig, ax = plt.subplots(1,1, figsize=(6,6))
# define the data
x = np.random.rand(20)
y = np.random.rand(20)
tag = np.random.randint(0,N,20) # Tag each point with a corresponding label    

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
scat = ax.scatter(x,y,c=tag,s=np.random.randint(100,500,N),cmap=cmap,     norm=norm)
ax.scatter([1,2],[1,2],s=10,c='k')
# create the colorbar
cb = plt.colorbar(scat, spacing='proportional',ticks=bounds)
cb.set_label('Custom cbar')
ax.set_title('Discrete color mappings')
plt.show()