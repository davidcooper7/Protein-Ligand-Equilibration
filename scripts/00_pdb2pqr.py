##USAGE 00_pdb2pqr.py PROTEIN.pdb pH 
import os, sys, json

#read options from INPUT.json
input_dir = '../input'
input_json = f'{input_dir}/INPUT.json'

with open(input_json, 'r') as f:
    data = json.load(f)

prot = sys.argv[1]
pH = data['pH']
alignment_bool = data['Alignment']

##set up output dir
if 'pqr' not in os.listdir(input_dir):
	os.mkdir(f'{input_dir}/pqr')
if 'prot_protein' not in os.listdir(input_dir):
	os.mkdir(f'{input_dir}/prot_protein')

##use pdb2pqr30 to fix/protonate structure
if alignment_bool:
    os.system(f'pdb2pqr30 {input_dir}/aligned_prot/{prot} {input_dir}/pqr/dummy.pqr --ff=AMBER --nodebump --pdb-output={input_dir}/prot_protein/{prot} --with-ph {pH} --ffout=AMBER --keep-chain')

else:
        os.system(f'pdb2pqr30 {input_dir}/original_protein/{prot} {input_dir}/pqr/dummy.pqr --ff=AMBER --nodebump --pdb-output={input_dir}/prot_protein/{prot} --with-ph {pH} --ffout=AMBER --keep-chain')
