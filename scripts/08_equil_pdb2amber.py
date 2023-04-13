import os, sys
import json

arg = sys.argv[1]

if 'post_equil' not in os.listdir('../equil/para/'):
    os.mkdir('../equil/para/post_equil')


##run pdb2amber

for analogue in os.listdir('../equil/output'):
    if analogue == arg:
        os.system(f'rm ../equil/output/{analogue}/*.rst')
        for pose in os.listdir(f'../equil/output/{analogue}'):
            if pose == '1':
                pdb = f'../equil/output/{analogue}/{pose}/{analogue}_{pose}.pdb'
            
                with open('./input.json', 'r') as f:
                    data = json.load(f)
                    f.close()

                data['fname_pdb'] = data['fname_pdb'].replace(data['fname_pdb'], pdb)
                data['fname_prmtop'] = data['fname_prmtop'].replace(data['fname_prmtop'], f'../equil/para/post_equil/{analogue}_{pose}.prmtop')
                data['fname_ff'][3] = f'../input/lig_xml/{analogue}_1.ff.xml'
                data['inpcrd_fname'] = f'../equil/para/post_equil/{analogue}_{pose}.inpcrd'
                
                filename = f'../equil/input_json/final_{analogue}_{pose}.json'
                with open(filename, 'w') as f:
                    json.dump(data,f)
                print(f'{analogue}_{pose}')
                os.system(f'python pdb2amber.py -i {filename}')
                if os.path.exists(f'../equil/para/post_equil/{analogue}_{pose}.prmtop'):
                    print(f'\n\n\n {analogue}_{pose}DONE \n\n\n')
