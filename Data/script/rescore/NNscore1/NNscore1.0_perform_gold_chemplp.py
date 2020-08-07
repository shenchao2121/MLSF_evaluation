#!/user/bin python
# -*- coding: utf-8 -*-

# ========================================================================
# NNscore1.0
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


def NNscore1_perform(pdbname, ligname, label, i, return_dict):
    mylist = []
    molname = open('%s/%s_%s_gold_chemplp/%s/%s_top1.sdf' % (pdbname, pdbname, label, ligname, ligname), 'r').readlines()[
        0].split('|')[0].strip()
    for n in range(1, 4):
        print('%s_%s_%s_%s' % (pdbname, label, ligname, n))
        if not os.path.exists('%s/%s_%s_gold_chemplp/%s/%s_top%s.pdbqt' % (pdbname, pdbname, label, ligname, ligname, n)):
            cmdline = 'cd %s/%s_%s_gold_chemplp/%s &&' % (pdbname, pdbname, label, ligname)
            cmdline += 'module load openbabel &&'
            cmdline += 'babel -isd %s_top%s.sdf -omol2 %s_top%s.mol2 &&' % (ligname, n, ligname, n)
            cmdline += 'module purge &&'
            cmdline += 'module load vina &&'
            cmdline += 'prepare_ligand4.py -l %s_top%s.mol2 -o %s_top%s.pdbqt -A checkhydrogens' % (
            ligname, n, ligname, n)
            os.system(cmdline)

        if os.path.exists('%s/%s_%s_gold_chemplp/%s/%s_top%s.pdbqt' % (pdbname, pdbname, label, ligname, ligname, n)):
            cmdline = 'cd %s/%s_%s_gold_chemplp/%s &&' % (pdbname, pdbname, label, ligname)
            cmdline += 'python2 /home/shenchao/AI_evaluation/software/NNscore1/NNScore.py -receptor ../../%s_prot/%s_p.pdbqt -ligand %s_top%s.pdbqt -networks_dir /home/shenchao/AI_evaluation/software/NNscore1/networks/top_24_networks' % (
                pdbname, pdbname, ligname, n)
            lines = os.popen(cmdline).readlines()
            scores = locals()
            for k in range(1, 25):
                scores['molscore_net%s' % k] = None
                for line in lines:
                    if line.startswith('	Using network /home/shenchao/AI_evaluation/software/NNscore1/networks/top_24_networks/%s.net to predict binding:' % k):
                        scores['molscore_net%s' % k] = line.split(':')[-1].split('(')[0].strip()
            molscore_ave24 = None
            for line in lines:
                if line.startswith('Average score:'):
                    molscore_ave24 = line.split(':')[-1].split('(')[0].strip()

            cmdline = 'cd %s/%s_%s_gold_chemplp/%s &&' % (pdbname, pdbname, label, ligname)
            cmdline += 'python2 /home/shenchao/AI_evaluation/software/NNscore1/NNScore.py -receptor ../../%s_prot/%s_p.pdbqt -ligand %s_top%s.pdbqt -networks_dir /home/shenchao/AI_evaluation/software/NNscore1/networks/top_3_networks' % (
                pdbname, pdbname, ligname, n)
            lines2 = os.popen(cmdline).readlines()
            molscore_ave3 = None
            for line in lines2:
                if line.startswith('Average score:'):
                    molscore_ave3 = line.split(':')[-1].split('(')[0].strip()
        score_list = [molname, ligname, 'top%s' % n, molscore_ave3, molscore_ave24]
        for k in range(1, 25):
            score_list.append(scores['molscore_net%s' % k])
        
        mylist.append(score_list)
    return_dict[i] = mylist

    # os.remove('%s/%s_%s_gold_chemplp/%s/%s_top1.mol2' % (pdbname, pdbname, label, ligname, ligname))
    # os.remove('%s/%s_%s_gold_chemplp/%s/%s_top1.pdbqt' % (pdbname, pdbname, label, ligname, ligname))
    # os.remove('%s/%s_%s_gold_chemplp/%s/%s_top2.mol2' % (pdbname, pdbname, label, ligname, ligname))
    # os.remove('%s/%s_%s_gold_chemplp/%s/%s_top2.pdbqt' % (pdbname, pdbname, label, ligname, ligname))
    # os.remove('%s/%s_%s_gold_chemplp/%s/%s_top3.mol2' % (pdbname, pdbname, label, ligname, ligname))
    # os.remove('%s/%s_%s_gold_chemplp/%s/%s_top3.pdbqt' % (pdbname, pdbname, label, ligname, ligname))    


def interagte_result(pdbname, label):
    lignames = [x for x in os.listdir('./%s/%s_%s_gold_chemplp' % (pdbname, pdbname, label)) if
                os.path.isdir('./%s/%s_%s_gold_chemplp/%s' % (pdbname, pdbname, label, x))]
    manger = Manager()
    return_dict = manger.dict()
    pool = multiprocessing.Pool(32)
    jobs = []
    for ligname in lignames:
        im = lignames.index(ligname)
        p = pool.apply_async(NNscore1_perform, args=(pdbname, ligname, label, im, return_dict))
        jobs.append(p)
    pool.close()
    pool.join()
    mycsv = open('%s/%s_%s_gold_chemplp/%s_%s_gold_chemplp_NNscore1_score.csv' % (pdbname, pdbname, label, pdbname, label),
                 'w')
    mycsvwriter = csv.writer(mycsv)
    header = ['molname', 'ligid', 'topn', 'molscore_ave3', 'molscore_ave24']
    for k in range(1, 25):
        header.append('molscore_net%s' % k)
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

