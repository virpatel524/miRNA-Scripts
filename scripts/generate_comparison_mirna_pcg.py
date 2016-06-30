import seaborn as sns
import matplotlib.pyplot as plt
import sys
import csv

def import_pcg():
	data = []

	with open(sys.argv[2], 'r') as pcg_ages_precursor_fle:
		data = list(csv.reader(pcg_ages_precursor_fle, delimiter='\t'))

	precursor_data = [a[-1] for a in data if '#' not in a[0]]

	time_tree_fle = open(sys.argv[3],'r')
	time_tree_data = list(csv.reader(time_tree_fle, delimiter='\t'))
	

def import_human_mirages():
	data = []	

	with open(sys.argv[1],'r') as mir_ages_fle:
		data = list(csv.reader(mir_ages_fle,delimiter='\t'))

	humanmirlst = [a for a in data if 'hsa' in a[0]]
	human_ages = [float(a[-1]) for a in humanmirlst]

	print human_ages





# import_human_mirages()
import_pcg()