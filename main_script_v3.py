import string
import re
import scipy
import time
import math, csv
import random
import operator, itertools
from distance import hamming
import numpy as np
from numpy.random import randn
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, mannwhitneyu
from distance import hamming
from numpy import mean, std, median
import pandas as pd

sns.axes_style('whitegrid')
sns.set_style("whitegrid")
sns.set_context("poster",font_scale=1.5)

# global variables

bad_lst = ['ghb','ssp','fru','hsv','hvt','ebv','rlc','hhv','mcm','pbi','jcv','bkv','mdv','hma','bpc','ksh']



def reverse_dict(dic):
	new_dic = {}
	for item in dic:
		vals = dic[item]
		for a in vals:
			new_dic.setdefault(a, []).append(item)

	return new_dic

def two_dic_common(dic1, dic2):
	b1 = dic1.keys()
	b2 = dic2.keys()

	return [val for val in b1 if val in b2]

def flatten(l):
	return [item for sublist in l for item in sublist]

def three_way_map(dic1, dic2):
	newdic = {}

	for item in dic1:
		all_sub_dic1 = dic1[item]
		meglst = []
		for alpha in all_sub_dic1:
			if alpha in dic2:
				meglst.append(dic2[alpha])
		finlst = list(set(flatten(meglst)))
		if len(finlst) != 0:
			newdic[item] = finlst

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
		if species in bad_lst:
			continue
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
			if lst[2][:3] in bad_lst: continue
			if 'v' in lst[2].split('-')[0]: continue
			if lst[2] not in mega_mir_lst: continue
			else:
				famdict.setdefault(current_fam,[]).append(lst[2])

	for key in famdict:
		new_lst  = [a for a in famdict[key] if 'hsa' in a]
		if len(new_lst) > 1:
			human_mirlst[key] = new_lst


	family_file_for_mirbase = open('/Users/virpatel/Desktop/pub_stuff/relevant_data/family_file_ph_selectmir.txt','w')

	for i in famdict:
		for mir in famdict[i]:
			if mir != famdict[i][-1]:
				family_file_for_mirbase.write('%s|mirBase:%s ' %(mir[:3], mir)) 
			else: family_file_for_mirbase.write('%s|mirBase:%s\n' %(mir[:3], mir)) 

	family_file_for_mirbase.close()





	return mega_mir_lst, mirlst_by_species, human_mirlst 


def diseaese_parser(disease_txt):
	disease2mirna = {}
	mirna2disease = {}

	disease_lst = list(csv.reader(disease_txt,delimiter='\t'))
	for i in disease_lst:
		disease2mirna.setdefault(i[1],[]).append(i[0])
		mirna2disease.setdefault(i[0],[]).append(i[1])

	return mirna2disease, disease2mirna	

	
	disease_txt.close()

def age_parser(age_txt):
	mirna2age = {}
	age2mirna = {}

	age_lst = [alpha for alpha in list(csv.reader(age_txt,delimiter='\t')) if alpha[0][0] != '#' ]

	for i in age_lst:
		mirna2age[i[0]] = float(i[1])
		age2mirna.setdefault(float(i[1]),[]).append(i[0])

	with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/hsa_all_mir_lst.txt','w') as mirlst:
		for mirna in mirna2age:
			mirlst.write(mirna + '\n')
			


	return mirna2age, age2mirna

def time_tree_parse(time_tree_db):
	age2clade = {}
	clade2age = {}
	with open(time_tree_db) as time_tree_fle:
		lst = [a for a in list(csv.reader(time_tree_fle,delimiter='\t')) if len(a) > 1]
		for alpha in lst:
			age2clade[float(alpha[-1])] = alpha[0]
			clade2age[alpha[0]] = float(alpha[-1])

	return age2clade, clade2age



def get_mirna_disease_age_relationship(mirna2age, mirna2disease):
	mirnas_in_q = list(set(mirna2age.keys()).intersection(mirna2disease.keys()))
	

	age_dict = []
	num_dis_dict = []


	for i in mirnas_in_q:
		age_dict.append(mirna2age[i])
		num_dis_dict.append(len(mirna2disease[i]))


def parse_target_data(tardb,taragedb,timetreedb):

	mirna2target = {}
	tar2age = {}
	clade2age = {}

	parsed_tar = []
	parsed_ages = []

	master_tarlst = []




	with open(tardb) as tardb_fle:
		parsed_tar = [a for a in list(csv.reader(tardb_fle,delimiter='\t') ) if len(a) > 1]
		for alpha in parsed_tar:
			mirna2target.setdefault(alpha[0],[]).append(alpha[1])
		

	master_tarlst = list(set([item for sublist in mirna2target.values() for item in sublist]))


	with open(taragedb) as tardb_fle:
		data = list(csv.reader(tardb_fle,delimiter='\t'))
		for i in data:
			tar2age[i[0]] = float(i[1]) 


	return mirna2target, tar2age

			

