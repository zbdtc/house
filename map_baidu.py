import json
import re
import requests
import pandas as pd
from pandas import DataFrame, Series
from urllib.request import urlopen, quote

def getlnglat(address):
	url='http://api.map.baidu.com/geocoder/v2/'
	output='json'
	ak='jwCUNZdjyO1SD30wpXf4im1perPncyPE'
	add = quote('镇海' + address)
	city = quote('宁波')
	uri = url + '?' + 'address=' + add + '&city=' + city + '&output=' + output + '&ak=' + ak
	rs =requests.get(uri)
	print(rs.status_code)
	res = rs.content.decode()
	temp = json.loads(res)
	return temp

def outlierFilter(df):
	df_des = df.describe()
	q1 = df_des.at['25%','avg']
	q2 = df_des.at['50%','avg']
	q3 = df_des.at['75%','avg']
	IQR = q3-q1
	UpperLimit = q3 + 1.5*IQR
	LowerLimit = q1 - 1.5*IQR
	return df[df.avg.between(LowerLimit, UpperLimit)]

df = pd.read_csv('house.csv',index_col=0)
df = df.applymap(lambda x: x.strip())
df = df[df['ageLimit']=='70年']
regex = re.compile(r'\d+')
df.avg = df.avg.map(lambda x: regex.findall(x)[0]).astype(int)
df_commuity = df[['community', 'avg']]
df_commuity = df_commuity.groupby('community').apply(outlierFilter)
df_mean = df_commuity.mean(level='community')

points = []
for index, row in df_mean.iterrows():
	temp = getlnglat(index)
	lng = temp['result']['location']['lng']
	lat = temp['result']['location']['lat']
	count = row.avg /100
	points.append({
		'lng': lng,
		'lat': lat,
		'count': count
	})


df_points = DataFrame(points)

df_points.to_csv('points.csv')