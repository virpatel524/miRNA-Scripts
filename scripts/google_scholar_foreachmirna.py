import urllib2
import string
import re
import time
import math, csv
import random
import sys, os, string, numpy, matplotlib.pyplot as plt
import requests


with open(sys.argv[-1],'r') as fle:
	data = [alpha[0] for alpha in list(csv.reader(fle,delimiter='\t'))]


with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/scholar_hits.txt','w') as scholar_txt:
	for i in data:
		print i


		site = 'https://scholar.google.com/scholar?hl=en&q="' + i + '"%22'
		print site

		hdr = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11',
		       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		       'Accept-Encoding': 'none',
		       'Accept-Language': 'en-US,en;q=0.8',
		       'Connection': 'keep-alive'}

		page = requests.get(site)
		page = page.text

		print page


		import re

		m = re.search('About (.+?) results', page)
	
		found = m.group(1)

		scholar_txt.write('big head')
		scholar_txt.write(found + '\n')

		time.sleep(randint(10,100))










