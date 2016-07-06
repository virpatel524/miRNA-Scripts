import csv
import pandas as pd

def parse_disease(disfle):
	distxt = list(csv.reader(open(disfle), delimiter='\t'))
	mirna2disease = {}

	for val in distxt:
		mirna2disease.setdefault(val[0],[]).append(val[1])

def age_parser(age_txt):
	mirna2age = {}
	age2mirna = {}

	age_lst = [alpha for alpha in list(csv.reader(open(agefle),delimiter='\t')) if alpha[0][0] != '#' ]

	for i in age_lst:
		mirna2age[i[0]] = float(i[1])
		age2mirna.setdefault(float(i[1]),[]).append(i[0])


	return mirna2age