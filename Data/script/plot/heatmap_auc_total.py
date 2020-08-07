import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
#import os, sys, glob, csv
import numpy as np
#from scipy.stats import friedmanchisquare
import scikit_posthocs as sp

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
	listnames = locals()
	df_stat_list = []
	for i in df_ref.index:
		j = list(df_ref.index).index(i)
		listnames['df_%s'%j] = df_out[df_out['SF']==i]['AUROC']
		df_stat_list.append(listnames['df_%s'%j])	
	
	tot_data = np.array(df_stat_list)
	df_stat = sp.posthoc_nemenyi(tot_data)
	df_stat.columns = list(df_ref.index)
	df_stat.index = list(df_ref.index)
	df_stat2 = pd.DataFrame(np.ones(42**2).reshape(42,42))
	df_stat2.columns = list(df_ref.index)
	df_stat2.index = list(df_ref.index)
	df_stat2 = df_stat2.astype('str')
	for a in range(42):
		for b in range(42):
			if df_stat.iloc[a,b] >= 0.10:
				df_stat2.iloc[a,b] = 5
			if 0.05 <= df_stat.iloc[a,b] < 0.10:
				df_stat2.iloc[a,b] = 4
			if 0.01 <= df_stat.iloc[a,b] < 0.05:
				df_stat2.iloc[a,b] = 3
			if 0.001 <= df_stat.iloc[a,b] < 0.01:
				df_stat2.iloc[a,b] = 2
			if 0.0 <= df_stat.iloc[a,b] < 0.001:
				df_stat2.iloc[a,b] = 1
			if df_stat.iloc[a,b] < 0.00:
				df_stat2.iloc[a,b] = 0	
	
	return df_stat2




def myheatmap():
    f = plt.subplots(figsize=(4, 3))
    mydata = data_prep('auc_zheng.csv')
    p = sns.heatmap(mydata,
                    # cmap='gnuplot2_r',
                    # cmap = 'inferno_r',
                    cmap=ListedColormap(['snow', 'lightsteelblue', 'royalblue', 'slateblue', 'mediumslateblue', 'thistle']),
                                        # cmap = 'jet_r',
                                        linewidths=0.05,
                                        # annot_kws={"size": 3},
                                        # annot=True,
                                        # cbar_kws 
                                        cbar_kws = {"ticks":[]},
                                        xticklabels=1,
                                        yticklabels=1
                                        )
	
    p.tick_params(axis='x', labelsize=5)
    p.tick_params(axis='y', labelsize=5)
    cb = plt.gcf().axes[-1]
    cb.text(2, 0.90, 'p > 0.10', 
			#style='italic', 
			fontsize='8', color='black')
    cb.text(2, 0.73, 'p < 0.10', fontsize='8', color='black')
    cb.text(2, 0.58, 'p < 0.05', fontsize='8', color='black')
    cb.text(2, 0.42, 'p < 0.01', fontsize='8', color='black')
    cb.text(2, 0.23, 'p < 0.001', fontsize='8', color='black')
    cb.text(2, 0.05, 'NS', fontsize='8', color='black')
    #cb = plt.gcf().axes[-1]
    #cbar_ax = f[-1]
    #cbar_solids = cbar_ax.collections[0]
    #cb.set_ticks(['NS','p<0.001','p<0.01','p<0.05','p<0.10','p>0.10'],'')
    # plt.xlabel('Targets', fontsize=10)
    # plt.ylabel('AUROC', fontsize=8)
    ##ax.set_xlim((0,14))
	
    # plt.show()
    plt.savefig('p-value_heatmap.png', format='png', bbox_inches='tight', transparent=True, dpi=600)


myheatmap()
