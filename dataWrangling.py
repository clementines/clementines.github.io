import pandas as pd
import numpy as np
from datetime import date, datetime
import requests
import re
from bs4 import BeautifulSoup
# CRYPTO data pull #################################
# flatten list of lists into a list
def flatten(l):
    lists_of_lists = l
    flattened = [val for sublist in lists_of_lists for val in sublist]
    return flattened
# create a dataframe with CURRENT crypto values for top 100
def liveCoin():
    liveCryptoAPI = 'https://api.coinmarketcap.com/v1/ticker/'
    r = requests.get(liveCryptoAPI)
    meta = r.headers
    returnMeta = pd.DataFrame([meta]).T
    returnDF = pd.read_json(liveCryptoAPI, orient='records')
    returnDF.set_index('symbol', inplace=True)
    return {'df':returnDF, 'meta':returnMeta}
# create a historical by-day panel with a dateframe for each coin
# startdate should by YYYYMMDD string
def histCoin(startDate):
    today = date.today()
    todayString = today.strftime('%Y%m%d')
    BTC_hist_link = 'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start='+startDate+'&end='+todayString
    r = requests.get(BTC_hist_link)
    meta = r.headers
    returnMeta = pd.DataFrame([meta]).T
    soup = BeautifulSoup(r.content, 'html.parser')
    histTableHTML = soup.find_all('tr')
    headerHTML = histTableHTML[0]
    headerColHTML = headerHTML.find_all('th')
    returnHeaders = []
    for x in headerColHTML:
        returnHeaders.append(x.contents)
    returnHeaders = flatten(returnHeaders)
    numRows = len(histTableHTML)
    rowsHTML = histTableHTML[1:numRows]
    returnRows = []
    for x in rowsHTML:
        cols = []
        colsHTML = x.find_all('td')
        for y in x.find_all('td'):
            cols.append(y.contents)
        colsFlatten = flatten(cols)
        returnRows.append(colsFlatten)
    returnDF = pd.DataFrame(returnRows, columns=returnHeaders)
    def cleanDate(row):
        return datetime.strptime(row['Date'].replace(',',''),'%b %d %Y')
    returnDF['Date'] = returnDF.apply(cleanDate, axis=1)
    returnDF = returnDF.set_index('Date')
    return {'df':returnDF, 'meta':returnMeta}
# main execution
cmcLive = liveCoin()
cmcLive['df']
cmcHist = histCoin('20140101')
cmcHist['df'].dtypes
workingDF = cmcHist['df']

writer = pd.ExcelWriter('cryptoOutput.xlsx')
cmcLive['df'].to_excel(writer, 'live')
cmcHist['df'].to_excel(writer, 'hist')
cmcLive['meta'].to_excel(writer, 'liveMeta')
cmcHist['meta'].to_excel(writer, 'histMeta')
writer.save()

cmcLive['df'].describe()
cmcLive['df'].dtypes
cmcHist['df'].describe()
cmcHist['df'].dtypes

# PANDAS MISC #################################
# create 4 by 4 matrix with random numbers
def randTSDF():
    dates = pd.date_range('20180101', periods=4)
    featureNames = list('ABCD')
    return pd.DataFrame(np.random.randn(4,4), index=dates, columns=featureNames)

# to numpy 2-d array
df = randTSDF()
df
df.index
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
