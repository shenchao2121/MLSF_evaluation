#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================================================
# docking with glide_SP
# =================================================================================================
import os, sys, glob, csv


# import multiprocessing
##from multiprocessing.dummy import Pool


def write_file(output_file, outline):
    buffer = open(output_file, 'w')
    buffer.write(outline)
    buffer.close()


def glide_SP(name, label):
    cmdline = 'cd %s &&' % name
    cmdline += 'mkdir -p %s_%s_glide_SP' % (name, label)
    os.system(cmdline)

    outline = '''GRIDFILE   ../%s_glide_grid/%s_glide-grid.zip
LIGANDFILE   ../%s_finalmy.sdf
POSES_PER_LIG   5
POSE_OUTTYPE   ligandlib
PRECISION   SP
''' % (name, name, label)
    write_file('%s/%s_%s_glide_SP/%s_SP.in' % (name, name, label, name), outline)

    cmdline = 'cd %s/%s_%s_glide_SP &&' % (name, name, label)
    cmdline += 'module load schrodinger/2019-2 &&'
    cmdline += 'glide %s_SP.in -HOST cu11:32 -NJOBS 32 -WAIT -LOCAL' % name
    # cmdline += 'canvasConvert -imae %s_SP_lib.maegz -ocsv %s.csv'%(name, name)
    os.system(cmdline)

    filenames = os.listdir('%s/%s_%s_glide_SP' % (name, name, label))
    for filename in filenames:
        if os.path.basename(filename) not in ['%s_SP_lib.maegz' % name]:
            os.remove('%s/%s_%s_glide_SP/%s' % (name, name, label, os.path.basename(filename)))


def main():
    names = [x for x in os.listdir('.') if os.path.isdir(x)]
    for name in names:
        if 0 <= names.index(name) <= 111:
            glide_SP(name, 'actives')
            glide_SP(name, 'decoys')


if __name__ == '__main__':
    main()
