import csv

data = list(csv.reader(open('../raw_data/hmdd_data.txt'), delimiter='\t'))

newlst = []

for alpha in data:
	newlst.append([alpha[1], alpha[2]])

with open('../relevant_data/hmdd_database.txt','w') as hmddd_fle:
	for alpha in newlst:
		hmddd_fle.write('%s\t%s\n' %(alpha[0], alpha[1]))

