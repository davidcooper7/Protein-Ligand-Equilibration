import os, sys, json

prot = sys.argv[1]
arg = sys.argv[2]
name = prot.split('.')[0]

with open('../input/INPUT.json', 'r') as f:
    data = json.load(f)
    f.close()

cx = data['Docking'][0]
cy = data['Docking'][1]
cz = data['Docking'][2]
sx = data['Docking'][3]
sy = data['Docking'][4]
sz = data['Docking'][5]


def write_autodock(ligand):
  with open(f"./docking_config/config_singledock_{ligand}","w") as f:
    f.write("#CONFIGURATION FILE (options not used are commented) \n")
    f.write("\n")
    f.write("#INPUT OPTIONS \n")
    f.write(f"receptor = ../docking/protein/{name}.pdbqt \n")
    f.write(f"ligand = ../input/lig_pdbqt/{ligand}.pdbqt \n")
    f.write("#flex = [flexible residues in receptor in pdbqt format] \n")
    f.write("#SEARCH SPACE CONFIGURATIONS \n")
    f.write("#Center of the box (values cx, cy and cz) \n")
  # -->CHANGE THE FOLLOWING DATA WITH YOUR BOX CENTER COORDINATES  
    f.write(f"center_x = {cx} \n")
    f.write(f"center_y = {cy} \n")
    f.write(f"center_z = {cz} \n")
  # -->CHANGE THE FOLLOWING DATA WITH YOUR BOX DIMENSIONS
    f.write("#Size of the box (values szx, szy and szz) \n")
    f.write(f"size_x = {sx} \n")
    f.write(f"size_y = {sy} \n")
    f.write(f"size_z = {sz} \n")
  #MORE OPTIONS
    f.write("#OUTPUT OPTIONS \n")
    f.write("#out = \n")
    f.write("#log = \n")
    f.write("\n")
    f.write("#OTHER OPTIONS \n")
    f.write("#cpu =  \n")
    f.write("exhaustiveness = 1000\n")
    f.write("num_modes = 20 \n")
    f.write("#energy_range = \n")
    f.write("#seed = ")
 
##do the docking

if 'output' not in os.listdir('../docking'):
    os.mkdir('../docking/output')
if 'pdbqt' not in os.listdir('../docking/output'):
    os.mkdir('../docking/output/pdbqt')
if 'pdb' not in os.listdir('../docking/output'):
    os.mkdir('../docking/output/pdb')

for ligand in os.listdir('../input/lig_pdbqt'):
    ligand = ligand.split('.')[0]
    if ligand == arg:
        write_autodock(ligand)
        os.system(f'vina --config ./docking_config/config_singledock_{ligand} --out ../docking/output/pdbqt/{ligand}.pdbqt')
        os.system(f'obabel -ipdbqt ../docking/output/pdbqt/{ligand}.pdbqt -opdb -O ../docking/output/pdb/{ligand}_.pdb -m')

for ligand in os.listdir('../docking/output/pdb'):
    ligand.split('_')[0]
    if ligand == arg:
        os.system(f'obabel -ipdb ../docking/output/pdb/{ligand} -opdb -O ../docking/output/pdb/{ligand} -h')
