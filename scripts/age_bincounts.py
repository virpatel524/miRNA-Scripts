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
from scipy.stats import skew, kurtosis, spearmanr
from distance import hamming
from numpy import mean
import pylab
import os



mir2age = []

species2mirna = {}


def import_ages(dir):

	with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/ph_dataset_with_time_tree.txt') as master_age_mirlst:
		mirlst = list(csv.reader(master_age_mirlst,delimiter='\t'))
		for mir in mirlst:
			spe = mir[0][:3]
			species2mirna.setdefault(spe,[]).append([mir[0],mir[-1]])

	age_lst = []


	for spe in species2mirna:
		for mir in species2mirna[spe]:
			age_lst.append(float(mir[-1]))

	return species2mirna, age_lst


def bincount(species2mirna,float_lst):

	# create master histogram

	labels = []



	skew_lst = []
	num_lst = []

	percent_lst = []



	labels = [float(alpha) for alpha in sorted(list(set(float_lst)))]
	str_labels = [str(alpha) for alpha in sorted(list(set(float_lst)))]

	binlst = [0] * len(labels)


	for el in float_lst:
		binlst[labels.index(float(el))] = binlst[labels.index(float(el))] + 1


	ind = np.arange(0,len(labels)*2.3,2.3)
	plt.figure(figsize=(30,10))


	plt.bar(ind, binlst,2)
	plt.xticks(ind,str_labels,rotation=55,ha='center')

	plt.xlabel('Ages (MYA)')
	plt.ylabel('Number of miRNAs')
	plt.title('Age of All miRNAs Histogram ')

	plt.savefig('/Users/virpatel/Desktop/pub_stuff/figures/all_mirbase.png')

	plt.close()



	# create histogram for each species


	for species in species2mirna:
		age_lst_for_species = []
		for mir in species2mirna[species]:
			age_lst_for_species.append(float(mir[-1]))



		age_lst_for_species = sorted(age_lst_for_species)


		skew_val = float(skew(age_lst_for_species))
		kurtval =  str(kurtosis(age_lst_for_species)) 


		labels = [float(alpha) for alpha in sorted(list(set(age_lst_for_species)))]
		str_labels = [str(alpha) for alpha in sorted(list(set(age_lst_for_species)))]

		if len(labels) <= 4:
			continue



		binlst = [0] * len(labels)




		for el in age_lst_for_species:
			binlst[labels.index(float(el))] = binlst[labels.index(float(el))] + 1


		ind = np.arange(0,len(labels)*2.3,2.3)

		if len(ind) == len(binlst) + 1:
			ind = np.arange(0,len(labels)*2.3-2.3,2.3)


		# plt.figure(figsize=(30,10))


		# plt.bar(ind, binlst,2)
		# plt.xticks(ind,str_labels,rotation=55,ha='center')

		# plt.xlabel('Ages (MYA)')
		# plt.ylabel('Number of miRNAs')
		# plt.title('Age of %s miRNAs Histogram' %(species))

		# plt.savefig('/Users/virpatel/Desktop/pub_stuff/figures/each_species_bincount/%s_bincount.png' %(species))

		# plt.close()


		with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/skew_data.txt','a') as skew_data:
			skew_data.write('%s\t%.3f\t%d\n' %(species, skew_val, len(age_lst_for_species)))

		skew_lst.append(float(skew_val))
		num_lst.append(float(len(age_lst_for_species)))


	skew_versus_numinlist = spearmanr(skew_lst, num_lst)


	










#initialize

fle = open('/Users/virpatel/Desktop/pub_stuff/relevant_data/skew_data.txt','w')	
fle.close()	





species2mirna, master_age_lst = import_ages('/Users/virpatel/Desktop/pub_stuff/relevant_data/all_ages')


bincount(species2mirna, master_age_lst)










