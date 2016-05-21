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
import os


mir2nivel = {}
mir2clade = {}
mir2timetree = {}

for root, dirs, fle_lst in os.walk('/Users/virpatel/Desktop/pub_stuff/relevant_data/selectmir_ages/'):
	for fle_name in fle_lst:
		tmp = fle_name.split('_')
		fle_type = tmp[-2].split('.')[0]
		species = tmp[0]

		if fle_type == 'phylo-profile': continue

		txt = []

		with open(os.path.realpath(os.path.join(root, fle_name))) as fle_inq:
			txt = list(csv.reader(fle_inq,delimiter='\t'))

		for el in txt:
			if '#' in el[0]:
				continue
			if fle_type == 'age-depth':
				mir2nivel[el[0]] = el[1]
			if fle_type == 'age-label':
				mir2clade[el[0]] = el[1]
			if fle_type == 'age-time':
				mir2timetree[el[0]] = el[1]



mirlst = sorted(mir2nivel.keys())


with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/ph_dataset_starmir.txt','w') as ph_dataset:
	for beta in mirlst:
		ph_dataset.write('%s\t%s\t%s\n' %(beta, mir2nivel[beta], mir2clade[beta]))


age_mirlst = sorted(mir2timetree.keys())

with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/ph_dataset_with_time_tree_starmir.txt','w') as ph_dataset_with_time_tree:
	for beta in age_mirlst:
		ph_dataset_with_time_tree.write('%s\t%s\t%s\t%s\n' %(beta,mir2nivel[beta], mir2clade[beta], mir2timetree[beta]))



mirswnoage = list(set.difference(set(mirlst), set(age_mirlst)))

clade_lst_noages = list(set([mir2clade[alpha] for alpha in mirswnoage]))

with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/need_ages_starmir.txt','w') as need_ages_fle:
	for el in clade_lst_noages:
		need_ages_fle.write('%s\n' %(el))

		



