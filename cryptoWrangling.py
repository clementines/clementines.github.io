import timeit #timer library
start = timeit.default_timer() # start timer
import pandas as pd # data munging library
import numpy as np # data munging library
from datetime import date, datetime # date preprocessing library
import requests # web request library
import re # regular expressions
from bs4 import BeautifulSoup # HTML parsing library
import pandas.io.formats.excel # expose defaults for excel output headers
pandas.io.formats.excel.header_style = None # delete original header formatting

# Parsing Functions ###########################################################
def parseHTMLTable(soup): # extract dataframe info from soupified HTML
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
    return pd.DataFrame(returnRows, columns=returnHeaders)

# Transformation and Formatting Functions #####################################
def flatten(l): # flatten list of lists into a list
    lists_of_lists = l
    flattened = [val for sublist in lists_of_lists for val in sublist]
    return flattened
def noComma1(row): # remove comma from column 'Volume'
    return row['Volume'].replace(',','')
def noComma2(row): # remove comma from column 'Market Cap'
    return row['Market Cap'].replace(',','')
def cleanDate(row): # remove comma from string 'Date' field - cast as Date
    return datetime.strptime(row['Date'].replace(',',''),'%b %d %Y')
def applyExcelFormat(writer, live, hist, n_rows_live, n_rows_hist): # add and
        # apply formats to excel
    # create formats
    workbook = writer.book
    text_fmt = workbook.add_format({'bold': True, 'text_wrap': True})
    fiat_fmt = workbook.add_format({'num_format': '$#,##0'})
    num_fmt = workbook.add_format({'num_format': '#,##0'})
    fiatDec_fmt = workbook.add_format({'num_format': '$#,###.00'})
    numDec_fmt = workbook.add_format({'num_format': '#,###.000000'})
    low = workbook.add_format({'bg_color': '#FFC7CE'})
    high = workbook.add_format({'bg_color': '#C6EFCE'})
    # apply format on live values
    worksheet = writer.sheets[live]
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
    # sequential conditional formatting on live values
    delta_short = "I2:I{}".format(n_rows_live+1) # identify 1h column
    delta_med = "J2:J{}".format(n_rows_live+1) # identify 24h column
    delta_high = "K2:K{}".format(n_rows_live+1) # identify 7d column
    delta_list = [delta_short, delta_med, delta_high]
    for x in delta_list:
        worksheet.conditional_format(x, {'type': 'top',
                                        'value': '10',
                                        'format': high})
        worksheet.conditional_format(x, {'type': 'bottom',
                                        'value': '10',
                                        'format': low})
    # apply format on historical values
    worksheet = writer.sheets[hist]
    worksheet.set_column('C:F', 10, fiatDec_fmt)
    worksheet.set_column('G:H', 16, fiat_fmt)
    worksheet.set_column('A:A', 8, text_fmt)
    worksheet.set_column('B:B', 22, text_fmt)
    worksheet.set_row(0, None, text_fmt)
    worksheet.freeze_panes('A2')

# Publishing functions ########################################################
def writeSimpleExcel(cmcLive, cmcHist): # write unformatted excel to file
    writer = pd.ExcelWriter('simpleCryptoOutput.xlsx')
    cmcLive['df'].to_excel(writer, 'live values')
    cmcHist['df'].to_excel(writer, 'hist values')
    cmcLive['meta'].to_excel(writer, sheet_name='API metadata')
    cmcHist['meta'].to_excel(writer, sheet_name='WebScrape metadata')
    writer.save()
    print('simpleCryptoOutput.xlsx')
def writeExcel(cmcLive, cmcHist, file): # write formatted excel to file
    writer = pd.ExcelWriter(file, engine='xlsxwriter'
            ,datetime_format='mm/dd/yy',date_format='mm/dd/yy')
    cmcLive['df'].rename(columns=lambda x: x.replace('_', ' '), inplace=True)
    cmcLive['df'].to_excel(writer, 'live values')
    cmcHist['df'].to_excel(writer, 'hist values')
    cmcLive['meta'].to_excel(writer, sheet_name='API metadata')
    cmcHist['meta'].to_excel(writer, sheet_name='WebScrape metadata')
    num_rows_Live = len(cmcLive['df'].index)
    num_rows_Hist = len(cmcHist['df'].index)
    applyExcelFormat(writer, 'live values', 'hist values',
        num_rows_Live, num_rows_Hist)
    writer.save()
    print(file)

# Domain specific build wrappers ####### ######################################
def liveCoin(): # dataframe - live crypto values for top 100 market cap
    liveCryptoAPI = 'https://api.coinmarketcap.com/v1/ticker/'
    r = requests.get(liveCryptoAPI)
    meta = r.headers
    returnMeta = pd.DataFrame([meta]).T
    print('converting json to dataframe')
    returnDF = pd.read_json(liveCryptoAPI, orient='records')
    returnDF.set_index('symbol', inplace=True)
    print('saving live coin data')
    return {'df':returnDF, 'meta':returnMeta}
def histCoin(startDate,coinList): # dataframe - daily historical values from
        # startDate for coin ID in coinList ('YYYYMMDD', ['bitcoin','litecoin'])
    today = date.today()
    todayString = today.strftime('%Y%m%d')
    returnDFList = []
    for x in coinList: # run for every coin ID specified
        print('scraping '+x+ ' historical')
        coin_hist_link = 'https://coinmarketcap.com/currencies/'+x+'/historical-data/?start='+startDate+'&end='+todayString
        r = requests.get(coin_hist_link)
        meta = r.headers
        returnMeta = pd.DataFrame([meta]).T
        soup = BeautifulSoup(r.content, 'html.parser')
        returnDF = parseHTMLTable(soup)
        returnDF['Date'] = returnDF.apply(cleanDate, axis=1)
        returnDF['Volume'] = returnDF.apply(noComma1, axis=1)
        returnDF['Market Cap'] = returnDF.apply(noComma2, axis=1)
        returnDF['Open'] = pd.to_numeric(returnDF['Open'])
        returnDF['High'] = pd.to_numeric(returnDF['High'])
        returnDF['Low'] = pd.to_numeric(returnDF['Low'])
        returnDF['Close'] = pd.to_numeric(returnDF['Close'])
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

# main execution ##############################################################
# run api pull and save as cmcLive
print('begin live API pull for top 100 coins')
cmcLive = liveCoin()
coinList = cmcLive['df'].id.tolist()
topten = coinList[0:10]
# run webscrape pull and save as cmcHist
hist_start_date = '20120101'
print('begin historical scrape from ',hist_start_date)
cmcHist = histCoin(hist_start_date,coinList)
num_rows_Live = len(cmcLive['df'].index)
num_rows_Hist = len(cmcHist['df'].index)
num_coins_Hist = len(cmcHist['df'].index.get_level_values(1).unique())
num_days_Hist = len(cmcHist['df'].index.get_level_values(0).unique())
print('Live values: ',num_rows_Live, ' Coins')
print('Historical values: ',num_days_Hist, ' Days for ',num_coins_Hist,' Coins')
# create formatted excel workbooks of data
writeSimpleExcel(cmcLive,cmcHist)
writeExcel(cmcLive,cmcHist,'CryptoOutput.xlsx')
stop = timeit.default_timer()
print(stop-start,' seconds for intialization')

# next steps - update live values continuously while spreadsheet is open
