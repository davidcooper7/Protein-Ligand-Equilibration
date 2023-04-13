##USAGE python 00_align_to_OPM.py 

import MDAnalysis as mda
from MDAnalysis.analysis import align
from MDAnalysis.analysis.rms import rmsd
import os
import sys
import json

input_dir = '../input'
input_json = f'{input_dir}/INPUT.json'

##read input_align.json
with open(input_json, 'r') as f:
	data = json.load(f)

##set reference and mobile pdb files
opm_pdb = f'{input_dir}/OPM_prot/' +data['OPM_structure']
opm_residues = data['OPM_alignment_sele']
mobile_pdb = f'{input_dir}/original_prot/'+data['Protein']
mobile_residues = data['Protein_alignment_sele']

if 'aligned_prot' not in os.listdir(input_dir):
	os.mkdir(f'{input_dir}/aligned_prot')

output = f'{input_dir}/aligned_prot/'+data['Protein']
ref = mda.Universe(opm_pdb)
mobile = mda.Universe(mobile_pdb)

##generate rotational matrix
mobile0 = mobile.select_atoms(mobile_residues).positions - mobile.atoms.center_of_mass()
ref0 = ref.select_atoms(opm_residues).positions - ref.atoms.center_of_mass()
R, rmsd = align.rotation_matrix(mobile0, ref0)

print('ROTATION MATRIX \n', R, 'RMSD\n', rmsd)

##align and write pdb
mobile.atoms.translate(-mobile.select_atoms(mobile_residues).center_of_mass())
mobile.atoms.rotate(R)
mobile.atoms.translate(ref.select_atoms(opm_residues).center_of_mass())
mobile.atoms.write(output)  
