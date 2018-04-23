import pandas as pd
import numpy as np
from datetime import date, datetime
import requests
import re
from bs4 import BeautifulSoup
CryptoAPI = 'https://api.coinmarketcap.com/v1/ticker/'
BTC_hist_link = 'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20180401&end=20180416'
r = requests.get(CryptoAPI)
r2 = requests.get(BTC_hist_link)
soup = BeautifulSoup(r2.content, 'html.parser')
soup
r.headers
r2.headers
cmcjson = r.json()
r2.content
testHistRows = soup.find_all('tr')
testHistRows
header = testHistRows[0]
header.contents
headerCol = header.find_all('th')
headerCol
headerCol[0].contents

# create a dataframe with live crypto values for top 100 coin
def resetCoinDF():
    toReturn = pd.read_json(CryptoAPI, orient='records')
    toReturn.set_index('symbol', inplace=True)
    return toReturn
def
# create 4 by 4 matrix with random numbers
def resetDF():
    dates = pd.date_range('20180101', periods=4)
    featureNames = list('ABCD')
    return pd.DataFrame(np.random.randn(4,4), index=dates, columns=featureNames)

df = resetDF()
df
cmc = resetCoinDF()
cmc
cmc.describe()
cmc.dtypes
# to numpy 2-d array
df.values
# axis 1 is column header, descending: ascending=False
df.sort_index(axis=0, ascending=True)
df.sort_index(axis=1, ascending=False)
df.sort_values(by='B')
cmc = cmc.sort_values(by='rank')
cmc
# graph percent_change_7d, percent_change_24h, percent_change_1h (significance hiearchy), order by market_cap_usd

df
# find mean of column A and use it to apply selection
df[df.A > df.mean().loc['A']]
# create zero matrix with same dimensions - using numpy library
dfZero = pd.DataFrame(np.zeros_like(df), index=df.index, columns=df.columns)
dfZero
# selection and setting to create positive matrix - using only pandas library
dfPos = df.copy()
dfdfPos[dfPos<0] = -dfPos
dfPos
# if newy year, multiply a,b,c,d and put it in E
# find index[0]
df.header['2018-01-01']
df.shape
df.shape[0]
df.index
df.index[0]
df[df.index[0]]
df[E] =

df2 = df.copy()
df2
df2['F'] = df2.apply(lambda x: x.max() - x.min())
df2
df2 = df.copy()
df
df2
newCol = []
for row in df.itertuples():
    # if(row.Index.date() == date(2018,1,1)):
    #     df2[row.Index.date(),'F'] = 0
    # else:
    #     df2[row.Index.date(),'F'] = 0
    print("A:",row.A,"B :",row.B,"C :",row.C,"D :",row.D)
    print(row.Index.date().type)
    print(date(2018,1,1))
    if(row.Index.date() == date(2018,1,1)): print("YES")
pd.to_datetime('20180101')
df2.loc[pd.to_datetime('20180101')]

df2.loc['20180101']
df2.index[0]
pd.to_datetime('20180101')
datetime(2018,1,1)
df2


# selection by label

df.loc['20180101']
df.loc['20180101','A']
# selection by position
df.iloc[3]
df.iloc[3,3]

# appending new column
df2 = df.copy()
df2['E'] = ['one', 'two', 'three', 'four']
df
df2.drop('E')
df2
df.apply(lambda x: x.max() - x.min())
df2['F'] = df2.apply(lambda x: x.max() - x.min())

df2
df2Cut = df2[df2['E'].isin(['two','four'])]
df
df.apply(np.cumsum)
df.apply(lambda x: x.max() - x.min()).values
