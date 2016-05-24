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

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


proxy_lst = [{'https': '137.135.166.225:8124'}, {'https': '177.107.97.245:8080'}, {'https': '137.135.166.225:8132'}, {'https': '188.165.79.184:9999'}, {'https': '137.135.166.225:8127'}, {'https': '189.89.227.117:3128'}, {'https': '164.132.57.130:3128'}, {'https': '90.154.127.19:8000'}, {'https': '186.203.134.5:3128'}, {'https': '62.220.59.105:8080'}, {'https': '91.217.42.2:8080'}, {'https': '187.44.1.167:8080'}, {'https': '91.217.42.4:8080'}, {'https': '213.168.37.86:8080'}, {'https': '128.199.69.60:3128'}, {'https': '197.253.6.69:8080'}, {'https': '202.130.104.236:8080'}, {'https': '190.228.110.194:8080'}, {'https': '177.22.111.113:3128'}, {'https': '61.7.149.69:8080'}, {'https': '118.96.42.150:8080'}, {'https': '46.97.103.50:3128'}, {'https': '202.69.38.82:8080'}, {'https': '211.218.126.189:3128'}, {'https': '89.218.214.106:9090'}, {'https': '46.97.103.50:3128'}, {'https': '211.218.126.189:3128'}, {'https': '202.69.38.82:8080'}, {'https': '61.7.149.69:8080'}, {'https': '197.253.6.69:8080'}, {'https': '128.199.69.60:3128'}, {'https': '202.130.104.236:8080'}, {'https': '213.168.37.86:8080'}]
with open(sys.argv[-1],'r') as fle:
	data = [alpha[0] for alpha in list(csv.reader(fle,delimiter='\t'))]


new_fle = open('test_scholar.txt','w')

datalst = []

with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/scholar_hits.txt','w') as scholar_txt:
	for i in data:




		site = 'http://www.ncbi.nlm.nih.gov/gene/?term=%22' + i + '%22'

		hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; WinNT; en; rv:1.0.2) Gecko/20030311 Beonex/0.8.2-stable',
		       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		       'Accept-Encoding': 'none',
		       'Accept-Language': 'en-US,en;q=0.8'}

		priv = True


		page = requests.get(site,headers=hdr)
		page = page.text



		if 'Summary' not in page:
			datalst.append(['0',found])
			continue





		print i
		print re.findall("(\d+) citations", page)
	


		# found = str(reg_return[0]).split(' ')[0]
		# datalst.append([i,found])
		# print datalst
		# new_fle.write('%s\t%s\n' %(i, found))

		# scholar_txt.write(i + '\t' + found + '\n')




with open('/Users/virpatel/Desktop/pub_stuff/relevant_data/scholar_hits.txt','w') as scholar_txt:
	for i in datalst:
		scholar_txt.write('%s\t%s\n' %(i[0],i[1]))



new_fle.close()





