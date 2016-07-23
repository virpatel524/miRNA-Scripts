import seaborn as sns
import pandas as pd
import csv
from data_import import *
from general_methods import *

mir_expdb = pd.read_csv('../relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])
mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')
mirna2numexp = {}

for alpha in mir_expdb.index:
	mirna2numexp[alpha] = sum(mir_expdb.loc[alpha].tolist())


newlst = []

for mirna in mirna2age:
	if mirna in mirna2numexp:
		newlst.append([mirna2age[mirna], mirna2numexp[mirna]])


exppd = pd.DataFrame(newlst, columns=['Age (MY)', 'Number of Tissues'])

sns.boxplot(x='Age (MY)', y='Number of Tissues', data=exppd, showfliers=False)
sns.stripplot(x='Age (MY)', y='Number of Tissues', data=exppd, jitter=True, color='k', alpha=0.5)
sns.plt.gca().set_ylim([0, 20])
sns.plt.show()
sns.plt.close()