#!/user/bin python
# -*- coding: utf-8 -*-

# =================================================
# docking with ledock 
# =================================================

import os, re, sys, glob
import multiprocessing
#from multiprocessing.dummy import Pool


def write_file(output_file, outline):
    buffer = open(output_file, 'w')
    buffer.write(outline)
    buffer.close()


def split_lig(pdbname, label):
    cmdline = 'cd %s &&' % pdbname
    cmdline += 'mkdir -p myligands_%s' % label
    os.system(cmdline)
    fileContent = open('%s/%s_finalmy.sdf' % (pdbname, label), 'r').read()
    paraList = fileContent.split('$$$$\n')
    paraList.remove(paraList[-1])
    for para in paraList:
        fileWriter = open('%s/myligands_%s/lig_%d.sdf' % (pdbname, label, paraList.index(para) + 1), 'w')
        fileWriter.write(para + '$$$$\n')
        fileWriter.close()


def ledock_perform(pdbname, lig, label):
    ligname = os.path.basename(lig).split('.')[0].strip()
    if not os.path.exists('%s/%s_prot/%s_c.pdb' % (pdbname, pdbname, pdbname)):
        cmdline = 'cd %s/%s_prot &&' % (pdbname, pdbname)
        cmdline += 'module load schrodinger &&'
        cmdline += 'structconvert %s_complex_prep.mae %s_c.pdb' % (pdbname, pdbname)
        os.system(cmdline)

    cmdline = 'cd %s &&' % pdbname
    cmdline += 'mkdir -p %s_%s_ledock &&' % (pdbname, label)
    cmdline += 'cd %s_%s_ledock &&' % (pdbname, label)
    cmdline += 'mkdir -p %s &&' % ligname
    cmdline += 'cd %s &&' % ligname
    cmdline += '/home/shenchao/AI_based_SFs/software/ledock/lepro ../../%s_prot/%s_c.pdb &&' % (pdbname, pdbname)
    cmdline += 'module load schrodinger &&'
    cmdline += 'structconvert ../../myligands_%s/%s.sdf ./%s.mol2 &&' % (label, ligname, ligname)
    cmdline += 'echo \'%s.mol2\' > ligands &&' % ligname
    cmdline += 'cat dock.in | sed \'/RMSD/{n;s/1.0/0.5/g}\' > dock0.in &&'
    cmdline += 'rm dock.in &&'
    cmdline += '/home/shenchao/AI_based_SFs/software/ledock/ledock dock0.in'
    os.system(cmdline)

    filenames = os.listdir('%s/%s_%s_ledock/%s' % (pdbname, pdbname, label, ligname))
    for filename in filenames:
        if os.path.basename(filename) not in ['%s.dok' % ligname]:
            os.remove('%s/%s_%s_ledock/%s/%s' % (pdbname, pdbname, label, ligname, os.path.basename(filename)))


def main():
    pdbnames = [x for x in os.listdir('.') if os.path.isdir(x)]
    #pdbnames = 'urok'
    for pdbname in pdbnames:
        if 0 <= pdbnames.index(pdbname) <= 111:
            if not os.path.exists('%s/myligands_actives/lig_1.sdf' % pdbname):
                split_lig(pdbname, 'actives')
            if not os.path.exists('%s/myligands_decoys/lig_1' % pdbname):
                split_lig(pdbname, 'decoys')
    
            ligs_actives = glob.glob('%s/myligands_actives/lig_*.sdf' % pdbname)
            pool = multiprocessing.Pool(32)
            jobs = []
            for lig in ligs_actives:
                p = pool.apply_async(ledock_perform, (pdbname, lig, 'actives'))
                jobs.append(p)
            pool.close()
            pool.join()
            ligs_decoys = glob.glob('%s/myligands_decoys/lig_*.sdf' % pdbname)
            pool = multiprocessing.Pool(32)
            jobs = []
            for lig in ligs_decoys:
                p = pool.apply_async(ledock_perform, (pdbname, lig, 'decoys'))
                jobs.append(p)
            pool.close()
            pool.join()



if __name__ == '__main__':
    main()
