##USAGE python 1_build_empty.py PROTEIN.pdb box_dimensions[x,y,z] mem(bool)

import os, json, sys
import MDAnalysis as mda
from MDAnalysis import topology

prot = sys.argv[1]
mem = sys.argv[3]
box_dims = sys.argv[2]
name = prot.split('.')[0]
empty_dir = '../empty_system'

##create protein.prmtop file to extract protein charge 

## create dir for para files

if 'empty_system' not in os.listdir('../'):
        os.mkdir(empty_dir)
if 'para' not in os.listdir(empty_dir):
        os.mkdir(f'{empty_dir}/para')
if 'unbuilt' not in os.listdir(f'{empty_dir}/para'):
        os.mkdir(f'{empty_dir}/para/unbuilt')
if 'input_json' not in os.listdir(empty_dir):
        os.mkdir(f'{empty_dir}/input_json')
if 'protein' not in os.listdir(empty_dir):
        os.mkdir(f'{empty_dir}/protein/')

##read template input.json file for pdb2amber
input_dir = '../input'
if os.path.exists(f'{input_dir}/prot_protein/{prot}'):
    prot_path = f'{input_dir}/prot_protein/{prot}'
else:
    prot_path = f'{input_dir}/original_protein/{prot}'
with open('./input.json', 'r') as f:
        prmtop = json.load(f)
        old_pdb = prmtop['fname_pdb']
        prmtop['fname_pdb'] = prmtop['fname_pdb'].replace(old_pdb, prot_path) 
        prmtop['fname_prmtop'] = prmtop['fname_prmtop'].replace('receptor.prmtop', f'{empty_dir}/para/unbuilt/{name}.prmtop')
        prmtop['inpcrd_fname'] = f'{empty_dir}/para/unbuilt/{name}.inpcrd'
        f.close()


## dump new input json 
filename = f'{empty_dir}/input_json/{name}_input.json'
with open(filename, 'w') as f:
        json.dump(prmtop, f)
        f.close()

##run pdb2amber.py 
os.system(f'python pdb2amber.py -i {filename}')

##get charge using MDA
u = mda.Universe(f'{empty_dir}/para/unbuilt/{name}.prmtop')
all = u.select_atoms('all')
charge = all.total_charge()
round_charge = round(charge)
print('///////TOTAL CHARGE OF PROTEIN is ' +str(charge) + '///////')


##read input_build.json template
with open('./input_build.json', 'r') as f:
        data = json.load(f)

##change input file according to job type
data['fname_protein'] = data['fname_protein'].replace('A_opm.pdb', f'{input_dir}/prot_protein/{prot}')
data['protein_charge'] = int(charge)
data['fname_system'] = data['fname_system'].replace('A_opm_system.pdb', f'{empty_dir}/protein/{prot}')
data['box'] = [int(box_dims), int(box_dims), int(box_dims)]

if mem:
    data['membrane'][0] = 'true'
else:
    data['membrane'][0] = 'false'

##dump input_build.json
filename = f'../empty_system/input_json/{name}_input_build.json'

print(data)

with open(filename, 'w') as f:
	json.dump(data, f)
	f.close()

##run build_system.py
os.system(f'python build_system.py -i {filename}')


print('////////EMPTY SYSTEM BUILT //////////')








