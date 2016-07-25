import seaborn as sns
import csv
from general_methods import *


data = parsetxt('../relevant_data/pvalues_disease.txt')
for alpha in data:
	print alpha.split('#')[-1]
