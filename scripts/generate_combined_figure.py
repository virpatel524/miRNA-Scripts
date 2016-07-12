import pandas as pd
import seaborn as sns
import csv
from data_import 

def data_import():
	mirna2disease = parse_disease('../relevant_data/hmdd_database.txt')
	mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')
	mirna2family = parse_families('../relevant_data/miFam.dat')

	mirna2family_edited = {}

	for alpha in mirna2family:
		if len(mirna2family[alpha]) > 3:
			mirna2family_edited[alpha] = mirna2family[alpha]



	round_robyn_target = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/target_heatmap_dataframe.txt', sep='\t',index_col=[0])
	round_robyn_exp = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/tis_exp_heatmap_dataframe.txt', sep='\t',index_col=[0])
	mir_expdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])
	mir_targetdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0], encoding='utf-8')


	return mirna2disease, mirna2age, mirna2family_edited, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb



