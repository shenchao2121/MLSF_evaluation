#!/user/bin python
# -*- coding: utf-8 -*-

# ========================================================================
# deltavina
# ========================================================================

import os, csv, sys, glob
import multiprocessing
from multiprocessing import Manager


# from multiprocessing.dummy import Pool


def deltavina_perform(pdbname, ligname, label, i, return_dict):
    mylist = []
    molname = open('%s/%s_%s_glide_SP/%s/%s_top1.sdf' % (pdbname, pdbname, label, ligname, ligname), 'r').readlines()[
        0].strip()
    for n in range(1, 4):
        print('%s_%s_%s_%s'%(pdbname, label, ligname, n))
        cmdline = 'cd %s/%s_%s_glide_SP/%s &&' % (pdbname, pdbname, label, ligname)
        cmdline += 'module load openbabel &&'
        cmdline += 'babel -isd %s_top%s.sdf -omol2 %s_top%s.mol2 &&' % (ligname, n, ligname, n)
        cmdline += 'dvrf20.py -r ../../%s_prot/%s_p.pdb -l %s_top%s.mol2' % (pdbname, pdbname, ligname, n)
        os.system(cmdline)
        molscore = open('%s/%s_%s_glide_SP/%s/output.csv' % (pdbname, pdbname, label, ligname), 'r').readlines()[1].split(',')[-1].strip()
        mylist.append([molname, ligname, 'top%s' % n, molscore])
    return_dict[i] = mylist

    filenames = os.listdir('%s/%s_%s_glide_SP/%s' % (pdbname, pdbname, label, ligname))
    for filename in filenames:
        if os.path.basename(filename) not in ['%s_top1.sdf' % ligname, '%s_top2.sdf' % ligname, '%s_top3.sdf' % ligname]:
            os.remove('%s/%s_%s_glide_SP/%s/%s' % (pdbname, pdbname, label, ligname, os.path.basename(filename)))


def interagte_result(pdbname, label):
    lignames = [x for x in os.listdir('./%s/%s_%s_glide_SP' % (pdbname, pdbname, label)) if
                os.path.isdir('./%s/%s_%s_glide_SP/%s' % (pdbname, pdbname, label, x))]
    manger = Manager()
    return_dict = manger.dict()
    pool = multiprocessing.Pool(32)
    jobs = []
    for ligname in lignames:
        im = lignames.index(ligname)
        p = pool.apply_async(deltavina_perform, args=(pdbname, ligname, label, im, return_dict))
        jobs.append(p)
    pool.close()
    pool.join()
    mycsv = open('%s/%s_%s_glide_SP/%s_%s_glide_SP_deltavina_score.csv' % (pdbname, pdbname, label, pdbname, label),
                 'w')
    mycsvwriter = csv.writer(mycsv)
    header = ['molname', 'ligid', 'topn', 'deltavina_score']
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
