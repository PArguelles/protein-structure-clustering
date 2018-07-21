import CASP12Utilities as util
import CASPKMeans as km
import CASPAgglomerative as agg

structures = ['T0859','T0860','T0861','T0862','T0863','T0864','T0865','T0866','T0867']

measures = ['RMSD','GDT-HA','GDT-TS','TM-score']

combinations = util.generateMeasureCombinations(measures) 

current_combo = 0
current_structure = 0

for structure in structures:
    _, gdt_ha, gdt_ts, rmsd, tmscore = util.readTargetSummary(structure)
    values = {'GDT-HA': gdt_ha, 'GDT-TS' : gdt_ts, 'RMSD' : rmsd, 'TM-score' : tmscore}
    
    while current_combo < len(combinations):
        parsed = combinations[current_combo].split(' ')
        measure1 = parsed[0]
        measure2 = parsed[1]

        km.kmeansFunc(structure, measure1, measure2, values[measure1], values[measure2])
        agg.agglo(structure, measure1, measure2, values[measure1], values[measure2])
        current_combo += 1

    current_combo = 0
    current_structure += 1   

 