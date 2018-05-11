import timeit
start = timeit.default_timer()

import pandas as pd
import numpy as np
from datetime import date, datetime
import requests
import re
from bs4 import BeautifulSoup
import pandas.io.formats.excel # delete original header formatting
pandas.io.formats.excel.header_style = None
# Pandas Utility Functions #####################################
def flatten(l):
    # flatten list of lists into a list
    lists_of_lists = l
    flattened = [val for sublist in lists_of_lists for val in sublist]
    return flattened
# Apply function - on columns
def noComma1(row):
    return row['Volume'].replace(',','')
def noComma2(row):
    return row['Market Cap'].replace(',','')
def cleanDate(row):
    # removes comma from string 'Date' field casts into date type
    return datetime.strptime(row['Date'].replace(',',''),'%b %d %Y')
# CRYPTO data pull #################################
def parseHTMLTable(soup):
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
def liveCoin():
    # create a dataframe with CURRENT crypto values for top 100
    liveCryptoAPI = 'https://api.coinmarketcap.com/v1/ticker/'
    r = requests.get(liveCryptoAPI)
    meta = r.headers
    returnMeta = pd.DataFrame([meta]).T
    print('converting json to dataframe')
    returnDF = pd.read_json(liveCryptoAPI, orient='records')
    returnDF.set_index('symbol', inplace=True)
    print('saving live coin data')
    return {'df':returnDF, 'meta':returnMeta}
def histCoin(startDate,coinList):
    # create a historical by-day panel with a dateframe for each coin
    # startdate should be YYYYMMDD string
    today = date.today()
    todayString = today.strftime('%Y%m%d')
    returnDFList = []
    for x in coinList:
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
        returnDF['Volume'] = pd.to_numeric(returnDF['Volume'])
        returnDF['Market Cap'] = pd.to_numeric(returnDF['Market Cap'], errors='coerce')
        returnDF['CoinID'] = x
        returnDF = returnDF.set_index(['Date','CoinID'])
        print('saving '+x+ ' historical')
        returnDFList.append(returnDF)
    print('combining all historical')
    returnDFconcat = pd.concat(returnDFList)
    return {'df':returnDFconcat, 'meta':returnMeta}
def writeSimpleExcel(cmcLive, cmcHist):
    writer = pd.ExcelWriter('simpleCryptoOutput.xlsx')
    cmcLive['df'].to_excel(writer, 'live values')
    cmcHist['df'].to_excel(writer, 'hist values')
    cmcLive['meta'].to_excel(writer, sheet_name='API metadata')
    cmcHist['meta'].to_excel(writer, sheet_name='WebScrape metadata')
    writer.save()
    print('simpleCryptoOutput.xlsx')
def applyExcelFormat(writer, live, hist):
    # create formats
    workbook = writer.book
    text_fmt = workbook.add_format({'bold': True, 'text_wrap': True})
    fiat_fmt = workbook.add_format({'num_format': '$#,##0'})
    num_fmt = workbook.add_format({'num_format': '#,##0'})
    fiatDec_fmt = workbook.add_format({'num_format': '$#,###.00'})
    numDec_fmt = workbook.add_format({'num_format': '#,###.000000'})
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

    color_range1 = "I2:I{}".format(num_rows_Live+1)
    color_range2 = "J2:J{}".format(num_rows_Live+1)
    color_range3 = "K2:K{}".format(num_rows_Live+1)
    format1 = workbook.add_format({'bg_color': '#FFC7CE'})
    format2 = workbook.add_format({'bg_color': '#C6EFCE'})
    # Highlight the top 10 values in Green
    worksheet.conditional_format(color_range1, {'type': 'top',
                                               'value': '10',
                                               'format': format2})
    # Highlight the bottom 10 values in Red
    worksheet.conditional_format(color_range1, {'type': 'bottom',
                                               'value': '10',
                                               'format': format1})
    worksheet.conditional_format(color_range2, {'type': 'top',
                                               'value': '10',
                                               'format': format2})
    # Highlight the bottom 10 values in Red
    worksheet.conditional_format(color_range2, {'type': 'bottom',
                                               'value': '10',
                                               'format': format1})
    worksheet.conditional_format(color_range3, {'type': 'top',
                                               'value': '10',
                                               'format': format2})
    # Highlight the bottom 10 values in Red
    worksheet.conditional_format(color_range3, {'type': 'bottom',
                                               'value': '10',
                                               'format': format1})
    # apply format on historical values
    worksheet = writer.sheets[hist]
    worksheet.set_column('C:F', 8, fiatDec_fmt)
    worksheet.set_column('G:H', 14, fiat_fmt)
    worksheet.set_column('A:A', 7, text_fmt)
    worksheet.set_row(0, None, text_fmt)
    worksheet.freeze_panes('A2')
def writeExcel(cmcLive, cmcHist):
    writer = pd.ExcelWriter('CryptoOutput.xlsx', engine='xlsxwriter',datetime_format='mm/dd/yy',
            date_format='mm/dd/yy')
    cmcLive['df'].rename(columns=lambda x: x.replace('_', ' '), inplace=True)
    cmcLive['df'].to_excel(writer, 'live values')
    cmcHist['df'].to_excel(writer, 'hist values')
    cmcLive['meta'].to_excel(writer, sheet_name='API metadata')
    cmcHist['meta'].to_excel(writer, sheet_name='WebScrape metadata')
    num_rows_Live = len(cmcLive['df'].index)
    num_rows_Hist = len(cmcHist['df'].index)
    applyExcelFormat(writer, 'live values', 'hist values')
    writer.save()
    print('CryptoOutput.xlsx')
# main execution ###############################################
# run api pull and save as cmcLive
print('begin live API pull for top 100 coins')
cmcLive = liveCoin()
coinList = cmcLive['df'].id.tolist()
# run webscrape pull and save as cmcLive
hist_start_date = '20140401'
print('begin historical scrape from ',hist_start_date)
cmcHist = histCoin(hist_start_date,coinList)
cmcHist['df'].index
num_rows_Live = len(cmcLive['df'].index)
num_rows_Hist = len(cmcHist['df'].index)
num_coins_Hist = len(coinList)
print('Live values: ',num_rows_Live, ' Coins')
print('Historical values: ',num_rows_Hist, ' Days for ',num_coins_Hist,' Coins')
# create formatted excel workbooks of data
writeSimpleExcel(cmcLive,cmcHist)
writeExcel(cmcLive,cmcHist)
stop = timeit.default_timer()
print(stop-start,' seconds')
