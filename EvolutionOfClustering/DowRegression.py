import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pandas as pd
from pandas_datareader import data as web
import numpy as np
import urllib2
import datetime
import pytz
import quandl
from sklearn import linear_model


start = datetime.datetime(2013, 1, 16)
#start = datetime.datetime(2016, 1, 1)
#end = datetime.datetime(2016, 7, 1)

#print end - start

DateList = [start + datetime.timedelta(days=x) for x in xrange(900)]



quandl.ApiConfig.api_key = 'yVXUYNQG5f8e_H3vgS1L'
D = quandl.get('YAHOO/INDEX_DJI')
D = D.ix[DateList]
D = D[['Adjusted Close']]
D = D.dropna()
D.columns = ['Dow Jones']

#Apple added 3-19-15
#Nike split 12-24-15
#Dupont split 7-1-15

###################################   
#start = datetime.datetime(2016, 1, 1)
#end = datetime.datetime(2016, 7, 1)
#Make a list of dates
#DateList = [start + datetime.timedelta(days=x) for x in xrange(1188)]
#List of tickers
#L = ['MMM','UTX','DD','CVX','GE','HD','NKE','MCD','AAPL','CAT','INTC','MSFT']  #DOW1
#L = ['MMM','UTX','DD','AAPL','CAT','INTC','MSFT'] #DOW2
#L = ['CVX','JNJ','MSFT','GE'] #DOW3
#L = ['XOM','GE','MMM','GS'] #DOW4
#L = ['CVX','XOM','AXP','BA'] #DOW5
#L = ['INTC','MSFT','HD','IBM','DIS','AXP','BA'] #DOW6
#L = ['AXP','CAT','MRK','HD'] #DOW7
#L = ['AXP','CAT']
#L = ['IBM','CSCO','TRV','PG','JNJ']
#L = ['PG','TRV','MSFT','MCD']
#L = ['JMP','XOM','MMM','JNJ'] # R2=.9704 from feb 2012 through now
#L = ['MMM','MSFT','UTX','AAPL']# R2=.978 from feb 2012 through now
#L = ['MMM','MSFT','UTX','NKE']# R2=.978 from feb 2012 through now, R2=.978 from feb 2012 for 500 days
#L = ['MMM','MSFT','UTX','NKE','V','HD','MRK','UNH','MCD']# R2=.985 from feb 2012 through now
#L = ['MMM','VZ','HD'] #R2=.952 from feb 2012 through now
#L = ['MMM','BA','DD','XOM','CVX','IBM']
###################################   
#7 steps starting on 3-3-14
#L = ['CSCO','KO','UTX']#.909
#CSCO,NKE same
#AXP,BA,UTX same
###################################   
#7 steps starting on 3-3-14
#L = ['NKE','CSCO','KO','UTX']#.92
#CSCO,NKE same
#AXP,BA,UTX same
###################################   
#11 steps starting on 3-3-14
#L = ['GE','BA','GS','UNH','JNJ']#.94
#L = ['PG','BA','GS','UNH','JNJ']#.95
#L = ['PG','UTX','GS','UNH','JNJ']#.966
#L = ['GE','UTX','GS','UNH','JNJ']#.97
L = ['GE','UTX','GS','UNH','JNJ','IBM']#.97
#L = ['GE','UTX','GS','UNH','JNJ','VZ']#.97
####L = ['AXP','BA','GS','JPM','NKE','MSFT']
######L = ['AXP','HD','UNH','JPM','NKE','IBM','JNJ']

###################################   

#L = ['JNJ','PG','MMM','INTC']#.985
#L = ['JNJ','PG','MMM','INTC','DD','UNH']#.986


#L = ['MMM','UNH','XOM','JNJ','AAPL','DD']#.98 jan 2013-jan 2015




# Get a list of the historic adjust closing prices over given dates for the Dow stocks
def StockPrices(symbols, DateList):
    start = DateList[0]
    end = DateList[-1]
    df = pd.DataFrame(index = DateList, columns = symbols)
    for ticker in symbols:
        data = web.DataReader(ticker, 'yahoo', start, end) 
        df[ticker] = data['Adj Close']
    return df



df = StockPrices(L,DateList)
df = df.dropna()


X = np.array(df)
X = np.c_[np.ones(len(X)),X]
Y = np.array(D)


Dates = np.array([x for x in xrange(len(X))])
Dates = Dates.reshape(1,-1)

clf = linear_model.LinearRegression(fit_intercept=False)
clf.fit(X,Y)
C = clf.coef_

accuracy = clf.score(X,Y)
print accuracy




C = C.reshape(-1,1)

Approx = np.dot(X,C).T

D['Simulated'] = Approx.tolist()[0]

D.plot()



#plt.xlabel('Dates')
plt.ylabel('Percent cluster overlap')
#plt.title('Rolling Window Analysis: Sequential Cluster Overlap (2 Clusters')
title = 'Simulating the DJIA using: '
for item in L:
    title = title + item + ', '
title = title[:-2] + '\n' + '(R'r'$^2$ = ' + str(round(accuracy,3)) + ')'


plt.title(title)

plt.show()


exit()







