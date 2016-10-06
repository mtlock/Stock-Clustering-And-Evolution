import matplotlib.pyplot as plt
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
#import jgraph
#import graphviz as gv

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

#######################################################################
# Filter the connection matrix to make an adjacency matrix
# Edges between only the strongest connections
def FilterCnxtn(X):
    L = []
    for i in xrange(len(X)):
        X[i,i] = 0 #KEEP THIS OUT SO ALL NODES SHOW UP
        tempA = X[i,:].tolist()
        tempB = [1 if x>=80 else 0 for x in tempA]
        L.append(tempB)
    return L

#######################################################################
# Initialize
Steps = 14
start = datetime.datetime(2014, 1, 16)
end = start+ datetime.timedelta(days=14)
Cnxtn = Central.Cluster(Tickers,start,end,2)

#######################################################################
# Roll forward and continue to sum connection matrices
for i in xrange(Steps):
    start = start + datetime.timedelta(days=7)
    end = end + datetime.timedelta(days=7)
    
    NewCnxtn = Central.Cluster(Tickers,start,end,2)
    
    Cnxtn = Cnxtn + NewCnxtn
    

Cnxtn = (100./(Steps + 1)) * Cnxtn
A = FilterCnxtn(Cnxtn)

Cnxtn = np.round((1./100)*Cnxtn,2)

MixDf = pd.DataFrame(index=Tickers,columns=Tickers)
HardDf = pd.DataFrame(index=Tickers,columns=Tickers)
for i in xrange(len(Tickers)):
    MixDf[Tickers[i]] = Cnxtn[i]
    HardDf[Tickers[i]] = np.array(A[i])


MixDf.to_csv('Mix_Matrix_11_Steps') 
HardDf.to_csv('Hard_Matrix_11_Steps')

for i in xrange(len(Cnxtn)):
    print Tickers[i],sum(A[i])
    

Graph = []

for i in xrange(len(A)):
    for j in range(i,len(A[i])):
        if A[i][j] == 1:
            Graph.append((Tickers[i],Tickers[j]))


Nodes = set([n1 for n1,n2 in Graph] + [n2 for n1,n2 in Graph])

G = nx.Graph()

for edge in Graph:
    G.add_edge(edge[0],edge[1])



ConnCom = nx.connected_components(G)
ConnComNodes = [c for c in ConnCom]

for item in ConnComNodes:
    print item

#Colors = [np.random.rand(3,1) for i in xrange(len(ConnComNodes))]


#for i in xrange(len(ConnComNodes)):
#    print ConnComNodes[i]
#    h = G.subgraph(ConnComNodes[i])
#    pos = nx.spring_layout(h,k = .3, iterations = 15)
#    nx.draw(h,pos,node_color=Colors[i],node_size=800,with_labels=True)
#    plt.show()

Colors = [np.random.rand(3,1) for i in xrange(len(ConnComNodes))]

color_map = []
for node in G.nodes():
    for i in xrange(len(ConnComNodes)):
        if node in ConnComNodes[i]:
            color_map.append(Colors[i])

title = 'Connectedness After ' + str(Steps + 1) + ' Steps\n(10 Day Window, Roll Forward 5 Days)'

plt.title(title)

#pos = nx.spring_layout(G,k = .3, iterations = 15)
pos = nx.shell_layout(G)
nx.draw(G,pos,node_color = color_map,node_size=800,with_labels=True)


plt.show()
    
    #for node in ConnComNodes[i]:
    #    G
        
        



exit()


#fruchterman_reingold
#pos = nx.shell_layout(G,k=.3,iterations=15)
#pos = nx.shell_layout(G)#,k=.3,iterations=15)
#nx.draw(G,pos,node_color='c',node_size=800,with_labels=True)
#nx.draw(G,node_color='c',node_size=800,with_labels=True)

#plt.show()




#exit()


#df = pd.DataFrame(A,index = Tickers, columns = Tickers)#,columns = C)


#G = nx.DiGraph(df.values)

#pos = nx.shell_layout(G)
#nx.draw(G,node_color='c',node_size=500,with_labels=True)#,pos)
#plt.show()
