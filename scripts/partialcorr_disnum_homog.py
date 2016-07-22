import seaborn as sns
import pandas as pd 
import csv
from jaccard import * 
from partialcorr import *
from data_import import * 
from general_methods import * 



mirna2disease = parse_disease()
mirna2age = parse_age()