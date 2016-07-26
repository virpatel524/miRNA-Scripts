from data_import import *


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


mirna2disease = parse_disease('../relevant_data/hmdd_database.txt')

a = collapse_cancer_lst(mirna2disease)

print list(set(flatten(a.values())))

