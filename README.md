# Protein-Ligand-Equilibration

CONDA:

	conda env 1: 
		MDAnalysis
		pdb2pqr
		openmm
		ambertools

	conda env 2:
		mgltools

	conda env 3:
		vina 
--------------------------------------------------------------------------------------------------------
INPUTS:

	Ligand prep: (sample command line workflow for generating ligand.pdbqt from smiles)
		obabel  a1.smiles -O a1.mol2 --gen3d --unique (CHECK STEREOCHEM)
		prepare_ligand4.py -l a1.mol2 -o a1.pdbqt -v (from MGL TOOLS)

	ADD INPUTS HERE:
		Add PROTEIN.pdb to input/original_prot
		Add OPM.pdb to input/OPM_prot (if membrane system, where OPM is the structure from the OPM database)	
		Make appropriate selections in input/INPUT.json
		Add Ligand .pdbqt files to input/lig_pdbqt
--------------------------------------------------------------------------------------------------------

PREPARATION for membrane equilibration -> RUN ALL PREPARATION STEPS USING scripts/PREP.py which completes the following steps:
	
	STEP00 (if necessary):
		scripts/00_align_to_opm.py (aligns PROTEIN.pdb coords to OPM.pdb with given selection arguments in INPUT.json using MDA selection language)
		scripts/00_pdb2pqr.py (protonates PROTEIN.pdb at desired pH specified in INPUT.json)
	STEP01:
		scripts/01_build_empty.py (builds empty system with .15 M NaCl and membrane(if specified in INPUT.json)) -->output in empty_system/protein
	STEP02:
		scripts/02_empty_pdb2amber.py (creates amber topology files for empty system) -->output in empty_system/para/built
	EQUIL SET UP:
		scripts/setup_empty_equil.py (creates folder structure with appropriate input files for job) -->input files located in empty_system/input_json
--------------------------------------------------------------------------------------------------------

MEMBRANE/SOLVENT EQUILIBRATION (equilibrate system while keeping restraints on protein):
	
	manually run scripts/empty_equil_job.job file --> output in appropriate empty_system/equil dir, final equilibration .pdb is empty_system/equil/step4PROTEIN_20.pdb  
	
DOCKING LIGANDS TO PROTEIN:

	Extract ligand from protein:
		run scripts/03_prepare_docking.py --> output pdb of just protein in docking/protein
	Get protein pdb:
		***must be different conda env with only mgltools installed***
		type into command line
		prepare_receptor4.py -r ../docking/protein/PROTEIN.pdb -o ../docking/protein/PROTEIN.pdbqt -v
	Docking:
		run scripts/04_docking.py (docks all files in input/lig_pdbqt to protein pdbqt structure) --> outputs 20 poses for in docking/output/pdb

BUILD SYSTEMS:

	COMBINING DOCKED POSES AND PROTEIN SYSTEM:
		run scripts/05_build_systems.py (numerates output ligand pdbs with numerate_a_model.py, creates new system with all components with combine_docked_pose_and_protein.sh) --> outputs in docking/systems
	REMOVING CONFLICTS:
		runscripts/ 06_remove_conflicts.py (using specific point-zone selection with mda, waters and ions within 15 A of specified point are removed in case of conflicts) --> overwrites systems in docking/systems
	GET SYSTEM PRMTOP FILE:
		run scripts/07_system_pdb2amber.py (gets .xml file for ligand using quick_xml.py and inserts in input/lig_xml, runs pdb2amber.py) --> outputs .prmtop file in equil/para/pre_equil

RUN EQUIL JOB (this step is done for every ligand that you have):

	SETUP: 
		run scripts/setup_equil.py LIGAND_NAME (setups up job files)
	RUN JOBS:
		run scripts/jobs/run_jobs.py LIGAND_NAME (runs equilibration job, with an energy minimization and a NPT (of at least 500 ps) until the last 250 frames have a std of PE and V less than 1500 J and 2.0 nm^3)--> output files in equil/output

GET EQUIL STRUCTURE AMBER FILES:

	run scripts/reorder_pdbs.py LIGAND_NAME --> reorders equil pdb so ligand is direclty after protein for corrent .prmtop
	run scripts/08_equil_pdb2amber.py LIGAND_NAME --> create .prmtop and .inpcrd for equilibrated structures --> output in /equil/para/post_equil/
--------------------------------------------------------------------------------------------------------
BUILD SOLVENT SYSTEMS:

	run scripts/09_build_water_systems.py LIGAND_NAME --> builds waters system in 60 60 60 box with just ligand --> output in water/systems/
	run scripts/10_water_systems_pdb2amber.py LIGAND_NAME --> creates .prmtop for water system --> output in water/para/pre_equil
	run setup_water_equil.py --> setups water equil jobs --> all pooled in /scripts/jobs/water
	cd to scripts/jobs/water
	sbatch job of choice --> output in /water/equil/step5
	run 11_water_equil_pdb2amber.py LIGAND_NAME --> returns .prmtop and .inpcrd for equilibrated water system --> output in /water/para/post_equil
--------------------------------------------------------------------------------------------------------

COLLECT OUTPUT:

	run 12_collect_final_output.py LIGAND_NAME -> output appears in own dir in /final/{LIGAND_NAME}
	

	
