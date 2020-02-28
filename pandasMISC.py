import pandas as pd # data munging library
import numpy as np # data munging library
from datetime import date, datetime # date preprocessing library

# PANDAS MISC #################################
# create 4 by 4 matrix with random numbers
def randTSDF():
    dates = pd.date_range('20180101', periods=4)
    featureNames = list('ABCD')
    return pd.DataFrame(np.random.randn(4,4), index=dates, columns=featureNames)

# to numpy 2-d array
df = randTSDF()
df
print(df)
df.index
df.values
df.shape
# axis 1 is column header, descending: ascending=False
df.sort_index(axis=0, ascending=True)
df.sort_index(axis=1, ascending=False)
df.sort_values(by='B')

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

#############################cryptoWrangling.py MISC###########################################

returnDF.dtypes

returnDF['isDate'] = None
for index, row in returnDF.iterrows():
    try:
        row['isDate'] = True
        datetime.strptime(row['Date'].replace(',',''),'%b %d %Y')
    except ValueError:
      	row['isDate'] = False
    print (row['Date'], row['isDate'])

returnDF = returnDF[returnDF['isDate'] == True]
returnDF.drop('isDate', axis=1, inplace=True)
returnDF.head()
returnDF.tail()

returnDFList
returnDFList.tail()

coinList
topten

#############################cryptoWrangling.py DEBUG###########################################

cmcHist = histCoin(hist_start_date,topten)

topone = []
topone.append(topten[0])

today = date.today()
todayString = today.strftime('%Y%m%d')
returnDFList = []
for x in topone: # run for every coin ID specified 
    print('scraping '+x+ ' historical')
    coin_hist_link = 'https://coinmarketcap.com/currencies/'+x+'/historical-data/?start='+hist_start_date+'&end='+todayString
    r = requests.get(coin_hist_link)
    meta = r.headers
    returnMeta = pd.DataFrame([meta]).T
    soup = BeautifulSoup(r.content, 'html.parser')
    returnDF = parseHTMLTable(soup)
    returnDF['isDate'] = None
    print(returnDF.describe())
    print(returnDF.dtypes)
    for index, row in returnDF.iterrows():
        try:
            row['isDate'] = True
            # datetime.strptime(row['Date'].replace(',',''),'%b %d %Y')
            datetime.strptime(row['Date'],'%b %d %Y')
            print(datetime.strptime(row['Date'],'%b %d %Y'))
        except TypeError:
            row['isDate'] = False
        print(row['Date'], row['isDate'])
        
    # returnDF[returnDF['isDate'] == True]
    returnDF = returnDF[returnDF['isDate'] == True]
    returnDF.drop('isDate', axis=1, inplace=True)
    returnDF['Date'] = returnDF.apply(noComma3, axis=1)
    returnDF['Date'] = returnDF.apply(cleanDate, axis=1)
    returnDF['Volume'] = returnDF.apply(noComma1, axis=1)
    returnDF['Market Cap'] = returnDF.apply(noComma2, axis=1)
    returnDF['Open'] = pd.to_numeric(returnDF['Open*'])
    returnDF['High'] = pd.to_numeric(returnDF['High'])
    returnDF['Low'] = pd.to_numeric(returnDF['Low'])
    returnDF['Close'] = pd.to_numeric(returnDF['Close**'])
    returnDF['Volume'] = pd.to_numeric(returnDF['Volume'], errors='coerce')
    returnDF['Market Cap'] = pd.to_numeric(returnDF['Market Cap'], errors='coerce')
    returnDF['CoinID'] = x
    returnDF = returnDF.set_index(['Date','CoinID'])
    print('saving '+x+ ' historical')
    returnDFList.append(returnDF)
print('combining all historical')
returnDFconcat = pd.concat(returnDFList) # combine all dataframes into one
returnDFconcat = returnDFconcat.reset_index().sort_values(by=['Date','Market Cap'], ascending=[False, False])
returnDFconcat = returnDFconcat.set_index(['Date','CoinID'])
return {'df':returnDFconcat, 'meta':returnMeta}