def mir_num_dis_bin(mirna2disease, mirna2age, age2clade):

	mirnotindis = []
	mirindis = []
	for mir in mirna2age:
		if mir in mirna2disease:
			mirindis.append(mirna2age[mir])
		else:
			mirnotindis.append(mirna2age[mir])

	print mean(mirnotindis), mean(mirindis)

	return



	agelst = []
	dislst = []

	for mir in list(set(mirna2age.keys()).intersection(mirna2disease.keys())):	
		agelst.append(float(mirna2age[mir])) 
		dislst.append(float(len(mirna2disease[mir])))


	oldage = agelst[:]


	mirindis = [mirna2age[a] for a in mirna2age  if a in mirna2disease]
	mir_not_dis = [mirna2age[a] for a in mirna2age  if a not in mirna2disease]




	labels = sorted(list(set(agelst)))
	str_labels = ['%s (%.1f)' %(age2clade[a], a) for a in labels]

	binlst = [[] for _ in xrange(len(labels))]

	for ind, alpha in enumerate(agelst):
		binlst[labels.index(alpha)].append(dislst[ind])


	disease_age_pd = pd.DataFrame({'mir_ages':agelst, 'mir_disease_nums': dislst})
	disease_age_pd = disease_age_pd.sort('mir_ages',ascending=1)

	f = plt.gcf()
	f.set_size_inches(20, 10)


	sns.boxplot(x='mir_ages',y='mir_disease_nums',data=disease_age_pd)

	plt.xticks(range(0,len(labels)), str_labels, rotation = 65)
	plt.gca().set_ylim([0,70])
	plt.ylabel('Number of Diseases', fontsize=15)
	plt.xlabel('miRNA Clade of Origination',fontsize=15)
	plt.subplots_adjust(bottom=0.20)



	num_of_dismir_perage = [len(disease_age_pd.loc[disease_age_pd['mir_ages'] == alpha]) for alpha in labels]

	plt.savefig('/Users/virpatel/Desktop/pub_stuff/figures/mirage_vs_numdis.pdf', bbox_inches='tight')

	plt.close()


	# with open('relevant_data/mirna2age_lst.txt','w') as mir_fle:
	# 	for mir in mirna2age:
	# 		mir_fle.write('%s\t%.1f\n' %(mir, mirna2age[mir]))


	# with open('relevant_data/mirdis_lst.txt','w') as mirdis_fle:
	# 	for mir in mirna2disease:
	# 		if mir in mirna2age:
	# 			mirdis_fle.write('%s\n' %(mir))

	# with open('relevant_data/age_label_fle.txt','w') as rel_fle:
	# 	for age in age2clade:
	# 		rel_fle.write('%.1f\t%s\n' %(age, age2clade[age]))







def mir_num_dis_bin_collapsed(mirna2disease, mirna2age, age2clade):

	agelst = []
	dislst = []

	for mir in list(set(mirna2age.keys()).intersection(mirna2disease.keys())):	
		agelst.append(float(mirna2age[mir])) 
		dislst.append(float(len(mirna2disease[mir])))


	oldage = agelst[:]


	mirindis = [mirna2age[a] for a in mirna2age  if a in mirna2disease]
	mir_not_dis = [mirna2age[a] for a in mirna2age  if a not in mirna2disease]




	labels = sorted(list(set(agelst)))
	str_labels = ['%s (%.1f)' %(age2clade[a], a) for a in labels]

	binlst = [[] for _ in xrange(len(labels))]

	for ind, alpha in enumerate(agelst):
		binlst[labels.index(alpha)].append(dislst[ind])


	disease_age_pd = pd.DataFrame({'mir_ages':agelst, 'mir_disease_nums': dislst})
	disease_age_pd = disease_age_pd.sort('mir_ages',ascending=1)

	f = plt.gcf()
	f.set_size_inches(20, 10)

	print spearmanr(disease_age_pd['mir_ages'], disease_age_pd['mir_disease_nums'])


	sns.boxplot(x='mir_ages',y='mir_disease_nums',data=disease_age_pd)

	plt.xticks(range(0,len(labels)), str_labels, rotation = 65)
	plt.gca().set_ylim([0,45])
	plt.ylabel('Number of Diseases', fontsize=15)
	plt.xlabel('miRNA Clade of Origination',fontsize=15)
	plt.subplots_adjust(bottom=0.20)



	num_of_dismir_perage = [len(disease_age_pd.loc[disease_age_pd['mir_ages'] == alpha]) for alpha in labels]

	plt.savefig('/Users/virpatel/Desktop/pub_stuff/figures/mirage_vs_numdis_collapsed.pdf', bbox_inches='tight')

	plt.close()


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





