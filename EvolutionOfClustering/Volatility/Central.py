import datetime
from dateutil.relativedelta import relativedelta
import pytz
from pytz import timezone
import urllib2
from bs4 import BeautifulSoup
import numpy as np
from random import randint



# Makes a matrix with 1 in ij if ij in same group and 0 otherwise
def CnxtnMtrx(X,A):
    # X is the connection matrix
    # A is the array with entries the cluster numbers
    for i in xrange(len(A)):
        for j in xrange(len(A)):
            if A[j] == A[i]:
                X[i,j] = X[i,j] + 1
    return X
    

def Cluster(Tickers,start,end,k):
    runs = 3000

    import Data
    VolReturns = Data.Data(Tickers,start,end)

    ##########################################################
    # Run kmeans clustering algorithm a number of times and return most frequent result
    import kmeansIterations

    L_cluster,C,L_clust_rep = kmeansIterations.ClustIter(VolReturns,Tickers,k,runs)
    
    FinalClust = L_cluster[C.index(max(C))]
    FinalClust_rep = L_clust_rep[C.index(max(C))]

    
    Cnxtn = CnxtnMtrx(np.zeros((len(FinalClust_rep),len(FinalClust_rep))),FinalClust_rep)
    return Cnxtn 

    

