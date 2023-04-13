#USAGE python numerate_a_model.py in_pdbname out_pdbname
#pdboutput of smiles may not numerate atoms, this numerates according to the force fieldmade

import sys

inpdb = sys.argv[1]
outname = sys.argv[2]

with open(inpdb, 'r') as f:
    atoms = [line for line in f.readlines() if line.startswith('ATOM') or line.startswith('HETATM') or line.startswith('CONECT')]

elm_di = {}

for i in range(len(atoms)):
    elm = atoms[i][12:14]
    #print(elm, elm_di)
    if elm not in elm_di:
        elm_di[elm] = 1
    elif elm_di[elm] < 10:
        atoms[i] = atoms[i][:12]+f'{elm}{elm_di[elm]}'+atoms[i][15:]
        elm_di[elm] += 1
    elif elm_di[elm] >= 10 and elm_di[elm] < 100:
        atoms[i] = atoms[i][:12]+f'{elm}{elm_di[elm]}'+atoms[i][16:]
        elm_di[elm] += 1

with open(outname, 'w') as g:
    g.writelines(atoms)

        
