import pandas as pd
from pandas_datareader import data as web
import numpy as np
import urllib2
from datetime import datetime
import pytz
from bs4 import BeautifulSoup


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
###################################   
# Get a list of the historic adjust closing prices over given dates for the Dow stocks
def StockPrices(symbols, start, end):
    #Prices = {}
    AdjClose = []
    indicator = 0
    for ticker in symbols:
        try:
            data = web.DataReader(ticker, 'yahoo', start, end)  
            AdjClose.append(np.array(data['Adj Close']))
        except:
            indicator = 1
            break
    AdjClose = np.array(AdjClose)
    return AdjClose,indicator
###################################   
# Array of volatility of returns
def PriceMovement(Prices):
    VolReturns = []
    for ticker in Prices:
        # takes (aj close each day - mean) / sigma
        sigma = np.std(ticker)
        mean = np.mean(ticker)
        VolReturns.append(np.array([(ticker[i] - mean)/sigma for i in range(1,len(ticker))]))
    VolReturns = np.array(VolReturns)
    return VolReturns
        

    
def Data(start,end):
    # List of stock tickers
    Tickers = ScrapeList()
    
    # Get a list of the prices over a period of time
    AdjClose,indicator = StockPrices(Tickers, start, end)
    # If indicator == 1, then cannot obtain all stock data for this period
    if indicator == 1:
        return [],[]
    else:
        # Get an array of log returns for each stock
        VolReturns = PriceMovement(AdjClose)
    
        return Tickers,VolReturns
