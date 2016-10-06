#import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
import pytz
from pytz import timezone
import numpy as np
import Central
import pandas as pd
from pandas_datareader import data as web
import networkx as nx
import urllib2
from bs4 import BeautifulSoup

print
print 'DIVISIVE CLUSTERING FOR DOW JONES '
print

##############################################################
# Enter the dates between which to examine the stocks
print 'DATES'
while True:
    print 'Enter a starting date for the analysis:'
    y = raw_input('Year: ')
    m = raw_input('Month: ')
    d = raw_input('Day: ')
    print 'For the ending date:'
    f = raw_input('How many days into the future: ')
    try:
        start = datetime.datetime(int(y),int(m),int(d), 0, 0, 0, 0, pytz.utc)
        end = start + datetime.timedelta(days=int(f))
        if end < start:# > end or end > datetime.datetime.now():
            print 
            print 'Please enter a valid range of dates'
            continue
        break
    except:
        print
        print 'Please enter a valid range of dates'
print

#######################################################################
print 'How many times would you like to run the divisive process?'
while True:
    num = raw_input('Please enter an integer between 1 and 4: ')
    try:
        num = int(num)
        if num < 1 or num > 4:
            print 'You must enter an integer in the appropriate range'
            continue
        break
    except: 
        print 'You must enter an integer in the appropriate range'
print     
#start = datetime.datetime(2016, 5, 2)
#end = start+ datetime.timedelta(days=8)
#######################################################################
# Get a list of companies in the Dow Jones Index
def ScrapeList():
    site = "http://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site, headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page,"lxml")
    table = soup.find('table', {'class': 'wikitable sortable'})
    Symbols = []
    for row in table.findAll('tr'):
        col = row.findAll('td')
        if len(col) > 0:
            ticker = str(col[2].string.strip())
            Symbols.append(ticker)
    return Symbols

Tickers = ScrapeList()

import Data
VolReturns = Data.Data(Tickers,start,end)


def C(Tickers,start,end,DivNum):
    if DivNum == 0:
        return Tickers
    else:
        Temp = Central.Cluster(Tickers,start,end,2)
        A = C(Temp[0],start,end,DivNum-1)
        B = C(Temp[1],start,end,DivNum-1)
        return [A,B]

L = C(Tickers,start,end,num)

  
print 'AFTER THE FIRST STEP:'
print L[0][0][0] + L[0][0][1] + L[0][1][0] + L[0][1][1]
print L[1][0][0] + L[1][0][1] + L[1][1][0] + L[1][1][1]
print
print 'AFTER THE SECOND STEP'
print L[0][0][0] + L[0][0][1]
print L[0][1][0] + L[0][1][1]
print L[1][0][0] + L[1][0][1]
print L[1][1][0] + L[1][1][1]
print
print 'AFTER THE THIRD STEP'
print L[0][0][0] 
print L[0][0][1]
print L[0][1][0]
print L[0][1][1]
print L[1][0][0]
print L[1][0][1]
print L[1][1][0]
print L[1][1][1]



 
 
 
 
#print 'AFTER THE FIRST STEP:'
#print L[0][0] + L[0][1]
#print L[1][0] + L[1][1]
#print
#print 'AFTER THE SECOND STEP'
#print L[0][0] 
#print L[0][1]
#print L[1][0]
#print L[1][1]


exit()
Rep = []
for ticker in Tickers:
    if ticker in L[0][0]:
        Rep.append(0)
    if ticker in L[0][1]:
        Rep.append(1)
    if ticker in L[1][0]:
        Rep.append(2)
    if ticker in L[1][1]:
        Rep.append(3)




###############################
# Visualization 
print 'VISUALIZATION'
print 'Would you like to see a visualization of the data?'
VisChoiceA = raw_input('Enter Y for yes or anything else for no: ')
if VisChoiceA != 'Y':
    print 'Goodbye'
    exit()
else:
    print 'Would you like to see the data represented in 2D, 3D or both?'
    while True:
        VisChoice2 = raw_input('Enter 2D, 3D or both: ')
        if VisChoice2 != '2D' and VisChoice2 != '3D' and VisChoice2 != 'both':
            print 'Enter 2D, 3D or both: '
            continue
        break
print
import DataVis2
DataVis2.Representation(VisChoice2,Rep,VolReturns)


