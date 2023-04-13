import os, sys, json

prot = sys.argv[1]
name = prot.split('.')[0]

if (os.path.isdir('../docking')):
    os.system('rm -r ../docking')
if 'docking' not in os.listdir('./..'):
    os.mkdir('./../docking')
if 'protein' not in os.listdir('./..'):
    os.mkdir('./../docking/protein') 


##extract protein from PROTEIN_20.pdb
with open(f'../empty_system/equil/step4/{name}_20.pdb', 'r') as f:
    lines = f.readlines()
    f.close()

write_lines = ['']
for line in lines:
    if line.find('HOH') == -1:
        if line.find('DPP') == -1:
            if line.find('NA') == -1:
                if line.find('CL') == -1:
                    write_lines.append(line)

with open(f'../docking/protein/{prot}', 'w') as f:
    for line in write_lines:
        f.write(line)
    f.close()
