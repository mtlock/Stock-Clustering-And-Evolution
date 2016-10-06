import datetime
from dateutil.relativedelta import relativedelta
import pytz
from pytz import timezone
import urllib2
from bs4 import BeautifulSoup
import numpy as np
from random import randint



#Play a movie
#Hope to see stability
#Look at distance between groups for subsequent weeks
#Static versus evolving segments of the market
#Particular times of year that are more stable

print
print 'DOW JONES CLUSTER ANALYSIS'
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
#start = datetime.datetime(2016, 6, 15)#,0, 0, 0, 0, pytz.utc)
#end = datetime.datetime(2016, 6, 29)#,0, 0, 0, 0, pytz.utc)

##############################################################
# Enter the number of clusters you would like for the analysis
print 'ANALYSIS SPECIFICATIONS'
print 'How many clusters would you like in the analysis?'
while True:
    num = raw_input('Please enter an integer between 2 and 6: ')
    try:
        k = int(num)
        if k < 2 or k > 6:
            print 'You must enter an integer in the appropriate range'
            continue
        break
    except: 
        print 'You must enter an integer in the appropriate range'
print     
##############################################################
# Enter the number of times you would like to run the algorithm       
print 'The kmeans algorithm will be run a certain number of times'
print 'The clustering with the greatest frequency will be returned'
print 
print 'How many time would you like to run it?'
while True:
    r = raw_input()
    try:
        runs = int(r)
        if runs < 1:
            print 'Please enter a positive integer'
            continue
        break
    except:
        print 'Please enter a positive integer'
print
##############################################################
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
FinalClust = L_cluster[C.index(max(C))]
FinalClust_rep = L_clust_rep[C.index(max(C))]
print 'RESULTS'
print 'From','{:%Y-%m-%d}'.format(start),'to','{:%Y-%m-%d}'.format(end),', the clustering:'
for item in FinalClust:
    print
    print item
    print
print 'has frequency', max(C), 'out of', runs


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
print FinalClust_rep
DataVis2.Representation(VisChoice2,FinalClust_rep,VolReturns)



