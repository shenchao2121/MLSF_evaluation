#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================================================
# docking with GOLD CHEMPLP
# =================================================================================================

import os, sys, glob, csv
import multiprocessing
# from multiprocessing.dummy import Pool


def write_file(output_file, outline):
    buffer = open(output_file, 'w')
    buffer.write(outline)
    buffer.close()

def split_lig(pdbname, label):
	cmdline = 'cd %s &&'%pdbname
	cmdline += 'mkdir -p myligands_%s'%label
	os.system(cmdline)
	fileContent = open('%s/%s_finalmy.sdf'%(pdbname, label), 'r').read()
	paraList = fileContent.split('$$$$\n')
	paraList.remove(paraList[-1])
	for para in paraList:
		fileWriter = open('%s/myligands_%s/lig_%d.sdf' % (pdbname, label, paraList.index(para) + 1), 'w')
		fileWriter.write(para + '$$$$\n')
		fileWriter.close()
	

def gold_dock(pdbname, lig, label):
    ligname = os.path.basename(lig).split('.')[0].strip()
    cmdline = 'cd %s &&' % pdbname
    cmdline += 'mkdir -p %s_%s_gold_chemplp &&' % (pdbname, label)
    cmdline += 'cd %s_%s_gold_chemplp &&' % (pdbname, label)
    cmdline += 'mkdir -p %s' % ligname
    os.system(cmdline)

    # x, y, z = get_mol_center('%s/%s_prot/%s_l.mol2' % (pdbname, pdbname, pdbname))
    outline = '''  GOLD CONFIGURATION FILE

  AUTOMATIC SETTINGS
autoscale = 1

  POPULATION
popsiz = auto
select_pressure = auto
n_islands = auto
maxops = auto
niche_siz = auto

  GENETIC OPERATORS
pt_crosswt = auto
allele_mutatewt = auto
migratewt = auto

  FLOOD FILL
radius = 10
origin = 0 0 0
do_cavity = 1
floodfill_atom_no = 0
cavity_file = ../../%s_prot/%s_l.mol2
floodfill_center = cavity_from_ligand

  DATA FILES
ligand_data_file ../../myligands_%s/%s.sdf 10
param_file = DEFAULT
set_ligand_atom_types = 1
set_protein_atom_types = 0
directory = .
tordist_file = DEFAULT
make_subdirs = 0
save_lone_pairs = 1
fit_points_file = fit_pts.mol2
read_fitpts = 0

  FLAGS
internal_ligand_h_bonds = 0
flip_free_corners = 0
match_ring_templates = 0
flip_amide_bonds = 0
flip_planar_n = 1 flip_ring_NRR flip_ring_NHR
flip_pyramidal_n = 0
rotate_carboxylic_oh = flip
use_tordist = 1
postprocess_bonds = 1
rotatable_bond_override_file = DEFAULT
solvate_all = 1

  TERMINATION
early_termination = 1
n_top_solutions = 3
rms_tolerance = 1.5

  CONSTRAINTS
force_constraints = 0

  COVALENT BONDING
covalent = 0

  SAVE OPTIONS
save_score_in_file = 1
save_protein_torsions = 1
concatenated_output = total_chemplp.sdf
clean_up_option delete_all_solutions
clean_up_option save_top_n_solutions 3
clean_up_option delete_redundant_log_files
clean_up_option delete_all_initialised_ligands
clean_up_option delete_empty_directories
clean_up_option delete_rank_file
clean_up_option delete_all_log_files
output_file_format = MACCS

  FITNESS FUNCTION SETTINGS
initial_virtual_pt_match_max = 3
relative_ligand_energy = 1
gold_fitfunc_path = plp
score_param_file = DEFAULT

  PROTEIN DATA
protein_datafile = ../../%s_prot/%s_goldp.mol2
''' % (pdbname, pdbname, label, ligname, pdbname, pdbname)
    write_file('%s/%s_%s_gold_chemplp/%s/gold_chemplp.conf' % (pdbname, pdbname, label, ligname), outline)

    cmdline = 'cd %s/%s_%s_gold_chemplp/%s &&' % (pdbname, pdbname, label, ligname)
    cmdline += 'module load ccdc &&'
    cmdline += 'gold_auto gold_chemplp.conf'
    os.system(cmdline)
    #cmdline = 'cd %s/%s_%s_gold_chemplp/%s &&' % (pdbname, pdbname, label, ligname)
    #cmdline += 'module load openeye &&'
    #cmdline += 'convert.py total_chemplp.sdf total_chemplp.csv'
    #os.system(cmdline)
    filenames = os.listdir('%s/%s_%s_gold_chemplp/%s' % (pdbname, pdbname, label, ligname))
    for filename in filenames:
        if os.path.basename(filename) not in ['total_chemplp.sdf', 'total_chemplp.csv']:
            os.remove('%s/%s_%s_gold_chemplp/%s/%s' % (pdbname, pdbname, label, ligname, os.path.basename(filename)))


def main():
	pdbnames = [x for x in os.listdir('.') if os.path.isdir(x)]
	for pdbname in pdbnames:
		if 0 <= pdbnames.index(pdbname) <= 111:
			if not os.path.exists('%s/myligands_actives/lig_1.sdf'%pdbname):
				split_lig(pdbname, 'actives')
			if not os.path.exists('%s/myligands_decoys/lig_1'%pdbname):
				split_lig(pdbname, 'decoys')
			
			ligs_actives = glob.glob('%s/myligands_actives/lig_*.sdf'%pdbname)
			pool = multiprocessing.Pool(32)
			jobs = []
			for lig in ligs_actives:
				p = pool.apply_async(gold_dock, (pdbname, lig, 'actives'))
				jobs.append(p)
			pool.close()
			pool.join()
			ligs_decoys = glob.glob('%s/myligands_decoys/lig_*.sdf'%pdbname)
			pool = multiprocessing.Pool(32)
			jobs = []
			for lig in ligs_decoys:
				p = pool.apply_async(gold_dock, (pdbname, lig, 'decoys'))
				jobs.append(p)
			pool.close()
			pool.join()
			

	

if __name__ == '__main__':
    main()


