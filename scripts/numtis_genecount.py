import pandas as pd
import seaborn as sns
import csv
from scipy.stats import spearmanr

def flatten(l):
	return [item for sublist in l for item in sublist]

def map_relatives(dic):
	newdic = {}

	for key in dic:
		for el in dic[key]:
			newdic[el] = [a for a in dic[key] if a != el]

	return newdic


def parse_families(txt):
	mega_mir_lst = []
	famdict = {}
	mirlst_by_species = {}
	human_mirlst = {}

	famlst = [alpha for alpha in list(csv.reader(open(txt),delimiter='\t'))]


	current_fam = ''

	for i in famlst:
		lst = [alpha for alpha in i[0].split(' ') if alpha != '']
		if i[0][:2] == 'ID' : 
			current_fam = lst[1]
		if i[0][:2] == 'MI' :
			if 'v' in lst[2].split('-')[0]: continue
			else:
				famdict.setdefault(current_fam,[]).append(lst[2])

	for key in famdict:
		new_lst  = [a for a in famdict[key] if 'hsa' in a]
		if len(new_lst) > 3:
			human_mirlst[key] = new_lst
	return human_mirlst 


mirna2family = parse_families('../relevant_data/miFam.dat')

mir_targetdb = pd.read_csv('../relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0])
mir_expdb = pd.read_csv('../relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])

mir2numtis = {}

mir2numexp = {}

for mir in mir_targetdb.index:
	if mir in mir_expdb.index:
		mir2numtis[mir] = float(sum(mir_targetdb.loc[mir].tolist()))

for mir in mir_expdb.index:
	if mir in mir_targetdb.index:
		mir2numexp[mir] = float(sum(mir_expdb.loc[mir].tolist()))

lst1 = []
lst2 = []


newlst = []

for mir in mir2numtis:
	newlst.append([mir2numexp[mir], mir2numtis[mir]])

db = pd.DataFrame(newlst, columns=['tissue', 'genes'])



sns.violinplot(x='tissue',y='genes', data=db, cut=0)
sns.plt.show()
sns.plt.close()


sns.plt.close()