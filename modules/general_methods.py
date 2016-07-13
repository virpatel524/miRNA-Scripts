import csv


def parsetxt(txt);
	data = list(csv.reader(open(txt,'r'),delimiter='\t'))
	return data