import csv
from general_methods import *


data = parsetxt('../relevant_data/pvalues_disease.txt')
lst = []

for alpha in data:
	lst.append(float(alpha[0].split('#')[-1].split('=')[-1].split(')')[0]))
count = 0

for a in lst:
	if a < 0.05:
		count += 1


print count