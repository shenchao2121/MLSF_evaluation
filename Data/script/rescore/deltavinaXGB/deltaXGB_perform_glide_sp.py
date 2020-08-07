#!/user/bin python
# -*- coding: utf-8 -*-

# ========================================================================
# deltavinaXGB
# ========================================================================

import os, csv, sys, glob
import multiprocessing
from multiprocessing import Manager


# from multiprocessing.dummy import Pool


def deltavina_perform(pdbname, ligname, label, i, return_dict):
    mylist = []
    molname = open('%s/%s_%s_glide_SP/%s/%s_top1.sdf' % (pdbname, pdbname, label, ligname, ligname), 'r').readlines()[
        0].strip()
    for n in range(1, 2):
        print('%s_%s_%s_%s' % (pdbname, label, ligname, n))
        cmdline = 'cd %s/%s_%s_glide_SP/%s &&' % (pdbname, pdbname, label, ligname)
        cmdline += 'mkdir -p %s_top%s_cal &&' % (ligname, n)
        cmdline += 'cp %s_top%s.sdf %s_top%s_cal/%s_ligand.sdf &&' % (ligname, n, ligname, n, pdbname)
        cmdline += 'cp ../../%s_prot/%s_p.pdb %s_top%s_cal/%s_protein.pdb &&' % (pdbname, pdbname, ligname, n, pdbname)
        cmdline += 'cp %s_top%s_cal/%s_protein.pdb %s_top%s_cal/%s_protein_all.pdb &&' % (
        ligname, n, pdbname, ligname, n, pdbname)
        cmdline += 'python /home/shenchao/AI_evaluation/software/deltaVinaXGB/build/lib/DXGB/run_DXGB.py '
        cmdline += '--modeldir /home/shenchao/AI_evaluation/software/deltaVinaXGB/Model '
        cmdline += '--runfeatures --datadir %s/%s/%s_%s_glide_SP/%s/%s_top%s_cal --pdbid %s --average' % (
        os.getcwd(), pdbname, pdbname, label, ligname, ligname, n, pdbname)
        os.system(cmdline)
        molscore_vina = \
        open('%s/%s_%s_glide_SP/%s/%s_top%s_cal/score.csv' % (pdbname, pdbname, label, ligname, ligname, n),
             'r').readlines()[1].split(',')[1].strip()
        molscore_XGB = \
        open('%s/%s_%s_glide_SP/%s/%s_top%s_cal/score.csv' % (pdbname, pdbname, label, ligname, ligname, n),
             'r').readlines()[1].split(',')[-1].strip()
        mylist.append([molname, ligname, 'top%s' % n, molscore_vina, molscore_XGB])
    return_dict[i] = mylist
    
    cmdline = 'cd %s/%s/%s_%s_glide_SP/%s &&' % (os.getcwd(), pdbname, pdbname, label, ligname)
    cmdline += 'rm -rf %s_top*_cal' % (ligname)
    os.system(cmdline)


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
    mycsv = open('%s/%s_%s_glide_SP/%s_%s_glide_SP_deltaXGB_score.csv' % (pdbname, pdbname, label, pdbname, label),
                 'w')
    mycsvwriter = csv.writer(mycsv)
    header = ['molname', 'ligid', 'topn', 'deltavina_score', 'deltaXGB_score']
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
