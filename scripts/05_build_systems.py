import os, sys, json

prot = sys.argv[1]
name = prot.split('.')[0]
arg = sys.argv[2]

##numerate ligands first

for lig in os.listdir('../docking/output/pdb'):
	lig_name = lig.split('_')[0]
	if lig_name == arg or arg == 'all':
		os.system(f'python numerate_a_model.py ../docking/output/pdb/{lig} ../docking/output/pdb/{lig}')
		print(f'{lig} numerated')

if 'systems' not in os.listdir('../docking/'):
	os.mkdir('../docking/systems')

for lig in os.listdir('../docking/output/pdb'):
	lig_name = lig.split('_')[0]
	if lig_name == arg or arg == 'all':
		os.system(f'./combine_docked_pose_and_protein.sh ../empty_system/equil/step4/{name}_20.pdb ../docking/output/pdb/{lig} ../docking/systems/system_{lig}')
		print(f'{lig} system built')