def target_analysis(mirna2age, mirna2disease, mirna2target, gene2age):


	mir_targetdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0], encoding='utf-8')


	target_lst = list(mir_targetdb.columns.values)

	mirnanumdis = []
	mirnanumtar = []
	mir_avg_tar_age_dis = []
	mir_avg_tar_age_nondis = []
	mir_age = []

	for mir in mir_targetdb.index:
		if mir not in mirna2disease: mirnanumdis.append(0)
		else: mirnanumdis.append(len(mirna2disease[mir]))
		bintarlt = mir_targetdb.loc[mir].tolist()
		mirnanumtar.append(sum(bintarlt))
		tarages = [float(gene2age[target_lst[ind]]) for ind, a in enumerate(bintarlt) if target_lst[ind] in gene2age and a == 1]
		# mir_avg_tar_age_all.append(median(tarage))
		mir_avg_tar_age_dis.append(mean(tarages))

	for mir in mir_targetdb.index:
		if mir not in mirna2disease:
			bintarlt = mir_targetdb.loc[mir].tolist()
			tarages = [float(gene2age[target_lst[ind]]) for ind, a in enumerate(bintarlt) if target_lst[ind] in gene2age and a == 1]
			mir_avg_tar_age_nondis.append(mean(tarages))




	print mannwhitneyu(mir_avg_tar_age_dis,mir_avg_tar_age_nondis)






def gen_dis_db(disease2mirna,mirna2age):
	for dis in disease2mirna:
		name = dis.replace(' ','-')
		with open('relevant_data/dis2mir_db/%s_mir.txt' %(name),'w') as cur_disfle:
			for mir in disease2mirna[dis]:
				if mir in mirna2age:
					cur_disfle.write('%s\n' %(mir))


def get_list_of_dictionary(dic):
	return sorted(list(set(list(itertools.chain.from_iterable(dic.values())))))


def generate_class_vector(biglst, element):
	new_vec = len(biglst) * [0]

	for alpha in element:
		new_vec[biglst.index(alpha)] = 1

	return new_vec

	
def family_homogenity(human_mirlst, mirna2disease, mirna2age):

	family_avg_age = []
	family_avg_hamming = []
	family_percent_invoved_dis = []
	
	all_mir_vector_df = pd.DataFrame()

	dislst = get_list_of_dictionary(mirna2disease)

	all_fam_mir = list(itertools.chain.from_iterable(human_mirlst.values()))

	for mir in all_fam_mir:
		if mir in mirna2disease:
			vec = generate_class_vector(dislst, mirna2disease[mir])
			tmp = pd.DataFrame([vec,],index=[str(mir),], columns=dislst)
			all_mir_vector_df = all_mir_vector_df.append(tmp)


	for fam in human_mirlst:
		family_vector = []
		mirlst = [a for a in human_mirlst[fam] if a in mirna2disease]
		if len(mirlst) < 4: continue
		for mir in mirlst:
			for other_mir in mirlst:
				if mir == other_mir: continue
				family_vector.append(hamming(all_mir_vector_df.loc[mir], all_mir_vector_df.loc[other_mir],normalized=True))
		
		family_avg_hamming.append(mean(family_vector))
		family_avg_age.append(round(mean([float(mirna2age[mirna]) for mirna in mirlst if mirna in mirna2age]),1))
		family_percent_invoved_dis.append(float(len(mirlst)) / float(len(human_mirlst[fam])))



	print spearmanr(family_percent_invoved_dis, family_avg_hamming)

	fam_df = pd.DataFrame(zip(family_avg_age,family_avg_hamming,family_percent_invoved_dis),columns=['fam_age','fam_hamming','fam_per'])


	fam_df = fam_df.sort('fam_age',ascending=1)

	f = plt.gcf()
	f.set_size_inches(20, 10)

	sns.boxplot(x='fam_age',y='fam_hamming',data=fam_df)

	plt.xticks(range(0,len(list(set(family_avg_age)))), [str(a) for a in sorted(list(set(family_avg_age)))])
	plt.gca().set_ylim([0,.12])
	plt.ylabel('Average Family Disease Vector Hamming Distance (0-1)', fontsize=15)
	plt.xlabel('Average Family Age',fontsize=15)
	plt.subplots_adjust(bottom=0.20)
	plt.savefig('figures/family_disease_hamming.pdf',bbox_inches='tight')
	plt.close()





