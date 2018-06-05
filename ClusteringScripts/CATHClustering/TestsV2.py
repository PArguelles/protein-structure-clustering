import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import time as time
import Utilities as util
from sklearn.cluster import DBSCAN
from sklearn import metrics

path = "D:/Dados/tmscore_parsed_results/"
structure1 = "140l.ent_"

st = time.time()

# #############################################################################
# Read files
X = util.readMeasureDataV2("RMSD","MaxSub","1c4zA02")

true_labels = util.getDomainClassificationV2()

i = 0
aux = []

while i < len(X):
    #print(X[i][0])
    domain = X[i][0]
    if domain in true_labels.keys():
        aux.append(true_labels[domain])
    i += 1

X = list(zip(X,aux))

print(true_labels)
print(X)




