import csv

with open('/Users/virpatel/Desktop/working_proxies.txt') as fle:
	data = list(csv.reader(fle,delimiter='\t'))

new_data = ["{'https': '%s'}" %(a) for a in data]