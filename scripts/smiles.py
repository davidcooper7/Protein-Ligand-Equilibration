import os, json

with open('../input/SMILES.json', 'r') as f:
	data = json.load(f)
	f.close()


i=0 
while i <len(data['Ligand_names']):
	lig_name = data['Ligand_names'][i]
	lig_smile = data['Ligand_SMILES'][i]
	with open(f'../smiles/{lig_name}.smiles' , 'w') as f:
		f.write(lig_smile)
		f.close()
	i=i+1

