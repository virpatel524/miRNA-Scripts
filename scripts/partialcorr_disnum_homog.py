import seaborn as sns
import pandas as pd 
import csv
from jaccard import * 
from partialcorr import *
from data_import import * 
from general_methods import * 
from scipy.stats import spearmanr, mannwhitneyu
import numpy as np



mirna2disease = parse_disease('../relevant_data/hmdd_database.txt')
mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')

mir_expdb = pd.read_csv('../relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])
mir_targetdb = pd.read_csv('../relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0])

exp_jaccard = pd.read_csv('../relevant_data/tis_exp_heatmap_jaccard_dataframe.txt', sep='\t',index_col=[0])
target_jaccard = pd.read_csv('../relevant_data/target_heatmap_jaccard_dataframe.txt', sep='\t', index_col=[0])


disease_jaccard = pd.read_csv('../relevant_data/disease_jaccard_dataframe.txt', sep='\t',index_col=[0])

namesbin = {}


for mirna in disease_jaccard.index:
	if mirna not in mirna2age: continue
	if mirna2age[mirna] == 220.2 or mirna2age[mirna] == 324.5: continue
	namesbin.setdefault(mirna2age[mirna], []).append(mirna)


newlst = []

for age in namesbin.keys():
	lst_havedone = []
	for mirna in namesbin[age]:
		if mirna not in mir_targetdb.index or mirna not in mir_expdb.index: continue
		lst_havedone.append(mirna)
		for secmirna in namesbin[age]:
			if secmirna not in mir_targetdb.index or secmirna not in mir_expdb.index: continue
			if secmirna in lst_havedone: continue
			tarnum = sum(mir_targetdb.loc[mirna].tolist())
			expnum = sum(mir_expdb.loc[mirna].tolist())
			tarjac_entry = target_jaccard[mirna][secmirna]
			expjac_entry = exp_jaccard[mirna][secmirna]
			newlst.append([disease_jaccard[mirna][secmirna], age, len(mirna2disease[mirna]), tarnum, expnum,tarjac_entry, expjac_entry])

dispd = pd.DataFrame.sort(pd.DataFrame(newlst, columns=['Jaccard Similarity Coefficent', 'Age (MY)', 'Number of Diseases', 'Number of Targets', 'Number of Tissues', 'Target Jaccard', 'Expression Jaccard']), columns='Age (MY)')

np.savetxt( '../relevant_data/partialcorr_alldata.txt', partial_corr(dispd.values))


sns.boxplot(x='Age (MY)', y='Jaccard Similarity Coefficent', data=dispd,showfliers=False)
sns.stripplot(x='Age (MY)', y='Jaccard Similarity Coefficent', data=dispd, jitter=True, color='k', alpha=0.5)
sns.plt.gca().set_ylim([0, 0.4])
sns.plt.savefig('../figures/disease_homo.pdf',bbox_inches='tight')
sns.plt.close()
