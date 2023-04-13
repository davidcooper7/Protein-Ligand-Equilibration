import os, sys
import json

arg = sys.argv[1]

if 'post_equil' not in os.listdir('../water/para/'):
    os.mkdir('../water/para/post_equil')


##run pdb2amber

for file in os.listdir('../water/equil/step5'):
    type = file.split('.')[1]
    if type == 'pdb':
        analogue = file.split('_')[1]
        if analogue == arg or arg == 'all':
            pdb = f'../water/equil/step5/solvent_{analogue}_1.pdb'
        
            with open('./input.json', 'r') as f:
                data = json.load(f)
                f.close()

            data['fname_pdb'] = data['fname_pdb'].replace(data['fname_pdb'], pdb)
            data['fname_prmtop'] = data['fname_prmtop'].replace(data['fname_prmtop'], f'../water/para/post_equil/solvent_{analogue}.prmtop')
            data['fname_ff'][3] = f'../input/lig_xml/{analogue}_1.ff.xml'
            data['inpcrd_fname'] = f'../water/para/post_equil/solvent_{analogue}.inpcrd'
            
            filename = f'../water/input_json/final_{analogue}.json'
            with open(filename, 'w') as f:
                json.dump(data,f)
            print(f'{analogue}')
            os.system(f'python pdb2amber.py -i {filename}')
            if os.path.exists(f'../water/para/post_equil/solvent_{analogue}.prmtop'):
                print(f'\n\n\n {analogue} DONE \n\n\n')
