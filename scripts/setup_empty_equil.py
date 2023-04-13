##USAGE setup_empty_equil.py PROTEIN.pdb

import os, sys, json

prot = sys.argv[1]
name = prot.split('.')[0]

##MIN
##read in input_min.json
with open('input_min.json', 'r') as f:
	data = json.load(f)
	f.close()

##change input_min.json
if 'equil' not in os.listdir('../empty_system/'):
	os.mkdir('../empty_system/equil')
if 'min' not in os.listdir('../empty_system/equil'):
	os.mkdir('../empty_system/equil/min')

data['min']['pdb'] = f'../empty_system/protein/{prot}'
data['min']['prmtop'] = f'../empty_system/para/built/{name}.prmtop'
data['min']['save_pdb'] = f'../empty_system/equil/min/{prot}'

##dump input_min.json
with open('../empty_system/input_json/input_min.json', 'w') as f:
	json.dump(data, f)
	f.close()
 
##STEP 1
##read input for input_step1_nvt.json
with open('input_step1_nvt.json', 'r') as f:
	data = json.load(f)
	f.close()

if 'step1' not in os.listdir('../empty_system/equil'):
	os.mkdir('../empty_system/equil/step1')

data['nvt']['pdb'] = f'../empty_system/equil/min/{prot}'
data['nvt']['prmtop'] = f'../empty_system/para/built/{name}.prmtop'
data['nvt']['save_pdb'] = f'../empty_system/equil/step1/{prot}'
data['nvt']['dcd'] = f'../empty_system/equil/step1/step1.dcd'
data['nvt']['save_state'] = f'../empty_system/equil/step1/step1.rst'
data['nvt']['stdout'] = f'../empty_system/equil/step1/step1.dat'

with open('../empty_system/input_json/input_step1_nvt.json', 'w') as f:
	json.dump(data, f)
	f.close()

##STEP 2
with open('input_step2_nvt.json', 'r') as f:
	data = json.load(f)
	f.close()

if 'step2' not in os.listdir('../empty_system/equil'):
	os.mkdir('../empty_system/equil/step2')

data['nvt']['pdb'] = f'../empty_system/equil/step1/{prot}'
data['nvt']['prmtop'] = f'../empty_system/para/built/{name}.prmtop'
data['nvt']['save_pdb'] = f'../empty_system/equil/step2/{prot}'
data['nvt']['dcd'] = f'../empty_system/equil/step2/step2.dcd'
data['nvt']['save_state'] = f'../empty_system/equil/step2/step2.rst'
data['nvt']['stdout'] = f'../empty_system/equil/step2/step2.dat'

with open('../empty_system/input_json/input_step2_nvt.json', 'w') as f:
	json.dump(data, f)
	f.close()

##STEP 3
with open('input_step3_npt.json', 'r') as f:
	data = json.load(f)
	f.close()

if 'step3' not in os.listdir('../empty_system/equil'):
	os.mkdir('../empty_system/equil/step3')

data['npt']['pdb'] = f'../empty_system/equil/step2/{prot}'
data['npt']['prmtop'] = f'../empty_system/para/built/{name}.prmtop'
data['npt']['save_pdb'] = f'../empty_system/equil/step3/{prot}'
data['npt']['dcd'] = f'../empty_system/equil/step3/step3.dcd'
data['npt']['load_state'] = f'../empty_system/equil/step2/step2.rst'
data['npt']['save_state'] = f'../empty_system/equil/step3/step3.rst'
data['npt']['stdout'] = f'../empty_system/equil/step3/step3.dat'

##dump input_in.json
with open('../empty_system/input_json/input_step3_npt.json', 'w') as f:
	json.dump(data, f)
	f.close()


##STEP 4
with open('input_step4_npt.json', 'r') as f:
	data = json.load(f)
	f.close()

if 'step4' not in os.listdir('../empty_system/equil'):
	os.mkdir('../empty_system/equil/step4')

data['npt']['pdb'] = f'../empty_system/equil/step3/{name}_20.pdb'
data['npt']['prmtop'] = f'../empty_system/para/built/{name}.prmtop'
data['npt']['save_pdb'] = f'../empty_system/equil/step4/{prot}'
data['npt']['dcd'] = f'../empty_system/equil/step4/step4.dcd'
data['npt']['load_state'] = f'../empty_system/equil/step3/step3_A.rst'
data['npt']['save_state'] = f'../empty_system/equil/step4/step4.rst'
data['npt']['stdout'] = f'../empty_system/equil/step4/step4.dat'

##dump input_in.json
with open('../empty_system/input_json/input_step4_npt.json', 'w') as f:
	json.dump(data, f)
	f.close()