def family_homogenity_collapsed(human_mirlst, mirna2disease, mirna2age):

	family_avg_age = []
	family_avg_hamming = []
	family_percent_invoved_dis = []
	
	all_mir_vector_df = pd.DataFrame()

	dislst = get_list_of_dictionary(mirna2disease)

	all_fam_mir = list(itertools.chain.from_iterable(human_mirlst.values()))

	for mir in all_fam_mir:
		if mir in mirna2disease:
			vec = generate_class_vector(dislst, mirna2disease[mir])
			tmp = pd.DataFrame([vec,],index=[str(mir),], columns=dislst)
			all_mir_vector_df = all_mir_vector_df.append(tmp)


	for fam in human_mirlst:
		family_vector = []
		mirlst = [a for a in human_mirlst[fam] if a in mirna2disease]
		if len(mirlst) < 4: continue
		for mir in mirlst:
			for other_mir in mirlst:
				if mir == other_mir: continue
				family_vector.append(hamming(all_mir_vector_df.loc[mir], all_mir_vector_df.loc[other_mir],normalized=True))
		
		family_avg_hamming.append(mean(family_vector))
		family_avg_age.append(round(mean([float(mirna2age[mirna]) for mirna in mirlst if mirna in mirna2age]),1))
		family_percent_invoved_dis.append(float(len(mirlst)) / float(len(human_mirlst[fam])))



	print spearmanr(family_percent_invoved_dis, family_avg_hamming)

	fam_df = pd.DataFrame(zip(family_avg_age,family_avg_hamming,family_percent_invoved_dis),columns=['fam_age','fam_hamming','fam_per'])


	fam_df = fam_df.sort('fam_age',ascending=1)

	f = plt.gcf()
	f.set_size_inches(20, 10)

	sns.boxplot(x='fam_age',y='fam_hamming',data=fam_df)

	plt.xticks(range(0,len(list(set(family_avg_age)))), [str(a) for a in sorted(list(set(family_avg_age)))])
	plt.gca().set_ylim([0,.094])
	plt.ylabel('Average Family Disease Vector Hamming Distance (0-1)', fontsize=15)
	plt.xlabel('Average Family Age',fontsize=15)
	plt.subplots_adjust(bottom=0.20)
	plt.savefig('figures/family_disease_hamming_collapsed.pdf',bbox_inches='tight')
	plt.close()








def target_gene_dataframe(mirna2age, mirna2disease,mirna2target, target2age):
	target_agedb = pd.DataFrame()
	mir_targetdb = pd.DataFrame()

	mir_age = []
	mir_tar_age = []

	for mir in mirna2target:
		if mir in mirna2age:
			mir_age.append(mirna2age[mir])
			for tar in mirna2target[mir]:
				mir_tar_age.append(tar)


	mir_tar_age = [target2age[a] for a  in  list(set(mir_tar_age)) if a  in target2age]

	mir_age  = np.array(mir_age)
	mir_tar_age = np.array(mir_tar_age)
	print mir_age.shape
	print mir_tar_age.shape
	print mannwhitneyu(mir, mir_tar_age)






	for target in target2age:
		tmp = pd.DataFrame([float(target2age[target]),], index=[target,], columns=['age',])
		target_agedb = target_agedb.append(tmp)

	tar_base_vec = get_list_of_dictionary(mirna2target)


	
	for index,mir in enumerate(mirna2target):
		print index + 1, len(mirna2target)
		newdata = generate_class_vector(tar_base_vec, mirna2target[mir])
		tmp = pd.DataFrame([newdata,], index=[mir,],columns=tar_base_vec)
		mir_targetdb = mir_targetdb.append(tmp)



	mir_targetdb.to_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/mir_target_vectordb.txt', sep='\t', encoding='utf-8')




def generate_matrix(db, str_rel):
	dic = {}
	for ind,item in enumerate(db.index):
		print str_rel, ind + 1,  len(db.index)
		secdic = {}
		for secitem in db.index:
			if secitem in dic:
				secdic[secitem] = dic[secitem][item]
				continue
			a = db.loc[item].tolist()
			b = db.loc[secitem].tolist()
			secdic[secitem] = hamming(a,b,normalized=True)

		dic[item] = secdic


	pd_pre = []

	for key in sorted(dic.keys()):
		newlst = [dic[key][i] for i in sorted(dic.keys())]
		pd_pre.append(newlst)

		

	new_pd = pd.DataFrame(pd_pre,columns=sorted(dic.keys()),index=sorted(dic.keys()))
	new_pd.to_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/%s_dataframe.txt' %(str_rel), sep='\t', encoding='utf-8')

	return dic





def target_gene_expression_analysis(mirna2age, mirna2disease,mirna2family,gene2age):
		mir_targetdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0], encoding='utf-8')
		mir_expdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])

		family_target_hamming = []
		family_target_avg_age = []
		family_perc_dis = []


		tardis = []
		tarnotindis = []




		generate_matrix(mir_targetdb,'target_heatmap')
		generate_matrix(mir_expdb,'tis_exp_heatmap')

		return








# 		# # for fam in mirna2family:
# 		# # 	family_vector = []
# 		# # 	mirlst = [a for a in mirna2family[fam] if a in mir_targetdb.index]
# 		# # 	mirdislst = [a for a in mirna2family[fam] if a in mirna2disease]
# 		# # 	if len(mirlst) < 4: continue
# 		# # 	if len(mirdislst) < 4: continue
# 		# # 	for mir in mirlst:
# 		# # 		for other_mir in mirlst:
# 		# # 			if mir == other_mir: continue
# 		# # 			family_vector.append(hamming(mir_targetdb.loc[mir], mir_targetdb.loc[other_mir],normalized=True))
				
# 		# # 	family_target_hamming.append(std(family_vector))
# 		# # 	family_target_avg_age.append(round(mean([float(mirna2age[mirna]) for mirna in mirlst if mirna in mirna2age]),1))
# 		# # 	family_perc_dis.append(float(len(mirdislst)) / float(len(mirna2family[fam])))


# 		# target_lst = list(mir_targetdb.columns.values)

