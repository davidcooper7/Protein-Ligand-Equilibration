##USAGE setup_empty_equil.py PROTEIN.pdb

import os, json, sys

arg = sys.argv[1]

if 'output' not in os.listdir('../equil/'):
	os.mkdir('../equil/output')
if 'input_json' not in os.listdir('../equil/'):
	os.mkdir('../equil/input_json')
if 'jobs' not in os.listdir():
	os.mkdir('./jobs')



for lig_file in os.listdir(f'../docking/systems/'):
	pre= lig_file.split('.')[0]
	analogue = pre.split('_')[1]
	pose = pre.split('_')[2]

	if analogue == arg:
		if analogue not in os.listdir('../equil/output'):
			os.mkdir(f'../equil/output/{analogue}')
		if pose not in os.listdir(f'../equil/output/{analogue}/'):
			os.mkdir(f'../equil/output/{analogue}/{pose}')


		##setup MIN job
		with open('./input_min.json', 'r') as f:
			data = json.load(f)
			f.close()
		
		data['min']['pdb'] = f'../../../../docking/systems/{lig_file}'
		if pose == 'crys':
			data['min']['prmtop'] = f'../../../../equil/para/pre_equil/system_{analogue}_crys.prmtop'
		else:
                        data['min']['prmtop'] = f'../../../../equil/para/pre_equil/system_{analogue}_1.prmtop'
		data['min']['save_pdb'] = f'../../../../equil/output/{analogue}/{pose}/{analogue}{pose}_min.pdb'

		filename = f'../equil/input_json/min_{analogue}_{pose}.json'
		with open(filename, 'w') as f:
			json.dump(data,f)
			f.close()
		
		##setup STEP 5 NPT job
		with open('./MORPHINE_TEST.json', 'r') as f:
			data = json.load(f)
			f.close()

		data['npt']['pdb'] =f'../../../../equil/output/{analogue}/{pose}/{analogue}{pose}_min.pdb'
		if pose == 'crys':
			data['npt']['prmtop'] = f'../../../../equil/para/pre_equil/system_{analogue}_crys.prmtop'
		else:
			data['npt']['prmtop'] = f'../../../../equil/para/pre_equil/system_{analogue}_1.prmtop'
		
		data['npt']['save_pdb'] =  f'../../../../equil/output/{analogue}/{pose}/{analogue}{pose}.pdb'
		data['npt']['save_state'] =f'../../../../equil/output/{analogue}/{pose}/{analogue}{pose}.rst'
		data['npt']['stdout'] =f'../../../../equil/output/{analogue}/{pose}/{analogue}{pose}.dat'
		data['npt']['dcd'] = f'../../../../equil/output/{analogue}/{pose}/{analogue}{pose}.dcd'

		with open(f'../equil/input_json/input_{analogue}_{pose}.json', 'w') as f:
			json.dump(data, f)
			f.close()


		if f'{analogue}' not in os.listdir('./jobs/'):
			os.mkdir(f'./jobs/{analogue}')
		if f'{pose}' not in os.listdir(f'./jobs/{analogue}'):
			os.mkdir(f'./jobs/{analogue}/{pose}')

		with open('./equil_job.job', 'r') as f:
			lines = f.readlines()
			f.close()

		lines[1] = f'#SBATCH --job-name="{analogue}_{pose}"\n'
		lines[2] = f'#SBATCH --output="{analogue}_{pose}.%j.%N.out"\n'
		lines[21] = f'python ../../../equil_OPENMM.py -i ../../../../equil/input_json/min_{analogue}_{pose}.json\n'
		lines[23] = f'python ../../../equil_OPENMM.py -i ../../../../equil/input_json/input_{analogue}_{pose}.json\n'
		
		with open(f'./jobs/{analogue}/{pose}/{analogue}_{pose}.job', 'w') as f:
			for line in lines:
				f.write(line)

os.system('cp ./run_jobs.py ./jobs')
		




	

