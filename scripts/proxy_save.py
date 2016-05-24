import csv

with open('/Users/virpatel/Desktop/proxies.txt') as fle:
	data = list(csv.reader(fle,delimiter='\t'))

print data