# 		# mirnanumdis = []
# 		# mirnanumtar = []
# 		# mir_avg_tar_age_dis = []
# 		# mir_avg_tar_age_nondis = []
# 		# mir_age = []
# 		# mir_median_tar_age_all = []

# 		# for mir in mir_targetdb.index:
# 		# 	if mir not in mirna2disease: mirnanumdis.append(0)
# 		# 	else: mirnanumdis.append(len(mirna2disease[mir]))
# 		# 	bintarlt = mir_targetdb.loc[mir].tolist()
# 		# 	mirnanumtar.append(sum(bintarlt))
# 		# 	tarages = [float(gene2age[target_lst[ind]]) for ind, a in enumerate(bintarlt) if target_lst[ind] in gene2age and a == 1]
# 		# 	mir_median_tar_age_all.append(median(tarages))
# 		# 	mir_avg_tar_age_dis.append(mean(tarages))

# 		# for mir in mir_targetdb.index:
# 		# 	if mir not in mirna2disease:
# 		# 		bintarlt = mir_targetdb.loc[mir].tolist()
# 		# 		tarages = [float(gene2age[target_lst[ind]]) for ind, a in enumerate(bintarlt) if target_lst[ind] in gene2age and a == 1]
# 		# 		mir_avg_tar_age_nondis.append(median


# 		# yung_num_tis = []
# 		# old_num_tis = []

# 		# dis_num = []
# 		# mir_age_lst = []
# 		# exp_val = []

# 		# for mir in mir_expdb.index:
# 		# 	if mir in mirna2age:
# 		# 		v = float(sum(mir_expdb.loc[mir].tolist()))
# 		# 		mir_age_lst.append(mirna2age[mir])
# 		# 		mirage = mirna2age[mir]



# 		# 		exp_val.append(v)

# 		# 		if mirage > 100.0: old_num_tis.append(sum(mir_expdb.loc[mir].tolist()))
# 		# 		else: yung_num_tis.append(sum(mir_expdb.loc[mir].tolist()))



# 		# plt.scatter(mir_age_lst, exp_val)
# 		# plt.ylabel('Tissue Expression Count')
# 		# plt.xlabel('miRNA Age')
# 		# plt.subplots_adjust(bottom=0.20)
# 		# plt.savefig('figures/mirna_exp_all.pdf',bbox_inches='tight')
# 		# plt.close()



# 		# print mannwhitneyu(yung_num_tis, old_num_tis)

# 		mir_in_fam_pot = []
# 		mir_in_fam = []
# 		mir_not_in_fam = []

# 		mirna_in_hamming_2_exp = {}

# 		for mir in mirna2family:
# 			if len(mirna2family[mir]) > 3:
# 				mir_in_fam_pot += mirna2family[mir]
# 		expdb = []

# 		for mirna in mir_expdb.index:
# 			if mirna not in mirna2age: continue
# 			mirna_in_hamming_2_exp[mirna] = mir_expdb.loc[mirna].tolist()
# 			if mirna in mir_in_fam_pot:
# 				mir_in_fam.append(mirna)
# 				expdb.append([float(sum(mir_expdb.loc[mirna].tolist())), float(mirna2age[mirna]), 'In miRNA Family'])			
# 			else:
# 				mir_not_in_fam.append(mirna)
# 				expdb.append([float(sum(mir_expdb.loc[mirna].tolist())), float(mirna2age[mirna]), 'Not In miRNA Family'])			

# 		age1 = [mirna2age[a] for a in mir_in_fam ]
# 		age2 = [mirna2age[a] for a in mir_not_in_fam]
# 		gen1 = [sum(mirna_in_hamming_2_exp[a]) for a in mir_in_fam ]
# 		gen2 = [sum(mirna_in_hamming_2_exp[a]) for a in mir_not_in_fam]


# 		expdb = pd.DataFrame(expdb, columns=['num','age','In miRNA Family?'])
# 		expdb = expdb.sort('age',ascending=1)


# 		with  sns.plotting_context(font_scale=300):
# 			sns.violinplot(x='age',y='num',hue='In miRNA Family?',data=expdb,palette="muted", width=.7,legend=False,cut = 0)

# 			fig = plt.gcf()
# 			frame = plt.legend(frameon=True, loc='bottom right' )
# 			fig.set_size_inches(30, 10.5)

# 			ax1 = plt.gca()
# 			ax1.set_xlim([-1,17])
# 			ax1.set_ylim([-0.1, 20.5])


# 			plt.savefig('figures/violin_fam_no_fam_exp.pdf',bbox_inches='tight')

# 			plt.close()



# 		# f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)


# 		# ax1.scatter(age2, gen2)
# 		# ax1.set_ylabel('Age of miRNAs Not Found in Families (MYA)')
# 		# ax1.set_xlabel('Number of Tissues with miRNA Expression')
# 		# ax1.set_ylim([0,20])
# 		# ax1.set_xlim([0,1000])

