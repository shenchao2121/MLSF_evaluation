#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================================================
# prepare the protein
# =================================================================================================

import os, sys, glob, csv
# import multiprocessing
##from multiprocessing.dummy import Pool
from ccdc.protein import Protein
from ccdc.io import MoleculeWriter

def prepare_protein(name):
    orign_protfile = '%s/%s_prot/%s_p.pdb' % (name, name, name)
    #orign_protfile = '%s/%s_prot/%s_p.mol2' % (name, name, name)
    
    mol = Protein.from_file(orign_protfile)
    ##name = os.path.basename(orign_protfile).split('_')[0]
    mol.remove_all_waters()
    mol.remove_unknown_atoms()
    mol.add_hydrogens()
    with MoleculeWriter('%s/%s_prot/%s_goldp.pdb' % (name, name, name)) as protein_writer:
        protein_writer.write(mol)


def main(name):
	prepare_protein(name)



if __name__ == '__main__':
    name = sys.argv[1]
    main(name)










