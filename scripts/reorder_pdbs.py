def reorder(input_filepath, output_filepath):
    with open(input_filepath, 'r') as f:
        org_lines = f.readlines()
        f.close
    ligand_lines = ['']
    prot_lines = ['']
    other_lines = ['']
    crystal_line = ''
    for line in org_lines:
        if line.find('UNL') != -1:
            ligand_lines.append(line)
        elif line.find(' R ') != -1:
            prot_lines.append(line)
        elif line.find('HEADER') != -1 or line.find('TITLE') != -1:
            pass
        elif line.find('CRYST') != -1:
            crystal_line = crystal_line + line
        else:
            other_lines.append(line)

    with open(output_filepath, 'w') as f:
        f.write(crystal_line)
        for line in prot_lines:
            f.write(line)
        for line in ligand_lines:
            f.write(line)
        for line in other_lines:
            f.write(line)
        f.close()

############################
import os, sys

arg = sys.argv[1]

for lig in os.listdir('../equil/output/'):
    if lig == arg:
        for pose in os.listdir(f'../equil/output/{lig}'):
            in_pdb = f'../equil/output/{lig}/{pose}/{lig}{pose}.pdb'
            out_pdb = f'../equil/output/{lig}/{pose}/{lig}_{pose}.pdb'
            reorder(input_filepath=in_pdb, output_filepath=out_pdb)
            print(f'{lig}_{pose}')

