import seaborn as sns
import pandas as pd
import csv

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
		if a[-2] in tmp:
			newlst.append(a)

	return newlst


def stratify_numtot_age(classifier, numtot_dict, class_name, class2_enter, mirna2age,finname):
	pd_precursor = []

	print 
	ages_yes = []
	ages_no = []


	for val in numtot_dict:
		if val not in mirna2age: continue
		pd_precursor.append([numtot_dict[val], 'In miRNA %s' %(class_name), mirna2age[val]])


	db = pd.DataFrame(pd_precursor, columns=[class2_enter, 'miRNA Class', 'Age (MY)'])

	sns.boxplot(x='Age (MY)', y=class2_enter, data=db)
	sns.plt.savefig('../figures/%s.pdf' %(finname),bbox_inches='tight')
	sns.plt.close()





mirna2disease = parse_disease('../relevant_data/hmdd_database.txt')
mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')
mirna2family = parse_families('../relevant_data/miFam.dat')
mirna2numdisease = {}
mirna2numtargets = {}



mir_targetdb = pd.read_csv('../relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0], encoding='utf-8')

stratify_numtot_age(mirna2family, mirna2numdisease, 'Family', 'Number of Associated Diseases', mirna2age, 'age_control_mirnumdis_all_box')
