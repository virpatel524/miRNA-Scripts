import csv

def flatten(l):
	return [item for sublist in l for item in sublist]



data = list(csv.reader(open('/Users/virpatel/projects/vanderbilt-summer-2014/data/list_of_HMDD_diseases.txt','r'),delimiter='\t'))
data = flatten(data)
canlst = []
nonlst = []
for ind,dis in enumerate(data):
	if 'oma' in dis or 'eoplas' in dis or 'Leukemia' in dis or 'Sezary' in dis or 'Macroglobulinemia' in dis:
		canlst.append(dis)
	else: nonlst.append(dis)


print nonlst