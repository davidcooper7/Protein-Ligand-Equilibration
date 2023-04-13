import os, sys, json

## read OPTIONS.json input 

with open('../input/INPUT.json', 'r') as f:
	data = json.load(f)
	protein = data["Protein"]
	prot = data["Protonate_protein"]
	pH = data["pH"]
	mem = data["Membrane"]
	opm = data["OPM_structure"]
	opm_sele = data["OPM_alignment_sele"]
	prot_sele = data["Protein_alignment_sele"]
	box_dims = data["Box_dimensions"][0]
	f.close()

##STEP 00 align to OPM if mem == True
if mem == True:
	os.system(f'python 00_align_to_OPM.py')

print(f'\n///////{protein} ALIGNED TO {opm}////////\n')


##STEP 00 Protoante if true
if prot == True:
	os.system(f'python 00_pdb2pqr.py {protein} {pH}')
print('\n//////////// PROTEIN PROTONATED/////////////////\n')

##STEP 01 build empty system
os.system(f'python 01_build_empty.py {protein} {box_dims} {mem}')

print('\n//////////// EMPTY SYSTEM BUILT/////////////////\n')

##STEP 02 create para files for empty system 
os.system(f'python 02_empty_pdb2amber.py {protein}')

##final prep setup 
os.system(f'python setup_empty_equil.py {protein}')

