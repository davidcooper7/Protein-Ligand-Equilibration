from openmm.app import *
from openmm import *
from openmm.unit import *
from sys import stdout
import numpy as np


def write_pdb(fname_pdb, fname_pdb_new, crds, box=None):
    f_pdb = open(fname_pdb)
    l_pdb = f_pdb.read().split('\n')
    f_pdb.close()

    fout = open(fname_pdb_new, 'w', 1)

    iat = 0
    for line in l_pdb[:-1]:
        if line[:6] in ['ATOM  ', 'HETATM']:
            x, y, z = crds[iat]  # .value_in_unit(unit.angstrom)
            sx = ("%8.3f" % x)[:8]
            sy = ("%8.3f" % y)[:8]
            sz = ("%8.3f" % z)[:8]
            sline = line[:30]+sx+sy+sz+line[54:]
            print(sline, file=fout)
            iat += 1
        elif line[:6] in ['CRYST1']:
            if box is None:
                print(line, file=fout)
            else:
                x, y, z = box[0][0], box[1][1], box[2][2]
                sx = ("%9.3f" % x)[:9]
                sy = ("%9.3f" % y)[:9]
                sz = ("%9.3f" % z)[:9]
                sline = line[:6]+sx+sy+sz+line[33:]
                print(sline, file=fout)
        elif len(line) == 0:
            continue
        elif len(line) > 0 and line[0] == ' ':
            continue
        else:
            print(line, file=fout)
    fout.close()


def get_positions_from_pdb(fname_pdb):
    nameMembrane = ['DPP', 'POP']
    f_pdb = open(fname_pdb)
    l_pdb = f_pdb.read().split('\n')
    f_pdb.close()

    coords = []
    prt_heavy_atoms = []
    mem_heavy_atoms = []
    iatom = 0
    for line in l_pdb[:-1]:
        if line[:6] in ['ATOM  ', 'HETATM']:
            words = line[30:].split()
            x = float(words[0])
            y = float(words[1])
            z = float(words[2])

            coords.append(Vec3(x, y, z))

            if line[17:20] in nameMembrane and words[-1] != 'H':
                mem_heavy_atoms.append(iatom)
            elif line[:6] in ['ATOM  '] and words[-1] != 'H':
                prt_heavy_atoms.append(iatom)
            
            iatom += 1

    return np.array(coords), prt_heavy_atoms, mem_heavy_atoms


def run_nvt(options):

    prmtop = AmberPrmtopFile(options['prmtop'])
    crds_A, prt_heavy_atoms, mem_heavy_atoms = get_positions_from_pdb(
        options['pdb'])

    system = prmtop.createSystem(nonbondedMethod=PME,
                                 nonbondedCutoff=1.2*nanometer,
                                 constraints=HBonds,
                                 rigidWater=True,
                                 ewaldErrorTolerance=0.0005)

    if "fc_pos" in options:
        # Restraints
        fc_pos = options['fc_pos']  # kJ/mol/nm^2
        prt_rest = CustomExternalForce('fc_pos*(px*px + py*py + pz*pz);\
                                px = abs(x - x0); \
                                py = abs(y - y0); \
                                pz = abs(z - z0);')

        prt_rest.addGlobalParameter('fc_pos', fc_pos)
        prt_rest.addPerParticleParameter('x0')
        prt_rest.addPerParticleParameter('y0')
        prt_rest.addPerParticleParameter('z0')

        for iatom in prt_heavy_atoms:
            x, y, z = crds_A[iatom]/10
            prt_rest.addParticle(iatom, [x, y, z])
        system.addForce(prt_rest)

        mem_rest = CustomExternalForce('fc_pos*(pz*pz);\
                                pz = abs(z - z0);')

        mem_rest.addGlobalParameter('fc_pos', fc_pos)
        mem_rest.addPerParticleParameter('z0')
        for iatom in mem_heavy_atoms:
            x, y, z = crds_A[iatom]/10
            mem_rest.addParticle(iatom, [z])
        system.addForce(mem_rest)

    dt = 1.0
    if "dt_fs" in options:
        dt = options['dt_fs']

    temp = 300.0
    if 'Temperature' in options:
        temp = options['Temperature']

    integrator = LangevinIntegrator(
        temp*kelvin, 1.0/picosecond, dt*femtoseconds)

    if "Platform" in options:
        if options["Platform"] == 'OpenCL':
            platform = Platform.getPlatformByName('OpenCL')
            properties = {'OpenCLPrecision': 'mixed'}
            simulation = Simulation(prmtop.topology, system,
                                    integrator, platform, properties)
        elif options["Platform"] == 'CUDA':
            platform = Platform.getPlatformByName('CUDA')
            properties = {'CudaPrecision': 'mixed'}
            simulation = Simulation(prmtop.topology, system,
                                    integrator, platform, properties)
        else:
            simulation = Simulation(prmtop.topology, system, integrator)
    else:  # CPU
        simulation = Simulation(prmtop.topology, system, integrator)

    simulation.context.setPositions(crds_A*0.1)  # A->nm

    simulation.context.setVelocitiesToTemperature(temp)

    nstep = 500000
    nstdout = 1000
    nstdcd = 5000
    freeze = False
    if 'totalSteps' in options:
        nstep = options['totalSteps']
    if 'nstdout' in options:
        nstdout = options['nstdout']
    if 'ndcd' in options:
        nstdcd = options['ndcd']
    if 'freeze_in' in options:
        freeze = options['freeze_in']
    
    
    simulation.reporters.append(app.StateDataReporter(options['stdout'],
                                                      nstdout,
                                                      step=True, time=True,
                                                      potentialEnergy=True,
                                                      temperature=True,
                                                      progress=False,
                                                      remainingTime=True,
                                                      speed=False,
                                                      volume=False,
                                                      totalSteps=nstep,
                                                      separator='     '))
    if 'dcd' in options:
        simulation.reporters.append(
            app.DCDReporter(options['dcd'], nstdcd))

    if not freeze: #IF Freeze is False or Undefined, simply run the simulation
        simulation.step(nstep)
    else: # IF Freeze is defined, it must be True to be this block
        steps = 0
        temp = 0.0
        simulation.context.setVelocitiesToTemperature(temp*kelvin)
        simulation.integrator.setTemperature(temp*kelvin)
        while steps < nstep:
            print(simulation.integrator.getTemperature())
            if temp < 300:
                simulation.step(1000)
                temp += 1
                simulation.context.setVelocitiesToTemperature(temp*kelvin)
                simulation.integrator.setTemperature(temp*kelvin)
                steps += 1000
            else:
                simulation.step(10000)
                
        
    state = simulation.context.getState(getPositions=True,
                                        enforcePeriodicBox=True)
    crds_A = state.getPositions(asNumpy=True).value_in_unit(angstrom)
    write_pdb(options['pdb'], options['save_pdb'], crds_A)

    if "save_state" in options:
        simulation.saveState(options['save_state'])


if __name__ == "__main__":
    import getopt
    import json

    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, "hi:",
                               ["help=", "input="])

    if len(opts) == 0:
        print('python AmberOpenMM.py -i <input json file> ')
        sys.exit(2)

    fname_json = 'input.json'
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('python AmberOpenMM.py -i <input json file> ')
            sys.exit(1)
        if opt in ("-i", "--ifile"):
            fname_json = arg

    with open(fname_json) as f:
        data = json.load(f)
        job = data['job']

        if job == 'min':
            run_min(data[job])
        elif job == 'nvt':
            run_nvt(data[job])
        elif job == 'npt':
            run_npt(data[job])
