import requests
from bs4 import BeautifulSoup 
import numpy as np
from pandas import Series, DataFrame
import pandas as pd

base_url = 'http://nb.58.com/luotuo/ershoufang/'
hrefs = []
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
}

def getSrc(page):
	url =  base_url + 'pn' + str(page+1)
	#get html
	while True:
		print('get page %s ...' % page)
		r = requests.get(url, headers=headers)
		print(r.status_code)
		if r.status_code == 200:
			break
			
	# deal with string
	soup = BeautifulSoup(r.content, 'lxml')
	# find ul
	List = soup.find('ul', class_="house-list-wrap")
	#find li
	items = List.find_all('li')
	# find hrefs
	for x in items:
		a = x.find('div', class_='pic').find('a')
		href = a['href']
		hrefs.append(href)

print('start get hrefs...')
for x in range(70):
	getSrc(x)

se = Series(hrefs)
se.to_csv('58_hrefs.csv', index=False)
input('----------------')