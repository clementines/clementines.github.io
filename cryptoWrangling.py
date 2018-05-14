import timeit #timer library
start = timeit.default_timer() # start timer
import pandas as pd # data munging library
import numpy as np # data munging library
from datetime import date, datetime # date preprocessing library
import requests # web request library
import re # regular expressions
from bs4 import BeautifulSoup # HTML parsing library
from bokeh.io import output_file, show
from bokeh.layouts import column, row, gridplot, layout
from bokeh.plotting import figure
from bokeh.palettes import Viridis3
from bokeh.models import NumeralTickFormatter,LinearColorMapper, BasicTicker, ColorBar, LabelSet
import time
from selenium import webdriver
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
def prior_1h(row):
    return row['price_usd']/((100 - row['percent_change_1h'])/100)
def prior_24h(row):
    return row['price_usd']/((100 - row['percent_change_24h'])/100)
def prior_7d(row):
    return row['price_usd']/((100 - row['percent_change_7d'])/100)
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
def forever(cmcHist): # plotting delta with Bokeh - run every 60 seconds
    print('beginning live chart update every 60 seconds')
    starttime=time.time()
    while True: # run every 60 seconds
        output_file("cryptoBokehCharts.html", title="crypto bokeh graphs")
        newLive = liveCoin()

        # volume graph
        factors = newLive['df'].index.tolist()[0:10]
        x = newLive['df']['24h_volume_usd'].tolist()[0:10]
        factors.reverse()
        x.reverse()
        dot = figure(title="24 Hour Volume for Top 10 Market Cap Coins", tools="hover",
                    y_range=factors, x_range=[0,max(x)])
        dot.segment(0, factors, x, factors, line_width=2, line_color="green", )
        dot.circle(x, factors, size=15, fill_color="orange", line_color="green", line_width=3, )
        # dot.ticker = SingleIntervalTicker(interval=max(x)/5, num_minor_ticks=5)
        dot.xaxis[0].formatter = NumeralTickFormatter(format='($ 0.00 a)')

        # delta graph
        yfactors = newLive['df'].loc[:,'percent_change_1h':'percent_change_7d'][0:10].index.tolist()
        yfactors.reverse()
        xfactors = ['Last Hour','Last 24 Hours','Last 7 Days']
        data = np.flipud(newLive['df'].loc[:,'percent_change_1h':'percent_change_7d'][0:10].values)
        color_mapper = LinearColorMapper(palette="Plasma256", low=np.amin(data), high=np.amax(data))
        plot = figure(title="Percent Change for Top 10 Market Cap Coins", tools="hover",
                x_range=xfactors, y_range=yfactors)
        plot.image(image=[data], color_mapper=color_mapper,
                   dh=[10], dw=[3.0], x=[0], y=[0])
        color_bar = ColorBar(color_mapper=color_mapper, ticker= BasicTicker(),
                             location=(0,0))
        # labels = LabelSet(x=xfactors, y=yfactors, text=yfactors, level='glyph',
        #       x_offset=0, y_offset=0, render_mode='canvas')
        # plot.add_layout(labels)
        plot.add_layout(color_bar, 'right')

        # hist graph
        volAgg = cmcHist['df']['Volume'].groupby('Date').sum()
        timeList = volAgg.index.tolist()
        volList = volAgg.values.tolist()
        # cmcHist['df']['Volume'].unstack()
        #colors = ['#%02x%02x%02x' % (r, g, 150) for r, g in zip(np.floor(50+2*x), np.floor(30+2*y))]
        # hist = figure(title="Historical Values of Top 10 Coins", tools="hover", x_axis_type='datetime', x_range=timeList, y_range=volList)
        hist = figure(title="Historical Total Volume of Top 100 Coins",
                tools="hover, wheel_zoom, pan, lasso_select", x_axis_type='datetime')
        hist.line(timeList, volList, line_color="orange")
        hist.yaxis[0].formatter = NumeralTickFormatter(format='($ 0.00 a)')

        #render graph
        l = layout([
            [plot,dot],
            [hist],
        ], sizing_mode='stretch_both')
        show(l) # open a broweser
        print('charts updated - waiting 60 seconds')

        time.sleep(60.0 - ((time.time() - starttime) % 60.0))
