import pandas as pd
import seaborn as sns
import csv
from data_import import *
import sys

def join_age_strat(lst1, lst2):
	tmp = lst1 + lst2
	ageset1 = set([a[-2] for a in lst1])
	ageset2 = set([a[-2] for a in lst2])
	agelst = list(ageset1.intersection(ageset2))

	newlst = [a for a in tmp if a[-2] in agelst]

	return newlst


def yaxis_switch(str_name):
	if 'tisnum' in str_name:
		return [0,20]
	if 'tarnum' in str_name:
		if 'binary' in str_name:
			return [0, 1000]
		else:
			return [0, 1500]
	if 'disnum' in str_name:
		if 'binary' in str_name:
			return [0, 75]
		if 'strat' in str_name:
			return [0, 120]
	if 'tarjac' in str_name:
		if 'binary' in str_name:
			return [0,.23]
		if 'strat' in str_name:
			return [0, 1.]

	





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

def genfig_v2():
	print len(numsimp[0])
	print len(numstrat[0])



def show_jaccard_target():
	reversed_dict = map_relatives(mirna2family)


	family = []
	non_family = []
	all_mir = []
	family_values = flatten(mirna2family.values())
	for val in round_robyn_target.index:
		for secval in round_robyn_target.index:
			lstvar = 0
			if val == secval: continue
			if val not in mirna2age: continue
			if val in family_values and secval in reversed_dict[val]:
				lstvar = True
			if val not in family_values and secval not in family_values:
				lstvar = False
			if lstvar == True: 
				family.append([round_robyn_target[val][secval], mirna2age[val], 'Family'])
				all_mir.append([round_robyn_target[val][secval], 'Family'])
			if lstvar == False: 
				non_family.append([round_robyn_target[val][secval], mirna2age[val], 'Non-Family'])
				all_mir.append([round_robyn_target[val][secval], 'Non-Family'])



	new_comb_agestrat = join_age_strat(family, non_family)
	genfig(all_mir, 'mirbinary_tarjac', 'Target Jaccard', 'miRNA Class', 2)
	genfig(new_comb_agestrat, 'mirstrat_tarjac', 'Target Jaccard', 'Age (MY)', 3)

def db_gen():
	mirna2disease = parse_disease('../relevant_data/hmdd_database.txt')
	mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')
	mirna2family = parse_families('../relevant_data/miFam.dat')

	mirna2family_edited = {}

	for alpha in mirna2family:
		if len(mirna2family[alpha]) > 3:
			mirna2family_edited[alpha] = mirna2family[alpha]

	mirna2family = mirna2family_edited.copy()

	round_robyn_target = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/target_heatmap_jaccard_dataframe.txt', sep='\t',index_col=[0])
	round_robyn_exp = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/tis_exp_heatmap_dataframe.txt', sep='\t',index_col=[0])
	mir_expdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])
	mir_targetdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0], encoding='utf-8')


	return mirna2disease, mirna2age, mirna2family, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb













