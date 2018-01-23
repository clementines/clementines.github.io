import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#
page = requests.get("https://finance.yahoo.com/cryptocurrencies/")
page
page.status_code
#page.content
soup = BeautifulSoup(page.content, 'html.parser')
allTables = soup.find_all('tbody')
print(len(allTables))
# for index in allTables:
#     print(index)
mainTable = allTables[0]
#print(mainTable.prettify())
mainRows = mainTable.find_all('tr')
print(len(mainRows))
firstRow = mainRows[0]
print(firstRow)
rowColumns = firstRow.find_all('td')
print(len(rowColumns))
firstRow_firstColumn = rowColumns[0]
firstRow_secondColumn = rowColumns[1] .contents
print(firstRow_secondColumn)
firstRow_thirdColumn = rowColumns[2].span.contents[1]
print(firstRow_thirdColumn)
rowTitle = []
rowValue = []
rowChange = []
for row in mainTable.children:
    rowCols = row.find_all('td')
    rowTitle.append(rowCols[1].contents[0])
    rowValue.append(rowCols[2].span.contents[1])
    rowChange.append(rowCols[3].find_all('span'))

print(rowTitle[0])
print(rowValue[0])
print(rowTitle[1])
print(rowValue[1])

cryptoDF = pd.DataFrame(rowValue, index = rowTitle)
print(cryptoDF)

# DEVELOPMENT BELOW
# # not able to pull content systematically - not handling list pointer correectly


print(rowTitle[0])
print(rowValue[0])
# print(rowChange[0])
# print(rowChange[0][0])
# print(rowChange[0][0].contents[1])
print(str(rowChange[0][0].contents[1]))

print(rowTitle[1])
print(rowValue[1])
# print(rowChange[1])
# print(rowChange[1][0])
# print(rowChange[1][0].contents[4])
print(str(rowChange[1][0].contents[1]) + str(rowChange[1][0].contents[4]))
realRowChange = []
for index in range(len(mainRows)):
    if(len(rowChange[0][0].contents) > 4):
        realRowChange.append(str(rowChange[index][0].contents[1]) + str(rowChange[index][0].contents[4]))
    else:
        realRowChange.append(str(rowChange[index][0].contents[1]))

print(rowTitle[0])
print(rowValue[0])
print(str(rowChange[0][0].contents[1]) + str(rowChange[0][0].contents[4]))
print(realRowChange[0])

print(rowTitle[1])
print(rowValue[1])
print(str(rowChange[1][0].contents[1]) + str(rowChange[1][0].contents[4]))
print(realRowChange[1])
for index in range(len(mainRows)):
    print(len(rowChange[index]))



rowChange[0][0].contents[4]
len(rowChange[1][0].contents

len(rowChange)
##############################
cryptoValDF = pd.DataFrame(rowValue, index = rowTitle)
cryptoChaDF = pd.DataFrame(rowChange, index = rowTitle)
cryptoValDF
cryptoChaDF
