import pandas as pd
import seaborn as sns
import csv
from data_import import *




def genfig(lst, name, yax, xax, length):
	if length == 2:
		tmp = pd.DataFrame(lst, columns=[yax, xax])

		sns.violinplot(x=xax, y=yax, cut=0, data=tmp, showfliers=False)
		sns.plt.gca().set_ylim(yaxis_switch(name))
		sns.plt.savefig('../figures/before_meeting/%s_violin.pdf' %(name), bbox_inches='tight')
		sns.plt.close()
		sns.boxplot(x=xax, y=yax, data=tmp,  showfliers=False) 
		sns.plt.gca().set_ylim(yaxis_switch(name))
		sns.plt.savefig('../figures/before_meeting/%s_boxplot.pdf' %(name), bbox_inches='tight')
		sns.plt.close()


	if length == 3:
		tmp = pd.DataFrame(lst, columns=[yax, xax, 'miRNA Class'])
		sns.violinplot(x=xax, y=yax, cut=0, data=tmp, hue='miRNA Class',  showfliers=False)
		sns.plt.gca().set_ylim(yaxis_switch(name))
		sns.plt.savefig('../figures/before_meeting/%s_violin.pdf' %(name), bbox_inches='tight')
		sns.plt.close()

		sns.boxplot(x=xax, y=yax, data=tmp, hue='miRNA Class',  showfliers=False)
		sns.plt.gca().set_ylim(yaxis_switch(name))
		sns.plt.savefig('../figures/before_meeting/%s_boxplot.pdf' %(name), bbox_inches='tight')
		sns.plt.close()

def show_jaccard_target():
	family = []
	non_family = []
	family_values = flatten(mirna2family.values())
	for val in round_robyn_target.index:
		for secval in round_robyn_target.index:
			print val, secval









def db_gen():
	mirna2disease = parse_disease('../relevant_data/hmdd_database.txt')
	mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')
	mirna2family = parse_families('../relevant_data/miFam.dat')

	mirna2family_edited = {}

	for alpha in mirna2family:
		if len(mirna2family[alpha]) > 3:
			mirna2family_edited[alpha] = mirna2family[alpha]

	mirna2family = mirna2family_edited.copy()

	round_robyn_target = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/target_heatmap_dataframe.txt', sep='\t',index_col=[0])
	round_robyn_exp = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/tis_exp_heatmap_dataframe.txt', sep='\t',index_col=[0])
	mir_expdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])
	mir_targetdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0], encoding='utf-8')


	return mirna2disease, mirna2age, mirna2family, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb



mirna2disease, mirna2age, mirna2family, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb = db_gen()
show_jaccard_target()

