#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================================================
# generate the grid
# =================================================================================================
import os, sys, glob, csv
# import multiprocessing
from multiprocessing.dummy import Pool


def write_file(output_file, outline):
    buffer = open(output_file, 'w')
    buffer.write(outline)
    buffer.close()


def get_mol_center(lig_mol2file):
    x = os.popen("cat %s | sed -n '/@<TRIPOS>ATOM/,/@<TRIPOS>BOND/'p | awk '{print $3}' | awk '{x+=$1} END {print x/(NR-2)}'" % lig_mol2file).read()
    y = os.popen("cat %s | sed -n '/@<TRIPOS>ATOM/,/@<TRIPOS>BOND/'p | awk '{print $4}' | awk '{y+=$1} END {print y/(NR-2)}'" % lig_mol2file).read()
    z = os.popen("cat %s | sed -n '/@<TRIPOS>ATOM/,/@<TRIPOS>BOND/'p | awk '{print $5}' | awk '{z+=$1} END {print z/(NR-2)}'" % lig_mol2file).read()
    return float(x.strip()), float(y.strip()), float(z.strip())


def glide_grid(name):
    x, y, z = get_mol_center('%s/%s_prot/%s_l.mol2' % (name, name, name))
    cmdline = 'cd %s &&' % name
    cmdline += 'mkdir -p %s_glide_grid' % name
    os.system(cmdline)
    outline = '''GRID_CENTER   %.10f, %.10f, %.10f
GRIDFILE   %s_glide-grid.zip
INNERBOX   10, 10, 10
OUTERBOX   30, 30, 30
RECEP_FILE   ../%s_prot/%s_complex_prep_receptor1.mae
RECEP_VSCALE   1.0
RECEP_CCUT   0.25
''' % (x, y, z, name, name, name)
    write_file('%s/%s_glide_grid/%s_grid.in' % (name, name, name), outline)
    cmdline = 'cd %s/%s_glide_grid &&' % (name, name)
    cmdline += 'module load schrodinger/2019-2 &&'
    cmdline += 'glide %s_grid.in -NOJOBID' % name
    os.system(cmdline)
    for f in [x for x in os.listdir('%s/%s_glide_grid' % (name, name)) if '.zip' not in x]:
        os.remove('%s/%s_glide_grid/%s'%(name, name, f))



def main():
    ##prots = glob.glob('*/*_prot/*_p.pdb')
    names = [x for x in os.listdir('.') if os.path.isdir(x)]
    # pool = multiprocessing.Pool(28)
    # results = []
    # for protfile in prots:
    #	results.append(pool.apply_async(gold_dock, args=(protfile, score)))
    pool = Pool(32)
    pool.map(glide_grid, names)
    pool.close()
    pool.join()
    ##interagte_result()


if __name__ == '__main__':
    main()


