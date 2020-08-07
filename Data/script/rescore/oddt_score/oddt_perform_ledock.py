#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================================================
# ODDT
# =================================================================================================

import os, sys, glob, csv
import multiprocessing
from multiprocessing import Manager
import pandas as pd
# from multiprocessing.dummy import Pool

def oddt_perform(pdbname, ligname, label, i, return_dict):
    mylist = []
    molname = open('%s/myligands_%s/%s.sdf' % (pdbname, label, ligname), 'r').readlines()[
        0].strip()
    
    for n in range(1, 4):
        print('%s_%s_%s_%s' % (pdbname, label, ligname, n))
        cmdline = 'cd %s/%s_%s_ledock/%s &&' % (pdbname, pdbname, label, ligname)
        cmdline += 'ln -s /home/shenchao/python_module2/oddt_model/*.pickle . &&'
        cmdline += '/home/shenchao/python_module2/bin/oddt_cli %s_top%s.sdf --receptor ../../%s_prot/%s_p.pdb ' % (
        ligname, n, pdbname, pdbname)
        cmdline += '--score rfscore_v1_pdbbind2007 '
        cmdline += '--score rfscore_v2_pdbbind2007 '
        cmdline += '--score rfscore_v3_pdbbind2007 '
        cmdline += '--score nnscore_pdbbind2007 '
        cmdline += '-O %s_top%s_oddt2007_out.sdf &&' % (ligname, n)
        cmdline += '/home/shenchao/python_module2/bin/oddt_cli %s_top%s.sdf --receptor ../../%s_prot/%s_p.pdb ' % (
        ligname, n, pdbname, pdbname)
        cmdline += '--score rfscore_v1_pdbbind2012 '
        cmdline += '--score rfscore_v2_pdbbind2012 '
        cmdline += '--score rfscore_v3_pdbbind2012 '
        cmdline += '--score nnscore_pdbbind2012 '
        cmdline += '-O %s_top%s_oddt2012_out.sdf &&' % (ligname, n)
        cmdline += '/home/shenchao/python_module2/bin/oddt_cli %s_top%s.sdf --receptor ../../%s_prot/%s_p.pdb ' % (
        ligname, n, pdbname, pdbname)
        cmdline += '--score rfscore_v1_pdbbind2013 '
        cmdline += '--score rfscore_v2_pdbbind2013 '
        cmdline += '--score rfscore_v3_pdbbind2013 '
        cmdline += '--score nnscore_pdbbind2013 '
        cmdline += '-O %s_top%s_oddt2013_out.sdf &&' % (ligname, n)
        cmdline += '/home/shenchao/python_module2/bin/oddt_cli %s_top%s.sdf --receptor ../../%s_prot/%s_p.pdb ' % (
        ligname, n, pdbname, pdbname)
        cmdline += '--score rfscore_v1_pdbbind2014 '
        cmdline += '--score rfscore_v2_pdbbind2014 '
        cmdline += '--score rfscore_v3_pdbbind2014 '
        cmdline += '--score nnscore_pdbbind2014 '
        cmdline += '-O %s_top%s_oddt2014_out.sdf &&' % (ligname, n)
        cmdline += '/home/shenchao/python_module2/bin/oddt_cli %s_top%s.sdf --receptor ../../%s_prot/%s_p.pdb ' % (
        ligname, n, pdbname, pdbname)
        cmdline += '--score rfscore_v1_pdbbind2015 '
        cmdline += '--score rfscore_v2_pdbbind2015 '
        cmdline += '--score rfscore_v3_pdbbind2015 '
        cmdline += '--score nnscore_pdbbind2015 '
        cmdline += '-O %s_top%s_oddt2015_out.sdf &&' % (ligname, n)
        cmdline += '/home/shenchao/python_module2/bin/oddt_cli %s_top%s.sdf --receptor ../../%s_prot/%s_p.pdb ' % (
        ligname, n, pdbname, pdbname)
        cmdline += '--score rfscore_v1_pdbbind2016 '
        cmdline += '--score rfscore_v2_pdbbind2016 '
        cmdline += '--score rfscore_v3_pdbbind2016 '
        cmdline += '--score nnscore_pdbbind2016 '
        cmdline += '--score pleclinear '
        cmdline += '--score plecnn '
        cmdline += '--score plecrf '
        cmdline += '-O %s_top%s_oddt2016_out.sdf &&' % (ligname, n)
        cmdline += 'rm -rf *.pickle'
        os.system(cmdline)

        lines2007 = open('%s/%s_%s_ledock/%s/%s_top%s_oddt2007_out.sdf' % (
        pdbname, pdbname, label, ligname, ligname, n)).readlines()
        nnscore_2007 = None
        rfscorev1_2007 = None
        rfscorev2_2007 = None
        rfscorev3_2007 = None
        for line2007 in lines2007:
            if line2007.startswith('>  <nnscore>'):
                nnscore_2007 = lines2007[lines2007.index(line2007) + 1].strip()
            if line2007.startswith('>  <rfscore_v1>'):
                rfscorev1_2007 = lines2007[lines2007.index(line2007) + 1].strip()
            if line2007.startswith('>  <rfscore_v2>'):
                rfscorev2_2007 = lines2007[lines2007.index(line2007) + 1].strip()
            if line2007.startswith('>  <rfscore_v3>'):
                rfscorev3_2007 = lines2007[lines2007.index(line2007) + 1].strip()

        lines2012 = open('%s/%s_%s_ledock/%s/%s_top%s_oddt2012_out.sdf' % (
        pdbname, pdbname, label, ligname, ligname, n)).readlines()
        nnscore_2012 = None
        rfscorev1_2012 = None
        rfscorev2_2012 = None
        rfscorev3_2012 = None
        for line2012 in lines2012:
            if line2012.startswith('>  <nnscore>'):
                nnscore_2012 = lines2012[lines2012.index(line2012) + 1].strip()
            if line2012.startswith('>  <rfscore_v1>'):
                rfscorev1_2012 = lines2012[lines2012.index(line2012) + 1].strip()
            if line2012.startswith('>  <rfscore_v2>'):
                rfscorev2_2012 = lines2012[lines2012.index(line2012) + 1].strip()
            if line2012.startswith('>  <rfscore_v3>'):
                rfscorev3_2012 = lines2012[lines2012.index(line2012) + 1].strip()

        lines2013 = open('%s/%s_%s_ledock/%s/%s_top%s_oddt2013_out.sdf' % (
        pdbname, pdbname, label, ligname, ligname, n)).readlines()
        nnscore_2013 = None
        rfscorev1_2013 = None
        rfscorev2_2013 = None
        rfscorev3_2013 = None
        for line2013 in lines2013:
            if line2013.startswith('>  <nnscore>'):
                nnscore_2013 = lines2013[lines2013.index(line2013) + 1].strip()
            if line2013.startswith('>  <rfscore_v1>'):
                rfscorev1_2013 = lines2013[lines2013.index(line2013) + 1].strip()
            if line2013.startswith('>  <rfscore_v2>'):
                rfscorev2_2013 = lines2013[lines2013.index(line2013) + 1].strip()
            if line2013.startswith('>  <rfscore_v3>'):
                rfscorev3_2013 = lines2013[lines2013.index(line2013) + 1].strip()

        lines2014 = open('%s/%s_%s_ledock/%s/%s_top%s_oddt2014_out.sdf' % (
        pdbname, pdbname, label, ligname, ligname, n)).readlines()
        nnscore_2014 = None
        rfscorev1_2014 = None
        rfscorev2_2014 = None
        rfscorev3_2014 = None
        for line2014 in lines2014:
            if line2014.startswith('>  <nnscore>'):
                nnscore_2014 = lines2014[lines2014.index(line2014) + 1].strip()
            if line2014.startswith('>  <rfscore_v1>'):
                rfscorev1_2014 = lines2014[lines2014.index(line2014) + 1].strip()
            if line2014.startswith('>  <rfscore_v2>'):
                rfscorev2_2014 = lines2014[lines2014.index(line2014) + 1].strip()
            if line2014.startswith('>  <rfscore_v3>'):
                rfscorev3_2014 = lines2014[lines2014.index(line2014) + 1].strip()

        lines2015 = open('%s/%s_%s_ledock/%s/%s_top%s_oddt2015_out.sdf' % (
        pdbname, pdbname, label, ligname, ligname, n)).readlines()
        nnscore_2015 = None
        rfscorev1_2015 = None
        rfscorev2_2015 = None
        rfscorev3_2015 = None
        for line2015 in lines2015:
            if line2015.startswith('>  <nnscore>'):
                nnscore_2015 = lines2015[lines2015.index(line2015) + 1].strip()
            if line2015.startswith('>  <rfscore_v1>'):
                rfscorev1_2015 = lines2015[lines2015.index(line2015) + 1].strip()
            if line2015.startswith('>  <rfscore_v2>'):
                rfscorev2_2015 = lines2015[lines2015.index(line2015) + 1].strip()
            if line2015.startswith('>  <rfscore_v3>'):
                rfscorev3_2015 = lines2015[lines2015.index(line2015) + 1].strip()

        lines2016 = open('%s/%s_%s_ledock/%s/%s_top%s_oddt2016_out.sdf' % (
        pdbname, pdbname, label, ligname, ligname, n)).readlines()
        nnscore_2016 = None
        rfscorev1_2016 = None
        rfscorev2_2016 = None
        rfscorev3_2016 = None
        pleclinear = None
        plecnn = None
        plecrf = None
        for line2016 in lines2016:
            if line2016.startswith('>  <nnscore>'):
                nnscore_2016 = lines2016[lines2016.index(line2016) + 1].strip()
            if line2016.startswith('>  <rfscore_v1>'):
                rfscorev1_2016 = lines2016[lines2016.index(line2016) + 1].strip()
            if line2016.startswith('>  <rfscore_v2>'):
                rfscorev2_2016 = lines2016[lines2016.index(line2016) + 1].strip()
            if line2016.startswith('>  <rfscore_v3>'):
                rfscorev3_2016 = lines2016[lines2016.index(line2016) + 1].strip()
            if line2016.startswith('>  <PLEClinear_p5_l1_s65536>'):
                pleclinear = lines2016[lines2016.index(line2016) + 1].strip()
            if line2016.startswith('>  <PLECnn_p5_l1_s65536>'):
                plecnn = lines2016[lines2016.index(line2016) + 1].strip()
            if line2016.startswith('>  <PLECrf_p5_l1_s65536>'):
                plecrf = lines2016[lines2016.index(line2016) + 1].strip()
        score_list = [molname, ligname, 'top%s' % n, nnscore_2007, rfscorev1_2007, rfscorev2_2007, rfscorev3_2007,
                      nnscore_2012, rfscorev1_2012, rfscorev2_2012, rfscorev3_2012, nnscore_2013, rfscorev1_2013,
                      rfscorev2_2013, rfscorev3_2013, nnscore_2014, rfscorev1_2014, rfscorev2_2014, rfscorev3_2014,
                      nnscore_2015, rfscorev1_2015, rfscorev2_2015, rfscorev3_2015, nnscore_2016, rfscorev1_2016,
                      rfscorev2_2016, rfscorev3_2016, pleclinear, plecnn, plecrf]
        mylist.append(score_list)
        os.remove('%s/%s_%s_ledock/%s/%s_top%s_oddt2007_out.sdf' % (pdbname, pdbname, label, ligname, ligname, n))
        os.remove('%s/%s_%s_ledock/%s/%s_top%s_oddt2012_out.sdf' % (pdbname, pdbname, label, ligname, ligname, n))
        os.remove('%s/%s_%s_ledock/%s/%s_top%s_oddt2013_out.sdf' % (pdbname, pdbname, label, ligname, ligname, n))
        os.remove('%s/%s_%s_ledock/%s/%s_top%s_oddt2014_out.sdf' % (pdbname, pdbname, label, ligname, ligname, n))
        os.remove('%s/%s_%s_ledock/%s/%s_top%s_oddt2015_out.sdf' % (pdbname, pdbname, label, ligname, ligname, n))
        os.remove('%s/%s_%s_ledock/%s/%s_top%s_oddt2016_out.sdf' % (pdbname, pdbname, label, ligname, ligname, n))
    
    return_dict[i] = mylist


