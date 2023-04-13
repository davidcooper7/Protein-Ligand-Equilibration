import MDAnalysis as mda 
import os, sys

arg = sys.argv[1]

for system in os.listdir('../docking/systems'):
	analogue = system.split('_')[1]
	if arg == 'all' or analogue == arg:
		print(system)
		u = mda.Universe(f'../docking/systems/{system}')
		all = u.select_atoms('all')
		zone = u.select_atoms('resname HOH NA CL and point 53.783  61.134  67.769 15.0')
		arr = zone.resids
		conflicts = u.select_atoms('')
		
		i=0
		for resid in arr:
		    atom = u.select_atoms('resid '+str(arr[i].item()))
		    conflicts = conflicts.concatenate(atom)
		    i=i+1

		select = all.subtract(conflicts)
		select.write(f'../docking/systems/{system}')
		print( all.n_residues, zone.n_residues, select.n_residues)
