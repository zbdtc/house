import pandas as pd
from pandas import DataFrame, Series

df = pd.read_csv('points.csv', index_col=0, header=0)
df['count'] = df['count'].map(lambda x: x-50)
df = df[['lng', 'lat', 'count']]

js = df.to_dict(orient='records')

for x in js:
	print(x)