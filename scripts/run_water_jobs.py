import os

os.chdir('./water')

for file in os.listdir():
	os.system(f'sbatch {file}')
	
