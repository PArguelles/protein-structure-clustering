import os 
from sklearn import metrics
from collections import OrderedDict

path_to_file = "D:Dados/casp12/summaries/"


def generateMeasureCombinations(measures):
    measures_copy = measures
    visited = []
    combinations = set()

    x = 0
    y = 0
    while x < len(measures):
        while y < len(measures_copy):
            if measures_copy[y] not in visited:
                line = measures[x]+' '+measures_copy[y]
                combinations.add(line)
            y += 1 
        visited.append(measures[x])      
        x += 1         
        y = 0
    
    combinations = list(combinations)
    return combinations

def readTargetSummary(model):

    gdt_ts = []
    gdt_ha = []
    rmsd = []
    tmscore = []
    models = []

    with open(path_to_file+model+'.txt','r') as fp:
        line = fp.readline() #skip first line
        line = fp.readline()
        while line: 
            if not str(line).isspace():
                models.append(str(line).split()[1])
                gdt_ts.append(float(str(line).split()[3]))
                gdt_ha.append(float(str(line).split()[10]))
                rmsd.append(float(str(line).split()[14]))
                tmscore.append(float(str(line).split()[45]))
         
            line = fp.readline()

    return models, gdt_ha, gdt_ts, rmsd, tmscore

def saveCASPResults(structure, algorithm, parameters, measure1, measure2, metrics):
    #date = str(getDate()).replace(':','-')

    #path = 'D:/Dados/cath/clustering_results/'+structure+'_'+measure1+'_'+measure2+'/'
    path = 'D:/Dados/casp12/clustering_results/'+structure+'/'
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path+structure+'_'+measure1+'_'+measure2+'_'+algorithm+'_'+str(parameters), 'w') as file:
        file.write('# ####################################################\n')
        file.write('Structure: '+structure+'\n')
        file.write('\n')
        file.write('# ####################################################\n')
        file.write('Algorithm: '+algorithm+'\n')
        file.write('\n')
        file.write('# ####################################################\n')
        file.write('Parameters: '+str(parameters).replace('_',' ')+'\n')
        file.write('\n')
        file.write('# ####################################################\n')
        file.write('Measures: '+measure1+' '+measure2+'\n')
        file.write('\n')
        file.write('# ####################################################\n')
        file.write('# Cluster evaluation: \n')
        file.write('Calinksi-Harabaz: %0.3f \n' % metrics[0])
        file.write('Silhouette coefficient: %0.3f \n' % metrics[1])
        file.write('\n')
 

def clusterEvaluationNoLabels(X, labels):
    values = []
    calinski_harabaz = metrics.calinski_harabaz_score(X, labels)
    silhouette = metrics.silhouette_score(X, labels, metric='sqeuclidean')
    values.append(calinski_harabaz)
    values.append(silhouette)
    return values



def saveImage(plt, path, name):
    plt.savefig(path+name+'.png',bbox_inches='tight')
    plt.clf() # Clear figure
    plt.cla() # Clear axis
    plt.close() # Close a figure window