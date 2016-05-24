import urllib2
import string
import re
import time
import math, csv
import random
import sys, os, string
import requests
import random
import re


proxy_lst = [{'http': '218.205.17.75:80'}, {'http': '178.155.14.10:8080'}, {'http': '104.236.48.178:8080'}, {'http': '218.205.17.78:80'}, {'http': '216.251.125.103:80'}, {'http': '221.178.181.125:80'}, {'http': '117.21.182.109:80'}, {'http': '203.66.159.45:3128'}, {'http': '203.66.159.44:3128'}, {'http': '203.223.143.51:8080'}, {'http': '112.16.87.160:8003'}, {'http': '112.65.200.211:80'}, {'http': '218.205.17.66:80'}, {'http': '120.52.72.24:80'}, {'http': '107.151.152.218:80'}, {'http': '120.52.72.59:80'}, {'http': '111.56.13.168:80'}, {'http': '221.178.181.250:80'}, {'http': '14.18.236.99:80'}, {'http': '202.100.167.145:80'}, {'http': '24.148.100.200:8080'}, {'http': '221.181.244.118:80'}, {'http': '221.178.181.193:80'}, {'http': '111.56.13.174:80'}, {'http': '117.135.157.188:80'}]

with open(sys.argv[-1],'r') as fle:
	data = [alpha[0] for alpha in list(csv.reader(fle,delimiter='\t'))]


datalst = []

with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/scholar_hits.txt','w') as scholar_txt:
	for i in data:




		site = 'http://scholar.google.com/scholar?as_vis=1&q="%s"+&hl=en&as_sdt=1,18' %(i)
		print site

		hdr = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11',
		       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		       'Accept-Encoding': 'none',
		       'Accept-Language': 'en-US,en;q=0.8'}

		priv = True

		while priv:
			# try:
			page = requests.get(site,proxies=random.choice(proxy_lst))
			# except:
			# 	print 'lol'
			# 	continue
			page = page.text
			print page
			if 'Privoxy' in page:
				continue
			if 'detected unusual traffic' in page:
				continue
			else:
				priv = False





		# m = re.search(' (.+?) results', page)
	
		# found = m.group(1)

		reg_return = re.findall(r'\d+ results',page)
		if len(reg_return) == 0:
			print page
			scholar_txt.write(i + '\t' + str(0) + '\n')
			datalst.append([i,str(0)])
			continue

		found = str(reg_return[0]).split(' ')[0]
		datalst.append([i,found])
		print datalst

		scholar_txt.write(i + '\t' + found + '\n')




with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/scholar_hits.txt','w') as scholar_txt:
	for i in datalst:
		scholar_txt.write('%s\t%s\n' %(i[0],i[1]))










