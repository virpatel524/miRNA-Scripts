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


# global variables

bad_lst = ['ghb','ssp','fru','hsv','hvt','ebv','rlc','hhv','mcm','pbi','jcv','bkv','mdv','hma','bpc','ksh']


def sort_mir(txt,txt2):
	mega_mir_lst = []
	famdict = {}
	mirlst_by_species = {}
	mirlst_by_family = {}

	meglst = [alpha[0] for alpha in list(csv.reader(txt,delimiter='\t'))]
	famlst = [alpha for alpha in list(csv.reader(txt2,delimiter='\t'))]

	for mir in meglst:
		species = mir[0:3]
		if species in bad_lst:
			continue
		if species[-1] == 'v':
			continue
		mega_mir_lst.append(mir)


		mirlst_by_species.setdefault(species,[]).append(mir)
	
	current_fam = ''

	for i in famlst:
		lst = [alpha for alpha in i[0].split(' ') if alpha != '']
		if i[0][:2] == 'ID' : 
			current_fam = lst[1]
		if i[0][:2] == 'MI' :
			if lst[2][:3] in bad_lst: continue
			if 'v' in lst[2].split('-')[0]: continue
			else:
				famdict.setdefault(current_fam,[]).append(lst[2])



	family_file_for_mirbase = open('/Users/virpatel/Desktop/pub_stuff/relevant_data/family_file_ph.txt','w')

	for i in famdict:
		for mir in famdict[i]:
			if mir != famdict[i][-1]:
				family_file_for_mirbase.write('%s|mirBase:%s ' %(mir[:3], mir)) 
			else: family_file_for_mirbase.write('%s|mirBase:%s\n' %(mir[:3], mir)) 

	family_file_for_mirbase.close()





	return mega_mir_lst, mirlst_by_species, mirlst_by_family


def diseaese_parser(disease_txt):
	disease2mirna = {}
	mirna2disease = {}

	disease_lst = list(csv.reader(disease_txt,delimiter='\t'))
	for i in disease_lst:
		disease2mirna.setdefault(i[1],[]).append(i[0])
		mirna2disease.setdefault(i[0],[]).append(i[1])

	return mirna2disease, disease2mirna	

	
	disease_txt.close()

def age_parser(age_txt):
	mirna2age = {}
	age2mirna = {}

	age_lst = [alpha for alpha in list(csv.reader(age_txt,delimiter='\t')) if alpha[0][0] != '#' ]

	for i in age_lst:
		mirna2age[i[0]] = float(i[1])
		age2mirna.setdefault(float(i[1]),[]).append(i[0])

	with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/hsa_mirlst.txt','w') as mirlst:
		for mirna in mirna2age:
			mirlst.write(mirna + '\n')
			


	return mirna2age, age2mirna

def get_mirna_disease_age_relationship(mirna2age, mirna2disease):
	mirnas_in_q = list(set(mirna2age.keys()).intersection(mirna2disease.keys()))
	
	print len(mirnas_in_q)

	age_dict = []
	num_dis_dict = []


	for i in mirnas_in_q:
		age_dict.append(mirna2age[i])
		num_dis_dict.append(len(mirna2disease[i]))
		print i, mirna2age[i], num_dis_dict[-1]





def main():
	mega_mir_lst = []

	mirlst_by_species = {}
	mirlst_by_mir = {}

	# mirdb = str(raw_input('Enter mirFile:'))
	# famdb = str(raw_input('\nEnter Family File:'))

	mirdb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/all_mir_lst.txt'
	famdb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/miFam.dat'
	diseasedb = '/Users/virpatel/projects/vanderbilt-summer-2014/data/microRNA_disease.txt'
	agedb = '/Users/virpatel/Desktop/pub_stuff/relevant_data/all_ages/hsa_family_file_ph_dollo_age-time.protein_list'


	mega_mir_lst, mirlst_by_species, mirlst_by_fam = sort_mir(open(mirdb,'r'),open(famdb,'r'))
	mirna2disease, disease2mirna = diseaese_parser(open(diseasedb,'r'))
	mirna2age, age2mirna = age_parser(open(agedb, 'r'))

	get_mirna_disease_age_relationship(mirna2age, mirna2disease)












main()
