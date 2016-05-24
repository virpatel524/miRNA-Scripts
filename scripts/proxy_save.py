import csv

with open('/Users/virpatel/Desktop/proxies.txt') as fle:
	data = list(csv.reader(fle,delimiter='\t'))

print ["{'https': '%s:%s'}" %(a[-1], a[-2]) for index, a in enumerate(data) if index % 2 == 1]