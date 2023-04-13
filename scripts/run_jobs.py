import os, sys

arg = sys.argv[1]

for analogue in os.listdir():
	if analogue == arg:
		for pose in os.listdir(f'{analogue}'):
			for file in os.listdir(f'{analogue}/{pose}'):
				os.chdir(f'./{analogue}/{pose}')
				os.system(f'sbatch {file}')
				os.chdir('../../')
