import seaborn as sns 
import pandas as pd
import csv 
from data_import import *
from general_methods import *


mirna2family = parse_families('../relevant_data/miFam.dat')
mir_expdb = pd.read_csv('/Users/virpatel/Desktop/pub_stuff/relevant_data/exp_data_alldmir.txt', sep='\t',index_col=[0])

print mir_expdb