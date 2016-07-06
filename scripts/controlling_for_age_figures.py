import seaborn as sns
import pandas as pd
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







def parse_disease(disfle):
	distxt = list(csv.reader(open(disfle), delimiter='\t'))
	mirna2disease = {}

	for val in distxt:
		mirna2disease.setdefault(val[0],[]).append(val[1])

	return mirna2disease

def parse_age(agefle):
	mirna2age = {}
	age2mirna = {}

	age_lst = [alpha for alpha in list(csv.reader(open(agefle),delimiter='\t')) if alpha[0][0] != '#' ]

	for i in age_lst:
		mirna2age[i[0]] = float(i[1])
		age2mirna.setdefault(float(i[1]),[]).append(i[0])


	return mirna2age


def clean_common_last(lst1, lst2, input_lst):
	tmp = list(set(lst1).intersection(set(lst2)))
	newlst = []
	for a in input_lst:
		if a[-1] in tmp:
			newlst.append(a)

	return newlst


def stratify_numtot_age(classifier, numtot_dict, class_name, class2_enter, mirna2age,finname):
	pd_precursor = []

	ages_yes = []
	ages_no = []

	class_vals = flatten(classifier.values())

	for val in numtot_dict:
		if val not in mirna2age: continue
		if val in class_vals:
			pd_precursor.append([numtot_dict[val], 'In miRNA %s' %(class_name), mirna2age[val]])
			ages_yes.append(mirna2age[val])
		else:
			pd_precursor.append([numtot_dict[val], 'Not in miRNA %s' %(class_name), mirna2age[val]])
			ages_no.append(mirna2age[val])

	ages_lst = list(set(ages_yes).intersection(set(ages_no)))


	db = pd.DataFrame(pd_precursor, columns=[class2_enter, 'miRNA Class', 'Age (MY)'])
	print spearmanr(db[class2_enter].tolist(), db['Age (MY)'].tolist())

	sns.boxplot(x='Age (MY)', y=class2_enter, showfliers=False, data=db)
	sns.plt.savefig('../figures/%s.pdf' %(finname),bbox_inches='tight')
	sns.plt.close()

def heatmap_analysis(classifier, hamming_df, class_name, class2_enter, mirna2age, finname):
	yes = []
	no = []

	yes_ages = []
	no_ages = []

	datalst = []


	flipped_exlus = map_relatives(classifier)


	for alpha in hamming_df.index:
		if alpha not in mirna2age: continue
		for beta in hamming_df.index:
			if alpha == beta: continue
			if alpha in flipped_exlus:
				if beta in flipped_exlus[alpha]: 
					datalst.append([float(hamming_df[alpha][beta]), '%s miRNAs' %(class_name), mirna2age[alpha]])
					yes.append(float(hamming_df[alpha][beta]))
					yes_ages.append(mirna2age[alpha])
			else:
				datalst.append([float(hamming_df[alpha][beta]), 'Non-%s miRNAs' %(class_name), mirna2age[alpha]])
				no.append(float(hamming_df[alpha][beta]))
				no_ages.append(mirna2age[alpha])




	new_df = pd.DataFrame(datalst,columns=['Hamming Distance', 'miRNA Class', 'Age (MY)'])
	print spearmanr(new_df['Hamming Distance'].tolist(), new_df['Age (MY)'].tolist())
	sns.boxplot(x='Age (MY)', y='Hamming Distance',data=new_df, fliersize=0)
	sns.plt.gca().set_ylim([0,.13])
	sns.plt.savefig('../figures/%s.pdf' %(finname),bbox_inches='tight')
	sns.plt.close()




mirna2disease = parse_disease('../relevant_data/hmdd_database.txt')
mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')
mirna2family = parse_families('../relevant_data/miFam.dat')
mirna2numdisease = {}
mirna2numtargets = {}



mir_targetdb = pd.read_csv('../relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0], encoding='utf-8')
round_robyn_target = pd.read_csv('../relevant_data/target_heatmap_dataframe.txt', sep='\t',index_col=[0])

for alpha in mirna2disease:
	mirna2numdisease[alpha] = len(mirna2disease[alpha])

for alpha in mir_targetdb.index:
	mirna2numtargets[alpha] = sum(mir_targetdb.loc[alpha].tolist())


# stratify_numtot_age(mirna2family, mirna2numdisease, 'Family', 'Number of Associated Diseases', mirna2age, 'age_control_mirnumdis_famnofam_box')
stratify_numtot_age(mirna2family, mirna2numtargets, 'Family', 'Number of PC Gene Targets', mirna2age, 'age_control_mirnumtar_famnofam_box')

heatmap_analysis(mirna2family, round_robyn_target, 'Families', 'test', mirna2age, 'hamming_targets_boxplot_agestrat')
