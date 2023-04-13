import os, json, sys
import MDAnalysis as mda
import numpy as np
from MDAnalysis import transformations
from MDAnalysis.transformations import translate
#from MDAnalysis.transformations import center

arg = sys.argv[1]

if 'water' not in os.listdir('../'):
    os.mkdir('../water')
if 'systems' not in os.listdir('../water/'):
    os.mkdir('../water/systems/')
if 'input_json' not in os.listdir('../water/'):
    os.mkdir('../water/input_json/')
if 'centered' not in os.listdir('../water/'):
    os.mkdir('../water/centered/')



for file in os.listdir('../docking/output/pdb'):
    name = file.split('.')[0]
    pose = name.split('_')[1]
    


    if pose == '1' and (name == arg or arg == 'all'):
        
        ##center ligand
        u = mda.Universe(f'../docking/output/pdb/{file}')
        sel = u.select_atoms('all')
        sel.translate(-sel.center_of_mass())
        sel.translate(np.array([30, 30, 30]))
        centered_pdb = f'../water/centered/{name}.pdb'
        sel.write(centered_pdb)


        with open('./input_water.json', 'r') as f:
            data = json.load(f)
            f.close()

        data['fname_protein'] = data['fname_protein'].replace(data['fname_protein'], centered_pdb)
        data['fname_system'] = data['fname_system'].replace(data['fname_system'], f'../water/systems/solvent_{file}')

        with open(f'../water/input_json/build_{name}.json', 'w') as f:
            json.dump(data, f)
            f.close()

        os.system(f'python ./build_system.py -i ../water/input_json/build_{name}.json')
       
        ##make corrections to header to correct box vector
        with open(f'../water/systems/solvent_{file}', 'r') as f:
            lines = f.readlines()
            f.close()


        write_lines = ['']
        i=0
        while i <len(lines):
            if i==0 or i >=10:
                write_lines.append(lines[i])
            i=i+1
        with open(f'../water/systems/solvent_{file}', 'w') as f:
            for line in write_lines:
                f.write(line)
           

