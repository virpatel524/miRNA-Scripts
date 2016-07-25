import seaborn as sns
import csv
from general_methods import *


data = parsetxt('../relevant_data/pvalues_disease.txt')
lst = []

for alpha in data:
	lst.append(float(alpha[0].split('#')[-1].split('=')[-1].split(')')[0]))

print lst[0]
