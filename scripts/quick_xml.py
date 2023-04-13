
import os, sys

# USAGE quick_xml.py yourpdb.pdb net_charge_as_int
#ASSUMING YOU ALREADY HAVE A LIGAND WITH HYDROGENS
#USE A FULL PATH

arg = sys.argv[1]
input = '../docking/output/pdb/'+arg
input_name = arg.split('.')[0]

if 'lig_xml' not in os.listdir('../input'):
    os.mkdir('../input/lig_xml')
output = f'../input/lig_xml/{input_name}'
try:    
    pdb_input = input_name
    name = pdb_input.replace('.pdb','')
    nc = int(sys.argv[2])
except:
    raise Exception("Check Usage")

if os.path.isfile(f"{output}.ff.xml"):
    raise Exception("xml already exist")

s_ante = f"antechamber -fi pdb -fo mol2 -i {input} -o {output}.mol2 -c bcc -pf y -nc {nc}"

os.system(s_ante)

s_parm = f"parmchk2 -i {output}.mol2 -o {output}.frcmod -f mol2"

os.system(s_parm)

s_leap = f"""source leaprc.gaff2
mol = loadmol2 {output}.mol2
loadamberparams {output}.frcmod
saveamberparm mol {output}.prmtop {output}.inpcrd
quit"""

with open('run_tleap.in', 'w') as f:
    f.write(s_leap)

os.system("tleap -s -f run_tleap.in")

s_json = ["{",
         f'    "fname_prmtop" : "{output}.prmtop",',
         f'    "fname_xml" : "{output}.ff.xml",',
          '    "ff_prefix" : "lig"',
          '}']

with open('run_python.json', 'w') as g:
    g.writelines(s_json)

os.system("python ./write_xml_pretty.py -i run_python.json")
