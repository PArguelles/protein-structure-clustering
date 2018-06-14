import numpy as np
import os
import CATHUtilities as util

domain = "1c4zA02"
measure1 = "RMSD"
measure2 = "MaxSub"

measure_data = util.readMeasureData(measure1,measure2,domain)

cath_names = util.readCATHNames()

data = util.intersectKeys(cath_names,measure_data)

pdb_ids,cath_names,values1,values2,true_labels = util.splitCATHTuples(data)

util.saveCATHResults(data,measure1,measure2)




