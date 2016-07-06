import seaborn as sns
import pandas as pd
import csv

from scipy.stats import mannwhitneyu


def age_parser(age_txt):
	mirna2age = {}
	age2mirna = {}

	age_lst = [alpha for alpha in list(csv.reader(age_txt,delimiter='\t')) if alpha[0][0] != '#' ]

	for i in age_lst:
		mirna2age[i[0]] = float(i[1])
		age2mirna.setdefault(float(i[1]),[]).append(i[0])



	return mirna2age, age2mirna

def sort_mir(txt,txt2):
	mega_mir_lst = []
	famdict = {}
	mirlst_by_species = {}
	human_mirlst = {}

	meglst = [alpha[0] for alpha in list(csv.reader(txt,delimiter='\t'))]
	famlst = [alpha for alpha in list(csv.reader(txt2,delimiter='\t'))]

	for mir in meglst:
		species = mir[0:3]
		if species[-1] == 'v':
			continue
		mega_mir_lst.append(mir)


		mirlst_by_species.setdefault(species,[]).append(mir)
	
	current_fam = ''

	for i in famlst:
		lst = [alpha for alpha in i[0].split(' ') if alpha != '']
		if i[0][:2] == 'ID' : 
			current_fam = lst[1]
		if i[0][:2] == 'MI' :
			if 'v' in lst[2].split('-')[0]: continue
			if lst[2] not in mega_mir_lst: continue
			else:
				famdict.setdefault(current_fam,[]).append(lst[2])

	for key in famdict:
		new_lst  = [a for a in famdict[key] if 'hsa' in a]
		if len(new_lst) > 1:
			human_mirlst[key] = new_lst


	family_file_for_mirbase = open('../relevant_data/family_file_ph_selectmir.txt','w')

	for i in famdict:
		for mir in famdict[i]:
			if mir != famdict[i][-1]:
				family_file_for_mirbase.write('%s|mirBase:%s ' %(mir[:3], mir)) 
			else: family_file_for_mirbase.write('%s|mirBase:%s\n' %(mir[:3], mir)) 

	family_file_for_mirbase.close()





	return mega_mir_lst, mirlst_by_species, human_mirlst 


def map_relatives(dic):
	newdic = {}

	for key in dic:
		for el in dic[key]:
			newdic[el] = [a for a in dic[key] if a != el]

	return newdic



def gen_twolsts(mirna2age, mirna2family):
	in_fam = []
	no_fam = []

	tmp_mirna2family = map_relatives(mirna2family)

	for val in mirna2age:
		if val not in tmp_mirna2family:
			no_fam.append(mirna2age[val])
		else:
			if len(tmp_mirna2family[val]) > 2:
				in_fam.append(mirna2age[val])
			else:
				no_fam.append(mirna2age[val])

	print mannwhitneyu(in_fam, no_fam)



	pd_precursor = []

	for val in in_fam:
		pd_precursor.append([val, 'In Family'])

	for val in no_fam: pd_precursor.append([val,'Not In Family'])

	db = pd.DataFrame(pd_precursor,columns=['Age (MY)', 'miRNA Class'])

	sns.violinplot(x='miRNA Class', y='Age (MY)', data=db, cut=0)
	sns.plt.gca().set_ylim([0,1000])
	sns.plt.savefig('../figures/fam_nofam_agecomp_violin.pdf',bbox_inches='tight')
	sns.plt.close()






mirdb = '../relevant_data/star_mir_lst.txt'
famdb = '../relevant_data/miFam.dat'
agedb = '../relevant_data/allmir_ages/hsa_family_file_ph_allmir_dollo_age-time.protein_list'




mega_mir_lst, mirlst_by_species, mirna2family = sort_mir(open(mirdb,'r'),open(famdb,'r'))
mirna2age, age2mirna = age_parser(open(agedb, 'r'))


gen_twolsts(mirna2age, mirna2family)

