import os, sys
import json

if 'equil' not in os.listdir('../'):
    os.mkdir('../equil')
if 'para' not in os.listdir('../equil'):
    os.mkdir('../equil/para')
if 'pre_equil' not in os.listdir('../equil/para/'):
    os.mkdir('../equil/para/pre_equil')


arg = sys.argv[1]
##get ligand xml 
for file in os.listdir('../docking/output/pdb'):
	pre = file.split('.')[0]
	pose = pre.split('_')[1]
	name = pre.split('_')[0]
	if pose == '1':
		if name == arg or arg == 'all':
		    print(f'{name}')
		    os.system(f'python quick_xml.py {file} 0')
		    print(f'{name} xml made')


##run pdb2amber
if 'input_json' not in os.listdir('../equil/'):
    os.mkdir('../equil/input_json')

for system in os.listdir('../docking/systems/'):
    name = system.split('.')[0]
    lig = name.split('_')[1]
    pose = name.split('_')[2]
    if pose == '1' and lig == arg or arg == 'all':
	    print(system)
	    with open('./input.json', 'r') as f:
	        data = json.load(f)
	        f.close()

	    data['fname_pdb'] = data['fname_pdb'].replace(data['fname_pdb'], f'../docking/systems/{system}')
	    data['fname_prmtop'] = data['fname_prmtop'].replace(data['fname_prmtop'], f'../equil/para/pre_equil/{name}.prmtop')
	    data['fname_ff'][3] = f'../input/lig_xml/{lig}_1.ff.xml'
	    
	    filename = f'../equil/input_json/{name}_input.json'
	    with open(filename, 'w') as f:
	        json.dump(data,f)
	    os.system(f'python pdb2amber.py -i {filename}')
	    print(f'\n\n\n {system} DONE \n\n\n')

    if pose == 'crys' and lig == arg:
            print(system)
            with open('./input.json', 'r') as f:
                data = json.load(f)
                f.close()

            data['fname_pdb'] = data['fname_pdb'].replace(data['fname_pdb'], f'../docking/systems/{system}')
            data['fname_prmtop'] = data['fname_prmtop'].replace(data['fname_prmtop'], f'../equil/para/pre_equil/{name}.prmtop')
            data['fname_ff'][3] = f'../input/lig_xml/{lig}_1.ff.xml'

            filename = f'../equil/input_json/{name}_input.json'
            with open(filename, 'w') as f:
                json.dump(data,f)
            os.system(f'python pdb2amber.py -i {filename}')
            print(f'\n\n\n {system} DONE \n\n\n')
