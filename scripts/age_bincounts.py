# import statements

import csv, shutil, os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

from scipy.stats import mannwhitneyu


# initalize sns

sns.axes_style('whitegrid')
sns.set_style("whitegrid")
sns.set_context("paper")


# initalize main dictionaires 



# import my protein historian data

def import_ages(ph_db):

	species2mirna = {}


	with open(ph_db) as master_age_mirlst:
		mirlst = list(csv.reader(master_age_mirlst,delimiter='\t'))
		for mir in mirlst:
			spe = mir[0][:3]
			species2mirna.setdefault(spe,[]).append([mir[0],mir[-1]])

	age_lst = []


	for spe in species2mirna:
		for mir in species2mirna[spe]:
			age_lst.append(float(mir[-1]))



	return species2mirna, age_lst



def bincount_style1(allmir_lst, starmir_lst, time_tree_fle):

	# create master histogram


	labels = [float(alpha) for alpha in sorted(list(set(allmir_lst + starmir_lst)))]

	age2clade = {}

	with open(time_tree_fle) as time_tree_data:
		time_tree_lst = [a for a in list(csv.reader(time_tree_data,delimiter='\t')) if len(a) > 1]
		for alpha in time_tree_lst:
			age2clade[alpha[-1]] = alpha[0]



	str_labels = ['%s (%.1f)' %(age2clade[str(alpha)], alpha) for alpha in sorted(list(set(allmir_lst)))]

	binlst_all = [0] * len(labels)
	binlst_star = [0] * len(labels)

	for el in allmir_lst: binlst_all[labels.index(float(el))] = binlst_all[labels.index(float(el))] + 1
	for el in starmir_lst: binlst_star[labels.index(float(el))] = binlst_star[labels.index(float(el))] + 1

	nd = np.arange(0,len(labels)*10,10)

	flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
	palette = itertools.cycle(flatui)





	f, ax = plt.subplots(2,1)
	f.set_size_inches(20, 10)

	ax1 = plt.subplot(211)
	barlst = plt.bar(nd, binlst_all, width=9,align='center')
	for i in range(len(barlst)): barlst[i].set_color(next(palette)) 
	plt.xticks(nd, str_labels, rotation=65)
	plt.ylabel('miRNA Count', fontsize=15)


	ax2 = plt.subplot(212)
	barlst = plt.bar(nd, binlst_star, width=9,align='center')
	palette = itertools.cycle(flatui)
	for i in range(len(barlst)): barlst[i].set_color(next(palette)) 
	plt.xticks(nd, str_labels, rotation=65)
	plt.xlabel('miRNA Clade of Origination',fontsize=15)
	plt.ylabel('miRNA Count', fontsize=15)

	
	plt.gcf().subplots_adjust(hspace=.2)
	plt.subplots_adjust(bottom=0.20)


	ax2.set_xlim(xmin=0-5,xmax=float(nd[-1])-4.5)
	ax1.set_xlim(xmin=0-5,xmax=float(nd[-1])-4.5)

	ax1.xaxis.grid(False)
	ax2.xaxis.grid(False)
	ax1.set_xticklabels([])




	plt.savefig('/Users/virpatel/Desktop/pub_stuff/figures/all_star_mir_comp.pdf', bbox_inches='tight')
	plt.close()














	# plt.figure(figsize=(20,10)) 

	# ax1 = plt.subplot(211)
	# sns.barplot(nd, binlst_all ,palette=flatui)
	# ax1.set_xticklabels(str_labels,rotation=65, ha='right')
	# plt.ylabel('miRNA Count', fontsize=10)




	# ax2 = plt.subplot(212)
	# sns.barplot(nd, binlst_star ,palette=flatui)
	# ax2.set_xticklabels(str_labels,rotation=65, ha='right')
	# plt.xlabel('miRNA Clade of Origination',fontsize=10)
	# plt.ylabel('miRNA Count', fontsize=10)

	# plt.gcf().subplots_adjust(hspace=.50)
	# plt.subplots_adjust(bottom=0.20)
















	# plt.subplot(211)
	# # cur_plot = plt.gcf()

	# # plt.tick_params(axis='y', which='major', labelsize=15)
	# # axarr[0].yaxis.labelpad = 15


	# sns.barplot(nd, binlst_all ,palette=flatui)



	# plt.subplot(212)
	# # cur_plot = plt.gcf()

	# # plt.tick_params(axis='x', which='major', labelsize=10)
	# # plt.tick_params(axis='y', which='major', labelsize=15)
	# # axarr[1].yaxis.labelpad = 15


	# sns.barplot(nd, binlst_star ,palette=flatui)


	# axarr[0].set_xticklabels(str_labels, rotation=65, ha='right')
	# axarr[1].set_xticklabels(str_labels, rotation=65, ha='right') 
 
 # 	plt.subplot(211)
	# plt.subplots_adjust(bottom=0.20)
	# plt.xlabel('miRNA Clade of Origination',fontsize=15)
	# plt.ylabel('miRNA Count', fontsize=15 )


	# plt.subplot(212)
	# plt.subplots_adjust(bottom=0.20)
	# plt.xlabel('miRNA Clade of Origination',fontsize=15)
	# plt.ylabel('miRNA Count', fontsize=15 )





	

	# plt.show()



	# ind = np.arange(0,len(labels)*2.3,2.3)
	# plt.figure(figsize=(30,10))


	# plt.bar(ind, binlst,2)
	# plt.xticks(ind,str_labels,rotation=55,ha='center')

	# plt.xlabel('Ages (MYA)')
	# plt.ylabel('Number of miRNAs')
	# plt.title('Age of All miRNAs Histogram ')

	# plt.savefig('/Users/virpatel/Desktop/pub_stuff/figures/all_mirbase.png')

	# plt.close()



	# # create histogram for each species


	# for species in species2mirna:
	# 	age_lst_for_species = []
	# 	for mir in species2mirna[species]:
	# 		age_lst_for_species.append(float(mir[-1]))



	# 	age_lst_for_species = sorted(age_lst_for_species)


	# 	skew_val = float(skew(age_lst_for_species))
	# 	kurtval =  str(kurtosis(age_lst_for_species)) 


	# 	labels = [float(alpha) for alpha in sorted(list(set(age_lst_for_species)))]
	# 	str_labels = [str(alpha) for alpha in sorted(list(set(age_lst_for_species)))]

	# 	if len(labels) <= 4:
	# 		continue



	# 	binlst = [0] * len(labels)




	# 	for el in age_lst_for_species:
	# 		binlst[labels.index(float(el))] = binlst[labels.index(float(el))] + 1


	# 	ind = np.arange(0,len(labels)*2.3,2.3)

	# 	if len(ind) == len(binlst) + 1:
	# 		ind = np.arange(0,len(labels)*2.3-2.3,2.3)


	# 	# plt.figure(figsize=(30,10))


	# 	# plt.bar(ind, binlst,2)
	# 	# plt.xticks(ind,str_labels,rotation=55,ha='center')

	# 	# plt.xlabel('Ages (MYA)')
	# 	# plt.ylabel('Number of miRNAs')
	# 	# plt.title('Age of %s miRNAs Histogram' %(species))

	# 	# plt.savefig('/Users/virpatel/Desktop/pub_stuff/figures/each_species_bincount/%s_bincount.png' %(species))

	# 	# plt.close()


	# 	with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/skew_data.txt','a') as skew_data:
	# 		skew_data.write('%s\t%.3f\t%d\n' %(species, skew_val, len(age_lst_for_species)))

	# 	skew_lst.append(float(skew_val))
	# 	num_lst.append(float(len(age_lst_for_species)))


	# skew_versus_numinlist = spearmanr(skew_lst, num_lst)


