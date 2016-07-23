import seaborn as sns
import pandas as pd 
import csv
from jaccard import * 
from partialcorr import *
from data_import import * 
from general_methods import * 
from scipy.stats import spearmanr, mannwhitneyu
import numpy as np

target_jaccard = pd.read_csv('../relevant_data/target_heatmap_jaccard_dataframe.txt', sep='\t', index_col=[0])
mirna2disease = parse_disease('../relevant_data/hmdd_database.txt')
mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')


namesbin = {}

for mirna in target_jaccard.index:
	if mirna not in mirna2age: continue
	namesbin.setdefault(mirna2age[mirna], []).append(mirna)


newlst = []

for age in namesbin.keys():
	lst_havedone = []
	for mirna in namesbin[age]:
		lst_havedone.append(mirna)
		for secmirna in namesbin[age]:
			if secmirna in lst_havedone: continue
			newlst.append([target_jaccard[mirna][secmirna], age, ])

tarpd = pd.DataFrame.sort(pd.DataFrame(newlst, columns=['Jaccard Similarity Coefficent', 'Age (MY)'])
print spearmanr(tarpd['Jaccard Similarity Coefficent'], tarpd['Age (MY)'])