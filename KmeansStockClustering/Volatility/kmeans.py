import numpy as np
from numpy import sum
from numpy import linalg
from random import randint

###################################
# Initialization of clusters using random partition method
def Initialize(NumSym,k):
    Clust = [randint(0,k-1) for i in xrange(NumSym)]
    if len(np.unique(Clust)) < k:
        return Initialize(NumSym,k)
    else:
        return Clust
###################################
# Take array representing clusters, X, k and get new centroids
def NewCent(Clust,X,k):
    Centroids = {t: np.zeros(X.shape[1]) for t in xrange(k)}
    for i in xrange(len(Clust)):
        Centroids[Clust[i]] = Centroids[Clust[i]] + X[i]
    for item in Centroids:
        if Clust.count(item) > 0:
            Centroids[item] = Centroids[item] / float(Clust.count(item))
        else:
            Centroids[item] = sum(X[j] for j in xrange(len(X)))/len(X)
    return Centroids            
###################################
# Take centroids, X, k get new clusters         
def NewClust(Centroids,X,k):
    Clust = []
    for item in X:
        SqDists = [np.linalg.norm(item - Centroids[t])**2 for t in xrange(k)]
        Clust.append(SqDists.index(min(SqDists)))
    return Clust             
###################################
# Called function 
def kmeansCluster(X,k): 
    # X is the array of data and k is the # of clusters
    # Initialize using random partition method
    Clust = Initialize(len(X),k)
    # Find centroids of initialized clusters
    Centroids = NewCent(Clust,X,k)
    # Make the centroids into a set so order is ignored and can be used for stopping
    CentSet = set(tuple(Centroids[item]) for item in Centroids)
    # Initialize another set to keep track of the previous centroids for stopping
    PriorCentSet = set('')  
    # Count keeps track of number of iterations until clusters stabilize  
    count = 1    
    while CentSet != PriorCentSet:
        PriorCentSet = CentSet
        Clust = NewClust(Centroids,X,k)
        Centroids = NewCent(Clust,X,k)
        CentSet = set(tuple(Centroids[item]) for item in Centroids)
        count = count + 1
    return Clust,Centroids,count