def individual_bincounts(allmir_lst, starmir_lst, age_dir_allmir, age_dir_starmir,time_tree_fle,image_dir):

	
	# skew_lst_all = []
	# num_lst_all = []
	# percent_lst_all = []

	# skew_lst_star = []
	# num_lst_star = []
	# percent_lst_star = []



	# labels = [float(alpha) for alpha in sorted(list(set(allmir_lst + starmir_lst)))]


	# age2clade = {}

	# with open(time_tree_fle,'r') as time_tree_data:
	# 	time_tree_lst = [a for a in list(csv.reader(time_tree_data,delimiter='\t')) if len(a) > 1]
	# 	for alpha in time_tree_lst:
	# 		age2clade[alpha[-1]] = alpha[0]


	# str_labels = ['%s (%.1f)' %(age2clade[str(alpha)], alpha) for alpha in sorted(list(set(allmir_lst)))]
	# nd = np.arange(0,len(labels)*10,10)

	# flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
	# palette = itertools.cycle(flatui)

	# ## ALL MIRNAS

	# try:
	# 	shutil.rmtree(os.path.join(image_dir, 'species_bincounts_allmir/'))
	# except:
	# 	pass

	# os.mkdir(os.path.join(image_dir, 'species_bincounts_allmir/'))



	allmir2age = {}

	with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/ph_dataset_with_time_tree_allmir.txt','r') as ph_allmir:
		allmir_ph = [a for a in list(csv.reader(ph_allmir,delimiter='\t'))]
		for mir in allmir_ph:
			allmir2age[mir[0]] = float(mir[-1])


	allmir_species = list(set([a[:3] for a in allmir2age.keys()]))
	print len(allmir_species)

	# for species in all_species:
	# 	ages_lst = [allmir2age[a] for a in allmir2age if a[:3] == species]
	# 	if len(ages_lst) < 5: continue

	# 	tmp_binlst = [0] * len(labels)
	# 	for el in ages_lst: tmp_binlst[labels.index(float(el))] = tmp_binlst[labels.index(float(el))] + 1

	# 	f, ax = plt.subplots(1)
	# 	f.set_size_inches(20, 10)


	# 	barlst = plt.bar(nd, tmp_binlst, width=9,align='center')

	# 	for i in range(len(barlst)): barlst[i].set_color(next(palette)) 


	# 	plt.xticks(nd, str_labels, rotation=65)

	# 	plt.ylabel('miRNA Count', fontsize=15)
	# 	plt.xlabel('miRNA Clade of Origination',fontsize=15)


	# 	plt.subplots_adjust(bottom=0.20)

	# 	ax.set_xlim(xmin=0-5,xmax=float(nd[-1])-4.5)
	# 	plt.gca().xaxis.grid(False)




	# 	plt.savefig(os.path.join(image_dir, 'species_bincounts_allmir/', '%s_bincount.pdf' %(species)))
	# 	plt.close()


	# ## STAR MIRNAS

	# try:
	# 	shutil.rmtree(os.path.join(image_dir, 'species_bincounts_starmir/'))
	# except:
	# 	pass

	# os.mkdir(os.path.join(image_dir, 'species_bincounts_starmir/'))



	# starmir2age = {}

	# with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/ph_dataset_with_time_tree_starmir.txt','r') as ph_starmir:
	# 	starmir_ph = [a for a in list(csv.reader(ph_starmir,delimiter='\t'))]
	# 	for mir in starmir_ph:
	# 		starmir2age[mir[0]] = float(mir[-1])


	# starmir_species = list(set([a[:3] for a in starmir2age.keys()]))

	# for species in all_species:
	# 	ages_lst = [starmir2age[a] for a in starmir2age if a[:3] == species]
	# 	if len(ages_lst) < 5: continue

	# 	tmp_binlst = [0] * len(labels)
	# 	for el in ages_lst: tmp_binlst[labels.index(float(el))] = tmp_binlst[labels.index(float(el))] + 1

	# 	f, ax = plt.subplots(1)
	# 	f.set_size_inches(20, 10)


	# 	barlst = plt.bar(nd, tmp_binlst, width=9,align='center')

	# 	for i in range(len(barlst)): barlst[i].set_color(next(palette)) 


	# 	plt.xticks(nd, str_labels, rotation=65)

	# 	plt.ylabel('miRNA Count', fontsize=15)
	# 	plt.xlabel('miRNA Clade of Origination',fontsize=15)


	# 	plt.subplots_adjust(bottom=0.20)

	# 	ax.set_xlim(xmin=0-5,xmax=float(nd[-1])-4.5)
	# 	plt.gca().xaxis.grid(False)




	# 	plt.savefig(os.path.join(image_dir, 'species_bincounts_starmir/', '%s_bincount.pdf' %(species)),bbox_inches='tight')
	# 	plt.close()












