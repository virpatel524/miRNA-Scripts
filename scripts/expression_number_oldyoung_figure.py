import seaborn as sns
import pandas as pd
import csv
from data_import import *
from general_methods import *

mir_expdb = pd.read_csv('../relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])

mirna2numexp = {}

for alpha in mir_expdb.index:
	mirna2numexp[alpha] = sum(mir_expdb.loc[alpha].tolist())
print mirna2numexp