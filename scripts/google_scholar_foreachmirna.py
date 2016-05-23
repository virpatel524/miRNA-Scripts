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


proxy_lst = [{'http': '207.210.220.165:3128'}, {'http': '71.42.250.218:80'}, {'http': '97.77.104.22:3128'}, {'http': '97.77.104.22:80'}, {'http': '209.17.113.28:80'}, {'http': '187.177.14.104:8080'}, {'http': '207.91.10.234:8080'}, {'http': '189.203.172.82:8080'}, {'http': '187.191.25.15:3128'}, {'http': '177.234.12.202:3128'}, {'http': '107.21.56.41:80'}, {'http': '189.254.38.169:80'}, {'http': '187.189.82.217:8080'}, {'http': '201.151.151.222:8080'}, {'http': '207.87.85.3:8080'}, {'http': '64.62.233.67:80'}, {'http': '50.254.4.194:3128'}, {'http': '64.12.236.2:80'}, {'http': '146.184.0.115:80'}, {'http': '165.139.149.169:3128'}, {'http': '51.254.129.191:8888'}, {'http': '201.159.19.141:8080'}, {'http': '50.30.152.130:8086'}, {'http': '209.173.8.221:8080'}, {'http': '50.240.46.244:7004'}, {'http': '100.44.118.68:8080'}, {'http': '50.206.36.254:3128'}, {'http': '204.14.188.53:7004'}, {'http': '76.3.249.242:3128'}, {'http': '209.150.253.81:80'}, {'http': '52.11.31.207:4444'}, {'http': '190.144.241.197:3128'}, {'http': '181.48.0.173:8081'}, {'http': '54.187.52.159:3128'}, {'http': '54.187.52.159:8080'}, {'http': '187.189.81.21:8080'}, {'http': '190.184.144.174:8080'}, {'http': '66.175.83.156:8080'}, {'http': '190.202.82.238:3128'}, {'http': '181.49.55.186:8080'}, {'http': '200.37.231.66:8080'}, {'http': '190.85.130.18:3128'}, {'http': '177.200.81.90:8080'}, {'http': '177.200.82.236:8080'}, {'http': '190.248.153.162:8080'}, {'http': '181.112.156.149:8080'}, {'http': '168.63.24.174:8118'}, {'http': '168.63.24.174:8123'}, {'http': '168.63.24.174:8128'}, {'http': '168.63.24.174:8120'}, {'http': '168.63.24.174:8132'}, {'http': '31.187.70.37:80'}, {'http': '94.23.234.179:8585'}, {'http': '164.132.28.153:3128'}, {'http': '176.31.96.198:8080'}, {'http': '5.135.190.199:3128'}, {'http': '176.31.96.198:3128'}, {'http': '91.121.93.140:9000'}, {'http': '184.69.67.122:80'}, {'http': '194.203.40.189:8085'}, {'http': '168.63.24.174:8145'}, {'http': '137.135.166.225:8120'}, {'http': '46.231.117.154:80'}, {'http': '5.135.254.35:3128'}, {'http': '137.135.166.225:8124'}, {'http': '137.135.166.225:8128'}, {'http': '137.135.166.225:8123'}, {'http': '137.135.166.225:8137'}, {'http': '164.132.28.157:3128'}, {'http': '164.132.11.206:3128'}, {'http': '149.202.249.227:3128'}, {'http': '195.154.136.197:8080'}, {'http': '82.165.151.230:80'}, {'http': '146.185.253.241:3128'}, {'http': '137.135.166.225:8118'}, {'http': '137.135.166.225:8121'}, {'http': '77.67.17.201:8080'}, {'http': '176.31.165.141:3128'}, {'http': '82.139.70.104:80'}, {'http': '80.77.29.22:80'}, {'http': '217.170.23.52:3128'}, {'http': '51.254.36.137:3128'}, {'http': '31.207.0.99:3128'}, {'http': '213.240.171.241:8080'}, {'http': '144.76.213.158:3128'}, {'http': '138.201.73.94:3128'}, {'http': '85.114.141.155:8000'}, {'http': '195.8.236.233:8080'}, {'http': '212.166.53.168:80'}, {'http': '80.156.238.188:3128'}, {'http': '201.7.216.85:3128'}, {'http': '200.1.181.126:8080'}, {'http': '200.27.79.74:8080'}, {'http': '109.233.127.36:9000'}, {'http': '82.198.197.62:80'}, {'http': '89.39.48.2:3128'}, {'http': '213.81.212.138:8080'}, {'http': '119.105.177.105:8118'}, {'http': '124.155.112.85:80'}, {'http': '93.51.247.104:80'}]



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

		page = requests.get(site,random.choice(proxy_lst))
		page = page.text




		# m = re.search(' (.+?) results', page)
	
		# found = m.group(1)

		reg_return = re.findall(r'\d+ results',page)
		if len(reg_return) == 0:
			print page
			scholar_txt.write(i + '\t' + str(0) + '\n')
			time.sleep(random.randint(10,15))
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










