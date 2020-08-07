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
		new_dataframes['df0'+str(i)]['SF'] = column_name.split('-')[0].strip()
		new_dataframes['df0'+str(i)]['topn'] = column_name.split('-')[-1].strip()
		new_dataframes['df0'+str(i)] = new_dataframes['df0'+str(i)].rename(columns={column_name:'AUROC'})
		new_dataframes['df0'+str(i)].set_index('pdbname', inplace=True)
		df_total.append(new_dataframes['df0'+str(i)])
	df_out = pd.concat(df_total, axis=0)
	return df_out





def myplot():
	sns.set(style="whitegrid")
	mydata = data_prep('glide_SP_auc.csv')
	
	p = sns.catplot(x="SF", y="AUROC", kind="box", hue='topn',
					height=4, aspect=2,
					#sharex=True,
					palette="Set1",
					#palette=sns.husl_palette(13),
					#palette=sns.color_palette('Paired',13),
					data=mydata, 
					#legend=False,
					showmeans = True,
					meanprops = dict(markeredgewidth=0.5, markeredgecolor='black', markerfacecolor='white', marker='s', markersize=4),
					)
	
	#p.set_xlabel('AUROC', fontsize=10)
	#p.set(ylim=(0.1,1.0))
	#plt.tick_params(labelsize=8)
	#p.set_axis_labels('Targets', 'AUROC')
	#p.set_ylabel('')
	#p.set_xlabels([''])
	#p.set_ylabels(['AUROC'], fontsize=8)
	#p.set_yticklabels([0.0, 1.0, 0.2], fontsize=6)
	#p.set_xticklabels(fontsize=6, rotation=90)
	
	
	#p = sns.boxplot(y="SF", x="AUROC", 
	#				#sharex=True,
	#				#palette="Set2",
	#				data=mydata, 
	#				)
	
	#p = sns.swarmplot(y="SF", x="AUROC", data=mydata, color='wheat', size=2)
	#p = sns.barplot(x="MLs", y="Rp", hue="dataset", data=mydata, errcolor='k')
	#ax.text(-0.2, 0.85, name, style='italic', fontsize='14', color='purple')
	#p.set_xlabel('AUROC', fontsize='10')
	#p.set_ylabel('')
	#p.map(plt.axvline, x=0.8, ls=":", c=".5", color='r')
	#p.legend(loc='upper right', fontsize='medium')
	
	##ax.set_xlim((0,14))
	#p.set_xlim((-1.0,1.0))
	
	
	#plt.show()
	plt.savefig('boxplot_glide_SP_auroc_top3.png', format='png', bbox_inches='tight', transparent=True, dpi=600)


myplot()
