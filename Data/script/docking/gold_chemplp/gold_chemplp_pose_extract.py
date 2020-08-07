#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================================================
# extract the top three poses of gold chemplp
# =================================================================================================

import os, sys, glob, csv
# import pandas as pd
import multiprocessing
# from multiprocessing import Manager
from multiprocessing.dummy import Pool


def split_lig(pdbname, ligname, label):
    fileContent = open('%s/%s_%s_gold_chemplp/%s/total_chemplp.sdf' % (pdbname, pdbname, label, ligname), 'r').read()
    paraList = fileContent.split('$$$$\n')
    paraList.remove(paraList[-1])
    for para in paraList[:3]:
        fileWriter = open('%s/%s_%s_gold_chemplp/%s/%s_top%d.sdf' % (
        pdbname, pdbname, label, ligname, ligname, paraList.index(para) + 1), 'w')
        fileWriter.write(para + '$$$$\n')
        fileWriter.close()

def main():
    pdbnames = [x for x in os.listdir('.') if os.path.isdir(x)]
    #pdbnames = ['fa7']
    for pdbname in pdbnames:
        lignames_actives = [x for x in os.listdir('./%s/%s_actives_gold_chemplp' % (pdbname, pdbname)) if
                            os.path.isdir('%s/%s_actives_gold_chemplp/%s' % (pdbname, pdbname, x))]
        pool = multiprocessing.Pool(32)
        jobs = []
        for ligname in lignames_actives:
            p = pool.apply_async(split_lig, (pdbname, ligname, 'actives'))
            jobs.append(p)
        pool.close()
        pool.join()
        lignames_decoys = [x for x in os.listdir('./%s/%s_decoys_gold_chemplp' % (pdbname, pdbname)) if
                            os.path.isdir('%s/%s_decoys_gold_chemplp/%s' % (pdbname, pdbname, x))]
        pool = multiprocessing.Pool(32)
        jobs = []
        for ligname in lignames_decoys:
            p = pool.apply_async(split_lig, (pdbname, ligname, 'decoys'))
            jobs.append(p)
        pool.close()
        pool.join()


if __name__ == '__main__':
    main()
