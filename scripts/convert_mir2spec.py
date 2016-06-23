import csv

with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/tree_species.txt') as tree_spe_fle:
	data = list(csv.reader(tree_spe_fle,delimiter='\t'))


with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/organisms.txt') as map_fle:
	species_map = list(csv.reader(map_fle,delimiter='\t'))



mapper_dict = {}

for item in species_map:
	if item[0] == '#': continue
	

	


with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/mapped_mir2species_4tree.txt','w') as mapped_fle:
