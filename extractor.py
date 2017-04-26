import argparse
import os
import shutil
import subprocess

from Bio.PDB import PDBParser, PDBIO
from Bio.PDB.Residue import Residue
from Bio.PDB.Chain import Chain

from config import DPOCKET_EXEC

parser = argparse.ArgumentParser()
parser.add_argument(
    'pdb',
    type=str,
    help='PDB file to extract descriptors from'
)
parser.add_argument(
    'entities',
    type=str,
    nargs='+',
    help=('One or more atoms or residues in the format of '
          '{model}/{chain}/{resnum}/{inscode}/[{atomname}]')
)

args = parser.parse_args()
mod_pdb = args.pdb + '_mod'
dpocket_prefix = os.path.split(args.pdb)[-1].replace('.', '_')

structure = PDBParser().get_structure('_', args.pdb)

# FAKE RESIDUE FOR DPOCKET POCKET DEFINITION
fake = Residue(('H_STP', 9999, ' '), 'STP', 1)
atom_counter = 0

for entity in args.entities:

    entity = entity.strip('/').split('/')
    atoms = []

    # RESIDUE
    if len(entity) == 4:

        model, chain, resnum, inscode = entity
        residue = structure[int(model)][chain][(' ', int(resnum),
                                           inscode if inscode else ' ')]

        atoms = list(residue.get_list())

    # ATOM
    elif len(entity) == 5:

        model, chain, resnum, inscode, atomname = entity
        atom = structure[int(model)][chain][(' ', int(resnum),
                                        inscode if inscode else ' ')][atomname]

        atoms.append(atom)

    for atom in atoms:

        # MAKE A FAKE ATOM FROM THE REAL ONE,
        # AND ADD THIS TO THE FAKE RESIDUE
        copy = atom.copy()

        copy.id = 'X' + str(atom_counter)
        copy.element = 'H'
        copy.name = 'X'
        copy.serial_number = max(
            [a.serial_number for a in structure.get_atoms()]) + 1

        copy.detach_parent()
        fake.add(copy)
        atom_counter += 1

# ADD FAKE RESIDUE TO FIRST CHAIN IN STRUCTURE
structure[0].get_list()[0].add(fake)

io = PDBIO()
io.set_structure(structure)
io.save(mod_pdb)

# MAKE THE DPOCKET INPUT FILE
input_file = mod_pdb + '.input'

with open(input_file, 'w') as fo:
    fo.write('{}\tSTP'.format(mod_pdb))

# RUN DPOCKET USING PDB WITH FAKE LIGAND
subprocess.call(
    '''{} -f {} -E -d 0.1 -o {}'''.format(
        DPOCKET_EXEC, input_file, dpocket_prefix),
    shell=True
)

# REMOVE OR MOVE OUTPUT FILES
try:
    os.remove('{}_fp.txt'.format(dpocket_prefix))
except:
    pass

try:
    os.remove('{}_fpn.txt'.format(dpocket_prefix))
except:
    pass

try:
    shutil.move(
        '{}_exp.txt'.format(dpocket_prefix),
        os.path.split(args.pdb)[0] or '.'
    )
except:
    pass
