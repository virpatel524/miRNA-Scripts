import csv
import sys

csv.field_size_limit(sys.maxsize)

def parsecsvexport(txt):
	data = list(csv.reader(open(txt,'r'),delimiter=',',skipinitialspace=True))
	return data