# 		# ax2.scatter(age1, gen1)
# 		# ax2.set_xlabel('Number of Tissues with miRNA Expression')
# 		# ax2.set_ylim([0,20])
# 		# ax2.set_xlim([0,1000])

# 		# plt.subplots_adjust(bottom=0.20)
# 		# plt.savefig('figures/fam_tis_2tile.pdf',bbox_inches='tight')
# 		# plt.close()






# 		# print gen1

# 		# print mannwhitneyu(gen1, gen2)



# 		# fam2allvals = {}

# 		# for fam in mirna2family:

# 		# 	if len([a for a in mirna2family[fam] if a in mir_expdb.index]) < 4: continue
# 		# 	lst_ham = []
# 		# 	fam_ages = [mirna2age[a] for a in mirna2family[fam] if a in mirna2age]
# 		# 	if len(fam_ages) == 0: continue

# 		# 	for mir in mirna2family[fam]:
# 		# 		for secmir in mirna2family[fam]:
# 		# 			if mir == secmir: continue
# 		# 			if mir not in mir_expdb.index: continue
# 		# 			if secmir not in mir_expdb.index: continue
# 		# 			lst_ham.append(hamming(mirna_in_hamming_2_exp[mir], mirna_in_hamming_2_exp[secmir], normalized=True))

# 		# 	fam2allvals[fam] = [len(mirna2family[fam]),mean(lst_ham), max(lst_ham), mean(fam_ages), max(fam_ages)]

# 		# # for mir in mir_not_in_fam

# 		# lst2 = [fam2allvals[fam][2] for fam in fam2allvals]
# 		# lst1 = [fam2allvals[fam][0] for fam in fam2allvals]
# 		# plt.scatter(lst1, lst2)
# 		# plt.savefig('figures/num_hererog.pdf')

		
# 		# plt.close()



# 		# lst2 = [fam2allvals[fam][2] for fam in fam2allvals]
# 		# lst1 = [fam2allvals[fam][-1] for fam in fam2allvals]
# 		# plt.scatter(lst1, lst2)
# 		# plt.savefig('figures/age_hererog.pdf')

# 		# # print speamanr(lst1, lst2)





def disease_bootstrapping(mirna2age, mirna2disease,mirna2target,gene2age):
	disease2mirna = reverse_dict(mirna2disease)

	# for dis in disease2mirna:
	# 	age_of_supporting_mir = [mirna2age[a] for a  in disease2mirna[dis] if a in mirna2age]
	# 	med_dis = float(mean(age_of_supporting_mir))
	# 	if len(age_of_supporting_mir) > 2:
	# 		counter_over  = 0
	# 		counter_under = 0
	# 		for i in range(10000):
	# 			while_loop_safety = 0
	# 			new_ages_lst = []

	# 			while_loop_safety += 1
	# 			new_ages_lst = [mirna2age[ran_choice] for ran_choice in random.sample(set(two_dic_common(mirna2age,mirna2disease)),len(age_of_supporting_mir))]
	# 			if float(mean(new_ages_lst)) > med_dis: counter_under += 1
	# 			if float(mean(new_ages_lst)) < med_dis: counter_under += 1

	# 		print "Disease:%s, prob it's younger:%f, prob it's older:%f" %(dis,float(counter_under)/ float(10000),float(counter_over)/ float(10000))


	with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/mann-whit-disagelst.txt','w') as dislstfle:
			alldismir = [mirna2age[a] for a in mirna2disease if a in mirna2age]
			cancers = flatten(list(csv.reader(open('/Users/virpatel/Desktop/pub_stuff/relevant_data/cancerlst.txt','r'),delimiter='\t')))
			num_canc_non = 0
			num_canc_yes = 0
			counter = 0
			for dis in disease2mirna:
				age_of_supporting_mir = [mirna2age[a] for a  in disease2mirna[dis] if a in mirna2age]
				z,b  = mannwhitneyu(alldismir, age_of_supporting_mir)
				z = float(b)

				if z < 0.005: 
					counter += 1
					if dis in cancers:
						num_canc_yes += 1
					dislstfle.write('Disease:%s, mann: %s\n' %(dis, z))
				else:
					num_canc_non += 1

			print float(counter) / float(len(disease2mirna))
			print float(num_canc_yes) / float(len(cancers))
			print float(num_canc_yes) / float(counter)




	## setup for gene analysis

	# dis2tar = three_way_map(disease2mirna, mirna2target)
	# alltar_age = [gene2age[a] for a  in list(set(flatten(dis2tar.values()))) if a  in gene2age]

	# for dis in dis2tar:
	# 	print dis
	# 	pottarage = [gene2age[a] for a  in dis2tar[dis] if a in gene2age]
	# 	medpot = median(pottarage)
	# 	counter_under = 0
	# 	counter_over = 0 

	# 	for i in range(10000):
	# 		new_ages_lst = random.sample(alltar_age, len(pottarage))
	# 		if float(median(new_ages_lst)) > medpot: counter_under += 1
	#  		if float(median(new_ages_lst)) < medpot: counter_under += 1



	# 	print "Disease:%s, prob it's younger:%f, prob it's older:%f" %(dis,float(counter_under)/ float(10000),float(counter_over)/ float(10000))


