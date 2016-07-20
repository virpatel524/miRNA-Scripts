import seaborn as sns 
import pandas as pd
import csv 
from data_import import *
from general_methods import *


mirna2family = parse_families('../relevant_data/miFam.dat')
mir_expdb = pd.read_csv('../relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])
mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')


newlst = []

family_mirs = flatten(mirna2family.values()) 

famlst = []
nonfamlst = []

for mirna in mirna2age:
	if mirna in mir_expdb.index:
		newlst.append([mirna2age[mirna], sum(mir_expdb.loc[mirna].tolist())])
		if mirna in family_mirs:
			famlst.append([mirna2age[mirna], sum(mir_expdb.loc[mirna].tolist())])
		else:
			nonfamlst.append([mirna2age[mirna], sum(mir_expdb.loc[mirna].tolist())])


fampd = pd.DataFrame(famlst, columns=['Age (MY)', 'Number'])
nonfampd = pd.DataFrame(nonfamlst, columns=['Age (MY)', 'Number'])


