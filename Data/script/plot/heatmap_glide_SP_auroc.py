import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, sys, glob, csv
import numpy as np


def data_prep(infile):
	df = pd.read_csv(infile, header=0, index_col=0)
	df.drop(['average','std'],inplace=True)
	df = df.reset_index()
	df['pdbname'] = df['pdbname'].apply(lambda x: x.upper())
	df.set_index('pdbname', inplace=True)	
	dfa0 = df.transpose()
	#dfa = dfa.reset_index()
	#dfa = dfa.rename(columns={'index':'pdbname'})
	#new_dataframes = locals()
	#df_total = []
	#for column_name in df.columns:
	#	i = df.columns.get_loc(column_name)
	#	new_dataframes['df0'+str(i)] = dfa[['pdbname', column_name, 'classification']]
	#	new_dataframes['df0'+str(i)]['SF'] = column_name
	#	new_dataframes['df0'+str(i)] = new_dataframes['df0'+str(i)].rename(columns={column_name:'AUROC'})
	#	#new_dataframes['df0'+str(i)].set_index('pdbname', inplace=True)
	#	df_total.append(new_dataframes['df0'+str(i)])
	#df_out = pd.concat(df_total, axis=0)
	#df_out = df_out.rename(columns={'pdbname':'Targets'})
	return dfa0


def myplot():
	#sns.set(style="whitegrid")
	f = plt.subplots(figsize = (10, 3))
	#mydata = data_prep('glide_SP_auc.csv', 'ref.csv')
	mydata = data_prep('glide_SP_auc.csv')
	
	p = sns.heatmap(mydata,
					#cmap='gnuplot2_r',
					#cmap = 'inferno_r',
					cmap = 'jet_r',
					linewidths = 0.05,
					#annot_kws={"size": 3},
					#annot=True,
					#cbar_kws 
					xticklabels=1, 
					yticklabels=1)
			
	p.tick_params(axis='x',labelsize=5.5)
	p.tick_params(axis='y',labelsize=10)
	plt.xlabel('Targets', fontsize=10)
	#plt.ylabel('AUROC', fontsize=8)
	##ax.set_xlim((0,14))
		
	#plt.show()
	plt.savefig('heatmap_glide_SP_auroc.png', format='png', bbox_inches='tight', transparent=True, dpi=600)


myplot()
