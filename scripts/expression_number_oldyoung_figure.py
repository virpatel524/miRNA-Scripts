import seaborn as sns
import pandas as pd
import csv
from data_import import *
from general_methods import *

mir_expdb = pd.read_csv('../exp_data_alldmir.txt', sep='\t',index_col=[0])