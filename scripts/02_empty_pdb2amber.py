##USAGE 02_empty_pdb2amber.py PROTEIN.pdb
import os, sys, json 

prot = sys.argv[1]
name = prot.split('.')[0]

if 'built' not in os.listdir('../empty_system/para'):
    os.mkdir('../empty_system/para/built')

##read and modify input.json
with open('./input.json', 'r') as f:
    data = json.load(f)
    f.close()

old_pdb = data['fname_pdb']
data['fname_pdb'] = data['fname_pdb'].replace(old_pdb, f'../empty_system/protein/{prot}')
old_prmtop = data['fname_prmtop']
data['fname_prmtop'] = data['fname_prmtop'].replace(old_prmtop, f'../empty_system/para/built/{name}.prmtop')
data['inpcrd_fname'] = f'../empty_system/para/built/{name}.inpcrd'
filename =f'../empty_system/input_json/empty_input.json'

##dump empty_input.json

with open(filename, 'w') as f:
    json.dump(data, f)


##run pdb2amber.py 

os.system(f'python pdb2amber.py -i {filename}')




print(f'/////// {name}.prmtop CREATED////////')

