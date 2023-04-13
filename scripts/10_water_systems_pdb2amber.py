import os, json


if 'para' not in os.listdir('../water/'):
    os.mkdir('../water/para')

if 'pre_equil' not in os.listdir('../water/para/'):
    os.mkdir('../water/para/pre_equil')

with open('./input.json', 'r') as f:
    data = json.load(f)
    f.close()

for file in os.listdir('../water/systems'):
    name = file.split('_')[1]

    data['fname_pdb'] = data['fname_pdb'].replace(data['fname_pdb'], f'../water/systems/{file}')
    data['fname_prmtop'] = data['fname_prmtop'].replace(data['fname_prmtop'], f'../water/para/pre_equil/{name}.prmtop')
    data['fname_ff'][3] = f'../input/lig_xml/{name}_1.ff.xml'

    filename = f'../water/input_json/pre_equil_{name}.json'
    with open(filename, 'w') as f:
        json.dump(data, f)

    os.system(f'python pdb2amber.py -i {filename} ')




