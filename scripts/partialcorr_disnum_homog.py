import seaborn as sns
import pandas as pd 
import csv
from jaccard import * 
from partialcorr import *
from data_import import * 
from general_methods import * 
from scipy.stats import spearmanr, mannwhitneyu



mirna2disease = parse_disease('../relevant_data/hmdd_database.txt')
mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')

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
		lst_havedone.append(mirna)
		for secmirna in namesbin[age]:
			if secmirna in lst_havedone: continue
			newlst.append([disease_jaccard[mirna][secmirna], age, len(mirna2disease[mirna])])

dispd = pd.DataFrame.sort(pd.DataFrame(newlst, columns=['Jaccard Similarity Coefficent', 'Age (MY)', 'Number of Diseases']), columns='Age (MY)')

print dispd.values()


sns.boxplot(x='Age (MY)', y='Jaccard Similarity Coefficent', data=dispd,showfliers=False)
sns.stripplot(x='Age (MY)', y='Jaccard Similarity Coefficent', data=dispd, jitter=True, color='k', alpha=0.5)
sns.plt.gca().set_ylim([0, 0.4])
sns.plt.savefig('../figures/disease_homo.pdf',bbox_inches='tight')
sns.plt.close()