def parse_target_data(tardb):
	with open(tardb) as tardb_fle:
		data = [float(a[-1]) for a in list(csv.reader(tardb_fle,delimiter='\t'))]
		return data






def bincount_style2(allmir_ages, target_ages,time_tree_fle):

	age2clade = {}

	with open(time_tree_fle) as time_tree_data:
		time_tree_lst = [a for a in list(csv.reader(time_tree_data,delimiter='\t')) if len(a) > 1]
		for alpha in time_tree_lst:
			age2clade[alpha[-1]] = alpha[0]


	labels_mir = [float(alpha) for alpha in sorted(list(set(allmir_ages)))]
	str_labels_mir = ['%s (%.1f)' %(age2clade[str(alpha)], alpha) for alpha in labels_mir]
	binlst_mir = [0] * len(labels_mir)
	for el in allmir_ages: binlst_mir[labels_mir.index(float(el))] = binlst_mir[labels_mir.index(float(el))] + 1
	nd_mir = np.arange(0,len(labels_mir)*10,10)


	labels_tar = [float(alpha) for alpha in sorted(list(set(target_ages)))]
	str_labels_tar = ['%s (%.1f)' %(age2clade[str(alpha)], alpha) for alpha in labels_tar]
	binlst_tar = [0] * len(labels_tar)
	for el in target_ages: binlst_tar[labels_tar.index(float(el))] = binlst_tar[labels_tar.index(float(el))] + 1
	nd_tar = np.arange(0,len(labels_tar)*10,10)

	flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
	palette = itertools.cycle(flatui)




	f, ax = plt.subplots(2,1)
	f.set_size_inches(20, 10)

	ax1 = plt.subplot(211)
	barlst = plt.bar(nd_mir, binlst_mir, width=9,align='center')
	for i in range(len(barlst)): barlst[i].set_color(next(palette)) 
	plt.xticks(nd_mir, str_labels_mir, rotation=65)
	plt.ylabel('miRNA Count', fontsize=15)
	plt.xlabel('miRNA Clade of Origination',fontsize=15)


	ax2 = plt.subplot(212)
	barlst = plt.bar(nd_tar, binlst_tar, width=9,align='center')
	palette = itertools.cycle(flatui)
	for i in range(len(barlst)): barlst[i].set_color(next(palette)) 
	plt.xticks(nd_tar, str_labels_tar, rotation=65)
	plt.xlabel('Target Gene Clade of Origination',fontsize=15)
	plt.ylabel('Target Gene Count', fontsize=15)

	
	plt.gcf().subplots_adjust(hspace=.75)
	plt.subplots_adjust(bottom=0.20)


	ax2.set_xlim(xmin=0-5,xmax=float(nd_tar[-1])-4.5)
	ax1.set_xlim(xmin=0-5,xmax=float(nd_mir[-1])-4.5)

	ax1.xaxis.grid(False)
	ax2.xaxis.grid(False)




	plt.savefig('/Users/virpatel/Desktop/pub_stuff/figures/mir_tar_agecomp.pdf', bbox_inches='tight')
	plt.close()


