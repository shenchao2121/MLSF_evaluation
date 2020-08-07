#!/user/bin python
# -*- coding: utf-8 -*-

# ========================================================================
# onionnet
# ========================================================================

import os, csv, sys, glob
import multiprocessing
from multiprocessing import Manager
# from multiprocessing.dummy import Pool


def onionnet_perform(pdbname, ligname, label, i, return_dict):
    mylist = []
    molname = open('%s/myligands_%s/%s.sdf' % (pdbname, label, ligname), 'r').readlines()[
        0].strip()
    for n in range(1, 2):
        print('%s_%s_%s_%s' % (pdbname, label, ligname, n))
        cmdline = 'cd %s/%s_%s_ledock/%s &&' % (pdbname, pdbname, label, ligname)
        cmdline += 'mkdir -p %s_top%s_onionnet &&' % (ligname, n)
        cmdline += 'cd %s_top%s_onionnet &&' % (ligname, n)
        cmdline += 'babel -isd ../%s_top%s.sdf -opdb %s_top%s.pdb &&' % (ligname, n, ligname, n)
        cmdline += 'cat ../../../%s_prot/%s_p.pdb | sed -n \'/^ATOM*/p\' > %s_c.pdb &&' % (pdbname, pdbname, pdbname)
        cmdline += 'cat %s_top%s.pdb | sed -n \'/^HETATM*/p\' >> %s_c.pdb &&' % (ligname, n, pdbname)
        cmdline += 'echo \'%s_c.pdb\' > input_complexes.dat &&' % pdbname
        cmdline += 'python /home/shenchao/AI_evaluation/software/onionnet/generate_features.py -inp input_complexes.dat -out features.csv -lig UNL &&'
        cmdline += 'python /home/shenchao/AI_evaluation/software/onionnet/predict_pKa.py -model /home/shenchao/AI_evaluation/software/onionnet/models/OnionNet_HFree.model -scaler /home/shenchao/AI_evaluation/software/onionnet/models/StandardScaler.model -fn features.csv -out output.csv'
        os.system(cmdline)
        molscore = \
        open('%s/%s_%s_ledock/%s/%s_top%s_onionnet/output.csv' % (pdbname, pdbname, label, ligname, ligname, n),
             'r').readlines()[1].split()[-1].strip()
        mylist.append([molname, ligname, 'top%s' % n, molscore])
    return_dict[i] = mylist

    cmdline = 'cd %s/%s/%s_%s_ledock/%s &&' % (os.getcwd(), pdbname, pdbname, label, ligname)
    cmdline += 'rm -rf %s_top*_onionnet' % (ligname)
    os.system(cmdline)


def interagte_result(pdbname, label):
    lignames = [x for x in os.listdir('./%s/%s_%s_ledock' % (pdbname, pdbname, label)) if
                os.path.isdir('./%s/%s_%s_ledock/%s' % (pdbname, pdbname, label, x))]
    manger = Manager()
    return_dict = manger.dict()
    pool = multiprocessing.Pool(32)
    jobs = []
    for ligname in lignames:
        im = lignames.index(ligname)
        p = pool.apply_async(onionnet_perform, args=(pdbname, ligname, label, im, return_dict))
        jobs.append(p)
    pool.close()
    pool.join()
    mycsv = open('%s/%s_%s_ledock/%s_%s_ledock_onionnet_score.csv' % (pdbname, pdbname, label, pdbname, label),
                 'w')
    mycsvwriter = csv.writer(mycsv)
    header = ['molname', 'ligid', 'topn', 'onionnet_score']
    mycsvwriter.writerow(header)
    for item_s in return_dict.values():
        for item_ in item_s:
            mycsvwriter.writerow(item_)
    mycsv.close()


def main():
    names = [x for x in os.listdir('.') if os.path.isdir(x)]
    #names = ['fa7']
    for name in names:
        if name not in []:
            interagte_result(name, 'actives')
            interagte_result(name, 'decoys')


if __name__ == '__main__':
    main()	
