from pandas import Series, DataFrame
import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup 

import time
import random

hrefs = pd.read_csv('58_hrefs.csv',header=None)
page = 1

# header = {
# 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
# 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
# 'Accept-Encoding': 'gzip, deflate',
# 'Cookie': 'userid360_xml=3C888359D4B9915A373946CA18F7E363; time_create=1528637215649; f=n; id58=N3yVgFdhXsBcNroRlqyrzg==; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1519386110,1519386172; 58tj_uuid=4e5304c7-9e0f-4c99-a038-0e9b6fd54733; new_uv=10; gr_user_id=71264283-c2e9-445c-9951-c2cc081abbae; wmda_uuid=c9c6f651513986cbb4a1bbc49ec57ea8; wmda_new_uuid=1; wmda_visited_projects=%3B1409632296065%3B2385390625025; bdshare_firstime=1519386115681; _ga=GA1.2.577129268.1519386120; xxzl_deviceid=aN12OH9jlCqJroACl%2BaYwcS%2F3gcVL0M%2B6H9c44idK0oUKkjUqXGSD7zo%2F%2F%2BsN9bA; 58home=nb; city=nb; als=0; commontopbar_myfeet_tooltip=end; XQH=%7B%22w%22%3A%5B%7B%22id%22%3A%22309040%22%2C%22t%22%3A1526046484751%7D%5D%7D; Hm_lvt_ae019ebe194212c4486d09f377276a77=1526046502; __utma=253535702.577129268.1519386120.1526046504.1526046504.1; __utmz=253535702.1526046504.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); myfeet_tooltip=end; new_session=0; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253D-YXWatiwNT65X81NcQyWRgSrWf49Iul8Vlvn852txCC%2526wd%253D%2526eqid%253Df8bde04200018e3f000000045af902db; commontopbar_new_city_info=135%7C%E5%AE%81%E6%B3%A2%7Cnb; commontopbar_ipcity=hz%7C%E6%9D%AD%E5%B7%9E%7C0; f=n; ppStore_fingerprint=5D5D86DE9F1B23C4729F2E6F1C45959E4C06CB33B9BAFF69%EF%BC%BF1526269359410',
# 'Upgrade-Insecure-Requests': '1',
# 'Connection': 'keep-alive'
# }

def getPage(url):
	global page
	try:
		while True:
			print('get page %d...' % (page))
			r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'})
			print(r.status_code)
			if r.status_code == 200:
				page = page+1
				break		
			else:
				time.sleep(random.uniform(0,5))
	except Exception as e:
		print('err', e)

	soup = BeautifulSoup(r.content, 'lxml')
	return soup

def getDetial(soup, url):
	row = {}

	house_title = soup.find('div', class_='house-title')
	row['title'] = house_title.find('h1', class_='c_333 f20').text
	row['tag'] = list(map(lambda x: x.text, house_title.select('span')))
	row['sum'] = soup.find('span', class_='price').text
	row['avg'] = soup.find('span', class_='unit').text

	general_situation = soup.find('div', id="generalSituation").select('li')
	row['type'] = general_situation[1].contents[1].text
	row['area'] = general_situation[2].contents[1].text
	row['floor'] = general_situation[4].contents[1].text
	row['decoration'] = general_situation[5].contents[2].text
	row['ageLimit'] = general_situation[6].contents[1].text
	row['years'] = soup.find('div', class_="house-basic-item2").find_all('span')[5].text

	basic_item3 = soup.find('ul', class_='house-basic-item3')
	row['community'] = basic_item3.contents[1].contents[3].contents[1].text.strip()
	row['street'] = basic_item3.contents[1].contents[3].contents[3].text
	row['district'] = basic_item3.contents[3].contents[3].contents[1].text
	row['address'] = basic_item3.contents[3].contents[3].contents[3].text
	row['url'] = url
	return row

def Crawler(url):
	soup = getPage(url)
	try:
		row = getDetial(soup, url)
		return row
	except Exception as e:
		print('err!')
		print('reason', e)

List = []



hrefs[0].map(lambda x: List.append(Crawler(x)))

df = DataFrame(list(filter(None,List)))

df.to_csv('house.csv')


# print(hrefs[28:50])


