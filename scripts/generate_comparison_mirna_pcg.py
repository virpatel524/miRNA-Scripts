import seaborn as sns
import matplotlib.pyplot as plt
import sys
import csv

def import_pcg():
	return
	

def import_human_mirages():
	data = []	

	with open(sys.argv[1],'r') as mir_ages_fle:
		data = list(csv.reader(mir_ages_fle,delimiter='\t'))

	humanmirlst = [a for a in data if 'hsa' in a[0]]
	human_ages = [float(a[-1]) for a in humanmirlst]

	print human_ages





import_human_mirages()