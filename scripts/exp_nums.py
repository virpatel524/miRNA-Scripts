import seaborn as sns 
import pandas as pd
import csv 
from data_import import *
from general_methods import *


mirna2family = parse_families('../relevant_data/miFam.dat')

print mirna2family