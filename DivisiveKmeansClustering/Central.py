import datetime
from dateutil.relativedelta import relativedelta
import pytz
from pytz import timezone
import urllib2
from bs4 import BeautifulSoup
import numpy as np
from random import randint


    

def Cluster(Tickers,start,end,k):
    runs = 1000

    import Data
    VolReturns = Data.Data(Tickers,start,end)

    ##########################################################
    # Run kmeans clustering algorithm a number of times and return most frequent result
    import kmeansIterations

    L_cluster,C,L_clust_rep = kmeansIterations.ClustIter(VolReturns,Tickers,k,runs)
    
    FinalClust = L_cluster[C.index(max(C))]
    #FinalClust_rep = L_clust_rep[C.index(max(C))]

    
    return FinalClust 

    

