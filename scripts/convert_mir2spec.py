import csv

with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/tree_species.txt') as tree_spe_fle:
	data = list(csv.reader(tree_spe_fle,delimiter='\t'))


with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/organisms.txt') as map_fle:
	species_map = list(csv.reader(map_fle,delimiter='\t'))



mapper_dict = {}

for item in species_map:
	if item[0][0] == '#': continue
	mapper_dict[item[0]] = item[2]
	print item[2]

	


with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/mapped_mir2species_4tree.txt','w') as mapped_fle:
	for i in data:
		mapped_fle.write(mapper_dict[i[0]] + '\n')