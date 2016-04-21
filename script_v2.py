import string
import re
import scipy
import time
import math, csv
import random
import operator
import numpy as np
from numpy.random import randn
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os, string, numpy, matplotlib.pyplot as plt
from scipy.stats import spearmanr
from distance import hamming
from numpy import mean
import pylab


def sort_mir(txt,txt2):
	mega_mir_lst = []
	famdict = {}
	mirlst_by_species = {}
	mirlst_by_family = {}

	meglst = [alpha[0] for alpha in list(csv.reader(txt,delimiter='\t'))]
	famlst = [alpha for alpha in list(csv.reader(txt2,delimiter='\t'))]

	for mir in meglst:
		mega_mir_lst.append(mir)
		species = mir[0:3]
		mirlst_by_species.setdefault(species,[]).append(mir)
	
	current_fam = ''

	for i in famlst:
		lst = [alpha for alpha in i[0].split(' ') if alpha != '']
		if i[0][:2] == 'ID' : current_fam = lst[1]
		if i[0][:2] == 'MI' : famdict.setdefault(current_fam,[]).append(lst[2])



	family_file_for_mirbase = open('/Users/virpatel/Desktop/pub_stuff/relevant_data/family_file_ph.txt','w')

	for i in famdict:
		for mir in famdict[i]:
			print mir
			if mir != famdict[i][-1]:
				family_file_for_mirbase.write('%s|mirBase:%s' %(mir[:3], mir)) 
			else: family_file_for_mirbase.write('%s|mirBase:%s\n' %(mir[:3], mir)) 

	family_file_for_mirbase.close()





	return mega_mir_lst, mirlst_by_species, mirlst_by_family




def main():
	mega_mir_lst = []

	mirlst_by_species = {}
	mirlst_by_mir = {}

	# mirdb = str(raw_input('Enter mirFile:'))
	# famdb = str(raw_input('\nEnter Family File:'))

	mirdb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/select_data_lst.txt'
	famdb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/miFam.dat'

	mega_mir_lst, mirlst_by_species, mirlst_by_fam = sort_mir(open(mirdb,'r'),open(famdb,'r'))












main()
