#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================================================
# extract the docking scores of ledock
# =================================================================================================

import os, sys, glob, csv
import pandas as pd
import multiprocessing
from multiprocessing import Manager
# from multiprocessing.dummy import Pool


def ledock_score_extract(pdbname, ligname, label, i, return_dict):
    lines0 = open('%s/myligands_%s/%s.sdf' % (pdbname, label, ligname), 'r').readlines()
    molname = lines0[0].strip()
    
    lines = open('%s/%s_%s_ledock/%s/%s.dok' % (pdbname, pdbname, label, ligname, ligname), 'r').readlines()
    molscore = lines[1].split()[-2].strip()
    return_dict[i] = [molname, molscore]


def interagte_result(pdbname, label):
    lignames = [x for x in os.listdir('./%s/%s_%s_ledock' % (pdbname, pdbname, label)) if
                os.path.isdir('./%s/%s_%s_ledock/%s' % (pdbname, pdbname, label, x))]
    manger = Manager()
    return_dict = manger.dict()
    pool = multiprocessing.Pool(32)
    jobs = []
    for ligname in lignames:
        im = lignames.index(ligname)
        p = pool.apply_async(ledock_score_extract, args=(pdbname, ligname, label, im, return_dict))
        jobs.append(p)
    pool.close()
    pool.join()
    mycsv = open('%s/%s_%s_ledock/%s_%s_ledock_score.csv' % (pdbname, pdbname, label, pdbname, label), 'w')
    mycsvwriter = csv.writer(mycsv)
    header = ['molname', 'ledock_score']
    mycsvwriter.writerow(header)
    for item_ in return_dict.values():
        mycsvwriter.writerow(item_)
    mycsv.close()


def main():
    names = [x for x in os.listdir('.') if os.path.isdir(x)]
    #names = ['fa7']
    for name in names:
        interagte_result(name, 'actives')
        interagte_result(name, 'decoys')


if __name__ == '__main__':
    main()
