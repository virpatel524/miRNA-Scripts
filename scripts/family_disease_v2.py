import seaborn as sns
import pandas as pd
import csv
from distance import jaccard
from scipy.stats import spearmanr



def ratio(a,b,vector):
	p = 0
	q = 0
	r = 0
	s = 0

	for i in range(len(vector[a])):
		if vector[a][i] == 1 and vector[b][i] == 1:
			p += 1
		if vector[a][i] == 1 and vector[b][i] == 0:
			q += 1
		if vector[a][i] == 0 and vector[b][i] == 1:
			r += 1
		if vector[a][i] == 0 and vector[b][i] == 0:
			s += 1

	return 1.0 - float(q + r) / float(p + q + r)


def collapse_cancer_lst(mirna2disease):
	gen_classes = ['neopl', 'carc', 'lymph']
	dis2genclass = {}
	for dis in flatten(mirna2disease.values()):
		for val in gen_classes:
			if val in dis.lower(): 
				if val not in dis2genclass:
					dis2genclass[dis] = val
				continue


	mirna2disease_collapsed = {}



	for mir in mirna2disease:
		newdislst = []
		dislst = mirna2disease[mir]
		for dis in dislst:
			if dis in dis2genclass.keys():
				newdislst.append(dis2genclass[dis])
			else: newdislst.append(dis)

		newdislst = list(set(newdislst))

		mirna2disease_collapsed[mir] = newdislst

	return mirna2disease_collapsed







def flatten(l):
	return [item for sublist in l for item in sublist]

def map_relatives(dic):
	newdic = {}

	for key in dic:
		for el in dic[key]:
			newdic[el] = [a for a in dic[key] if a != el]

	return newdic


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


	mirna2family = human_mirlst.copy()

	mirna2family_edited = {}

	for alpha in mirna2family:
		if len(mirna2family[alpha]) > 3:
			mirna2family_edited[alpha] = mirna2family[alpha]




	return mega_mir_lst, mirlst_by_species, mirna2family_edited 


def diseaese_parser(disease_txt):
	disease2mirna = {}
	mirna2disease = {}

	disease_lst = list(csv.reader(disease_txt,delimiter='\t'))
	for i in disease_lst:
		disease2mirna.setdefault(i[1],[]).append(i[0])
		mirna2disease.setdefault(i[0],[]).append(i[1])

	return mirna2disease, disease2mirna


def age_parser(age_txt):
	mirna2age = {}
	age2mirna = {}

	age_lst = [alpha for alpha in list(csv.reader(age_txt,delimiter='\t')) if alpha[0][0] != '#' ]

	for i in age_lst:
		mirna2age[i[0]] = float(i[1])
		age2mirna.setdefault(float(i[1]),[]).append(i[0])

	return mirna2age, age2mirna


def binary_pd_gen(dic, biglst):
	mir_targetdb = pd.DataFrame()

	for val in dic:
		tmp = pd.DataFrame([dic[val],], index=[val,], columns=biglst)
		mir_targetdb.append(tmp)

	mir_targetdb.to_csv('../relevant_data/mir_predictions_target_vectordb.txt', sep='\t', encoding='utf-8')





def generate_class_vector(biglst, element):
	new_vec = len(biglst) * [0]

	for alpha in element:
		new_vec[biglst.index(alpha)] = 1

	return new_vec



def generate_matrix(db, str_rel):
	dic = {}
	for ind,item in enumerate(db.keys()):
		print str_rel, ind + 1,  len(db.keys())
		secdic = {}
		for secitem in db.keys():
			if secitem in dic:
				secdic[secitem] = dic[secitem][item]
				continue
			a = db[item]
			b = db[secitem]
			secdic[secitem] = compute_jaccard_index(a,b)

		dic[item] = secdic


	pd_pre = []

	for key in sorted(dic.keys()):
		newlst = [dic[key][i] for i in sorted(dic.keys())]
		pd_pre.append(newlst)

		

	new_pd = pd.DataFrame(pd_pre,columns=sorted(dic.keys()),index=sorted(dic.keys()))
	print new_pd
	new_pd.to_csv('../relevant_data/%s_dataframe.txt' %(str_rel), sep='\t', encoding='utf-8')

	return new_pd



