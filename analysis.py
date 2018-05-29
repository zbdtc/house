from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.gridspec as gridspec

#set font
matplotlib.rcParams['font.family'] = 'SimHei'

#get data from csv
df = pd.read_csv('house.csv',index_col=0)

#compiled regex
regex_n = re.compile(r'\d+')
regex_s = re.compile(r'\w期$')

#cleaning data
df = df[df['ageLimit']=='70年']
df['floor'] = df['floor'].map(lambda x: x.split('/')[0])
df = df.applymap(lambda x: x.strip())
for x in ['avg', 'sum', 'area']:
	df[x] = df[x].map(lambda x: regex_n.findall(x)[0])
df[['avg', 'sum', 'area']] = df[['avg', 'sum', 'area']].astype(int)
df['community'] = df['community'].map(lambda x: regex_s.sub('', x) )

df_avg = df[['community', 'avg']]
#sort index by count of house and select witch more than 10
df_count  = df_avg.groupby('community').count().sort_values('avg')
index = df_count[df_count['avg']>10].index

#create figure
# fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(25.4,13))
# fig.set_facecolor('None')


#fig1
fig1, axe1 = plt.subplots(nrows=1, ncols=1, figsize=(25.4,8))
df_box = df_avg.reset_index().\
	set_index(['community', 'index']).\
	unstack(0).stack(0).\
	reindex(columns=index)
bp = df_box.boxplot(return_type='dict',
	rot=60,
	ax = axe1,
	meanline=True,
	showmeans=True,
	meanprops=dict(
		linewidth=1,
		color='purple'
	)
)
axe1.set_title('price boxplot')
axe1.set_axisbelow(True)
axe1.set_ylabel("average price")
axe1.set_xlabel('community')
axe1.set_ylim(6000,25000)
axe1.set_yticks(np.arange(6000,25000,1000))
axe1.yaxis.grid(True, color='lightgrey', alpha=0.5)
axe1.xaxis.grid(False)

plt.subplots_adjust(
	left=0.05,
	bottom=0.23,
	right=0.98,
	top=0.95,
	wspace=0.13,
	hspace=0.45
)


#fig2
fig2, axe2 = plt.subplots(nrows=1, ncols=1, figsize=(25.4,8))
bar = df_avg.groupby('community').mean().sort_values('avg')[-10:].plot.barh(
	# y=0,
	ax=axe2,
	color='darkgrey',

)
axe2.set_title('Average price of community top10')
axe2.set_xlim(15000,20000)
axe2.set_xticks(np.arange(15000,20500,500))
axe2.set_xlabel('average price')

#fig3
fig3, axe3 = plt.subplots(
	nrows=1, ncols=2, figsize=(25.4,8),
	sharex=True, sharey=True
)
plt.xticks(np.arange(len(index)),list(index))
plt.xlabel('community')
plt.subplots_adjust(
	left=0.05,
	bottom=0.23,
	right=0.98,
	top=0.95,
	wspace=0,
	hspace=0.45
)
def outlierFilter(df):
	df_des = df.describe()
	q1 = df_des.at['25%','avg']
	q2 = df_des.at['50%','avg']
	q3 = df_des.at['75%','avg']
	IQR = q3-q1
	UpperLimit = q3 + 1.5*IQR
	LowerLimit = q1 - 1.5*IQR
	return df[df.avg.between(LowerLimit, UpperLimit)]
##size
df['size'] = df['area'].map(lambda x: 'smlall' if(x<100) else 'big')
df_size = df[['community', 'size', 'avg']]
df_size = df_size.groupby('community', as_index=False).apply(outlierFilter)
df_size = df_size.groupby(['community', 'size']).mean()
df_size = df_size.unstack().reindex(index)['avg']
df_size.plot.line(
	marker='o',
	linestyle='',
	rot=90,
	ax=axe3[0]
)
axe3[0].set_title('size')
##floor
df_floor = df[['community', 'floor', 'avg']]
df_floor = df_floor.groupby('community', as_index=False).apply(outlierFilter)
df_floor = df_floor.groupby(['community', 'floor']).mean()
df_floor = df_floor.unstack().reindex(index)['avg'][['高层', '中层', '低层']]

df_floor.plot.line(
	ax=axe3[1],
	marker='o',
	linestyle='',
	rot=90
)
axe3[1].set_title('floor')

#fig4
fig4 = plt.figure(figsize=(25.4,8))
gs = gridspec.GridSpec(2,2) 
axe4=[]
axe4.append(plt.subplot(gs[0,0]))
axe4.append(plt.subplot(gs[0,1]))
axe4.append(plt.subplot(gs[1,:]))
##count
pie = df_count[-10:].plot.pie(
	ax=axe4[0],
	subplots=True,
	autopct='%1.1f%%',
	explode=(0,0,0,0,0,0,0,0,0.05,0.1),
	shadow=True
)
axe4[0].set_title('proportion of community top10')
axe4[0].set_ylabel('')
##floor
pie2 = df['avg'].groupby(df['floor']).count().reindex(['高层', '中层', '低层']).sort_values(0).plot.pie(
	ax=axe4[1],
	autopct='%1.1f%%',
	shadow=True,
	explode=(0,0,0.07)
)
axe4[1].set_title('proportion of floor')
axe4[1].set_ylabel('')
##area
hist = df[df['area']<=200]['area'].plot.hist(
	ax=axe4[2],
	bins=17,
	# color='darkgrey',
	edgecolor='#E6E6E6',
	color='#EE6666',
	alpha=0.7
)
axe4[2].set_title("count of area")
axe4[2].set_xlim(30,200)
axe4[2].set_xticks(np.arange(30,200,10))
axe4[2].set_facecolor('#E6E6E6')
axe4[2].set_xlabel('area')
axe4[2].set_xlabel('count')


plt.show()