#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================================================
# extract the glide_sp score
# =================================================================================================

import os, sys, glob, csv
import pandas as pd
#import multiprocessing
from multiprocessing.dummy import Pool

def glide_sp_score_extract(pdbname, label):
	cmdline = 'cd %s/%s_%s_glide_SP &&'%(pdbname, pdbname, label)
	cmdline += 'module load schrodinger &&'
	cmdline += 'canvasConvert -imae %s_SP_lib.maegz -ocsv %s_SP_lib.csv'%(pdbname, pdbname)
	os.system(cmdline)
	
	df = pd.read_csv('%s/%s_%s_glide_SP/%s_SP_lib.csv'%(pdbname, pdbname, label, pdbname), header=0)
	df2 = df.loc[:,['NAME', 'r_i_docking_score']]
	df2.sort_values(by='r_i_docking_score', ascending=True, inplace=True) 
	df2.drop_duplicates(subset=['NAME'],keep='first',inplace=True)
	df2.to_csv('%s/%s_%s_glide_SP/%s_%s_SP_score.csv'%(pdbname, pdbname, label, pdbname, label), index=False)
	
	os.remove('%s/%s_%s_glide_SP/%s_SP_lib.csv'%(pdbname, pdbname, label, pdbname))
	
def addict(pdbname):
	glide_sp_score_extract(pdbname, 'actives')
	glide_sp_score_extract(pdbname, 'decoys')

def main():
    names = [x for x in os.listdir('.') if os.path.isdir(x)]
    #names = ['fa7']
    pool = Pool(28)
    pool.map(addict, names)
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()






