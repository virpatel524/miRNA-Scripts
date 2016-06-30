import seaborn as sns
import matplotlib.pyplot as plt
import sys
import csv
import pandas as pd




sns.axes_style('whitegrid')
sns.set_style("whitegrid")
sns.set_context("paper")

def import_pcg():
	data = []

	with open(sys.argv[2], 'r') as pcg_ages_precursor_fle:
		data = list(csv.reader(pcg_ages_precursor_fle, delimiter='\t'))

	precursor_data = [a[-1] for a in data if '#' not in a[0]]

	time_tree_fle = open(sys.argv[3],'r')
	time_tree_data = list(csv.reader(time_tree_fle, delimiter='\t'))
	time_tree_data = [a for a in time_tree_data if '#' not in a[0]]

	time_tree_dict = {}
	time_tree_dict_reverse = {}

	for a in time_tree_data:
		time_tree_dict_reverse[float(a[-1])] = a[0]
		time_tree_dict[a[0]] = float(a[-1])

	newlst = []

	for alpha in precursor_data:
		newlst.append(time_tree_dict[alpha])

	return newlst, time_tree_dict_reverse


	

def import_human_mirages():
	data = []	

	with open(sys.argv[1],'r') as mir_ages_fle:
		data = list(csv.reader(mir_ages_fle,delimiter='\t'))

	humanmirlst = [a for a in data if 'hsa' in a[0]]
	human_ages = [float(a[-1]) for a in humanmirlst]

	return human_ages





human_mirna_ages = import_human_mirages()
human_gene_ages, time_tree_dict = import_pcg()

newlst = []


all_labels = sorted(list(set(human_gene_ages + human_mirna_ages)))



for age in human_mirna_ages:
	newlst.append(['%s (%.1f)' %(time_tree_dict[age], age), 'miRNA'])


for age in human_gene_ages:
	newlst.append(['%s (%.1f)' %(time_tree_dict[age], age), 'PC Gene'])

full_df = pd.DataFrame(newlst, columns=['Age (MYA)', 'Type' ])

sns.countplot(x='Age (MYA)', hue='Type', data=full_df)
sns.plt.show()

