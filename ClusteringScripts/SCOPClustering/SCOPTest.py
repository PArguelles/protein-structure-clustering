import SCOPUtilities as util
import KMeansScript as km
import AgglomerativeScript as agg

measure1 = 'RMSD'
measure2 = 'MaxSub'
structures = ['1iym']

for structure in structures:
    measure_data,_,_ = util.readMeasureData(measure1,measure2,structure)
    print(measure_data)

    scop_names = util.readSCOPNames()

    print(scop_names)

    data = util.intersectSCOPKeys(scop_names,measure_data)
    _,values1,values2,true_labels = util.splitSCOPTuples(data)

    km.kmeansFunc(structure, measure1, measure2, values1, values2, data, true_labels)

    print(data)


    print(values1)
