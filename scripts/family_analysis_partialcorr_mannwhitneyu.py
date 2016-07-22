import seaborn as sns
import pandas as pd
import csv
from data_import import *
from partialcorr import *
from general_methods import *
from scipy.stats import mannwhitneyu



def allages_cmp(el1, el2):
	if type(el1) == str:
		return -1
	if type(el2) == str:
		return 1
	if el2 == el1:
		return 0
	if el1 > el2:
		return 1
	if el2 > el1:
		return -1



def num(s):
	try:
		return float(s)
	except:
		return s

def float_conv(entry):
	 return [[num(a) for a in beta] for beta in entry]


def append_allage(lst):
	tmp = lst[:]
	for alpha in tmp:
		alpha.insert(1, 'ALL AGES')
		alpha.append(1)
	return tmp

def append_haveage(lst):
	tmp = lst[:]
	for alpha in tmp:
		alpha.append(0)

	return tmp


def do_man():
	for index, alpha in enumerate(all_data):
		famlst = []
		nonfamlst = []
		for beta in alpha:
			if 'Family' in beta:
				famlst.append(beta[0])
			if 'Non-Family' in beta:
				nonfamlst.append(beta[0])

		print mannwhitneyu(famlst, nonfamlst), data_names[index]












mirbinary_disjac = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_disjac')))
mirbinary_expjac = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_expjac')))
mirbinary_tarjac = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tarjac')))
mirbinary_disnum = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_disnum')))
mirbinary_expnum = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tisnum')))
mirbinary_tarnum = append_allage(float_conv(parsecsvexport('../relevant_data/precursor_pd/mirbinary_tarnum')))

all_data = [mirbinary_disjac, mirbinary_expjac, mirbinary_tarjac, mirbinary_disnum, mirbinary_expnum, mirbinary_tarnum]
data_names = ['mirbinary_disjac', 'mirbinary_expjac', 'mirbinary_tarjac', 'mirbinary_disnum', 'mirbinary_expnum', 'mirbinary_tarnum']
