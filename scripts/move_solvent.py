import os

for file in os.listdir('../water/equil/step5'):
	type = file.split('.')[1]
	try:
		prm = 'solvent_'+file.split('_')[1]+'.prmtop'
		inp = 'solvent_'+file.split('_')[1]+'.inpcrd'
	except:
		pass
	if type == 'pdb':
		analogue = file.split('_')[1]
		os.system(f'cp ../water/equil/step5/{file} ../final/{analogue}/')
		os.system(f'cp ../water/para/post_equil/{inp} ../final/{analogue}/')
		os.system(f'cp ../water/para/post_equil/{prm} ../final/{analogue}')
		try:
			os.system(f'cp ../water/equil/step5/{file} ../../yank/{analogue}/')
			os.system(f'cp ../water/para/post_equil/{prm} ../../yank/{analogue}/')
			os.system(f'cp ../water/para/post_equil/{inp} ../../yank/{analogue}')
			print(f'{analogue} UPDATED')
		except:
			print(f'{analogue} not found')