def bincount_style3(allmir_ages, target_ages,time_tree_fle):

	age2clade = {}

	with open(time_tree_fle) as time_tree_data:
		time_tree_lst = [a for a in list(csv.reader(time_tree_data,delimiter='\t')) if len(a) > 1]
		for alpha in time_tree_lst:
			age2clade[alpha[-1]] = alpha[0]


	labels_mir = [float(alpha) for alpha in sorted(list(set(allmir_ages + target_ages)))]
	str_labels_mir = ['%s (%.1f)' %(age2clade[str(alpha)], alpha) for alpha in labels_mir]
	binlst_mir = [0] * len(labels_mir)
	for el in allmir_ages: binlst_mir[labels_mir.index(float(el))] = binlst_mir[labels_mir.index(float(el))] + 1
	nd_mir = np.arange(0,len(labels_mir)*10,10)



	binlst_tar = [0] * len(labels_mir)
	for el in target_ages: binlst_tar[labels_mir.index(float(el))] = binlst_tar[labels_mir.index(float(el))] + 1
	nd_mir = np.arange(0,len(labels_mir)*10,10)

	flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
	palette = itertools.cycle(flatui)




	f, ax = plt.subplots(2,1)
	f.set_size_inches(20, 10)

	ax1 = plt.subplot(211)
	barlst = plt.bar(nd_mir, binlst_mir, width=9,align='center')
	for i in range(len(barlst)): barlst[i].set_color(next(palette)) 
	plt.xticks(nd_mir, str_labels_mir, rotation=65)
	plt.ylabel('miRNA Count', fontsize=15)
	plt.xlabel('miRNA Clade of Origination',fontsize=15)


	ax2 = plt.subplot(212)
	barlst = plt.bar(nd_mir, binlst_tar, width=9,align='center')
	palette = itertools.cycle(flatui)
	for i in range(len(barlst)): barlst[i].set_color(next(palette)) 
	plt.xticks(nd_mir, str_labels_mir, rotation=65)
	plt.xlabel('Target Gene Clade of Origination',fontsize=15)
	plt.ylabel('Target Gene Count', fontsize=15)

	
	plt.gcf().subplots_adjust(hspace=.75)
	plt.subplots_adjust(bottom=0.20)


	ax2.set_xlim(xmin=0-5,xmax=float(nd_mir[-1])-4.5)
	ax1.set_xlim(xmin=0-5,xmax=float(nd_mir[-1])-4.5)


	props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

	ax1.text(.5, 3000,'Vir test', fontsize=30, bbox=dict(facecolor='none', edgecolor='red'), alpha = .1)
	ax1.xaxis.grid(False)
	ax2.xaxis.grid(False)




	plt.savefig('/Users/virpatel/Desktop/pub_stuff/figures/mir_tar_agecomp_2.pdf', bbox_inches='tight')
	plt.close()






