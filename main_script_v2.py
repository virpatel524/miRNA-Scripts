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
sns.set_context("paper")

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

	agelst = []
	dislst = []

	for mir in list(set(mirna2age.keys()).intersection(mirna2disease.keys())):	
		agelst.append(float(mirna2age[mir])) 
		dislst.append(float(len(mirna2disease[mir])))


	oldage = agelst[:]





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


	with open('relevant_data/mirna2age_lst.txt','w') as mir_fle:
		for mir in mirna2age:
			mir_fle.write('%s\t%.1f\n' %(mir, mirna2age[mir]))


	with open('relevant_data/mirdis_lst.txt','w') as mirdis_fle:
		for mir in mirna2disease:
			if mir in mirna2age:
				mirdis_fle.write('%s\n' %(mir))

	with open('relevant_data/age_label_fle.txt','w') as rel_fle:
		for age in age2clade:
			rel_fle.write('%.1f\t%s\n' %(age, age2clade[age]))




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


def target_gene_dataframe(mirna2age, mirna2disease,mirna2target, target2age):
	target_agedb = pd.DataFrame()
	mir_targetdb = pd.DataFrame()

	for target in target2age:
		tmp = pd.DataFrame([float(target2age[target]),], index=[target,], columns=['age',])
		target_agedb = target_agedb.append(tmp)

	tar_base_vec = get_list_of_dictionary(mirna2target)

	return tar_base_vec
	
	for index,mir in enumerate(mirna2target):
		print index + 1, len(mirna2target)
		newdata = generate_class_vector(tar_base_vec, mirna2target[mir])
		tmp = pd.DataFrame([newdata,], index=[mir,],columns=tar_base_vec)
		mir_targetdb = mir_targetdb.append(tmp)


	mir_targetdb.to_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/mir_target_vectordb.txt', sep='\t', encoding='utf-8')



def target_gene_expression_analysis(mirna2age, mirna2disease,mirna2family,gene2age):
		mir_targetdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0], encoding='utf-8')
		mir_expdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])

		family_target_hamming = []
		family_target_avg_age = []
		family_perc_dis = []

		# for fam in mirna2family:
		# 	family_vector = []
		# 	mirlst = [a for a in mirna2family[fam] if a in mir_targetdb.index]
		# 	mirdislst = [a for a in mirna2family[fam] if a in mirna2disease]
		# 	if len(mirlst) < 4: continue
		# 	if len(mirdislst) < 4: continue
		# 	for mir in mirlst:
		# 		for other_mir in mirlst:
		# 			if mir == other_mir: continue
		# 			family_vector.append(hamming(mir_targetdb.loc[mir], mir_targetdb.loc[other_mir],normalized=True))
				
		# 	family_target_hamming.append(std(family_vector))
		# 	family_target_avg_age.append(round(mean([float(mirna2age[mirna]) for mirna in mirlst if mirna in mirna2age]),1))
		# 	family_perc_dis.append(float(len(mirdislst)) / float(len(mirna2family[fam])))


		target_lst = list(mir_targetdb.columns.values)

		mirnanumdis = []
		mirnanumtar = []
		mir_avg_tar_age_dis = []
		mir_avg_tar_age_nondis = []
		mir_age = []
		mir_median_tar_age_all = []

		# for mir in mir_targetdb.index:
		# 	if mir not in mirna2disease: mirnanumdis.append(0)
		# 	else: mirnanumdis.append(len(mirna2disease[mir]))
		# 	bintarlt = mir_targetdb.loc[mir].tolist()
		# 	mirnanumtar.append(sum(bintarlt))
		# 	tarages = [float(gene2age[target_lst[ind]]) for ind, a in enumerate(bintarlt) if target_lst[ind] in gene2age and a == 1]
		# 	mir_median_tar_age_all.append(median(tarages))
		# 	mir_avg_tar_age_dis.append(mean(tarages))

		# for mir in mir_targetdb.index:
		# 	if mir not in mirna2disease:
		# 		bintarlt = mir_targetdb.loc[mir].tolist()
		# 		tarages = [float(gene2age[target_lst[ind]]) for ind, a in enumerate(bintarlt) if target_lst[ind] in gene2age and a == 1]
		# 		mir_avg_tar_age_nondis.append(median


		yung_num_tis = []
		old_num_tis = []

		dis_num = []
		mir_age_lst = []
		exp_val = []

		for mir in mir_expdb.index:
			if mir in mirna2disease:
				v = float(sum(mir_expdb.loc[mir].tolist()))
				dis_num.append(len(mirna2disease[mir]))
				# mirage = mirna2age[mir]
				# mir_age_lst.append(mirage)


				exp_val.append(v)

					# if mirage > 100.0: old_num_tis.append(sum(mir_expdb.loc[mir].tolist()))
					# else: yung_num_tis.append(sum(mir_expdb.loc[mir].tolist()))




		print spearmanr(dis_num, exp_val)
		plt.scatter(dis_num, exp_val)
		plt.show()
		plt.close()
		# print mannwhitneyu(yung_num_tis, old_num_tis)


