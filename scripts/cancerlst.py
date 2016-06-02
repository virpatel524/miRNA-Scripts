import csv

data = list(csv.reader(open('/Users/virpatel/projects/vanderbilt-summer-2014/data/list_of_HMDD_diseases.txt','r'),delimiter='\t'))
canlst = []
for el in data:
	dis = el[0]
	if 'oma' in dis or 'eoplas' in dis:
		canlst.append(dis)
		data.remove(el)

print data