def main_fraction_under_figure(mirna2tar, mirna2age, target2age):

	counter = 0
	perc_younger_lst = []
	tot_counter = 0
	for mirna in mirna2tar:
		if mirna not in mirna2age: continue
		age_set = [target2age[alpha] for alpha in mirna2tar[mirna] if alpha in target2age]


		perc_younger_lst.append(float(sum(i < mirna2age[mirna] for i in  age_set))/ float(len(age_set)))



	print len(sorted(perc_younger_lst))


	sns.distplot(perc_younger_lst)

	plt.gca().set_xlim([0,.6])
	plt.ylabel('Number of miRNAs')
	plt.xlabel('Fraction of Protein Coding Targets Younger than miRNA')
	plt.subplots_adjust(bottom=0.20)
	plt.savefig('figures/mirna_age_fraction.pdf',bbox_inches='tight')
	plt.close()



def generate_violin_pd(dictionary, pd_db):
	return






def heatmap_analysis(mirna2age, mirna2disease, mirna2family, gene2age):



	mirna2family_edited = {}

	for alpha in mirna2family:
		if len(mirna2family[alpha]) > 3:
			mirna2family_edited[alpha] = mirna2family[alpha]


	# round_robyn_target = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/target_heatmap_dataframe.txt', sep='\t',index_col=[0])
	# round_robyn_exp = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/tis_exp_heatmap_dataframe.txt', sep='\t',index_col=[0])


	# mirnas_in_family = []
	# mirnas_notin_family = []

	# for a in mirna2family:
	# 	if len(mirna2family[a]) < 4: continue
	# 	else: mirnas_in_family = mirnas_in_family + mirna2family[a]

	# for a in mirna2age:
	# 	if a not in mirnas_in_family:
	# 		mirnas_notin_family.append(a)


	# mirnas_in_dis = mirna2disease.keys()
	# mirnas_notindis = [a for a in mirna2age.keys() if a not in mirna2disease]

	# dis_nondis_target_val = []
	# dis_nondis_target_bool = []

	# dis_nondis_target_master = []

	# mir_dis_target = []
	# mir_nondis_target = []

	# for alpha in round_robyn_target.index:
	# 	for beta in round_robyn_target.index:
	# 		if alpha == beta: continue
	# 		if alpha in mirna2disease and beta in mirna2disease:
	# 			mir_dis_target.append(float(round_robyn_target[alpha][beta]))
	# 			dis_nondis_target_val.append([float(round_robyn_target[alpha][beta]), 'Disease miRNAs'])
				
	# 		else:
	# 			mir_nondis_target.append(float(round_robyn_target[alpha][beta]))
	# 			dis_nondis_target_val.append([float(round_robyn_target[alpha][beta]), 'Non-Disease miRNAs'])




	# dis_nondis_target_master = pd.DataFrame(dis_nondis_target_val,columns=['Comparison Normalized Hamming Distance (0.0-1.0)','miRNA Class'])

	# print dis_nondis_target_master


	# sns.violinplot(x='miRNA Class',y='Comparison Normalized Hamming Distance (0.0-1.0)',data=dis_nondis_target_master, cut=0)
	# tot = float(round_robyn_target.values.max())

	# plt.gca().set_ylim([-0.005,.13])




	# plt.savefig('figures/mir_dis_tar_hamming.pdf',bbox_inches='tight')

	# plt.close()



	# mir_targetdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0], encoding='utf-8')

	# masterlst = []
	# totnumdis = []
	# totnumnondis = []

	# for mir in mir_targetdb.index:
	# 	if mir in mirna2disease:
	# 		masterlst.append([sum(mir_targetdb.loc[mir].tolist()), 'Disease miRNAs'])
	# 		totnumdis.append(sum(mir_targetdb.loc[mir].tolist()))
	# 	else: 
	# 		masterlst.append([sum(mir_targetdb.loc[mir].tolist()), 'Non-Disease miRNAs'])
	# 		totnumnondis.append(sum(mir_targetdb.loc[mir].tolist()))


	# print mean(totnumdis), mean(totnumnondis)


	# dis_nondis_target_master = pd.DataFrame(masterlst,columns=['Number of Associated Targets', 'miRNA Class'])

	# sns.violinplot(x='miRNA Class',y='Number of Associated Targets',data=dis_nondis_target_master, cut=0)
	# plt.gca().set_ylim([-10, 3000])

	# plt.savefig('figures/mir_dis_num_tar_violin.pdf',bbox_inches='tight')


	# mir_expdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])


	# masterlst = []
	# totnumfam = []
	# totnumfam = []

	# for mir in mir_expdb.index:
	# 	if mir in mirna2disease:
	# 		masterlst.append([sum(mir_expdb.loc[mir].tolist()), 'Disease miRNAs'])
	# 		totnumdis.append(sum(mir_expdb.loc[mir].tolist()))
	# 	else: 
	# 		masterlst.append([sum(mir_expdb.loc[mir].tolist()), 'Non-Disease miRNAs'])
	# 		totnumnondis.append(sum(mir_expdb.loc[mir].tolist()))


	# print mean(totnumdis), mean(totnumnondis)
	# print median(totnumdis), median(totnumnondis)


	# dis_nondis_target_master = pd.DataFrame(masterlst,columns=['Number of Expressed Tissues', 'miRNA Class'])

	# sns.violinplot(x='miRNA Class',y='Number of Expressed Tissues',data=dis_nondis_target_master, cut=0)
	# plt.gca().set_ylim([0, 20])

	# plt.savefig('figures/mir_dis_num_tis_violin.pdf',bbox_inches='tight')



	mirnas_in_family = []
	mirnas_notin_family = []

	for a in mirna2family:
		if len(mirna2family[a]) < 4: continue
		else: mirnas_in_family = mirnas_in_family + mirna2family[a]

	for a in mirna2age:
		if a not in mirnas_in_family:
			mirnas_notin_family.append(a)


	mirnas_in_fam = mirna2family_edited.keys()
	mirnas_notinfam = [a for a in mirna2age.keys() if a not in mirna2family_edited]

	fam_nonfam_target_val = []
	fam_nonfam_target_bool = []

	fam_nonfam_target_master = []

	mir_fam_target = []
	mir_nonfam_target = []

	for alpha in round_robyn_target.index:
		for beta in round_robyn_target.index:
			if alpha == beta: continue
			if alpha in mirna2family_edited and beta in mirna2family_edited:
				mir_fam_target.append(float(round_robyn_target[alpha][beta]))
				fam_nonfam_target_val.append([float(round_robyn_target[alpha][beta]), 'Family miRNAs'])
				
			else:
				mir_nondis_target.append(float(round_robyn_target[alpha][beta]))
				dis_nondis_target_val.append([float(round_robyn_target[alpha][beta]), 'Non-Disease miRNAs'])




	dis_nondis_target_master = pd.DataFrame(dis_nondis_target_val,columns=['Comparison Normalized Hamming Distance (0.0-1.0)','miRNA Class'])

	print dis_nondis_target_master


	sns.violinplot(x='miRNA Class',y='Comparison Normalized Hamming Distance (0.0-1.0)',data=dis_nondis_target_master, cut=0)
	tot = float(round_robyn_target.values.max())

	plt.gca().set_ylim([-0.005,.13])




	plt.savefig('figures/mir_dis_tar_hamming.pdf',bbox_inches='tight')

	plt.close()