tardb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/tar2age_all.txt'
time_treedb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/time_tree_dates.txt'





species2mir_allmir, master_age_lst_allmir = import_ages('/Users/virpatel/Desktop/pub_stuff/relevant_data/ph_dataset_with_time_tree_allmir.txt')
species2mirna_starmir, master_age_lst_starmir = import_ages('/Users/virpatel/Desktop/pub_stuff/relevant_data/ph_dataset_with_time_tree_starmir.txt')

target_bincount = parse_target_data(tardb)

# print mannwhitneyu([float(a) for a in target_bincount], [float(a) for a in master_age_lst_allmir])

# bincount_style2(master_age_lst_allmir, target_bincount,time_treedb)
# bincount_style3(master_age_lst_allmir, target_bincount, time_treedb)

# all_species = list(set(species2mir_allmir.keys() + species2mirna_starmir.keys()))

# bincount_style1(master_age_lst_allmir, master_age_lst_starmir, '/Users/virpatel/Desktop/pub_stuff/relevant_data/time_tree_dates.txt')
individual_bincounts(master_age_lst_allmir, master_age_lst_starmir, '/Users/virpatel/Desktop/pub_stuff/relevant_data/allmir_ages/','/Users/virpatel/Desktop/pub_stuff/relevant_data/selectmir_ages/','/Users/virpatel/Desktop/pub_stuff/relevant_data/time_tree_dates.txt','/Users/virpatel/Desktop/pub_stuff/figures/')








