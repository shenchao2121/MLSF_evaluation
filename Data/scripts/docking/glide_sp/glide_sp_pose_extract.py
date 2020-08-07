#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================================================
# extract the top three poses of glide sp
# =================================================================================================

import os, sys, glob, csv
# import pandas as pd
# import multiprocessing
# from multiprocessing import Manager
from multiprocessing.dummy import Pool


def split_lig(pdbname, label):
    fileContent = open('%s/%s_%s_glide_SP/%s_SP_lib.sdf' % (pdbname, pdbname, label, pdbname), 'r').read()
    paraList = fileContent.split('$$$$\n')
    paraList.remove(paraList[-1])
    ref_list = []
    for para in paraList:
        fileWriter = open('%s/%s_%s_glide_SP/my_%d.sdf' % (pdbname, pdbname, label, paraList.index(para) + 1), 'w')
        fileWriter.write(para + '$$$$\n')
        fileWriter.close()
        ref_list.append([paraList.index(para) + 1, para.split('\n')[0].strip()])
    return dict(ref_list)


def glide_sp_pose_extract(pdbname, label):
    cmdline = 'cd %s/%s_%s_glide_SP &&' % (pdbname, pdbname, label)
    cmdline += 'rm -rf li_* &&'
    cmdline += 'module load schrodinger &&'
    cmdline += 'structconvert %s_SP_lib.maegz %s_SP_lib.sdf' % (pdbname, pdbname)
    os.system(cmdline)

    ref_dict = split_lig(pdbname, label)
    set_to = list(set(ref_dict.values()))
    set_to.sort(key=list(ref_dict.values()).index)
    for i in range(len(set_to)):
        ks = [k for (k, v) in ref_dict.items() if v == set_to[i]]
        cmdline = 'cd %s/%s_%s_glide_SP &&' % (pdbname, pdbname, label)
        cmdline += 'mkdir -p li_%s' % i
        os.system(cmdline)
        for k in ks:
            cmdline = 'cd %s/%s_%s_glide_SP &&' % (pdbname, pdbname, label)
            cmdline += 'mv my_%s.sdf li_%s' % (k, i)
            os.system(cmdline)

    dirnames = [x for x in os.listdir('./%s/%s_%s_glide_SP' % (pdbname, pdbname, label)) if
                os.path.isdir('%s/%s_%s_glide_SP/%s' % (pdbname, pdbname, label, x))]
    for dirname in dirnames:
        posefiles = glob.glob('%s/%s_%s_glide_SP/%s/my_*.sdf' % (pdbname, pdbname, label, dirname))
        if len(posefiles) == 0:
            os.rmdir('%s/%s_%s_glide_SP/%s' % (pdbname, pdbname, label, dirname))
        if len(posefiles) == 1:
            os.rename(posefiles[0], '%s/%s_%s_glide_SP/%s/%s_top1.sdf' % (pdbname, pdbname, label, dirname, dirname))
        if len(posefiles) == 2:
            if int(os.path.basename(posefiles[0]).split('.')[0].split('_')[-1].strip()) < int(
                    os.path.basename(posefiles[1]).split('.')[0].split('_')[-1].strip()):
                os.rename(posefiles[0],
                          '%s/%s_%s_glide_SP/%s/%s_top1.sdf' % (pdbname, pdbname, label, dirname, dirname))
                os.rename(posefiles[1],
                          '%s/%s_%s_glide_SP/%s/%s_top2.sdf' % (pdbname, pdbname, label, dirname, dirname))
            else:
                os.rename(posefiles[1],
                          '%s/%s_%s_glide_SP/%s/%s_top1.sdf' % (pdbname, pdbname, label, dirname, dirname))
                os.rename(posefiles[0],
                          '%s/%s_%s_glide_SP/%s/%s_top2.sdf' % (pdbname, pdbname, label, dirname, dirname))
        if len(posefiles) >= 3:
            myids = list(set([int(os.path.basename(x).split('.')[0].split('_')[-1].strip()) for x in posefiles]))
            os.rename('%s/%s_%s_glide_SP/%s/my_%s.sdf' % (pdbname, pdbname, label, dirname, myids[0]),
                      '%s/%s_%s_glide_SP/%s/%s_top1.sdf' % (pdbname, pdbname, label, dirname, dirname))
            os.rename('%s/%s_%s_glide_SP/%s/my_%s.sdf' % (pdbname, pdbname, label, dirname, myids[1]),
                      '%s/%s_%s_glide_SP/%s/%s_top2.sdf' % (pdbname, pdbname, label, dirname, dirname))
            os.rename('%s/%s_%s_glide_SP/%s/my_%s.sdf' % (pdbname, pdbname, label, dirname, myids[2]),
                      '%s/%s_%s_glide_SP/%s/%s_top3.sdf' % (pdbname, pdbname, label, dirname, dirname))
            posefiles2 = glob.glob('%s/%s_%s_glide_SP/%s/*.sdf' % (pdbname, pdbname, label, dirname))
            for posefile2 in posefiles2:
                if 'top' not in posefile2:
                    os.remove(posefile2)
    os.remove('%s/%s_%s_glide_SP/%s_SP_lib.sdf' % (pdbname, pdbname, label, pdbname))


def addict(pdbname):
    glide_sp_pose_extract(pdbname, 'actives')
    glide_sp_pose_extract(pdbname, 'decoys')


def main():
    names = [x for x in os.listdir('.') if os.path.isdir(x)]
    # names = ['fa7']
    # pool = Pool(32)
    # pool.map(addict, names)
    # pool.close()
    # pool.join()
    for name in names:
        addict(name)


if __name__ == '__main__':
    main()