def main():
	mega_mir_lst = []

	mirlst_by_species = {}
	mirlst_by_mir = {}

	# mirdb = str(raw_input('Enter mirFile:'))
	# famdb = str(raw_input('\nEnter Family File:'))

	mirdb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/star_mir_lst.txt'
	famdb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/miFam.dat'
	diseasedb = '/Users/virpatel/projects/vanderbilt-summer-2014/data/microRNA_disease.txt'
	agedb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/allmir_ages/hsa_family_file_ph_allmir_dollo_age-time.protein_list'
	tardb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/all_targets.txt'
	expdb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/exp_data_alldmir.txt'
	taragedb = '/Users/virpatel/projects/vanderbilt-summer-2014/main_script/hgnc_names_2_age.txt'
	timetreedb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/time_tree_dates.txt'

	mega_mir_lst, mirlst_by_species, human_mirlst = sort_mir(open(mirdb,'r'),open(famdb,'r'))
	mirna2disease, disease2mirna = diseaese_parser(open(diseasedb,'r'))
	mirna2age, age2mirna = age_parser(open(agedb, 'r'))
	age2clade, clade2age = time_tree_parse(timetreedb)
	# get_mirna_disease_age_relationship(mirna2age, mirna2disease)


	mirna2tar, tar2age = parse_target_data(tardb,taragedb,timetreedb)
	gene2age = tar2age.copy()
	mirna2family = human_mirlst.copy()

	# target_analysis(mirna2age, mirna2disease, mirna2tar, tar2age)

	# mir_num_dis_bin(mirna2disease, mirna2age,age2clade)


	# gen_dis_db(disease2mirna, mirna2age)

	# family_homogenity(human_mirlst, mirna2disease, mirna2age


	# master_tarlst = target_gene_dataframe(mirna2age, mirna2disease, mirna2tar, tar2age)

	# target_gene_expression_analysis(mirna2age, mirna2disease,human_mirlst, tar2age)


	# mirna2disease_collapsed =  collapse_cancer_lst(mirna2disease)

	# family_homogenity_collapsed(human_mirlst, mirna2disease_collapsed, mirna2age)

	# mir_num_dis_bin_collapsed(mirna2disease_collapsedf, mirna2age, age2clade)

	# main_fraction_under_figure(mirna2tar, mirna2age, tar2age)



	heatmap_analysis(mirna2age, mirna2disease, mirna2family, gene2age)

main()
