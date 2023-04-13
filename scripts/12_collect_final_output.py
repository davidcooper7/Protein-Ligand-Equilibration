import os, sys

arg = sys.argv[1]

if 'final' not in os.listdir('..'):
    os.mkdir('../final')

if arg not in os.listdir('../final'):
    os.mkdir(f'../final/{arg}')

# collect system files 
for analogue in os.listdir(f'../equil/output'):
    if analogue == arg:
        for pose in os.listdir(f'../equil/output/{analogue}'):
            os.system(f'cp ../equil/output/{analogue}/{pose}/{analogue}_{pose}.pdb ../final/{analogue}/{analogue}_{pose}.pdb')
            print(f'{analogue}_{pose} added')
            ##move para for pose == 1
            if pose == '1':
                os.system(f'cp ../equil/para/post_equil/{analogue}* ../final/{analogue}/')
            
        ##move solvent files 

        os.system(f'cp ../water/equil/step5/solvent_{analogue}_1.pdb ../final/{analogue}/solvent_{analogue}.pdb')
        os.system(f'cp ../water/para/post_equil/solvent_{analogue}* ../final/{analogue}')
    
    
        
