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
import traceback


proxy_lst = [{'https': '74.113.170.46:8080'}, {'https': '207.91.10.234:8080'}, {'https': '207.87.85.3:8080'}, {'https': '201.151.151.222:8080'}, {'https': '146.184.0.116:8080'}, {'https': '146.184.0.115:8080'}, {'https': '207.5.112.114:8080'}, {'https': '73.129.7.140:80'}, {'https': '146.184.0.115:80'}, {'https': '51.254.129.191:8888'}, {'https': '165.139.149.169:3128'}, {'https': '146.184.0.116:80'}, {'https': '209.173.8.221:8080'}, {'https': '50.30.152.130:8086'}, {'https': '201.159.19.141:8080'}, {'https': '71.162.154.163:3130'}, {'https': '54.187.52.159:3128'}, {'https': '181.48.87.226:3128'}, {'https': '24.148.100.200:8080'}, {'https': '200.24.198.242:8080'}, {'https': '190.85.130.18:3128'}, {'https': '24.205.244.90:7004'}, {'https': '181.49.36.162:3128'}, {'https': '177.107.97.245:8080'}, {'https': '190.0.33.18:3128'}, {'https': '168.63.24.174:8125'}, {'https': '168.63.24.174:8145'}, {'https': '168.63.24.174:8121'}, {'https': '168.63.24.174:8128'}, {'https': '168.63.24.174:8124'}, {'https': '168.63.24.174:8127'}, {'https': '168.63.24.174:8123'}, {'https': '177.55.254.196:8080'}, {'https': '176.31.96.198:3128'}, {'https': '164.132.28.153:3128'}, {'https': '168.63.24.174:8143'}, {'https': '178.33.191.53:3128'}, {'https': '168.63.24.174:8118'}, {'https': '164.132.28.157:3128'}, {'https': '137.135.166.225:8118'}, {'https': '137.135.166.225:8124'}, {'https': '137.135.166.225:8146'}, {'https': '137.135.166.225:8125'}, {'https': '188.165.79.184:9999'}, {'https': '137.135.166.225:8123'}, {'https': '137.135.166.225:8136'}, {'https': '201.38.196.50:3128'}, {'https': '149.202.249.227:3128'}, {'https': '137.135.166.225:8132'}, {'https': '137.135.166.225:8128'}, {'https': '137.135.166.225:8127'}, {'https': '46.231.117.154:8085'}, {'https': '200.46.86.66:3128'}, {'https': '151.80.108.134:3128'}, {'https': '94.23.158.49:80'}, {'https': '31.207.0.99:3128'}, {'https': '186.103.169.165:8080'}, {'https': '190.82.94.13:80'}, {'https': '88.198.69.186:3128'}, {'https': '200.229.225.54:80'}, {'https': '201.33.184.234:8080'}, {'https': '213.211.36.146:8080'}, {'https': '31.31.73.195:3128'}, {'https': '82.85.8.99:8080'}, {'https': '46.41.130.135:3128'}, {'https': '109.196.34.51:8080'}, {'https': '178.19.98.1:8088'}, {'https': '5.56.12.13:8080'}, {'https': '200.113.19.21:8080'}, {'https': '189.8.10.132:3128'}, {'https': '201.54.5.115:8080'}, {'https': '82.78.191.159:8080'}, {'https': '200.195.135.195:3128'}, {'https': '176.31.165.141:3128'}, {'https': '189.89.227.117:3128'}, {'https': '189.45.56.98:3128'}, {'https': '92.62.225.4:8888'}, {'https': '194.186.45.72:8080'}, {'https': '84.22.35.37:3129'}, {'https': '91.221.233.82:8080'}, {'https': '203.66.159.46:3128'}, {'https': '194.8.47.6:8080'}, {'https': '194.85.37.90:3128'}, {'https': '94.228.198.82:8080'}, {'https': '187.45.112.5:3128'}, {'https': '130.193.65.155:3128'}, {'https': '177.54.106.198:8081'}, {'https': '194.154.128.65:8080'}, {'https': '178.151.149.227:80'}, {'https': '203.66.159.45:3128'}, {'https': '203.66.159.44:3128'}, {'https': '164.132.57.130:3128'}, {'https': '186.203.134.5:3128'}, {'https': '31.173.74.73:8080'}, {'https': '178.151.69.119:3128'}, {'https': '210.101.131.231:8080'}, {'https': '90.154.127.19:8000'}, {'https': '211.77.5.41:3128'}, {'https': '193.194.69.36:3128'}, {'https': '211.77.5.41:80'}]

with open(sys.argv[-1],'r') as fle:
	data = [alpha[0] for alpha in list(csv.reader(fle,delimiter='\t'))]


datalst = []

with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/scholar_hits.txt','w') as scholar_txt:
	for i in data:




		site = 'https://scholar.google.com/scholar?as_vis=1&q="%s"+&hl=en&as_sdt=1,18' %(i)
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
			except Exception, e:
				traceback.print_exc()
				continue
			if 'include citations' in page:
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










