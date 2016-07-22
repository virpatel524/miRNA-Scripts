import pandas as pd
from data_import import *
from general_methods import *


disease_data = parse_disease('../relevant_data/hmdd_database.txt')

diseases_biglst = sorted(list(set(flatten(disease_data.values()))))

print diseases_biglst