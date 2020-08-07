#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================================================
# extract the top three poses of ledock
# =================================================================================================

import os, sys, glob, csv
# import pandas as pd
import multiprocessing
# from multiprocessing import Manager
from multiprocessing.dummy import Pool


def split_lig(pdbname, ligname, label):
    fileContent = open('%s/%s_%s_ledock/%s/%s.dok' % (pdbname, pdbname, label, ligname, ligname), 'r').read()
    paraList = fileContent.split('END\n')
    paraList.remove(paraList[-1])
    for para in paraList[:3]:
        fileWriter = open('%s/%s_%s_ledock/%s/%s_top%d.pdb' % (
            pdbname, pdbname, label, ligname, ligname, paraList.index(para) + 1), 'w')
        fileWriter.write(para + 'END\n')
        fileWriter.close()

    cmdline = 'cd %s/%s_%s_ledock/%s &&' % (pdbname, pdbname, label, ligname)
    cmdline += 'module load openeye &&'
    cmdline += 'convert.py %s_top1.pdb %s_top1.sdf &&' % (ligname, ligname)
    cmdline += 'convert.py %s_top2.pdb %s_top2.sdf &&' % (ligname, ligname)
    cmdline += 'convert.py %s_top3.pdb %s_top3.sdf &&' % (ligname, ligname)
    cmdline += 'rm %s_top1.pdb &&' % ligname
    cmdline += 'rm %s_top2.pdb &&' % ligname
    cmdline += 'rm %s_top3.pdb' % ligname
    os.system(cmdline)


def main():
    pdbnames = [x for x in os.listdir('.') if os.path.isdir(x)]
    #pdbnames = ['fa7']
    for pdbname in pdbnames:
        lignames_actives = [x for x in os.listdir('./%s/%s_actives_ledock' % (pdbname, pdbname)) if
                            os.path.isdir('%s/%s_actives_ledock/%s' % (pdbname, pdbname, x))]
        pool = multiprocessing.Pool(32)
        jobs = []
        for ligname in lignames_actives:
            p = pool.apply_async(split_lig, (pdbname, ligname, 'actives'))
            jobs.append(p)
        pool.close()
        pool.join()

        lignames_decoys = [x for x in os.listdir('./%s/%s_decoys_ledock' % (pdbname, pdbname)) if
                           os.path.isdir('%s/%s_decoys_ledock/%s' % (pdbname, pdbname, x))]
        pool = multiprocessing.Pool(32)
        jobs = []
        for ligname in lignames_decoys:
            p = pool.apply_async(split_lig, (pdbname, ligname, 'decoys'))
            jobs.append(p)
        pool.close()
        pool.join()


if __name__ == '__main__':
    main()
