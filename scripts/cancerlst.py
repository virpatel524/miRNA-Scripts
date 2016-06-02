import csv

def flatten(l):
	return [item for sublist in l for item in sublist]



data = list(csv.reader(open('/Users/virpatel/projects/vanderbilt-summer-2014/data/list_of_HMDD_diseases.txt','r'),delimiter='\t'))
data = flatten(data)
canlst = []
for ind,dis in enumerate(data):
	if dis == 'Glioblastoma':
		print 'ah'
	if 'oma' in dis or 'eoplas' in dis:
		canlst.append(dis)
		data.pop(ind)

print data