def interagte_result(pdbname, label):
    lignames = [x for x in os.listdir('./%s/%s_%s_ledock' % (pdbname, pdbname, label)) if
                os.path.isdir('./%s/%s_%s_ledock/%s' % (pdbname, pdbname, label, x))]
    manger = Manager()
    return_dict = manger.dict()
    pool = multiprocessing.Pool(32)
    jobs = []
    for ligname in lignames:
        im = lignames.index(ligname)
        p = pool.apply_async(oddt_perform, args=(pdbname, ligname, label, im, return_dict))
        jobs.append(p)
    pool.close()
    pool.join()
    mycsv = open('%s/%s_%s_ledock/%s_%s_ledock_oddt_score.csv' % (pdbname, pdbname, label, pdbname, label),
                 'w')
    mycsvwriter = csv.writer(mycsv)
    header = ['molname', 'ligid', 'topn', 'nnscore_2007', 'rfscorev1_2007', 'rfscorev2_2007', 'rfscorev3_2007',
              'nnscore_2012', 'rfscorev1_2012', 'rfscorev2_2012', 'rfscorev3_2012', 'nnscore_2013', 'rfscorev1_2013',
              'rfscorev2_2013', 'rfscorev3_2013', 'nnscore_2014', 'rfscorev1_2014', 'rfscorev2_2014', 'rfscorev3_2014',
              'nnscore_2015', 'rfscorev1_2015', 'rfscorev2_2015', 'rfscorev3_2015', 'nnscore_2016', 'rfscorev1_2016',
              'rfscorev2_2016', 'rfscorev3_2016', 'pleclinear', 'plecnn', 'plecrf']
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
