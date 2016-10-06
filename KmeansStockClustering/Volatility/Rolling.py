#import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
import pytz
from pytz import timezone
import numpy as np
import ModMain
import pandas as pd


Steps = 30
start = datetime.datetime(2015, 6, 1)
end = start+ datetime.timedelta(days=14)
Old = np.array(ModMain.Cluster(start,end,2))
Dates = []
Rolling = []

#Results = np.zeros(30)



#def UpdateCnxtn(X,A):
    # X is the connection matrix
    # A is the array with entries the cluster numbers
#    for i in xrange(len(A)):
#        for j in xrange(len(A)):
#            if A[j] == A[i]:
#                X[i,j] = X[i,j] + 1
#    return X

#Cnxtn = UpdateCnxtn(np.zeros((30,30)),Old)    


Results = np.zeros(30)


for i in xrange(Steps):
    Dates.append(start)
    start = start + datetime.timedelta(days=7)
    end = end + datetime.timedelta(days=7)
    L = np.array(ModMain.Cluster(start,end,2))
    Flip = L - np.ones(len(L))
    Flip = np.array([int(np.abs(i)) for i in Flip])
    if sum(np.abs(L - Old)) < sum(np.abs(Flip - Old)):
        #Rolling.append(100*(30 - sum(np.abs(L - Old)))/30.)
        #print round(100*(30 - sum(np.abs(L - Old)))/30.,2)#L
        #Results = Results + L
        #print L
        Results = Results + L
        Old = L
    else:
        #Rolling.append(100*(30 - sum(np.abs(Flip - Old)))/30.)
        #print round(100*(30 - sum(np.abs(Flip - Old)))/30.,2)#Flip
        #Results = Results + Flip
        #print Flip
        Results = Results + Flip
        Old = Flip
        
    #Cnxtn = UpdateCnxtn(Cnxtn,Old)

Results = (100./Steps)*Results
Results = [ int(100-x) if x<50 else int(x) for x in Results]
#Results = [ round(1-x,2) if x<.5 else round(x,2) for x in Results]
#print Results 
#Results = [ 5 - x if x<3 else x for x in Results]
print Results






#Cnxtn = (1./(Steps + 1)) * Cnxtn
#print Cnxtn  

#Results = (1./Steps)*Results
#Results = [ round(1-x,2) if x<.5 else round(x,2) for x in Results]
#print Results




#D ={'Dates':Dates,'Percent':Rolling}

#df = pd.DataFrame(D)

#df.plot(x='Dates',y='Percent')
#plt.xlabel('Dates')
#plt.ylabel('Percent cluster overlap')
#plt.title('Rolling Window Analysis: Sequential Cluster Overlap (2 Clusters')
#plt.show()
