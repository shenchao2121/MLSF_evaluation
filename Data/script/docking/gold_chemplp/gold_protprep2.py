#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================================================
# prepare the protein
# =================================================================================================

import os, sys, glob, csv
# import multiprocessing
from multiprocessing.dummy import Pool

def prepare_protein(name):
	cmdline = 'module load ccdc &&'
	cmdline += 'export CCDC_PYTHON_API_NO_QAPPLICATION=10 &&'
	cmdline += 'python gold_protprep1.py %s'%name
	os.system(cmdline)



def main():
    names = [x for x in os.listdir('.') if os.path.isdir(x)]
    pool = Pool(32)
    pool.map(prepare_protein, names)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()










