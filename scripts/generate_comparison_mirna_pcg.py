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

	print data




import_human_mirages()