def violin3cluster(originial_df, dict2clusterby, final_name, stratifier, dis_vector):
	clust_mirs = [alpha for alpha in originial_df.index if alpha in dict2clusterby]
	all_clust_vals = []
	newlst = []


	age2mirna = {}

	for mir in dict2clusterby:
		age2mirna.setdefault(dict2clusterby[mir],[]).append(mir)


	valslst = []

	for age in age2mirna:
		valslst.append([a for a in age2mirna[age] if a in originial_df.index])

	for el in valslst:
		for a in el:
			for b in el:
				if a == b: continue
				newlst.append([ratio(a,b,dis_vector), dict2clusterby[a]])



	new_pd = pd.DataFrame(newlst, columns=['Hamming Value', 'Age (MY)'])

	print spearmanr(new_pd['Hamming Value'].tolist(), new_pd['Age (MY)'].tolist())
	sns.boxplot(x='Age (MY)',y='Hamming Value', data=new_pd,showfliers=False)
	sns.plt.savefig('../figures/%s.pdf' %(final_name), bbox_inches='tight')

	sns.plt.close()

	# pd_precursor = []

	# for alpha in newlst:
	# 	if alpha[-1] in good_ages:
	# 		pd_precursor.append(alpha)




	# new_pd = pd.DataFrame(newlst, columns=['Hamming Value', 'miRNA Class', 'Age (MY)'])


	# sns.boxplot(x='Age (MY)',y='Hamming Value', data=new_pd)



mirdb = '../relevant_data/star_mir_lst.txt'
famdb = '../relevant_data/miFam.dat'
agedb = '../relevant_data/allmir_ages/hsa_family_file_ph_allmir_dollo_age-time.protein_list'
tardb = '../relevant_data/all_targets.txt'
expdb = '../relevant_data/exp_data_alldmir.txt'
timetreedb = '../relevant_data/time_tree_dates.txt'
diseasedb = '../relevant_data/hmdd_database.txt'

mega_mir_lst, mirlst_by_species, mirna2family = sort_mir(open(mirdb,'r'),open(famdb,'r'))
mirna2disease, disease2mirna = diseaese_parser(open(diseasedb,'r'))
mapped_mirna2family = map_relatives(mirna2family)
mirna2age, age2mirna = age_parser(open(agedb))

mirinfam = flatten(mirna2family.values())

mirdisfam = [a for a in mirinfam if a in mirna2disease]
mirdisnofam = [a for a in mirna2disease if a not in mirdisfam]

big_dis_lst = sorted(list(set(flatten(mirna2disease.values()))))

dis_vector = {}

for val in mirna2disease:
	dis_vector[val] = generate_class_vector(big_dis_lst, mirna2disease[val])

dis_pd = pd.read_csv('../relevant_data/disease_mirna_hamming_dataframe.txt', delimiter='\t', index_col=[0], encoding='utf-8')





mirna2disease_collapsed = collapse_cancer_lst(mirna2disease)


big_dis_lst_collapsed = sorted(list(set(flatten(mirna2disease_collapsed.values()))))

dis_vector_collapsed = {}

for val in mirna2disease_collapsed:
	dis_vector_collapsed[val] = generate_class_vector(big_dis_lst_collapsed, mirna2disease_collapsed[val])

violin3cluster(dis_pd, mirna2age, 'age_strat_dis_all_boxplot_ratio_uncollapsed', mirna2disease, dis_vector)
violin3cluster(dis_pd, mirna2age, 'age_strat_dis_all_boxplot_ratio_collapsed', mirna2disease_collapsed, dis_vector_collapsed)


