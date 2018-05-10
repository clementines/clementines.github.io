import pandas as pd
import numpy as np
from datetime import date, datetime
import requests
import re
from bs4 import BeautifulSoup
import pandas.io.formats.excel

# Pandas Utility Functions #####################################
def flatten(l):
    # flatten list of lists into a list
    lists_of_lists = l
    flattened = [val for sublist in lists_of_lists for val in sublist]
    return flattened
# Apply function - on columns
def cleanDate(row):
    # removes comma from string 'Date' field casts into date type
    return datetime.strptime(row['Date'].replace(',',''),'%b %d %Y')
# CRYPTO data pull #################################
def liveCoin():
    # create a dataframe with CURRENT crypto values for top 100
    liveCryptoAPI = 'https://api.coinmarketcap.com/v1/ticker/'
    r = requests.get(liveCryptoAPI)
    meta = r.headers
    returnMeta = pd.DataFrame([meta]).T
    returnDF = pd.read_json(liveCryptoAPI, orient='records')
    returnDF.set_index('symbol', inplace=True)
    return {'df':returnDF, 'meta':returnMeta}
def histCoin(startDate):
    # create a historical by-day panel with a dateframe for each coin
    # startdate should by YYYYMMDD string
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
    returnDF['Date'] = returnDF.apply(cleanDate, axis=1)
    returnDF = returnDF.set_index('Date')
    return {'df':returnDF, 'meta':returnMeta}
# main execution ###############################################
cmcLive = liveCoin()
cmcLive['df']
cmcHist = histCoin('20140101')
cmcHist['df']

writerSimple = pd.ExcelWriter('simpleCryptoOutput.xlsx')
cmcLive['df'].to_excel(writerSimple, 'live')
cmcHist['df'].to_excel(writerSimple, 'hist')
cmcLive['meta'].to_excel(writerSimple, 'liveMeta')
cmcHist['meta'].to_excel(writerSimple, 'histMeta')
writerSimple.save()

pandas.io.formats.excel.header_style = None
writerFancy = pd.ExcelWriter('fancyCryptoOutput.xlsx', engine='xlsxwriter',datetime_format='mm/dd/yy',
        date_format='mm/dd/yy')
cmcLive['df'].rename(columns=lambda x: x.replace('_', ' '), inplace=True)
cmcLive['df'].to_excel(writerFancy, 'live')
cmcHist['df'].to_excel(writerFancy, 'hist')
cmcLive['meta'].to_excel(writerFancy, 'liveMeta')
cmcHist['meta'].to_excel(writerFancy, 'histMeta')
workbook = writerFancy.book
text_fmt = workbook.add_format({'bold': True, 'text_wrap': True})
fiat_fmt = workbook.add_format({'num_format': '$#,##0'})
num_fmt = workbook.add_format({'num_format': '#,##0'})
fiatDec_fmt = workbook.add_format({'num_format': '$#,###.00'})
numDec_fmt = workbook.add_format({'num_format': '#,###.000000'})
worksheet = writerFancy.sheets['live']
worksheet.set_column('B:B', 15, fiat_fmt)
worksheet.set_column('C:C', 16, num_fmt)
worksheet.set_column('F:F', 17, fiat_fmt)
worksheet.set_column('G:G', 18, num_fmt)
worksheet.set_column('H:H', 20)
worksheet.set_column('L:L', 8, numDec_fmt)
worksheet.set_column('M:M', 9, fiatDec_fmt)
worksheet.set_column('O:O', 18, num_fmt)
worksheet.set_column('A:A', 7, text_fmt)
worksheet.set_row(0, None, text_fmt)
worksheet.freeze_panes('A2')
worksheet = writerFancy.sheets['hist']
worksheet.set_column('B:E', 8, fiatDec_fmt)
worksheet.set_column('F:G', 14, fiat_fmt)
worksheet.set_column('A:A', 7, text_fmt)
worksheet.set_row(0, None, text_fmt)
worksheet.freeze_panes('A2')
writerFancy.save()

# dateFormat = workbook.add_format({'num_format': 'dd/mm/yy'})
# worksheet.write('A2', number, format2)       # 28/02/13




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