stop = timeit.default_timer()
print(stop-start,' seconds for import and function compile')
# main execution ##############################################################

# run api pull and save as cmcLive
start = timeit.default_timer()
print('begin live API pull for top 100 coins')
cmcLive = liveCoin()
coinList = cmcLive['df'].id.tolist()
topten = coinList[0:10]
stop = timeit.default_timer()
print(stop-start,' seconds for live API pull')

# run webscrape pull and save as cmcHist
start = timeit.default_timer()
hist_start_date = '20140101'
print('begin historical scrape from ',hist_start_date)
cmcHist = histCoin(hist_start_date,coinList)
# cmcHist = histCoin(hist_start_date,topten) # test
stop = timeit.default_timer()
print(stop-start,' seconds for historical scrape from ',hist_start_date)
num_rows_Live = len(cmcLive['df'].index)
num_rows_Hist = len(cmcHist['df'].index)
num_coins_Hist = len(cmcHist['df'].index.get_level_values(1).unique())
num_days_Hist = len(cmcHist['df'].index.get_level_values(0).unique())
print('Live values: ',num_rows_Live, ' Coins')
print('Historical values: ',num_days_Hist, ' Days for ',num_coins_Hist,' Coins')

# testing historical graphs
# num_rows_Hist = len(cmcHist['df'].index)
# num_coins_Hist = len(cmcHist['df'].index.get_level_values(1).unique())
# num_days_Hist = len(cmcHist['df'].index.get_level_values(0).unique())
# cmcHist['df'].index
# cmcHist['df'].columns
# cmcHist['df']['Volume'].head()
# volAgg = cmcHist['df']['Volume'].groupby('Date').sum()
# timeList = volAgg.index.tolist()
# volList = volAgg.values.tolist()
# # cmcHist['df']['Volume'].unstack()
# #colors = ['#%02x%02x%02x' % (r, g, 150) for r, g in zip(np.floor(50+2*x), np.floor(30+2*y))]
#
# # hist graphs
# # hist = figure(title="Historical Values of Top 10 Coins", tools="hover", x_axis_type='datetime', x_range=timeList, y_range=volList)
# hist = figure(title="Historical Volume of Top 10 Coins",
#         tools="hover, wheel_zoom, pan", x_axis_type='datetime')
# hist.line(timeList, volList)
# show(hist)
# create formatted excel workbooks of data
start = timeit.default_timer()
writeSimpleExcel(cmcLive,cmcHist)
writeExcel(cmcLive,cmcHist,'CryptoOutput.xlsx')
stop =print(stop-start,' seconds for writing to excel')

# hit live api, create html charts, open using bokeh.show - every 60 seconds
# use initial run version of historical data in every graph update
forever(cmcHist)

# # testing browser closing
# from subprocess import Popen, check_call
# p1 = Popen('start C:/Users/Yuri/Documents/GitHub/clementines.github.io/cryptoBokehCharts.html',shell=True)
# time.sleep(60)
# for pid in [p1.pid]:
#     check_call(['taskkill', '/F', '/T', '/PID', str(pid)])

# # testing selenium
# print('testing selenium')
# dr = webdriver.Edge()
# dr.get('http://stackoverflow.com/')
# dr.execute_script("$(window.open('http://www.google.com/'))")
# dr.execute_script("$(window.open('http://facebook.com/'))")
# time.sleep(5)
# dr.close()
# dr.switch_to.window(dr.window_handles[-1])
# dr.close()
# dr.switch_to.window(dr.window_handles[-1])
# dr.close()

####  NEXT STEPS #############################################################
## show last 12 months daily values for top 10 coins, append current value

## update live values continuously while spreadsheet is open
    # from openpyxl import Workbook
    # from openpyxl import load_workbook
    # wb = load_workbook('CryptoOutput.xlsx')
    # print(wb.get_sheet_names())
    # ws1 = wb.get_sheet_by_name('live values')
    # ws1
    # ws1['P2'] = 0.00
    # wb.save('CryptoOutput.xlsx')
