import pandas as pd
from pandas_datareader import data as web
import numpy as np
import urllib2
from datetime import datetime
import pytz
from bs4 import BeautifulSoup


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