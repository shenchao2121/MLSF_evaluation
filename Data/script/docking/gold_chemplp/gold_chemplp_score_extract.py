#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================================================
# extract the docking scores of gold_chemplp
# =================================================================================================

import os, sys, glob, csv
import pandas as pd
import multiprocessing
from multiprocessing import Manager
# from multiprocessing.dummy import Pool


def gold_chemplp_score_extract(pdbname, ligname, label, i, return_dict):
    lines = open('%s/%s_%s_gold_chemplp/%s/total_chemplp.sdf' % (pdbname, pdbname, label, ligname), 'r').readlines()
    molname = lines[0].split('|')[0].strip()
    for line in lines:
        if line.startswith('> <Gold.PLP.Fitness>'):
            molscore = lines[lines.index(line) + 1].strip()
            break
    return_dict[i] = [molname, molscore]


def interagte_result(pdbname, label):
    lignames = [x for x in os.listdir('./%s/%s_%s_gold_chemplp' % (pdbname, pdbname, label)) if
                os.path.isdir('./%s/%s_%s_gold_chemplp/%s' % (pdbname, pdbname, label, x))]
    manger = Manager()
    return_dict = manger.dict()
    pool = multiprocessing.Pool(32)
    jobs = []
    for ligname in lignames:
        im = lignames.index(ligname)
        p = pool.apply_async(gold_chemplp_score_extract, args=(pdbname, ligname, label, im, return_dict))
        jobs.append(p)
    pool.close()
    pool.join()
    mycsv = open('%s/%s_%s_gold_chemplp/%s_%s_gold_chemplp_score.csv' % (pdbname, pdbname, label, pdbname, label), 'w')
    mycsvwriter = csv.writer(mycsv)
    header = ['molname', 'gold_chemplp_score']
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
