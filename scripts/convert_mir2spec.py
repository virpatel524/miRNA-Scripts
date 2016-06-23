import csv

with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/tree_species.txt') as tree_spe_fle:
	data = list(csv.reader(tree_spe_fle,delimiter='\t'))


with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/organisms.txt') as map_fle:
	species_map = list(csv.reader(map_fle,delimiter='\t'))


for item in species_map:
	print item