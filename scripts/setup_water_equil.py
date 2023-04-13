import os, json

if 'water' not in os.listdir('./jobs/'):
    os.mkdir('./jobs/water')

##MIN
##read in input_min.json
with open('input_min.json', 'r') as f:
	data = json.load(f)
	f.close()

##change input_min.json
if 'equil' not in os.listdir('../water/'):
	os.mkdir('../water/equil')
if 'min' not in os.listdir('../water/equil'):
	os.mkdir('../water/equil/min')

for file in os.listdir('../water/systems/'):
    name = file.split('_')[1]
        
    data['min']['pdb'] = f'../../../water/systems/{file}'
    data['min']['prmtop'] = f'../../../water/para/pre_equil/{name}.prmtop'
    data['min']['save_pdb'] = f'../../../water/equil/min/{file}'

    ##dump input_min.json
    with open(f'../water/input_json/min_{name}.json', 'w') as f:
        json.dump(data, f)
        f.close()
	
##STEP 2
with open('input_step2_nvt.json', 'r') as f:
	data = json.load(f)
	f.close()

if 'step2' not in os.listdir('../water/equil'):
	os.mkdir('../water/equil/step2')

for file in os.listdir('../water/systems/'):
    name = file.split('_')[1]

    data['nvt']['pdb'] = f'../../../water/equil/min/{file}'
    data['nvt']['prmtop'] = f'../../../water/para/pre_equil/{name}.prmtop'
    data['nvt']['save_pdb'] = f'../../../water/equil/step2/{file}'
    data['nvt']['dcd'] = f'../../../water/equil/step2/{name}.dcd'
    data['nvt']['save_state'] = f'../../../water/equil/step2/{name}.rst'
    data['nvt']['stdout'] = f'../../../water/equil/step2/{name}.dat'

    with open(f'../water/input_json/nvt_{name}.json', 'w') as f:
        json.dump(data, f)
        f.close()
	
##STEP 5
with open('MORPHINE_TEST.json', 'r') as f:
	data = json.load(f)
	f.close()

if 'step5' not in os.listdir('../water/equil'):
	os.mkdir('../water/equil/step5')

for file in os.listdir('../water/systems/'):
    name = file.split('_')[1]

    data['npt']['pdb'] = f'../../../water/equil/step2/{file}'
    data['npt']['prmtop'] = f'../../../water/para/pre_equil/{name}.prmtop'
    data['npt']['save_pdb'] = f'../../../water/equil/step5/{file}'
    data['npt']['dcd'] = f'../../../water/equil/step5/{name}.dcd'
    data['npt']['save_state'] = f'../../../water/equil/step5/{name}.rst'
    data['npt']['stdout'] = f'../../../water/equil/step5/{name}.dat'

    with open(f'../water/input_json/npt_{name}.json', 'w') as f:
        json.dump(data, f)
        f.close()


##job file
    with open('./equil_job.job', 'r') as f:
        lines = f.readlines()
        f.close()


    lines[1] = '#SBATCH --job-name="WaterRelax"\n'
    lines[2] = '#SBATCH --output="WaterRelax.%j.%N.out"\n'
    lines[21] = f'python ../../water_equil_OPENMM.py -i ../../../water/input_json/min_{name}.json\n'
    lines[23] = f'python ../../water_equil_OPENMM.py -i ../../../water/input_json/nvt_{name}.json\n'
    lines.append('echo STEP5\n')
    lines.append(f'python ../../water_equil_OPENMM.py -i ../../../water/input_json/npt_{name}.json\n')
    with open(f'./jobs/water/{name}.job', 'w') as f:
        for line in lines:
            f.write(line)


os.system('cp run_water_jobs.py ./jobs')
