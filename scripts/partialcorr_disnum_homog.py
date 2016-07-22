import seaborn as sns
import pandas as pd 
import csv
from jaccard import * 
from partialcorr import *
from data_import import * 
from general_methods import * 



mirna2disease = parse_disease('../relevant_data/hmdd_database.txt')
mirna2age = parse_age('../relevant_data/mirna2age_lst.txt')

disease_jaccard = pd.read_csv('../relevant_data/disease_jaccard_dataframe.txt', sep='\t',index_col=[0])

print disease_jaccard