def disease_bootstrapping(mirna2age, mirna2disease,mirna2target,gene2age):
	disease2mirna = reverse_dict(mirna2disease)

	# for dis in disease2mirna:
	# 	age_of_supporting_mir = [mirna2age[a] for a  in disease2mirna[dis] if a in mirna2age]
	# 	med_dis = float(median(age_of_supporting_mir))
	# 	if len(age_of_supporting_mir) > 2:
	# 		counter_over  = 0
	# 		counter_under = 0
	# 		for i in range(10000):
	# 			while_loop_safety = 0
	# 			new_ages_lst = []

	# 			while_loop_safety += 1
	# 			new_ages_lst = [mirna2age[ran_choice] for ran_choice in random.sample(set(two_dic_common(mirna2age,mirna2disease)),len(age_of_supporting_mir))]
	# 			if float(median(new_ages_lst)) > med_dis: counter_under += 1
	# 			if float(median(new_ages_lst)) < med_dis: counter_under += 1

	# 		print "Disease:%s, prob it's younger:%f, prob it's older:%f" %(dis,float(counter_under)/ float(10000),float(counter_over)/ float(10000))

	alldismir = [mirna2age[a] for a in mirna2disease if a in mirna2age]
	counter = 0
	for dis in disease2mirna:
		age_of_supporting_mir = [mirna2age[a] for a  in disease2mirna[dis] if a in mirna2age]
		z,b  = mannwhitneyu(alldismir, age_of_supporting_mir)
		z = float(b)

		if z < 0.005: 
			print 'Disease:%s, mann: %s' %(dis, z)
			counter += 1
	print float(counter) / float(len(disease2mirna))



	## setup for gene analysis

	allmirinq = [gene2age[a] for a in two_dic_common(mirna2target, mirna2disease) if a  in gene2age]

	counter = 0
	for dis in disease2mirna:
		potmir +=[a for a in disease2mirna[dis] if in allmirinq]

		z,b  = mannwhitneyu(alldismir, age_of_supporting_mir)
		z = float(b)

		if z < 0.005: 
			print 'Disease:%s, mann: %s' %(dis, z)
			counter += 1
	print float(counter) / float(len(disease2mirna))









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



	# mir_num_dis_bin(mirna2disease, mirna2age,age2clade)


	# gen_dis_db(disease2mirna, mirna2age)

	# family_homogenity(human_mirlst, mirna2disease, mirna2age


	master_tarlst = target_gene_dataframe(mirna2age, mirna2disease, mirna2tar, tar2age)

	# target_gene_expression_analysis(mirna2age, mirna2disease,human_mirlst, tar2age)

	disease_bootstrapping(mirna2age, mirna2disease, mirna2tar, tar2age)






main()
