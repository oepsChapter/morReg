#!/usr/bin/python
# -*- coding: utf-8 -*- 

import multiprocessing as mp
import urllib2
from bs4 import BeautifulSoup
import csv
import sys
import time

class Ship(object):
	"""docstring for Ship"""
	def __init__(self, id):
		super(Ship, self).__init__()
		self.id = id
		self.url = "http://info.rs-head.spb.ru/webFS/regbook/vessel?fleet_id="+str(self.id)
		self.maxAttempt = 3
		self.name = ''
		self.port = ''
		self.flag = ''
		self.ship_class = ''
		self.ownerInfo = ''
		self.ownerName = ''
		self.ownerAddr = ''
		self.ownerIMO = ''
		self.ownerEmail = ''
		self.ownerSite = ''
	def grab(self):
		error = 0
		try :
			web_page = urllib2.urlopen(self.url, timeout=5).read()
			soup = BeautifulSoup(web_page)
			div_GeneralInfo = soup.find("div", {"id": "GeneralInfo"})
			if div_GeneralInfo is not None:
				div_GeneralInfo_rowws = div_GeneralInfo.find_all('tr')
				self.name = div_GeneralInfo_rowws[0].find_all('td')[1].text.encode('utf-8').strip()
				self.port = div_GeneralInfo_rowws[4].find_all('td')[1].text.encode('utf-8').strip()
				self.flag = div_GeneralInfo_rowws[5].find_all('td')[1].text.encode('utf-8').strip()
				self.ship_class = div_GeneralInfo_rowws[6].find_all('td')[1].string.encode('utf-8').strip()
			else:
				error = 1
			div_Owners = soup.find("div", {"id": "Owners"})
			if div_Owners is not None:
				div_Owners_rowws = div_Owners.find_all('td')
				ownerInfo = div_Owners_rowws[1].text.encode('utf-8').strip()
				ownerInfo = ownerInfo.split('\r\n')
				self.ownerName = ownerInfo[0].strip()
				self.ownerAddr = ownerInfo[1].strip()
				self.ownerIMO = ownerInfo[2].strip()
				self.ownerEmail = ownerInfo[3].strip()
				self.ownerSite = ownerInfo[4].strip()
			else:
				error = 2
			div_ShipsType = soup.find("div", {"id": "ShipsType"})
			if div_ShipsType is not None:
				div_ShipsType_rowws = div_ShipsType.find_all('td')
				ShipsTypeInfo = div_ShipsType_rowws[1].text.encode('utf-8').strip()
				ShipsTypeInfo = ShipsTypeInfo.split('\r\n')
				self.type = ShipsTypeInfo[0].strip()
			else:
				error = 3

		except urllib2.HTTPError, e :
			error  = 4
			print("HTTPERROR! on id: ", self.id)
		except urllib2.URLError :
			error = 5
			print("URLERROR! on id: ", self.id)
		sys.stdout.flush()
		return error
		

	def fillInfo(self):
		for nbAttempt in xrange(1,self.maxAttempt + 1):
			res = self.grab()
			if  res < 4:
				if res == 0:
					print self.name
					sys.stdout.flush()
				break
			else:
				time.sleep(2)
				print 'reAttempt id: ',self.id
				sys.stdout.flush()


def worker(id, q):
	s = Ship(id)
	s.fillInfo();
	res = ''
	if s.name != '':
		res = s.name
		res = s.id, s.name, s.port, s.flag, s.ship_class, s.ownerName, s.ownerAddr, s.ownerIMO, s.ownerEmail, s.ownerSite, s.type
		q.put(res)
	return res

def listener(q):
		fo = open(output_file, "wb")
		fo.close()
		while 1:
			m = q.get()
			if m == 'kill':
				fo.close
				break
			fo = open(output_file, "ab")
			spamwriter = csv.writer(fo, delimiter=';')
			spamwriter.writerow(m)
			fo.close()
		fo.close()

def main():
	#must use Manager queue here, or will not work
	manager = mp.Manager()
	q = manager.Queue()	
	pool = mp.Pool(5)

	#put listener to work first
	watcher = pool.apply_async(listener, (q,))

	#fire off workers
	jobs = []
	for i in globalIDs:
		job = pool.apply_async(worker, (i, q))
		jobs.append(job)

	# collect results from the workers through the pool result queue
	for job in jobs: 
		try:
			job.get()
		except Exception, e:
			print e

	#now we are done, kill the listener
	q.put('kill')
	pool.close()

output_file = 'output.txt'
globalIDs = []
with open('ship_ids.txt', 'r') as f:
	globalIDs = [int(line.rstrip('\n')) for line in f]

if __name__ == "__main__":
   main()