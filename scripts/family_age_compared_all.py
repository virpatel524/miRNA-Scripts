import seaborn as sns
import pandas as pd
import csv
from scipy.stats import mannwhitneyu

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


def genfig(lst1, lst2, name, xax, yax):
	newlst1 = [[a,'Family'] for a in lst1]
	newlst2 = [[a,'Non-Family'] for a in lst2]

	tmp = newlst1 + newlst2

	tmp = pd.DataFrame(tmp, columns=[yax, xax])

	sns.violinplot(x=xax, y=yax, data=tmp, cut=0, showfliers=False)
	sns.plt.gca().set_ylim([0,400])
	sns.plt.savefig('../figures/%s_violin.pdf' %(name),bbox_inces='tight')
	sns.plt.close()

	sns.boxplot(x=xax, y=yax, data=tmp, showfliers=False)
	sns.plt.savefig('../figures/%s_boxplot.pdf' %(name),bbox_inces='tight')
	sns.plt.close()	



def data_import():
	mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')
	mirna2family = parse_families('../relevant_data/miFam.dat')

	mirna2family_edited = {}

	for alpha in mirna2family:
		if len(mirna2family[alpha]) > 3:
			mirna2family_edited[alpha] = mirna2family[alpha]


	return mirna2age, mirna2family_edited, mirna2family


mirna2age, mirna2family, mirna2family_raw = data_import()
familymirlst = flatten(mirna2family.values())


remove = [a for a in flatten(mirna2family_raw.values()) if a not in familymirlst]

familymirages = []
nonfamilymirages = []

for mir in mirna2age:
	if mir in remove: continue
	if mir in familymirlst:
		familymirages.append(mirna2age[mir])
	else:
		nonfamilymirages.append(mirna2age[mir])

print mannwhitneyu(familymirages, nonfamilymirages)

genfig(familymirages, nonfamilymirages, 'mirbinary_ageum', 'miRNA Class', 'Age Distribution (MY)')



