#!/user/bin python
# -*- coding: utf-8 -*-

# ========================================================================
# rfscorev4
# ========================================================================

import os, csv, sys, glob
import multiprocessing
from multiprocessing import Manager


# from multiprocessing.dummy import Pool

def prot_pre(name):
    cmdline = 'module purge &&'
    cmdline += 'module load vina &&'
    cmdline += 'cd %s/%s_prot &&' % (name, name)
    cmdline += 'prepare_receptor4.py -r %s_p.pdb -o %s_p.pdbqt -A checkhydrogens -U nphs_lps_waters_nonstdres' % (
        name, name)
    os.system(cmdline)


def rfscore_perform(pdbname, ligname, label, i, return_dict):
    mylist = []
    molname = open('%s/%s_%s_glide_SP/%s/%s_top1.sdf' % (pdbname, pdbname, label, ligname, ligname), 'r').readlines()[
        0].strip()
    for n in range(1, 4):
        if not os.path.exists('%s/%s_%s_glide_SP/%s/%s_top%s.pdbqt' % (pdbname, pdbname, label, ligname, ligname, n)):
            cmdline = 'cd %s/%s_%s_glide_SP/%s &&' % (pdbname, pdbname, label, ligname)
            cmdline += 'module load openbabel &&'
            cmdline += 'babel -isd %s_top%s.sdf -omol2 %s_top%s.mol2 &&' % (ligname, n, ligname, n)
            cmdline += 'module purge &&'
            cmdline += 'module load vina &&'
            cmdline += 'prepare_ligand4.py -l %s_top%s.mol2 -o %s_top%s.pdbqt -A checkhydrogens' % (
            ligname, n, ligname, n)
            os.system(cmdline)

        if os.path.exists('%s/%s_%s_glide_SP/%s/%s_top%s.mol2' % (pdbname, pdbname, label, ligname, ligname, n)):
            cmdline = 'cd %s/%s_%s_glide_SP/%s &&' % (pdbname, pdbname, label, ligname)
            cmdline += '/home/shenchao/AI_evaluation/software/rf-score-4/rf-score /home/shenchao/AI_evaluation/software/rf-score-4/pdbbind-2013-refined.rf ../../%s_prot/%s_p.pdbqt %s_top%s.pdbqt' % (
                pdbname, pdbname, ligname, n)
            molscore413 = os.popen(cmdline).read().strip()

            cmdline = 'cd %s/%s_%s_glide_SP/%s &&' % (pdbname, pdbname, label, ligname)
            cmdline += '/home/shenchao/AI_evaluation/software/rf-score-4/rf-score /home/shenchao/AI_evaluation/software/rf-score-4/pdbbind-2014-refined.rf ../../%s_prot/%s_p.pdbqt %s_top%s.pdbqt' % (
                pdbname, pdbname, ligname, n)
            molscore414 = os.popen(cmdline).read().strip()

            mylist.append([molname, ligname, 'top%s' % n, molscore413, molscore414])
    # os.remove('%s/%s_%s_glide_SP/%s/%s_top1.mol2' % (pdbname, pdbname, label, ligname, ligname))
    # os.remove('%s/%s_%s_glide_SP/%s/%s_top1.pdbqt' % (pdbname, pdbname, label, ligname, ligname))
    # os.remove('%s/%s_%s_glide_SP/%s/%s_top2.mol2' % (pdbname, pdbname, label, ligname, ligname))
    # os.remove('%s/%s_%s_glide_SP/%s/%s_top2.pdbqt' % (pdbname, pdbname, label, ligname, ligname))
    # os.remove('%s/%s_%s_glide_SP/%s/%s_top3.mol2' % (pdbname, pdbname, label, ligname, ligname))
    # os.remove('%s/%s_%s_glide_SP/%s/%s_top3.pdbqt' % (pdbname, pdbname, label, ligname, ligname))
    return_dict[i] = mylist


def interagte_result(pdbname, label):
    lignames = [x for x in os.listdir('./%s/%s_%s_glide_SP' % (pdbname, pdbname, label)) if
                os.path.isdir('./%s/%s_%s_glide_SP/%s' % (pdbname, pdbname, label, x))]
    manger = Manager()
    return_dict = manger.dict()
    pool = multiprocessing.Pool(32)
    jobs = []
    for ligname in lignames:
        im = lignames.index(ligname)
        p = pool.apply_async(rfscore_perform, args=(pdbname, ligname, label, im, return_dict))
        jobs.append(p)
    pool.close()
    pool.join()
    mycsv = open('%s/%s_%s_glide_SP/%s_%s_glide_SP_rfscore4_score.csv' % (pdbname, pdbname, label, pdbname, label),
                 'w')
    mycsvwriter = csv.writer(mycsv)
    header = ['molname', 'ligid', 'topn', 'rfscore4_2013_score', 'rfscore4_2014_score']
    mycsvwriter.writerow(header)
    for item_s in return_dict.values():
        for item_ in item_s:
            mycsvwriter.writerow(item_)
    mycsv.close()


def main():
    names = [x for x in os.listdir('.') if os.path.isdir(x)]
    #names = ['fa7']
    # names = ['inha']
    for name in names:
        if not os.path.basename('%s/%s_prot/%s_p.pdbqt' % (name, name, name)):
            prot_pre(name)
        interagte_result(name, 'actives')
        interagte_result(name, 'decoys')


if __name__ == '__main__':
    main()	
