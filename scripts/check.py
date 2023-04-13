import os, sys

arg = sys.argv[1]

for analogue in os.listdir('../equil/output/'):
	if analogue == arg:
		os.system(f'rm ../equil/output/{analogue}/*.rst')
		for pose in os.listdir(f'../equil/output/{analogue}'):
			if os.path.exists(f'../equil/output/{analogue}/{pose}/{analogue}{pose}.pdb'):
				print(f'{analogue}_{pose} RAN TO COMPLETION')
			else:
				print(f'\n\nPROBLEM WITH {analogue}_{pose}\n\n')