def simple_family_nofamily():
	argslst_nums = []
	argslst_jac = []

	fam_mir_lst = flatten(mirna2family.values())
	reverse_mirdict = map_relatives(mirna2family)


	## disease number
	mirfamval_disnum = []
	mirnofamval_disnum = []

	for mirna in mirna2disease:
		if mirna in fam_mir_lst:
			mirfamval_disnum.append(len(mirna2disease[mirna]))
		else:
			mirnofamval_disnum.append(len(mirna2disease[mirna]))


	mod_mirfamval_disnum = add_end_cat(mirfamval_disnum, 'Family')
	mod_mirnofamval_disnum = add_end_cat(mirnofamval_disnum, 'Non-Family')


	genfig(join_simple(mod_mirfamval_disnum, mod_mirnofamval_disnum), 'mirbinary_disnum', 'Number of Diseases', 'miRNA Class', 2)

	argslst_nums.append(join_simple(mod_mirfamval_disnum, mod_mirnofamval_disnum))


	mirfamval_targetnum = []
	mirnofamval_targetnum = []



	for mirna in mir_targetdb.index:
		if mirna in fam_mir_lst:
			mirfamval_targetnum.append(sum(mir_targetdb.loc[mirna].tolist()))
		else:
			mirnofamval_targetnum.append(sum(mir_targetdb.loc[mirna].tolist()))

	mod_mirfamval_tarnum = add_end_cat(mirfamval_targetnum, 'Family')
	mod_mirnofamval_tarnum = add_end_cat(mirnofamval_targetnum, 'Non-Family')


	genfig(join_simple(mod_mirfamval_tarnum, mod_mirnofamval_tarnum), 'mirbinary_tarnum', 'Number of Targets', 'miRNA Class', 2)

	argslst_nums.append(join_simple(mod_mirfamval_tarnum, mod_mirnofamval_tarnum))


	mirfamval_expnum = []
	mirnofamval_expnum = []



	for mirna in mir_expdb.index:
		if mirna in fam_mir_lst:
			mirfamval_expnum.append(sum(mir_expdb.loc[mirna].tolist()))
		else:
			mirnofamval_expnum.append(sum(mir_expdb.loc[mirna].tolist()))


	mod_mirfamval_expnum = add_end_cat(mirfamval_expnum, 'Family')
	mod_mirnofamval_expnum = add_end_cat(mirnofamval_expnum, 'Non-Family')


	genfig(join_simple(mod_mirfamval_expnum, mod_mirnofamval_expnum), 'mirbinary_tisnum', 'Number of Tissues', 'miRNA Class', 2)


	argslst_nums.append(join_simple(mod_mirfamval_expnum, mod_mirnofamval_expnum))

	fampair, nonfampair = genpairs(reverse_mirdict, mirna2disease.keys())

	## disease jaccard 

	mirfamval_disjac = []
	mirnofamval_disjac = []
	dislst = flatten(mirna2disease.values())




	for pair in fampair:
		mirfamval_disjac.append(jaccard(   generate_class_vector(dislst, mirna2disease[pair[0]]),  generate_class_vector(dislst, mirna2disease[pair[1]])))

	for pair in nonfampair:
		mirnofamval_disjac.append(jaccard(   generate_class_vector(dislst, mirna2disease[pair[0]]),  generate_class_vector(dislst, mirna2disease[pair[1]])))


	mod_mirfamval_disjac = add_end_cat(mirfamval_disjac, 'Family')
	mod_mirnofamval_disjac = add_end_cat(mirnofamval_disjac, 'Non-Family')

	genfig(join_simple(mod_mirfamval_disjac, mod_mirnofamval_disjac), 'mirbinary_disjac', 'Jaccard Diseases', 'miRNA Class', 2)

	argslst_jac.append(join_simple(mod_mirfamval_disjac, mod_mirnofamval_disjac))

	## expression jaccard

	fampair, nonfampair = genpairs(reverse_mirdict, mir_expdb.index)


	mirfamval_expjac = []
	mirnofamval_expjac = []

	for pair in fampair:
		mirfamval_expjac.append(jaccard(mir_expdb.loc[pair[0]].tolist(),mir_expdb.loc[pair[1]].tolist()))

	for pair in nonfampair:
		mirnofamval_expjac.append(jaccard(mir_expdb.loc[pair[0]].tolist(),mir_expdb.loc[pair[1]].tolist()))


	mod_mirfamval_expjac = add_end_cat(mirfamval_expjac, 'Family')
	mod_mirnofamval_expjac = add_end_cat(mirnofamval_expjac, 'Non-Family')


	genfig(join_simple(mod_mirfamval_expjac, mod_mirnofamval_expjac), 'mirbinary_tisjac', 'Jaccard Tissues', 'miRNA Class', 2)


	argslst_jac.append(join_simple(mod_mirfamval_expjac, mod_mirnofamval_expjac))

	fampair, nonfampair = genpairs(reverse_mirdict, round_robyn_target.index)


	mirfamval_tarjac = []
	mirnofamval_tarjac = []

	for pair in fampair:
		mirfamval_tarjac.append(round_robyn_target[pair[0]][pair[1]])

	for pair in nonfampair:
		mirnofamval_tarjac.append(round_robyn_target[pair[0]][pair[1]])


	mod_mirfamval_tarjac = add_end_cat(mirfamval_tarjac, 'Family')
	mod_mirnofamval_tarjac = add_end_cat(mirnofamval_tarjac, 'Non-Family')


	genfig(join_simple(mod_mirfamval_tarjac, mod_mirnofamval_tarjac), 'mirbinary_tarjac', 'Jaccard Targets', 'miRNA Class', 2)
	argslst_jac.append(join_simple(mod_mirfamval_tarjac, mod_mirnofamval_tarjac))


	return argslst_nums, argslst_jac

