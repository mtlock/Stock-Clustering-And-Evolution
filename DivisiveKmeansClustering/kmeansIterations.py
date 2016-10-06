import kmeans


# Function to take 1d array where entries are clusters and reassociate stock symbols
def ClusSym(Clust,Tickers,k):
    L = [[] for i in xrange(k)]
    for i in xrange(len(Clust)):
        L[Clust[i]] =  L[Clust[i]] + [Tickers[i]]
    return L
##########################################################
# Run kmeans clustering algorithm a number of times and return most frequent result
def ClustIter(VolReturns,Tickers,k,runs):
    # List with set of unique clusters as entries
    # In order of initial appearance
    # To keep count of how many times each appears
    C = []
    # List of sets of clusters to compare independent of order
    L_set = []
    # Corresponding list of returned clusters
    L_cluster = []
    # List of arrays of integers representing clusters
    L_clust_rep = []
    for i in xrange(runs):
        Clust, Centroids, count = kmeans.kmeansCluster(VolReturns,k) 
        Clusters = ClusSym(Clust,Tickers,k)
        ClusterSet = set(tuple(sorted(Clusters[i])) for i in xrange(k))  
        if ClusterSet in L_set:
            C[L_set.index(ClusterSet)] = C[L_set.index(ClusterSet)] + 1
        else:
            L_set.append(ClusterSet)
            L_cluster.append(Clusters)
            C.append(1)
            L_clust_rep.append(Clust)    
    return L_cluster,C,L_clust_rep
