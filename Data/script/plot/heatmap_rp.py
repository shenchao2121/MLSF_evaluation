import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, sys, glob, csv
import numpy as np

def data_prep(infile):
	name0 = os.path.basename(infile).split('_')[0].strip()
	if name0 == 'NNscore1':
		name = 'NNscore1.0'
	elif name0 == 'NNscore2':
		name = 'NNscore2.0'
	else:
		name = name0
	
	df = pd.read_csv(infile, header=0, index_col=0)
	df_act = df.iloc[:,[0,3,6]]
	df_act.columns = ['Glide_GOLD_%s'%name, 'GOLD_LeDock_%s'%name, 'LeDock_Glide_%s'%name]
	df_dec = df.iloc[:,[1,4,7]]
	df_dec.columns = ['Glide_GOLD_%s'%name, 'GOLD_LeDock_%s'%name, 'LeDock_Glide_%s'%name]	
	df_tot = df.iloc[:,[2,5,8]]
	df_tot.columns = ['Glide_GOLD_%s'%name, 'GOLD_LeDock_%s'%name, 'LeDock_Glide_%s'%name]		
	return df_act, df_dec, df_tot

def data_integrate(reffile):
	infiles = glob.glob('*_Rp.csv')
	df_act_list = []
	df_dec_list = []
	df_tot_list = []
	for infile in infiles:
		df_act, df_dec, df_tot = data_prep(infile)
		df_act_list.append(df_act)
		df_dec_list.append(df_dec)
		df_tot_list.append(df_tot)
	
	dfa_act = pd.concat(df_act_list, axis=1)
	dfa_dec = pd.concat(df_dec_list, axis=1)
	dfa_tot = pd.concat(df_tot_list, axis=1)
	
	list_sorted = ['Glide_GOLD_docking', 'GOLD_LeDock_docking', 'LeDock_Glide_docking',
					'Glide_GOLD_deltaVinaRF', 'GOLD_LeDock_deltaVinaRF', 'LeDock_Glide_deltaVinaRF',
					'Glide_GOLD_RFscore-VS', 'GOLD_LeDock_RFscore-VS', 'LeDock_Glide_RFscore-VS',
					'Glide_GOLD_pafnucy', 'GOLD_LeDock_pafnucy', 'LeDock_Glide_pafnucy',
					'Glide_GOLD_OnionNet', 'GOLD_LeDock_OnionNet', 'LeDock_Glide_OnionNet',
					'Glide_GOLD_RFscorev4', 'GOLD_LeDock_RFscorev4', 'LeDock_Glide_RFscorev4',
					'Glide_GOLD_RFscorev3', 'GOLD_LeDock_RFscorev3', 'LeDock_Glide_RFscorev3',
					'Glide_GOLD_NNscore1.0', 'GOLD_LeDock_NNscore1.0', 'LeDock_Glide_NNscore1.0',
					'Glide_GOLD_NNscore2.0', 'GOLD_LeDock_NNscore2.0', 'LeDock_Glide_NNscore2.0',
					'Glide_GOLD_NNscore(ODDT)', 'GOLD_LeDock_NNscore(ODDT)', 'LeDock_Glide_NNscore(ODDT)',
					'Glide_GOLD_RFscorev1(ODDT)', 'GOLD_LeDock_RFscorev1(ODDT)', 'LeDock_Glide_RFscorev1(ODDT)',
					'Glide_GOLD_RFscorev2(ODDT)', 'GOLD_LeDock_RFscorev2(ODDT)', 'LeDock_Glide_RFscorev2(ODDT)',
					'Glide_GOLD_RFscorev3(ODDT)', 'GOLD_LeDock_RFscorev3(ODDT)', 'LeDock_Glide_RFscorev3(ODDT)',
					'Glide_GOLD_PLECRF(ODDT)', 'GOLD_LeDock_PLECRF(ODDT)', 'LeDock_Glide_PLECRF(ODDT)'
					]
	df_ref = pd.read_csv(reffile, header=0, index_col=0)
	df_ref = df_ref.reset_index()
	df_ref['pdbname'] = df_ref['pdbname'].apply(lambda x: x.lower())
	df_ref.set_index('pdbname', inplace=True)
	dfb_act = pd.concat([dfa_act,df_ref], axis=1)
	dfb_act.sort_values(by=['classification', dfa_act.columns[0]], ascending = [True,True], inplace=True)
	dfb_act.drop(['classification'], axis=1,inplace=True)
	dfb_act = dfb_act.reset_index()
	dfb_act['pdbname'] = dfb_act['pdbname'].apply(lambda x: x.upper())
	dfb_act.set_index('pdbname', inplace=True)		
	dfb_act0 = dfb_act.transpose()
	dfb_act0 = dfb_act0.reset_index()
	dfb_act0['index'] = dfb_act0['index'].astype('category').cat.set_categories(list_sorted)
	dfb_act0 = dfb_act0.sort_values(by=['index'], ascending=[True])
	dfb_act0.set_index('index', inplace=True)
	
	dfb_dec = pd.concat([dfa_dec,df_ref], axis=1)
	dfb_dec.sort_values(by=['classification', dfa_dec.columns[0]], ascending = [True,True], inplace=True)
	dfb_dec.drop(['classification'], axis=1,inplace=True)
	dfb_dec = dfb_dec.reset_index()
	dfb_dec['pdbname'] = dfb_dec['pdbname'].apply(lambda x: x.upper())
	dfb_dec.set_index('pdbname', inplace=True)		
	dfb_dec0 = dfb_dec.transpose()
	dfb_dec0 = dfb_dec0.reset_index()
	dfb_dec0['index'] = dfb_dec0['index'].astype('category').cat.set_categories(list_sorted)
	dfb_dec0 = dfb_dec0.sort_values(by=['index'], ascending=[True])	
	dfb_dec0.set_index('index', inplace=True)
	
	
	dfb_tot = pd.concat([dfa_tot,df_ref], axis=1)
	dfb_tot.sort_values(by=['classification', dfa_tot.columns[0]], ascending = [True,True], inplace=True)
	dfb_tot.drop(['classification'], axis=1,inplace=True)
	dfb_tot = dfb_tot.reset_index()
	dfb_tot['pdbname'] = dfb_tot['pdbname'].apply(lambda x: x.upper())
	dfb_tot.set_index('pdbname', inplace=True)		
	dfb_tot0 = dfb_tot.transpose()
	dfb_tot0 = dfb_tot0.reset_index()
	dfb_tot0['index'] = dfb_tot0['index'].astype('category').cat.set_categories(list_sorted)
	dfb_tot0 = dfb_tot0.sort_values(by=['index'], ascending=[True])	
	dfb_tot0.set_index('index', inplace=True)	
	
	return dfb_act0, dfb_dec0, dfb_tot0
	


def myplot(mydata, name):
	#sns.set(style="whitegrid")
	f = plt.subplots(figsize = (8, 6))
	#mydata = data_prep('glide_SP_auprc.csv', 'ref.csv')
	
	
	p = sns.heatmap(mydata,
					#cmap='gnuplot2_r',
					#cmap = 'inferno_r',
					cmap = 'jet_r',
					linewidths = 0.1,
					#annot_kws={"size": 3},
					#annot=True,
					#cbar_kws 
					xticklabels=1, 
					yticklabels=1)
			
	p.tick_params(axis='x',labelsize=4.5)
	p.tick_params(axis='y',labelsize=8)
	plt.xlabel('Targets', fontsize=10)
	plt.ylabel('')
	#plt.ylabel('AUROC', fontsize=8)
	##ax.set_xlim((0,14))
		
	#plt.show()
	plt.savefig('heatmap_corr_%s.png'%name, format='png', bbox_inches='tight', transparent=True, dpi=600)


mydata_act, mydata_dec, mydata_tot = data_integrate('ref.csv')
myplot(mydata_act, 'act')
myplot(mydata_dec, 'dec')
myplot(mydata_tot, 'tot')