def stratage():

	argslst_nums = []
	argslst_jac = []

	fam_mir_lst = flatten(mirna2family.values())
	reverse_mirdict = map_relatives(mirna2family)


	## disease number
	mirfamval_disnum = []
	mirnofamval_disnum = []

	for mirna in mirna2disease:
		if mirna not in mirna2age: continue
		if mirna in fam_mir_lst:
			mirfamval_disnum.append([len(mirna2disease[mirna]), mirna2age[mirna]])
		else:
			mirnofamval_disnum.append([len(mirna2disease[mirna]), mirna2age[mirna]])


	mod_mirfamval_disnum = add_end_cat(mirfamval_disnum, 'Family')
	mod_mirnofamval_disnum = add_end_cat(mirnofamval_disnum, 'Non-Family')


	genfig(join_age_strat(mod_mirfamval_disnum, mod_mirnofamval_disnum), 'mirstrat_disnum', 'Number of Diseases', 'Age (MY)', 3)
	argslst_nums.append(join_age_strat(mod_mirfamval_disnum, mod_mirnofamval_disnum))



	mirfamval_targetnum = []
	mirnofamval_targetnum = []





	for mirna in mir_targetdb.index:
		if mirna not in mirna2age: continue
		if mirna in fam_mir_lst:
			mirfamval_targetnum.append([sum(mir_targetdb.loc[mirna].tolist()), mirna2age[mirna]])
		else:
			mirnofamval_targetnum.append([sum(mir_targetdb.loc[mirna].tolist()), mirna2age[mirna]])


	mod_mirfamval_tarnum = add_end_cat(mirfamval_targetnum, 'Family')
	mod_mirnofamval_tarnum = add_end_cat(mirnofamval_targetnum, 'Non-Family')


	genfig(join_age_strat(mod_mirfamval_tarnum, mod_mirnofamval_tarnum), 'mirstrat_tarnum', 'Number of Targets', 'Age (MY)', 3)
	argslst_nums.append(join_age_strat(mod_mirfamval_tarnum, mod_mirnofamval_tarnum))


	mirfamval_expnum = []
	mirnofamval_expnum = []



	for mirna in mir_expdb.index:
		if mirna not in mirna2age: continue
		if mirna in fam_mir_lst:
			mirfamval_expnum.append([sum(mir_expdb.loc[mirna].tolist()), mirna2age[mirna]])
		else:
			mirnofamval_expnum.append([sum(mir_expdb.loc[mirna].tolist()), mirna2age[mirna]])


	mod_mirfamval_expnum = add_end_cat(mirfamval_expnum, 'Family')
	mod_mirnofamval_expnum = add_end_cat(mirnofamval_expnum, 'Non-Family')


	genfig(join_age_strat(mod_mirfamval_expnum, mod_mirnofamval_expnum), 'mirstrat_tisnum', 'Number of Tissues', 'Age (MY)', 3)
	argslst_nums.append(join_age_strat(mod_mirfamval_expnum, mod_mirnofamval_expnum))


	fampair, nonfampair = genpairs_agestrat(reverse_mirdict, mirna2disease.keys(), mirna2age)


	## disease jaccard 

	mirfamval_disjac = []
	mirnofamval_disjac = []
	dislst = flatten(mirna2disease.values())

	for pair in fampair:
		mirfamval_disjac.append([jaccard(   generate_class_vector(dislst, mirna2disease[pair[0]]),  generate_class_vector(dislst, mirna2disease[pair[1]])), pair[-2]])

	for pair in nonfampair:
		mirnofamval_disjac.append([jaccard( generate_class_vector(dislst, mirna2disease[pair[0]]),  generate_class_vector(dislst, mirna2disease[pair[1]])), pair[-2]])

	mod_mirfamval_disjac = add_end_cat(mirfamval_disjac, 'Family')
	mod_mirnofamval_disjac = add_end_cat(mirnofamval_disjac, 'Non-Family')


	genfig(join_age_strat(mod_mirfamval_disjac, mod_mirnofamval_disjac), 'mirstrat_disjac', 'Disease Jaccard', 'Age (MY)', 3)
	argslst_jac.append(join_age_strat(mod_mirfamval_disjac, mod_mirnofamval_disjac))

	## expression jaccard


	fampair, nonfampair = genpairs_agestrat(reverse_mirdict, mir_expdb.index, mirna2age)


	mirfamval_expjac = []
	mirnofamval_expjac = []

	for pair in fampair:
		mirfamval_expjac.append([jaccard(mir_expdb.loc[pair[0]].tolist(),mir_expdb.loc[pair[1]].tolist()), pair[-2]])

	for pair in nonfampair:
		mirnofamval_expjac.append([jaccard(mir_expdb.loc[pair[0]].tolist(),mir_expdb.loc[pair[1]].tolist()), pair[-2]])


	mod_mirfamval_expjac = add_end_cat(mirfamval_expjac, 'Family')
	mod_mirnofamval_expjac = add_end_cat(mirnofamval_expjac, 'Non-Family')


	genfig(join_age_strat(mod_mirfamval_expjac, mod_mirnofamval_expjac), 'mirstrat_tisjac', 'Tissues Jaccard', 'Age (MY)', 3)
	argslst_jac.append(join_age_strat(mod_mirfamval_expjac, mod_mirnofamval_expjac))


	fampair, nonfampair = genpairs_agestrat(reverse_mirdict, round_robyn_target.index, mirna2age)




	mirfamval_tarjac = []
	mirnofamval_tarjac = []

	for pair in fampair:
		mirfamval_tarjac.append([round_robyn_target[pair[0]][pair[1]], pair[-2]])

	for pair in nonfampair:
		mirnofamval_tarjac.append([round_robyn_target[pair[0]][pair[1]], pair[-2]])



	mod_mirfamval_tarjac = add_end_cat(mirfamval_tarjac, 'Family')
	mod_mirnofamval_tarjac = add_end_cat(mirnofamval_tarjac, 'Non-Family')


	genfig(join_age_strat(mod_mirfamval_tarjac, mod_mirnofamval_tarjac), 'mirstrat_tarjac', 'Targets Jaccard', 'Age (MY)', 3)

	argslst_jac.append(join_age_strat(mod_mirfamval_tarjac, mod_mirnofamval_tarjac))

	return argslst_nums, argslst_jac




mirna2disease, mirna2age, mirna2family, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb = db_gen()
show_jaccard_target()

numsimp, jacsimp = simple_family_nofamily()
numstrat, jacstrat = stratage()



