#!/user/bin python
# -*- coding: utf-8 -*-

# ========================================================================
# pafnucy
# ========================================================================

import os, csv, sys, glob
import multiprocessing
from multiprocessing import Manager
# from multiprocessing.dummy import Pool


def pafnucy_perform(pdbname, ligname, label, i, return_dict):
    mylist = []
    molname = open('%s/%s_%s_gold_chemplp/%s/%s_top1.sdf' % (pdbname, pdbname, label, ligname, ligname), 'r').readlines()[
        0].split('|')[0].strip()
    for n in range(1, 4):
        print('%s_%s_%s_%s' % (pdbname, label, ligname, n))
        if os.path.exists('%s/%s_%s_gold_chemplp/%s/%s_top%s.sdf' % (pdbname, pdbname, label, ligname, ligname, n)):
            cmdline = 'cd %s/%s_%s_gold_chemplp/%s &&' % (pdbname, pdbname, label, ligname)
            cmdline += 'python2 /home/shenchao/AI_evaluation/software/pafnucy/pafnucy-master/prepare.py --ligand %s_top%s.sdf --pocket ../../%s_prot/%s_p.pdb --ligand_format sdf --pocket_format pdb --output %s_top%s.hdf &&'%(ligname, n, pdbname, pdbname, ligname, n)
            cmdline += 'python2 /home/shenchao/AI_evaluation/software/pafnucy/pafnucy-master/predict.py -i %s_top%s.hdf -o %s_top%s_pafnucy.csv -n /home/shenchao/AI_evaluation/software/pafnucy/pafnucy-master/results/batch5-2017-06-05T07_58_47-best'%(ligname, n, ligname, n)
            os.system(cmdline)
            molscore = None
            if os.path.exists('%s/%s_%s_gold_chemplp/%s/%s_top%s_pafnucy.csv'%(pdbname, pdbname, label, ligname, ligname, n)):
			    molscore = open('%s/%s_%s_gold_chemplp/%s/%s_top%s_pafnucy.csv'%(pdbname, pdbname, label, ligname, ligname, n), 'r').readlines()[1].split(',')[-1].strip()
            mylist.append([molname, ligname, 'top%s' % n, molscore])
    return_dict[i] = mylist

    os.remove('%s/%s_%s_gold_chemplp/%s/%s_top1.hdf' % (pdbname, pdbname, label, ligname, ligname))
    os.remove('%s/%s_%s_gold_chemplp/%s/%s_top1_pafnucy.csv' % (pdbname, pdbname, label, ligname, ligname))
    os.remove('%s/%s_%s_gold_chemplp/%s/%s_top2.hdf' % (pdbname, pdbname, label, ligname, ligname))
    os.remove('%s/%s_%s_gold_chemplp/%s/%s_top2_pafnucy.csv' % (pdbname, pdbname, label, ligname, ligname))
    os.remove('%s/%s_%s_gold_chemplp/%s/%s_top3.hdf' % (pdbname, pdbname, label, ligname, ligname))
    os.remove('%s/%s_%s_gold_chemplp/%s/%s_top3_pafnucy.csv' % (pdbname, pdbname, label, ligname, ligname))


def interagte_result(pdbname, label):
    lignames = [x for x in os.listdir('./%s/%s_%s_gold_chemplp' % (pdbname, pdbname, label)) if
                os.path.isdir('./%s/%s_%s_gold_chemplp/%s' % (pdbname, pdbname, label, x))]
    manger = Manager()
    return_dict = manger.dict()
    pool = multiprocessing.Pool(40)
    jobs = []
    for ligname in lignames:
        im = lignames.index(ligname)
        p = pool.apply_async(pafnucy_perform, args=(pdbname, ligname, label, im, return_dict))
        jobs.append(p)
    pool.close()
    pool.join()
    mycsv = open('%s/%s_%s_gold_chemplp/%s_%s_gold_chemplp_pafnucy_score.csv' % (pdbname, pdbname, label, pdbname, label),
                 'w')
    mycsvwriter = csv.writer(mycsv)
    header = ['molname', 'ligid', 'topn', 'molscore']
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

