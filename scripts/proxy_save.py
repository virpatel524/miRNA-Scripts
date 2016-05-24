import csv

with open('/Users/virpatel/Desktop/proxies.txt') as fle:
	data = list(csv.reader(fle,delimiter='\t'))

alpha =  ['%s:%s' %(a[-1], a[-2]) for index, a in enumerate(data) if index % 2 == 1]
for al in alpha:
	print al