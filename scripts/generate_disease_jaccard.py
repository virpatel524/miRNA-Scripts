import pandas as pd
from data_import import *
from general_methods import *


def generate_class_vector(biglst, element):
	new_vec = len(biglst) * [0]

	for alpha in element:
		new_vec[biglst.index(alpha)] = 1

	return new_vec



disease_data = parse_disease('../relevant_data/hmdd_database.txt')

diseases_biglst = sorted(list(set(flatten(disease_data.values()))))

mirna2binary = {}


for mirna in disease_data:
	mirna2binary[mirna] = generate_class_vector(diseases_biglst, disease_data[mirna])


print mirna2binary