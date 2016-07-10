import seaborn as sns
import pandas as pd
import csv 



def jaccard(a,b):
	p = 0
	q = 0
	r = 0
	s = 0
	if sum(a) == 0 and sum(b) == 0: return 1.0

	for i in range(len(a)):
		if a[i] == 1 and b[i] == 1:
			p += 1
		if a[i] == 1 and b[i] == 0:
			q += 1
		if a[i] == 0 and b[i] == 1:
			r += 1
		if a[i] == 0 and b[i] == 0:
			s += 1

	return 1.0 - float(q + r) / float(p + q + r)

def join_age_strat(lst1, lst2):
	tmp = lst1 + lst2
	ageset1 = set([a[-2] for a in lst1])
	ageset2 = set([a[-2] for a in lst2])
	agelst = list(ageset1.intersection(ageset2))


	newlst = [a for a in tmp if a[-2] in agelst]


	return newlst


def join_simple(lst1, lst2):
	return lst1 + lst2


def flatten(l):
	return [item for sublist in l for item in sublist]

def generate_class_vector(biglst, element):
	new_vec = len(biglst) * [0]

	for alpha in element:
		new_vec[biglst.index(alpha)] = 1

	return new_vec


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







def parse_age(agefle):
	mirna2age = {}
	age2mirna = {}

	age_lst = [alpha for alpha in list(csv.reader(open(agefle),delimiter='\t')) if alpha[0][0] != '#' ]

	for i in age_lst:
		mirna2age[i[0]] = float(i[1])
		age2mirna.setdefault(float(i[1]),[]).append(i[0])


	return mirna2age





def data_import():
	mirna2disease = parse_disease('../relevant_data/hmdd_database.txt')
	mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')
	mirna2family = parse_families('../relevant_data/miFam.dat')

	mirna2family_edited = {}

	for alpha in mirna2family:
		if len(mirna2family[alpha]) > 3:
			mirna2family_edited[alpha] = mirna2family[alpha]



	round_robyn_target = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/target_heatmap_dataframe.txt', sep='\t',index_col=[0])
	round_robyn_exp = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/tis_exp_heatmap_dataframe.txt', sep='\t',index_col=[0])
	mir_expdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])
	mir_targetdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/mir_target_vectordb.txt', sep='\t',index_col=[0], encoding='utf-8')


	return mirna2disease, mirna2age, mirna2family_edited, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb




def genpairs(mapped, matrix_indices):
	paira = []
	pairb = []


	for val in matrix_indices:
		for secval in matrix_indices:
			if val == secval: continue
			if val not in mapped and secval not in mapped:
				pairb.append([val, secval])
			if val in mapped and secval in mapped[val]:
				paira.append([val, secval])



	return paira, pairb



def genpairs_agestrat(mapped, oldind, mirna2age):
	newlst = []


	paira = []
	pairb = []

	matrix_indices = [a for a in oldind if a in mirna2age]


	for val in matrix_indices:
		for secval in matrix_indices:
			if val == secval: continue
			if val not in mapped and secval not in mapped:
				pairb.append([val, secval, mirna2age[val], mirna2age[secval]])
			if val in mapped and secval in mapped[val]:
				paira.append([val, secval, mirna2age[val], mirna2age[secval]])


	pairb_new = [a for a in pairb if a[-2] == a[-1]]

	return paira, pairb_new


def add_end_cat(lst, alpha):
	newlst = []

	for el in lst:
		if type(el)!= list:
			newlst.append([el, alpha])
		else:

			tmp = list(el[:])
			tmp = tmp + [alpha,]
			newlst.append(tmp)

	return newlst


def yaxis_switch(str_name):
	if 'tisnum' in str_name:
		return [0,20]
	if 'tarnum' in str_name:
		if 'binary' in str_name:
			return [0, 1000]
		else:
			return [0, 1500]
	if 'jac' in str_name:
		return [0,1.0]
	if 'disnum' in str_name:
		if 'binary' in str_name:
			return [0, 75]
		if 'strat' in str_name:
			return [0, 120]
	if 'tarham' in str_name:
		return [0, 0.10]






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





def simple_family_nofamily(mirna2disease, mirna2age,mirna2family, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb):

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



	fampair, nonfampair = genpairs(reverse_mirdict, round_robyn_target.index)


	mirfamval_tarham = []
	mirnofamval_tarham = []

	for pair in fampair:
		mirfamval_tarham.append(round_robyn_target[pair[0]][pair[1]])

	for pair in nonfampair:
		mirnofamval_tarham.append(round_robyn_target[pair[0]][pair[1]])


	mod_mirfamval_tarham = add_end_cat(mirfamval_tarham, 'Family')
	mod_mirnofamval_tarham = add_end_cat(mirnofamval_tarham, 'Non-Family')


	genfig(join_simple(mod_mirfamval_tarham, mod_mirnofamval_tarham), 'mirbinary_tarham', 'Hamming Targets', 'miRNA Class', 2)



def stratage(mirna2disease, mirna2age,mirna2family, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb):


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



	fampair, nonfampair = genpairs_agestrat(reverse_mirdict, round_robyn_target.index, mirna2age)




	mirfamval_tarham = []
	mirnofamval_tarham = []

	for pair in fampair:
		mirfamval_tarham.append([round_robyn_target[pair[0]][pair[1]], pair[-2]])

	for pair in nonfampair:
		mirnofamval_tarham.append([round_robyn_target[pair[0]][pair[1]], pair[-2]])



	mod_mirfamval_tarham = add_end_cat(mirfamval_tarham, 'Family')
	mod_mirnofamval_tarham = add_end_cat(mirnofamval_tarham, 'Non-Family')


	genfig(join_age_strat(mod_mirfamval_tarham, mod_mirnofamval_tarham), 'mirstrat_tarham', 'Targets Hamming', 'Age (MY)', 3)








def diseases_strat(mirna2disease, mirna2age,mirna2family, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb):


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


	genfig(join_age_strat(mod_mirfamval_disnum, mod_mirnofamval_disnum), 'mirstrat_disnum_collapse', 'Number of Diseases', 'Age (MY)', 3)




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


	genfig(join_age_strat(mod_mirfamval_disjac, mod_mirnofamval_disjac), 'mirstrat_disjac_collapse', 'Disease Jaccard', 'Age (MY)', 3)

















mirna2disease, mirna2age, mirna2family, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb = data_import()
simple_family_nofamily(mirna2disease, mirna2age, mirna2family, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb)
stratage(mirna2disease, mirna2age,mirna2family, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb) 

diseases_strat(collapse_cancer_lst(mirna2disease), mirna2age, mirna2family, round_robyn_target, round_robyn_exp, mir_expdb, mir_targetdb)
