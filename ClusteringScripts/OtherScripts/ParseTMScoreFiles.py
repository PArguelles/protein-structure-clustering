
import os

def rename(structure):
    structure = structure.replace("pdb","")
    structure = structure.replace(".ent","")
    return structure

def parseTMScoreFiles():    
    path_to_files = "D:/Dados/scop/scop_tmscore/"
    path_to_parsed = "D:/Dados/scop/scop_tmscore_parsed/"

    empty = "There is no common residues in the input structures"

    for filename in os.listdir(path_to_files):
        print(filename)
        with open(path_to_files+filename) as fp:
            split = str(filename).split('_')
            structure1 = split[0]
            structure2 = split[1]
            structure1 = rename(structure1)
            structure2 = rename(structure2)

            line = fp.readline()

            if empty not in line:  
                with open(path_to_parsed+'parsed_'+structure1+'_'+structure2,"w") as nf:      
                    while line:
                        if "RMSD" in line:
                            nf.write(line)
                        elif "TM-score    =" in line:
                            nf.write(line)
                        elif "MaxSub-score=" in line:
                            nf.write(line)
                        elif "GDT-TS-score=" in line: 
                            nf.write(line)  
                        elif "GDT-HA-score=" in line:
                            nf.write(line)
                            break
                        line = fp.readline()

parseTMScoreFiles()                        


   

