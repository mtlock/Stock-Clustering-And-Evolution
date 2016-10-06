import datetime
from dateutil.relativedelta import relativedelta
import pytz
from pytz import timezone
import urllib2
from bs4 import BeautifulSoup
import numpy as np
from random import randint




def Cluster(start,end,k):
    runs = 1000
    # Scrape the ticker symbols, pull historic price data using yahoo finance api
    # Return list of ticker symbols and an array of corresponding log returns 
    import Data
    Tickers,VolReturns = Data.Data(start,end)

    if len(VolReturns) == 0:
        print 'There is not complete data for this period'
        print 'Please try a more recent range of dates'
        exit()
    ##########################################################
    # Run kmeans clustering algorithm a number of times and return most frequent result
    import kmeansIterations

    L_cluster,C,L_clust_rep = kmeansIterations.ClustIter(VolReturns,Tickers,k,runs)


    FinalClust_rep = L_clust_rep[C.index(max(C))]
    return FinalClust_rep
    
    
