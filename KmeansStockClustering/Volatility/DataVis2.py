import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn.decomposition import PCA


def OrderedData(FinalClust_rep,X):
    OrderedX = {t:[] for t in np.unique(FinalClust_rep)}
    for i in xrange(len(FinalClust_rep)):
        OrderedX[FinalClust_rep[i]].append(X[i])
    OrderedArray = []
    ClusterSize = []
    for item in OrderedX:
        OrderedArray = OrderedArray + OrderedX[item]
        ClusterSize.append(len(OrderedX[item]))
    OrderedArray = np.array(OrderedArray)
    return OrderedArray,ClusterSize


def TwoDim(OrderedArray,ClusterSize):
    # Make a list of k distinct colors
    Colors = [np.random.rand(3,1) for i in xrange(len(ClusterSize))]
    PCA_data = PCA(n_components=2).fit_transform(OrderedArray)
    position = 0
    for i in xrange(len(ClusterSize)):
        x = PCA_data[position:position+ClusterSize[i],0]
        y = PCA_data[position:position+ClusterSize[i],1]
        plt.scatter(x,y,c=Colors[i],label = i)
        position = position + ClusterSize[i]
    plt.title('2D Visualization Using PCA (2 Clusters)\nWindow: May 2-10, 2016')
    plt.legend()
    plt.show()


def ThreeDim(OrderedArray,ClusterSize):
    # Make a list of k distinct colors
    Colors = [np.random.rand(3,1) for i in xrange(len(ClusterSize))]
    PCA_data = PCA(n_components=3).fit_transform(OrderedArray)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    position = 0
    for i in xrange(len(ClusterSize)):
        x = PCA_data[position:position+ClusterSize[i],0]
        y = PCA_data[position:position+ClusterSize[i],1]
        z = PCA_data[position:position+ClusterSize[i],2]
        ax.scatter(x,y,z,c=Colors[i],label=i)
        position = position + ClusterSize[i]
    plt.title('3D Visualization Using PCA (2 Clusters)\nWindow: May 2-10, 2016')
    plt.legend()
    plt.show()



def Representation(VisChoice2,FinalClust_rep,X):
    # Make an ordered lists of tickers and corresponding sizes of clusters to go back from PCA
    OrderedArray,ClusterSize = OrderedData(FinalClust_rep,X)    
    if VisChoice2 == '2D':
        TwoDim(OrderedArray,ClusterSize)
    elif VisChoice2 == '3D':
        ThreeDim(OrderedArray,ClusterSize)
    elif VisChoice2 == 'both':
        TwoDim(OrderedArray,ClusterSize)
        ThreeDim(OrderedArray,ClusterSize)
        
    

