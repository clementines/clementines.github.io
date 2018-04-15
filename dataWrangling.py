import pandas as pd
import numpy as np
import requests
import re
CryptoAPI = 'https://api.coinmarketcap.com/v1/ticker/'
r = requests.get(CryptoAPI)
r.headers
cmcjson = r.json()

# create 4 by 4 matrix with random numbers
def resetCoinDF():
    toReturn = pd.read_json(CryptoAPI, orient='records')
    toReturn.set_index('symbol', inplace=True)
    return toReturn
def resetDF():
    dates = pd.date_range('20180101', periods=4)
    featureNames = list('ABCD')
    return pd.DataFrame(np.random.randn(4,4), index=dates, columns=featureNames)

df = resetDF()
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


# find mean of column A and use it to apply selection
df[df.A > df.mean().loc['A']]
# create zero matrix with same dimensions - using numpy library
dfZero = pd.DataFrame(np.zeros_like(df), index=df.index, columns=df.columns)
dfZero
# selection and setting to create positive matrix - using only pandas library
dfPos = df.copy()
dfPos[dfPos<0] = -dfPos
dfPos
# selection by label
df.loc['20180101']
df.loc['20180101','A']
# selection by position
df.iloc[3]
df.iloc[3,3]
df2 = df.copy()
# appending new column
df2['E'] = ['one', 'two', 'three', 'four']
df
df2.drop('E')
df2
df.apply(lambda x: x.max() - x.min())
df2['F'] = df2.apply(lambda x: x.max() - x.min()).

df2
df2Cut = df2[df2['E'].isin(['two','four'])]
df
df.apply(np.cumsum)
df.apply(lambda x: x.max() - x.min()).values
