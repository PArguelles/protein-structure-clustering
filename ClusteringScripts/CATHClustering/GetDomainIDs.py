import os

cath_names_path = "D:/Dados/cath/cath-classification-data/cath-names.txt"

id_map = {}

# #############################################################################
# Read files
structure = "4gv5A00" 

with open(cath_names_path) as fp:
    line = fp.readline()
    while line:
        if '#' not in line:
            id_map[str(line).split()[1]] = str(line).split()[0]
        line = fp.readline()   

print(str(id_map[structure]).split('.')[0])
print(str(id_map[structure]).split('.')[1])
print(str(id_map[structure]).split('.')[2])
print(str(id_map[structure]).split('.')[3])