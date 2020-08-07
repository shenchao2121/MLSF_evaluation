#!/user/bin python
# -*- coding: utf-8 -*-

# ========================================================================
# rfscore-vs
# ========================================================================

import os, csv, sys, glob
import multiprocessing
from multiprocessing import Manager
# from multiprocessing.dummy import Pool


def rfscorevs_perform(pdbname, ligname, label, i, return_dict):
    mylist = []
    molname = open('%s/%s_%s_gold_chemplp/%s/%s_top1.sdf' % (pdbname, pdbname, label, ligname, ligname), 'r').readlines()[
        0].split('|')[0].strip()
    for n in range(1, 4):
        cmdline = 'cd %s/%s_%s_gold_chemplp/%s &&' % (pdbname, pdbname, label, ligname)
        cmdline += '/home/shenchao/AI_evaluation/software/rfscore-vs/rf-score-vs_v1.0.1/rf-score-vs %s_top%s.sdf -n 1 -isdf -ocsv -O %s_top%s.csv --receptor ../../%s_prot/%s_p.pdb --field RFScoreVS_v2'%(ligname, n, ligname, n, pdbname, pdbname)
        os.system(cmdline)
        molscore = open('%s/%s_%s_gold_chemplp/%s/%s_top%s.csv' % (pdbname, pdbname, label, ligname, ligname, n), 'r').readlines()[1].strip()
        mylist.append([molname, ligname, 'top%s' % n, molscore])

    os.remove('%s/%s_%s_gold_chemplp/%s/%s_top1.csv' % (pdbname, pdbname, label, ligname, ligname))
    os.remove('%s/%s_%s_gold_chemplp/%s/%s_top2.csv' % (pdbname, pdbname, label, ligname, ligname))
    os.remove('%s/%s_%s_gold_chemplp/%s/%s_top3.csv' % (pdbname, pdbname, label, ligname, ligname))
    return_dict[i] = mylist


def interagte_result(pdbname, label):
    lignames = [x for x in os.listdir('./%s/%s_%s_gold_chemplp' % (pdbname, pdbname, label)) if
                os.path.isdir('./%s/%s_%s_gold_chemplp/%s' % (pdbname, pdbname, label, x))]
    manger = Manager()
    return_dict = manger.dict()
    pool = multiprocessing.Pool(32)
    jobs = []
    for ligname in lignames:
        im = lignames.index(ligname)
        p = pool.apply_async(rfscorevs_perform, args=(pdbname, ligname, label, im, return_dict))
        jobs.append(p)
    pool.close()
    pool.join()
    mycsv = open('%s/%s_%s_gold_chemplp/%s_%s_gold_chemplp_rfscorevs_score.csv' % (pdbname, pdbname, label, pdbname, label),
                 'w')
    mycsvwriter = csv.writer(mycsv)
    header = ['molname', 'ligid', 'topn', 'rfscorevs_score']
    mycsvwriter.writerow(header)
    for item_s in return_dict.values():
        for item_ in item_s:
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
