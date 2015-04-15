#!/usr/bin/python
# -*- coding: utf-8 -*- 

import urllib
import urllib2
from bs4 import BeautifulSoup
import re

countrys = [
{'name' : 'Азербайджан','id' : 11, 'pageCount' : 0},
{'name' : 'Антигуа и Барбуда','id' : 4, 'pageCount' : 0},
{'name' : 'Барбадос','id' : 12, 'pageCount' : 0},
{'name' : 'Белиз','id' : 21, 'pageCount' : 0},
{'name' : 'Болгария','id' : 15, 'pageCount' : 0},
{'name' : 'Вануату','id' : 133, 'pageCount' : 0},
{'name' : 'Гондурас','id' : 52, 'pageCount' : 0},
{'name' : 'Греция','id' : 49, 'pageCount' : 0},
{'name' : 'Грузия','id' : 44, 'pageCount' : 0},
{'name' : 'Доминика','id' : 140, 'pageCount' : 0},
{'name' : 'Израиль','id' : 55, 'pageCount' : 0},
{'name' : 'Казахстан','id' : 68, 'pageCount' : 0},
{'name' : 'Камбоджа','id' : 65, 'pageCount' : 0},
{'name' : 'Кипр','id' : 31, 'pageCount' : 0},
{'name' : 'Коморские острова','id' : 154, 'pageCount' : 0},
{'name' : 'Корея','id' : 67, 'pageCount' : 0},
{'name' : 'Кука острова','id' : 156, 'pageCount' : 0},
{'name' : 'Латвия','id' : 75, 'pageCount' : 0},
{'name' : 'Либерия','id' : 73, 'pageCount' : 0},
{'name' : 'Ливан','id' : 69, 'pageCount' : 0},
{'name' : 'Литва','id' : 72, 'pageCount' : 0},
{'name' : 'Мальта','id' : 83, 'pageCount' : 0},
{'name' : 'Маршалловы острова','id' : 80, 'pageCount' : 0},
{'name' : 'Мексика','id' : 84, 'pageCount' : 0},
{'name' : 'Молдова','id' : 79, 'pageCount' : 0},
{'name' : 'Монголия','id' : 216, 'pageCount' : 0},
{'name' : 'Нигерия','id' : 89, 'pageCount' : 0},
{'name' : 'Новая Зеландия','id' : 94, 'pageCount' : 0},
{'name' : 'Объединенные Арабские Эмираты','id' : 2, 'pageCount' : 0},
{'name' : 'Палау','id' : 193, 'pageCount' : 0},
{'name' : 'Панама','id' : 95, 'pageCount' : 0},
{'name' : 'Перу','id' : 96, 'pageCount' : 0},
{'name' : 'Россия','id' : 102, 'pageCount' : 0},
{'name' : 'Сент-Винсент и Гренадины','id' : 130, 'pageCount' : 0},
{'name' : 'Сент-Китс и Невис','id' : 109, 'pageCount' : 0},
{'name' : 'Страна неизвестна','id' : 137, 'pageCount' : 0},
{'name' : 'Сьерра-Леоне','id' : 110, 'pageCount' : 0},
{'name' : 'Танзания','id' : 125, 'pageCount' : 0},
{'name' : 'Того','id' : 117, 'pageCount' : 0},
{'name' : 'Тувалу','id' : 123, 'pageCount' : 0},
{'name' : 'Туркменистан','id' : 120, 'pageCount' : 0},
{'name' : 'Турция','id' : 122, 'pageCount' : 0},
{'name' : 'Украина','id' : 126, 'pageCount' : 0},
{'name' : 'Эстония','id' : 36, 'pageCount' : 0},
{'name' : 'Ямайка','id' : 177, 'pageCount' : 0}
]

url = 'http://info.rs-head.spb.ru/webFS/regbook/regbookVessel'
namer = 'Поиск судна по имени, ИМО, РС'
allIDs = []
for country in countrys:
#country = countrys[1]
	print country['name']
	values = { 'gorod_id1':0,'stran_id1':country['id'], 'statgr_id':0, 'pageNav': 1 }
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	result = response.read()
	soup = BeautifulSoup(result, 'html.parser')
	count = 1
	if soup.find('input',{'id':'pageNav'}):
	 	table = soup.findAll("table")[-1]
		count = int(table.findAll("a")[-2].text)
	country['pageCount'] = count

	curIDS = []
	for x in xrange(1,count + 1):
		print 'page ', x
		values = { 'gorod_id1':0,'stran_id1':country['id'], 'statgr_id':0, 'pageNav': x }
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		result = response.read()
		soup = BeautifulSoup(result, 'html.parser')

		imgs = soup.findAll('img')
		for img in imgs:
			if '/ship.png' in img['src']:
				m = re.search('\?fleet_id=(\d+)', img['onclick'])
				curID = int(m.group(1))
				curIDS.append(curID)
	allIDs.extend(curIDS)
	print country['name'], ' pages: ', count, ' ships: ', len(curIDS)

with open('ship_ids.txt', 'w') as f:
    for s in allIDs:
        f.write(str(s) + '\n')