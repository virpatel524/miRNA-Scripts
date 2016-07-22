import pandas as pd
from data_import import *
from general_methods import *


def generate_class_vector(biglst, element):
	new_vec = len(biglst) * [0]

	for alpha in element:
		new_vec[biglst.index(alpha)] = 1

	return new_vec



def generate_matrix(db, str_rel):
	dic = {}
	for ind, item in enumerate(db.keys()):
		print str_rel, ind + 1,  len(db.index)
		secdic = {}
		for secitem in db.keys():
			




	for ind,item in enumerate(db.index):
		print str_rel, ind + 1,  len(db.index)
		secdic = {}
		for secitem in db.index:
			if secitem in dic:
				secdic[secitem] = dic[secitem][item]
				continue
			a = db.loc[item].tolist()
			b = db.loc[secitem].tolist()
			secdic[secitem] = jaccard.jaccard_calculate(a,b)

		dic[item] = secdic


	pd_pre = []

	for key in sorted(dic.keys()):
		newlst = [dic[key][i] for i in sorted(dic.keys())]
		pd_pre.append(newlst)

		

	new_pd = pd.DataFrame(pd_pre,columns=sorted(dic.keys()),index=sorted(dic.keys()))
	new_pd.to_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/%s_dataframe.txt' %(str_rel), sep='\t', encoding='utf-8')

	return dic









disease_data = parse_disease('../relevant_data/hmdd_database.txt')

diseases_biglst = sorted(list(set(flatten(disease_data.values()))))

mirna2binary = {}


for mirna in disease_data:
	mirna2binary[mirna] = generate_class_vector(diseases_biglst, disease_data[mirna])


print mirna2binary