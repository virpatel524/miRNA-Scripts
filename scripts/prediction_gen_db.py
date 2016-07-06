import seaborn as sns
import pandas as pd
import csv
from distance import hamming


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
			secdic[secitem] = hamming(a,b,normalized=True)

		dic[item] = secdic


	pd_pre = []

	for key in sorted(dic.keys()):
		newlst = [dic[key][i] for i in sorted(dic.keys())]
		pd_pre.append(newlst)

		

	new_pd = pd.DataFrame(pd_pre,columns=sorted(dic.keys()),index=sorted(dic.keys()))
	print new_pd
	new_pd.to_csv('../relevant_data/%s_dataframe.txt' %(str_rel), sep='\t', encoding='utf-8')

	return new_pd








with open('../relevant_data/target_predictions_targetscan.txt') as pred_fle:
	data = list(csv.reader(pred_fle, delimiter='\t'))


all_genes = sorted(list(set(([a[1] for a in data]))))


pred_dict = {}

for val in data:
	pred_dict.setdefault(val[0],[]).append(val[1])

pred_vector = {}

for val in pred_dict:
	pred_vector[val] = generate_class_vector(all_genes, pred_dict[val])


binary_pd_gen(pred_vector, all_genes)
generate_matrix(pred_vector, 'predictions_hamming_target')










