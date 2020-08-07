import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, sys, glob, csv
import numpy as np


def data_prep(infile):
	df = pd.read_csv(infile, header=0, index_col=0)
	df.drop(['average','std'],inplace=True)
	dfa = df.reset_index()
	new_dataframes = locals()
	df_total = []
	for column_name in df.columns:
		i = df.columns.get_loc(column_name)
		new_dataframes['df0'+str(i)] = dfa[['pdbname', column_name]]
		new_dataframes['df0'+str(i)]['SF'] = column_name
		new_dataframes['df0'+str(i)] = new_dataframes['df0'+str(i)].rename(columns={column_name:'AUROC'})
		new_dataframes['df0'+str(i)].set_index('pdbname', inplace=True)
		df_total.append(new_dataframes['df0'+str(i)])
	df_out = pd.concat(df_total, axis=0)
	df_ref = df_out.groupby(['SF']).mean()
	df_ref.sort_values(by=['AUROC'], ascending = False, inplace=True)
	name_index = list(df_ref.index)
	df_out['SF'] = df_out['SF'].astype('category')
	df_out['SF'].cat.reorder_categories(name_index, inplace=True)
	df_out.sort_values('SF', inplace=True)
	return df_out





def myplot():
	#sns.set(style="whitegrid")
	sns.set(style="darkgrid")
	f = plt.subplots(figsize = (3, 10))
	mydata = data_prep('auc_zheng.csv')
	
	
	p = sns.boxplot(y="SF", x="AUROC", 
					#sharex=True,
					#palette="Set2",
					data=mydata, 
					fliersize = 1,
					showmeans = True,
					meanprops = dict(markeredgewidth=0.5, markeredgecolor='black', markerfacecolor='white', marker='s', markersize=4),
					)
	
	#p = sns.swarmplot(y="SF", x="AUROC", data=mydata, color='wheat', size=2)
	#p = sns.barplot(x="MLs", y="Rp", hue="dataset", data=mydata, errcolor='k')
	#ax.text(-0.2, 0.85, name, style='italic', fontsize='14', color='purple')
	p.set_xlabel('AUROC', fontsize='10')
	p.set_ylabel('', fontsize='6')
	#p.map(plt.axvline, x=0.8, ls=":", c=".5", color='r')
	#p.legend(loc='upper right', fontsize='medium')
	#p.tick_params(axis='x',labelsize=6, rotation=90)
	##ax.set_xlim((0,14))
	#p.set_xlim((-1.0,1.0))
	
	
	#plt.show()
	#plt.savefig('auroc_zheng.png', format='png', bbox_inches='tight', transparent=True, dpi=600)
	plt.savefig('auroc_zheng.png', format='png', bbox_inches='tight', transparent=False, dpi=600)


myplot()
