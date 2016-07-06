import csv

ensembl2hgnc_data = list(csv.reader(open('../raw_data/hgnc-ensembl.txt'), delimiter='\t'))[1:]
ph_ages = [a for a in list(csv.reader(open('../ProteinHistorian/example/ages/human_age-label_dollo.txt'), delimiter='\t')) if '#' not in a[0]]
time_tree_ages = [a for a in list(csv.reader(open('../relevant_data/time_tree_dates.txt'), delimiter='\t')) if '#' not in a[0]]

ens2hgnc_dic = {}

for alpha in ensembl2hgnc_data:
	ensembl2hgnc_data[alpha[0]] = ensembl2hgnc_data[alpha[-1]]





