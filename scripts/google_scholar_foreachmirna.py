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


proxy_lst = [{'http': '58.154.33.12:8080'}, {'http': '122.96.59.104:82'}, {'http': '122.96.59.107:843'}, {'http': '122.96.59.99:80'}, {'http': '122.96.59.107:81'}, {'http': '111.23.6.166:8080'}, {'http': '210.101.131.232:8080'}, {'http': '122.96.59.102:80'}, {'http': '52.35.67.51:8118'}, {'http': '222.45.58.64:8118'}, {'http': '114.40.111.124:80'}, {'http': '202.117.54.247:808'}, {'http': '118.141.221.71:80'}, {'http': '111.23.6.147:8080'}, {'http': '113.252.181.81:80'}, {'http': '113.252.11.26:80'}, {'http': '117.136.234.8:82'}, {'http': '94.203.96.16:80'}, {'http': '91.211.112.248:8080'}, {'http': '117.136.234.6:843'}, {'http': '221.181.8.214:8090'}, {'http': '117.135.250.134:8081'}, {'http': '221.181.8.214:8090'}, {'http': '117.135.250.133:80'}, {'http': '117.135.250.134:80'}, {'http': '88.13.168.126:8080'}, {'http': '117.136.234.1:82'}, {'http': '112.5.220.199:83'}, {'http': '112.5.220.199:83'}, {'http': '117.135.250.133:8081'}, {'http': '117.135.250.133:8082'}, {'http': '117.135.250.134:8082'}, {'http': '117.135.250.133:8081'}, {'http': '117.136.234.8:843'}, {'http': '117.136.234.8:82'}, {'http': '117.136.234.8:83'}, {'http': '117.136.234.8:843'}, {'http': '117.136.234.8:83'}, {'http': '117.136.234.8:80'}, {'http': '190.12.92.51:80'}, {'http': '212.126.102.238:8080'}, {'http': '117.136.234.1:80'}, {'http': '94.203.42.225:80'}, {'http': '117.136.234.1:80'}, {'http': '94.203.96.16:80'}, {'http': '40.113.118.174:8130'}, {'http': '88.159.172.245:80'}, {'http': '83.128.190.244:80'}, {'http': '31.151.206.243:80'}, {'http': '88.159.140.239:80'}, {'http': '213.197.43.122:80'}]

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
			try:
				page = requests.get(site,proxies=random.choice(proxy_lst))
				print page.text()
			except:
				print 'lol'
				continue
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
			time.sleep(random.randint(0,5))
			datalst.append([i,str(0)])
			continue

		found = str(reg_return[0]).split(' ')[0]
		datalst.append([i,found])
		print datalst

		scholar_txt.write(i + '\t' + found + '\n')

		time.sleep(random.randint(0,5))



with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/scholar_hits.txt','w') as scholar_txt:
	for i in datalst:
		scholar_txt.write('%s\t%s\n' %(i[0],i[1]))










